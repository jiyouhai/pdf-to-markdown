# PDF → Markdown Evaluation

**Website:** [https://jiyouhai.github.io/pdf-to-markdown/](https://jiyouhai.github.io/pdf-to-markdown/)
**Repo:** [https://github.com/jiyouhai/pdf-to-markdown](https://github.com/jiyouhai/pdf-to-markdown)

Reproducible, parser-agnostic benchmarks for turning PDFs into Markdown—and measuring **downstream usefulness** with retrieval-QA, not just visual fidelity.

---

## Table of Contents

* Goals
* Methods at a Glance
* Repository Layout
* Quick Start
* Metrics & Thresholds
* Evaluation Pipeline (Automated QA)
* Results Snapshot (Aug 16, 2025)
* Add a New PDF Dataset
* Question Set (JSONL) Format
* Parsers & Output Conventions
* Publishing with GitHub Pages
* Optional: Build a PDF Report via LaTeX + CI
* Roadmap • FAQ • Contributing • License • Citation

---

## Goals

* **Apples-to-apples** comparison of multiple PDF→Markdown parsers.
* Emphasize **downstream quality** (retrieval/QA over Markdown) alongside structural/visual fidelity.
* Keep everything **simple, auditable, reproducible** in a public repo.

---

## Methods at a Glance

We use two human-in-the-loop methods plus one automated benchmark:

1. **LLM Desk Review (“Deep Research”)**
   Zip each parser’s outputs, upload to ChatGPT (GPT-5 Thinking / Pro), and have it draft a report against a rubric (structure, formatting, tables/math, cleanliness, post-processing, automation readiness).

2. **Side-by-Side PDF ↔ Markdown Review**
   Open the original PDF next to the Markdown for each parser (9 windows for 9 docs). The LLM scores against the rubric while you spot-check.

3. **Automated Retrieval-QA Benchmark (this repo’s code)**
   Treat each Markdown set as a knowledge base. Run BM25 retrieval + grounded QA + rubric judge to get **accuracy** and **overconfidence** that reflect real RAG usage. This is the main quantitative signal we publish.

---

## Repository Layout

```
pdf-to-markdown/
├─ docs/                      # Served via GitHub Pages
│  ├─ index.html              # Landing page
│  ├─ pdfs/                   # Original PDFs & rendered reports
│  ├─ md/                     # Parser outputs (Markdown)
│  │  └─ <parser>/<doc_id>/   # Many per-page .md OR a single .md
│  └─ questions/              # One JSONL per dataset (up to 100 Qs)
├─ report/                    # (Optional) LaTeX sources for a printable report
├─ runs_rubric/               # Outputs from automated QA runs
└─ .github/workflows/         # (Optional) CI for LaTeX & site checks
```

Naming
• doc\_id: short, URL-safe (e.g., TP-MVD8MV2-rotated).
• Parser names are free (e.g., textin, Reducto, md\_mathpix, md\_marker, own tool)—be consistent.

---

## Quick Start

1. Prepare data
   • Put PDFs in `docs/pdfs/<doc_id>.pdf`.
   • Put each parser’s Markdown in `docs/md/<parser>/<doc_id>/` (either per-page `001.md`, `002.md`, … or a single `full.md`).
   • Author up to **100 questions** in `docs/questions/<doc_id>.jsonl` (format below).

2. Install

   python -m venv .venv && source .venv/bin/activate
   pip install -U pandas jsonlines rapidfuzz rank\_bm25 openai tiktoken
   export OPENAI\_API\_KEY=sk-...   # required for answering/judging

3. Run the automated QA benchmark

   python eval\_pdfmd\_rubric.py&#x20;
   \--parsers md\_marker md\_mathpix Reducto textin "own tool"&#x20;
   \--chunk 1000 --overlap 200 --topk 5&#x20;
   \--answer-model gpt-4.1 --judge-model o3-mini&#x20;
   \--ok-threshold 0.75

4. Inspect outputs
   • Per-Q details: `runs_rubric/per_question.csv`
   • Aggregates: `runs_rubric/summary.csv`
   • Static site: enable GitHub Pages for `/docs` and browse datasets/outputs online.

Reference run (“what we did”)
• 9 PDFs; 100 questions per PDF (JSONL).
• Read Markdown for each parser from `docs/md/<parser>/<doc_id>/` (dir or single-file).
• Chunk: 1000 tokens with 200-token overlap; BM25 per doc; retrieve top-k=5.
• Answer with gpt-4.1 using **only** retrieved text (may return NOT\_FOUND).
• Fast rules: exact; numeric≈ (±2% or 1e-6 abs); fuzzy≥90 (RapidFuzz).
• Else judge with o3-mini (evidence-only rubric) → score∈\[0,1].
• Derive per-Q flags and aggregate per (parser, doc): acc, score\_mean, overconf\_rate.

---

## Metrics & Thresholds

For parser p, document d, question i, the judge returns score\[p,d,i]∈\[0,1] from an evidence-only rubric.

• **Accuracy (acc)**: pass rate at threshold 0.75
acc\[p,d] = (1/n\_d) ∑\_i 1\[ score\[p,d,i] ≥ 0.75 ]
Why 0.75? Most questions decompose into 4–6 atomic facts. 0.75 ≈ “clear majority supported” (≥3/4 or ≥4/5). In pilot sweeps (0.60–0.90) it best balanced: (i) low false-accepts on manuals, (ii) not punishing concise correct answers, (iii) stable rankings across 0.70–0.80.

• **Mean score (score\_mean)**: continuous quality
score\_mean\[p,d] = (1/n\_d) ∑\_i score\[p,d,i]
Useful to see near-misses beyond the binary cut.

• **Overconfidence (overconf\_rate)**: wrong assertions vs. abstain
overconf\_rate\[p,d] = (1/n\_d) ∑\_i 1\[ ok=0 and prediction≠NOT\_FOUND ]
A wrong assertion is worse than abstaining. This measures that.

• **Penalized score** (optional, calibration-aware):
penalized\_λ = acc\_mean − λ · overconf\_mean
Default λ=0.5; λ∈\[0.25,1.0] yields the same ordering on our 9-doc set.

Fast rule matches (auto full credit before judging)
• Exact normalized match
• Numeric≈: all gold numbers within 2% (or 1e-6 abs)
• Fuzzy: RapidFuzz partial ratio ≥90
• Gold empty + prediction = NOT\_FOUND

---

## Evaluation Pipeline (Automated QA)

1. Inputs → read Markdown (dir or single-file), concatenate & normalize
2. Chunk 1000 tokens + 200 overlap
3. BM25 index (per document)
4. For each question: retrieve top-k=5 chunks
5. gpt-4.1 answers using only retrieved text (may return NOT\_FOUND)
6. Fast rules (exact / numeric≈ / fuzzy≥90); else o3-mini rubric judge (score∈\[0,1])
7. Compute per-Q flags: ok=(score≥0.75); overconf=(ok=0 and pred≠NOT\_FOUND)
8. Aggregate per (parser, doc): n, acc, score\_mean, overconf\_rate
9. Write CSVs and publish tables on the site

Defaults: `--chunk 1000`, `--overlap 200`, `--topk 5`, `--ok-threshold 0.75`, `--answer-model gpt-4.1`, `--judge-model o3-mini`.

---

## Results Snapshot (Aug 16, 2025)

Ranking by mean accuracy (9 docs):

1. textin (0.578) → 2) md\_mathpix (0.568) → 3) md\_marker (0.564) → 4) Reducto (0.543) → 5) own tool (0.454)

