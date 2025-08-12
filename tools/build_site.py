import json, pathlib, shutil, datetime, html

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets"
DATASETS = DOCS / "datasets"
DOCS_Q = DOCS / "questions"
QDIR = ROOT / "questions"
INDEX = ROOT / "questions" / "index.json"

REPO_HTTP = "https://github.com/jiyouhai/pdf-to-markdown"
REPO_TREE = REPO_HTTP + "/tree/main/"
RAW_BASE  = "https://raw.githubusercontent.com/jiyouhai/pdf-to-markdown/main/"

def safe_read_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def read_count_lines(p):
    try:
        with open(p, encoding="utf-8") as f:
            return sum(1 for line in f if line.strip())
    except FileNotFoundError:
        return 0

def count_md_files(path):
    p = ROOT / path
    if not p.exists():
        return 0
    return sum(1 for _ in p.rglob("*.md"))

def copy_questions(doc_id):
    src = QDIR / doc_id / "questions.jsonl"
    if src.exists():
        dst = DOCS_Q / f"{doc_id}.jsonl"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        return f"questions/{doc_id}.jsonl", read_count_lines(src)
    return None, 0

def htmlesc(s): return html.escape(s, quote=True)

def dataset_page(doc_id, meta, q_rel, q_count):
    pdf_rel = meta.get("pdf","")
    pdf_site = "../" + pdf_rel if pdf_rel else "#"
    pdf_git  = REPO_TREE + pdf_rel if pdf_rel else REPO_HTTP

    parsers = meta.get("md", {})
    rows = []
    for pname, pdir in parsers.items():
        exists = (ROOT / pdir).exists()
        md_count = count_md_files(pdir) if exists else 0
        repo_link = REPO_TREE + pdir
        rows.append(f"""
          <tr class="row{' off' if not exists else ''}">
            <td><code>{htmlesc(pname)}</code></td>
            <td><code>{htmlesc(pdir)}</code></td>
            <td>{md_count if exists else '—'}</td>
            <td><a href="{repo_link}" target="_blank" rel="noopener">View in GitHub</a></td>
          </tr>
        """)

    q_link = f"../{q_rel}" if q_rel else (RAW_BASE + f"questions/{doc_id}/questions.jsonl")
    q_badge = f"{q_count} questions" if q_count else "questions.jsonl (not found)"

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{htmlesc(doc_id)} · PDF-to-Markdown Evaluation</title>
  <link rel="stylesheet" href="../assets/style.css"/>
</head>
<body>
<header class="site-header"><a href="../index.html">PDF→MD Evaluation</a></header>

<main class="container">
  <section class="hero small">
    <h1>{htmlesc(doc_id)}</h1>
    <div class="cta">
      <a class="btn" href="{pdf_site}" target="_blank" rel="noopener">📄 Open PDF</a>
      <a class="btn" href="{q_link}" target="_blank" rel="noopener">❓ {htmlesc(q_badge)}</a>
      <a class="btn ghost" href="{pdf_git}" target="_blank" rel="noopener">🔎 PDF in GitHub</a>
    </div>
  </section>

  <section class="card">
    <h2>Parser outputs</h2>
    <p>Below are registered parser output folders for this document (from <code>questions/index.json</code>). Counts are <em>*.md files</em> currently in the repo.</p>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Parser</th><th>Path</th><th>*.md</th><th>Link</th></tr></thead>
        <tbody>
          {"".join(rows)}
        </tbody>
      </table>
    </div>
    <p class="note">Tip: to expose raw Markdown on this site, you can add small index pages per folder or link to GitHub as above.</p>
  </section>

  <section class="card">
    <h2>Artifacts</h2>
    <ul class="list">
      <li>Report PDF (latest CI): <a href="../pdfs/evaluation-report.pdf" target="_blank" rel="noopener">docs/pdfs/evaluation-report.pdf</a></li>
      <li>Full repo: <a href="{REPO_HTTP}" target="_blank" rel="noopener">{REPO_HTTP}</a></li>
    </ul>
  </section>
