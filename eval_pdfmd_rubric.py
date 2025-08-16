#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eval_pdfmd_rubric.py (clean + progress + single-file support)
- 加载题库 -> 分块 -> BM25 检索 -> gpt-4.1 回答
- 规则命中=1.0；否则用 o3/o3-mini 基于证据做 0~1 细则评分（rubric）
- 同时支持两种 MD 布局：
  A) 子目录：docs/md/<parser>/<doc_id>/**.md(.markdown/.mdx)
  B) 单文件：docs/md/<parser>/<doc_id>.md  或  own tool: livex_<doc_id>_markdown.md
- 打印进度与用时
"""
import os, re, glob, json, argparse, time, sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import jsonlines, pandas as pd
from functools import lru_cache
from rapidfuzz import fuzz
from rank_bm25 import BM25Okapi
from openai import OpenAI

# ---------- OpenAI ----------
@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise SystemExit("OPENAI_API_KEY is not set. export OPENAI_API_KEY=...")
    return OpenAI(api_key=key)

# ---------- CLI ----------
def build_cli():
    p = argparse.ArgumentParser(description="Eval PDF→MD via QA (gpt-4.1) + Rubric Judge (o3/o3-mini)")
    p.add_argument("--parsers", nargs="+", default=["md_marker","md_mathpix","Reducto","textin","own tool"])
    p.add_argument("--md-root", type=str, default=None)
    p.add_argument("--q-root", type=str, default=None)
    p.add_argument("--runs-root", type=str, default=None)
    p.add_argument("--chunk", type=int, default=1000)
    p.add_argument("--overlap", type=int, default=200)
    p.add_argument("--topk", type=int, default=5)
    p.add_argument("--answer-model", type=str, default="gpt-4.1")
    p.add_argument("--judge-model", type=str, default="o3-mini")  # 快省默认
    p.add_argument("--ok-threshold", type=float, default=0.75)
    p.add_argument("--only-docs", nargs="*", default=None)
    p.add_argument("--max-output-tokens", type=int, default=256)
    return p

# ---------- paths ----------
def get_paths(args):
    base = Path(os.getenv("PDFMD_ROOT", Path(__file__).resolve().parent))
    docs_md = Path(args.md_root) if args.md_root else base / "docs" / "md"
    qs_dir  = Path(args.q_root)  if args.q_root  else base / "docs" / "questions"
    runs    = Path(args.runs_root) if args.runs_root else base / "runs_rubric"
    runs.mkdir(parents=True, exist_ok=True)
    return base, docs_md, qs_dir, runs

# ---------- questions ----------
def load_questions(qdir: Path, only_docs: Optional[List[str]]=None) -> Dict[str, List[dict]]:
    qfiles = glob.glob(str(qdir / "*.jsonl")) + glob.glob(str(qdir / "*" / "questions.jsonl"))
    out: Dict[str, List[dict]] = {}
    for qf in qfiles:
        if qf.endswith(".jsonl"):
            doc_id = Path(qf).stem if Path(qf).parent.name != "questions" else Path(qf).stem
        else:
            doc_id = Path(qf).parent.name
        if only_docs and doc_id not in only_docs: 
            continue
        rows = []
        with jsonlines.open(qf) as rd:
            for obj in rd:
                qid  = str(obj.get("id") or obj.get("qid") or obj.get("index") or f"Q{len(rows)+1:03d}")
                qtxt = obj.get("q") or obj.get("question")
                gold = obj.get("a") or obj.get("answer") or obj.get("gold")
                if qtxt:
                    rows.append({"id": qid, "q": qtxt, "gold": gold})
        if rows:
            out[doc_id] = rows
    return out

# ---------- chunking ----------
def split_into_chunks(text: str, target_tokens: int=1000, overlap: int=200) -> List[str]:
    try:
        import tiktoken
        enc = tiktoken.encoding_for_model("gpt-4.1")
        toks = enc.encode(text)
        step = max(1, target_tokens - overlap)
        chunks = []
        for i in range(0, len(toks), step):
            sub = toks[i:i+target_tokens]
            if not sub: break
            chunks.append(enc.decode(sub))
        return chunks
    except Exception:
        avg = 4
        chunk_chars = target_tokens * avg
        step_chars  = max(1, (target_tokens - overlap) * avg)
        chunks, i = [], 0
        while i < len(text):
            chunks.append(text[i:i+chunk_chars]); i += step_chars
        return chunks

# ---------- MD reader (supports dir/single-file/own tool naming) ----------
def read_md_chunks(md_root: Path, parser: str, doc_id: str, target_tokens=1000, overlap=200) -> List[str]:
    folder = md_root / parser / doc_id
    allowed = (".md",".markdown",".mdx")

    def norm(name: str) -> str:
        x = name.lower()
        x = re.sub(r'(^livex_|_markdown$)','', x)  # own tool 前后缀
        x = re.sub(r'[\s_\-]+','', x)
        x = re.sub(r'[^a-z0-9]','', x)
        return x

    files: List[Path] = []

    # A) 子目录：docs/md/<parser>/<doc_id>/**.md
    if folder.exists():
        files = sorted([pp for pp in folder.rglob("*") if pp.is_file() and pp.suffix.lower() in allowed])

    # B) 单文件：docs/md/<parser>/<doc_id>.md 或 livex_<doc_id>_markdown.md
    if not files:
        base = md_root / parser
        if base.exists():
            # 直配
            for ext in allowed:
                cand = base / f"{doc_id}{ext}"
                if cand.exists():
                    files = [cand]; break
            # 规范化匹配
            if not files:
                ndoc = norm(doc_id)
                cands = []
                for fp in base.iterdir():
                    if fp.is_file() and fp.suffix.lower() in allowed:
                        if (norm(fp.stem) == ndoc) or (ndoc in norm(fp.stem)):
                            cands.append(fp)
                files = sorted(cands)

    if not files:
        return []

    text = ""
    for fp in files:
        try:
            text += f"\n\n[FILE:{fp.name}]\n" + fp.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            pass
    text = text.strip()
    if not text:
        return []
    return split_into_chunks(text, target_tokens=target_tokens, overlap=overlap)

# ---------- retrieval ----------
def build_bm25(chunks: List[str]):
    toks = [re.findall(r"\w+", c.lower()) for c in chunks]
    return BM25Okapi(toks), toks

def bm25_topk(bm25: BM25Okapi, q: str, chunks: List[str], k: int=5) -> Tuple[str, List[int]]:
    toks = re.findall(r"\w+", q.lower())
    scores = bm25.get_scores(toks)
    idxs = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    ctx = "\n\n---\n\n".join(chunks[i] for i in idxs)
    return ctx, idxs

# ---------- answering ----------
SYS_ANSWER = (
    "You answer ONLY using the provided CONTEXT. "
    'If the context does not contain the answer, reply strictly with JSON: {"id":"<qid>","answer":"NOT_FOUND"}'
)
USR_ANSWER = """Return strictly one JSON line:
{{"id":"{qid}","answer":"<short but complete answer>"}}

Rules:
- Use only CONTEXT; do not guess. If missing, return NOT_FOUND.
- If the answer has multiple factual points, list them concisely separated by '; '.

CONTEXT:
{ctx}

QUESTION:
{q}
"""

def call_answer_model(model: str, qid: str, q: str, ctx: str, max_output_tokens: int=256) -> dict:
    prompt = f"{SYS_ANSWER}\n\n" + USR_ANSWER.format(qid=qid, q=q, ctx=ctx[:15000])
    resp = get_client().responses.create(
        model=model,
        input=prompt,
        temperature=0,             # 仅 gpt-4.1 用；o3 系列不走这里
        max_output_tokens=max_output_tokens,
    )
    txt = resp.output_text.strip()
    m = re.search(r"\{.*\}", txt, flags=re.S)
    if m:
        try:
            obj = json.loads(m.group(0))
            if "id" not in obj: obj["id"] = qid
            if "answer" not in obj: obj["answer"] = ""
            return obj
        except Exception:
            pass
    return {"id": qid, "answer": txt}

# ---------- rule scoring ----------
def norm(s: Optional[str]) -> str:
    if not s: return ""
    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^\w\s\.\-/%]", "", s)
    return s

def extract_numbers(s: str) -> List[float]:
    if not s: return []
    vals = []
    for t in re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", s):
        try: vals.append(float(t))
        except: pass
    return vals

def soft_match(gold: Optional[str], pred: Optional[str]) -> Tuple[bool, str]:
    if gold is None:
        return ((pred or "").strip().upper() == "NOT_FOUND", "no-gold")
    g, p = norm(gold), norm(pred)
    if g == p: return True, "exact"
    gn, pn = extract_numbers(g), extract_numbers(p)
    if gn and pn:
        ok_all = True
        for a in gn:
            if not any(abs(a-b) <= max(0.02*abs(a), 1e-6) for b in pn):
                ok_all = False; break
        if ok_all: return True, "numeric≈"
    if fuzz.partial_ratio(g, p) >= 90:
        return True, "fuzzy≥90"
    return False, "mismatch"

# ---------- rubric judge (o3 / o3-mini) ----------
GRADER_SYS = "You are a strict, evidence-based grader. Only use the given EVIDENCE snippets."
GRADER_RUBRIC = """Return strictly JSON:
{{
  "score": 0.0-1.0,
  "verdict": "correct" | "partially_correct" | "incorrect",
  "missing_points": ["<short atomic claim>", ...],
  "superfluous_points": ["<short atomic claim>", ...],
  "reason": "<1-3 sentences explaining, quote evidence if helpful>"
}}

How to grade:
1) Decompose GOLD (reference answer) into 3-10 atomic factual points (unordered).
2) For each point, check if PREDICTION is supported by EVIDENCE. Unsupported or contradicted -> missing_points.
3) If PREDICTION includes claims that are not supported by EVIDENCE -> superfluous_points.
4) score = matched_points / max(total_points,1). No credit without evidence.
5) If all points matched and no contradictions -> verdict=correct; some matched -> partially_correct; none -> incorrect.

QUESTION: {q}

GOLD: {gold}

PREDICTION: {pred}

EVIDENCE:
{ctx}
"""

def grade_with_o3_rubric(model: str, q: str, gold: Optional[str], pred: str, ctx: str) -> Tuple[float, dict]:
    if (not gold) and (pred or "").strip().upper() == "NOT_FOUND":
        return 1.0, {"verdict":"correct","reason":"gold-empty->NOT_FOUND","missing_points":[],"superfluous_points":[]}
    prompt = f"{GRADER_SYS}\n\n" + GRADER_RUBRIC.format(q=q, gold=gold, pred=pred, ctx=ctx[:12000])
    resp = get_client().responses.create(
        model=model,                 # o3 / o3-mini
        input=prompt,
        max_output_tokens=300,       # 不传 temperature 给 o3
    )
    txt = resp.output_text.strip()
    m = re.search(r"\{.*\}", txt, flags=re.S)
    if not m:
        return 0.0, {"verdict":"incorrect","reason":"judge-parse-error","missing_points":[],"superfluous_points":[]}
    try:
        obj = json.loads(m.group(0))
        score = float(obj.get("score", 0.0))
        score = 0.0 if score < 0 else 1.0 if score > 1 else score
        return score, obj
    except Exception:
        return 0.0, {"verdict":"incorrect","reason":"judge-json-error","missing_points":[],"superfluous_points":[]}

# ---------- main ----------
def evaluate(args):
    start_all = time.time()
    base, md_root, q_root, runs_root = get_paths(args)
    doc2qs = load_questions(q_root, args.only_docs)
    if not doc2qs: 
        raise SystemExit(f"No question files found under {q_root}")

    rows = []

    for parser in args.parsers:
        doc_ids = sorted([doc for doc in doc2qs.keys() if (md_root / parser).exists()])
        if args.only_docs:
            doc_ids = [d for d in doc_ids if d in args.only_docs]
        if not doc_ids:
            continue

        for doc_id in doc_ids:
            chunks = read_md_chunks(md_root, parser, doc_id, target_tokens=args.chunk, overlap=args.overlap)
            if not chunks:
                # 没有可读 MD（文件缺失或仅图片）
                # print(f"[{parser} :: {doc_id}] no markdown files, skip.")
                continue
            bm25, _ = build_bm25(chunks)

            outdir = runs_root / parser / doc_id
            outdir.mkdir(parents=True, exist_ok=True)
            gpt_answers = []

            total_q = len(doc2qs[doc_id])
            start_doc = time.time()
            ok_cnt = 0
            judge_calls = 0
            last_print = 0
            print(f"[{parser} :: {doc_id}] {total_q} Qs | chunk={args.chunk} overlap={args.overlap} topk={args.topk}")

            for idx, item in enumerate(doc2qs[doc_id], 1):
                qid, q, gold = item["id"], item["q"], item.get("gold")
                ctx, idxs = bm25_topk(bm25, q, chunks, k=args.topk)
                pred_obj = call_answer_model(args.answer_model, qid, q, ctx, max_output_tokens=args.max_output_tokens)
                pred = pred_obj.get("answer","")

                # 规则命中 => 直接满分
                ok_rule, how = soft_match(gold, pred)
                if ok_rule:
                    score = 1.0
                    verdict = "correct"
                    judge_reason = "rule:"+how
                    missing_points = []
                    superfluous_points = []
                    ok = 1
                else:
                    score, judge_obj = grade_with_o3_rubric(args.judge_model, q, gold, pred, ctx)
                    verdict = str(judge_obj.get("verdict",""))
                    judge_reason = judge_obj.get("reason","")
                    missing_points = judge_obj.get("missing_points",[])
                    superfluous_points = judge_obj.get("superfluous_points",[])
                    ok = int(score >= args.ok_threshold)
                    how = "llm-rubric"
                    judge_calls += 1

                overconf = int((ok==0) and (pred.strip().upper() != "NOT_FOUND"))

                rows.append({
                    "parser": parser, "doc_id": doc_id, "id": qid,
                    "gold": gold, "pred": pred,
                    "score": score, "ok": ok,
                    "match_type": how, "verdict": verdict,
                    "overconfident": overconf,
                    "judge_reason": judge_reason,
                    "missing_points": "; ".join(missing_points) if isinstance(missing_points, list) else "",
                    "superfluous_points": "; ".join(superfluous_points) if isinstance(superfluous_points, list) else "",
                })
                gpt_answers.append({"id": qid, "answer": pred})

                # 进度：每 10 题或最后一题
                if (idx - last_print) >= 10 or idx == total_q:
                    elapsed = time.time() - start_doc
                    rate = (idx/elapsed) if elapsed>0 else 0.0
                    eta = (total_q - idx)/rate if rate>0 else 0.0
                    print(f"  progress: {idx}/{total_q} | ok={ok_cnt+ok} | judge={judge_calls} | {rate:.2f} q/s | ETA ~{int(eta)}s", flush=True)
                    last_print = idx
                ok_cnt += ok

            # 文档完成统计
            elapsed_doc = time.time() - start_doc
            rate_doc = (total_q/elapsed_doc) if elapsed_doc>0 else 0.0
            print(f"[{parser} :: {doc_id}] done in {elapsed_doc:.1f}s | avg {rate_doc:.2f} q/s | judge_calls={judge_calls}")

            # 写出该文档的模型答案
            with jsonlines.open(outdir / f"answers.{args.answer_model}.jsonl", "w") as w:
                for r in gpt_answers: w.write(r)

    if not rows:
        print("No results, nothing to summarize.")
        return

    df = pd.DataFrame(rows)
    df.to_csv((runs_root / "per_question.csv"), index=False)

    summary = (
        df.groupby(["parser","doc_id"])
          .agg(n=("ok","size"),
               acc=("ok","mean"),
               score_mean=("score","mean"),
               overconf_rate=("overconfident","mean"))
          .reset_index()
          .sort_values(["parser","doc_id"])
    )
    summary.to_csv((runs_root / "summary.csv"), index=False)
    print("\n== Summary ==")
    print(summary.to_string(index=False))
    total_elapsed = time.time() - start_all
    print(f"\nTotal elapsed: {total_elapsed:.1f}s")

if __name__ == "__main__":
    args = build_cli().parse_args()
    evaluate(args)