Overall by parser (macro≈micro; n constant per doc)

| Parser      | Docs | Total n | acc\_mean | acc\_median | acc\_min | acc\_max | overconf\_mean |
| ----------- | ---: | ------: | --------: | ----------: | -------: | -------: | -------------: |
| textin      |    9 |     900 |     0.578 |       0.600 |    0.100 |    0.930 |          0.379 |
| md\_mathpix |    9 |     900 |     0.568 |       0.680 |    0.120 |    0.940 |          0.373 |
| md\_marker  |    9 |     900 |     0.564 |       0.610 |    0.120 |    0.940 |          0.372 |
| Reducto     |    9 |     900 |     0.543 |       0.570 |    0.110 |    0.940 |          0.389 |
| own tool    |    9 |     900 |     0.454 |       0.400 |    0.090 |    0.950 |          0.392 |

Penalized (λ=0.5) — ordering unchanged

| Parser      | penalized\_0.5 |
| ----------- | -------------: |
| textin      |          0.388 |
| md\_mathpix |          0.381 |
| md\_marker  |          0.378 |
| Reducto     |          0.349 |
| own tool    |          0.258 |

Per-doc winners are split (textin/mathpix/marker/own-tool: 2 each; Reducto: 1). CSVs are under `runs_rubric/`.

---

## Add a New PDF Dataset