</main>

<footer class="site-footer">
  &copy; {datetime.date.today().year} Xiaoxiao · Built from repo contents · <a href="../index.html">Home</a>
</footer>
</body></html>"""

def homepage(docs_blocks, total_docs, total_q):
    updated = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>PDF-to-Markdown Evaluation</title>
  <link rel="stylesheet" href="./assets/style.css"/>
  <script defer src="./assets/app.js"></script>
</head>
<body>
<header class="site-header"><a href="./index.html">PDF→MD Evaluation</a></header>

<main class="container">
  <section class="hero">
    <h1>PDF→Markdown Evaluation</h1>
    <p class="sub">9 PDFs · {total_q} questions · Multiple parsers (Mathpix / TextIn / Reducto / Marker / Internal)</p>
    <div class="cta">
      <a class="btn" href="./pdfs/evaluation-report.pdf" target="_blank" rel="noopener">📘 Read the Report</a>
      <a class="btn ghost" href="{REPO_HTTP}" target="_blank" rel="noopener">⭐ GitHub</a>
    </div>
    <p class="meta">Last updated: {updated}</p>
  </section>

  <section class="card">
    <div class="split">
      <div>
        <h2>Datasets <span class="muted">({total_docs})</span></h2>
      </div>
      <div>
        <input id="search" class="search" type="search" placeholder="Search by doc id…"/>
      </div>
    </div>
    <div id="grid" class="grid">
      {"".join(docs_blocks)}
    </div>
  </section>

  <section class="card">
    <h2>How this works</h2>
    <ol class="steps">
      <li>Convert each PDF with multiple parsers → store Markdown under <code>docs/md/&lt;parser&gt;/&lt;doc_id&gt;/</code></li>
      <li>100 PDF-specific questions per doc → <code>questions/&lt;doc_id&gt;/questions.jsonl</code> (mirrored to site)</li>
      <li>Run RAG pipelines → write answers to <code>runs/&lt;parser&gt;/&lt;doc_id&gt;/answers.jsonl</code></li>
      <li>Use an LLM evaluator (or exact-match) against the original PDF to score</li>
    </ol>
  </section>
</main>

<footer class="site-footer">
  &copy; {datetime.date.today().year} Xiaoxiao · <a href="./pdfs/evaluation-report.pdf">Report PDF</a>
</footer>
</body></html>"""

# --- main build ---
data = safe_read_json(INDEX)
cards = []
total_docs = 0
total_q = 0

DOCS.mkdir(exist_ok=True, parents=True)
ASSETS.mkdir(exist_ok=True, parents=True)
DATASETS.mkdir(exist_ok=True, parents=True)
DOCS_Q.mkdir(exist_ok=True, parents=True)

for doc_id, meta in sorted(data.items()):
    total_docs += 1
    q_rel, q_cnt = copy_questions(doc_id)
    total_q += q_cnt
    # dataset card
    pdf_rel = meta.get("pdf","")
    detail_href = f"./datasets/{doc_id}.html"
    pdf_href = "./" + pdf_rel if pdf_rel else "#"
    cards.append(f"""
      <a class="card card-link" href="{detail_href}">
        <div class="card-title">{htmlesc(doc_id)}</div>
        <div class="card-body">
          <div class="pill">PDF</div>
          <div class="pill">{q_cnt or 0} Qs</div>
        </div>
      </a>
    """)
    # dataset page
    (DATASETS / f"{doc_id}.html").write_text(dataset_page(doc_id, meta, q_rel, q_cnt), encoding="utf-8")

# homepage
(DOCS / "index.html").write_text(homepage(cards, total_docs, total_q), encoding="utf-8")
print(f"Built site: {total_docs} docs, {total_q} questions mirrored.")