1. Put the PDF: `docs/pdfs/<doc_id>.pdf`
2. Add each parser’s Markdown:
   • `docs/md/<parser>/<doc_id>/001.md`, `002.md`, …
   • or `docs/md/<parser>/<doc_id>/full.md`
3. Author up to 100 questions: `docs/questions/<doc_id>.jsonl`
4. Commit:

   git add docs/pdfs/\<doc\_id>.pdf docs/md/\*\* docs/questions/\<doc\_id>.jsonl
   git commit -m "docs: add \<doc\_id> (PDF, parser MD, questions)"
   git push

---

## Question Set (JSONL) Format

One JSON object per line.

Minimal

```
{"id":"Q001","q":"What is the warranty term?"}
{"id":"Q002","q":"Report the rated voltage from the spec table."}
```

With reference answers (preferred for rubric)

```
{"id":"Q001","q":"What is the warranty term?","a":"5 years"}
{"id":"Q002","q":"Report the rated voltage from the spec table.","a":"56 V"}
```

Loaders also accept legacy keys (`qid`, `question`, `answer`, `gold`). The script normalizes them.

---

## Parsers & Output Conventions

Place each parser’s output under `docs/md/<parser>/<doc_id>/`.
Both multi-file (per page) and single-file are supported. The reader also recognizes internal-tool names like `livex_<doc_id>_markdown.md`.

Tips
• If a parser emits **tables as images**, retrieval degrades (no cells to index). Prefer Markdown/HTML tables.
• Keep figure captions and references as **text** near images for better grounding.
• Normalize headings (`#`, `##`, `###`) and math (`$...$`, `$$...$$`) to ease downstream parsing.

---

## Publishing with GitHub Pages

• Settings → Pages → Source: “Deploy from a branch” → Branch: `main` → folder: `/docs`
• After pushing to `docs/`, your site updates automatically:
– `docs/pdfs/` — PDFs and generated reports
– `docs/questions/` — JSONL question sets
– `docs/md/` — parser outputs
– `docs/index.html` — homepage (list datasets/parsers)

---

## Optional: Build a PDF Report via LaTeX + CI

Place LaTeX here:

```
report/main.tex
report/assets/...
```

Example CI (save as `.github/workflows/latex.yml`), compiles on push and publishes to `docs/pdfs/evaluation-report.pdf`:

```
name: build-report
on:
  push:
    paths:
      - "report/**"
      - ".github/workflows/latex.yml"
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: xu-cheng/latex-action@v3
        with:
          root_file: main.tex
          working_directory: report
      - name: Publish PDF into docs/pdfs
        run: |
          mkdir -p docs/pdfs
          cp report/main.pdf docs/pdfs/evaluation-report.pdf
      - name: Commit report
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add docs/pdfs/evaluation-report.pdf
          git commit -m "ci: publish evaluation report" || echo "No changes"
          git push
```

---

## Roadmap

• Side-by-side PDF vs. Markdown diff/preview in the site
• Built-in retrieval test harness (simple configs per parser)
• Question harvesting helpers (tables → value Qs; figure → caption Qs)
• Weighted scoring profiles (table-heavy vs. math-heavy docs)
• Dataset metadata cards to drive the homepage automatically

---

## FAQ

**Do I need one Markdown file per page?**
No. Per-page is helpful for debugging; single-file also works.

**Why do QA results differ across parsers for the same PDF?**
Structural losses (tables as images, headings flattened, math dropped) harm retrieval and precision.

**Which models are used?**
Default: `gpt-4.1` to answer (context-only, can return `NOT_FOUND`), `o3-mini` to judge. Both are pluggable via CLI flags.

**Can I change the 0.75 threshold?**
Yes (`--ok-threshold`). We chose 0.75 after sweeps for a “clear majority of facts” bar that keeps false accepts low.

---

## Contributing

• Add datasets via “Add a New PDF Dataset”.
• Add parser outputs under `docs/md/<parser>/<doc_id>/`.
• PRs/issues welcome for homepage, metrics, pipeline, or CI improvements.

---

## License

• Code & configs: MIT (`LICENSE`)
• Datasets & generated content: use an appropriate content license (e.g., CC BY 4.0) depending on source material.

---

## Citation

```
@misc{pdf_to_markdown_eval_2025,
  title        = {PDF→Markdown Evaluation},
  author       = {Repository Contributors},
  year         = {2025},
  howpublished = {https://github.com/jiyouhai/pdf-to-markdown}
}
```

Tip: Keep `docs/` as the public snapshot; keep experimental runs in `runs_rubric/`. Small, auditable, reproducible.
