# PDF → Markdown Evaluation

[website](https://jiyouhai.github.io/pdf-to-markdown/)

For the report, we use two methods to evaluate the performance of these PDF-to-Markdown tools. The first method is to use ChatGPT’s deep research capability: upload all the zip files and have it generate a report based on our criteria. The second method is to place each PDF alongside its corresponding Markdown file. Since we have nine samples, we open nine separate windows and let ChatGPT 5 Pro or Deep Thinking score the tools according to our standards.

*Reproducible, parser-agnostic benchmarks for turning PDFs into Markdown—and measuring downstream usefulness with QA.*

> This repository hosts a lightweight evaluation framework and a static site (GitHub Pages) that publishes datasets, parser outputs, and question sets (JSONL). The goal is to judge **downstream usability** (search, RAG, automation), not just visual fidelity.

---

## Table of Contents

* [Goals](#goals)
* [Key Ideas](#key-ideas)
* [Repository Layout](#repository-layout)
* [Quick Start](#quick-start)
* [Add a New PDF Dataset](#add-a-new-pdf-dataset)
* [Question Set (JSONL) Format](#question-set-jsonl-format)
* [Parsers & Outputs](#parsers--outputs)
* [Evaluation Methods](#evaluation-methods)
* [Publishing with GitHub Pages](#publishing-with-github-pages)
* [Optional: Build a PDF Report via LaTeX + CI](#optional-build-a-pdf-report-via-latex--ci)
* [Roadmap](#roadmap)
* [FAQ](#faq)
* [Contributing](#contributing)
* [License](#license)
* [Citation](#citation)

---

## Goals

* **Apples-to-apples comparison** of multiple PDF→Markdown parsers.
* Emphasize **downstream quality** (QA over Markdown / retrieval) alongside visual/structural fidelity.
* Keep everything **simple, auditable, and reproducible** inside a public repo.

---

## Key Ideas

1. **Datasets:** Each PDF is a dataset with a unique `doc_id`.
2. **Multiple Parsers:** For each dataset, store each parser’s Markdown in its own subfolder.
3. **Questions (JSONL):** Up to 100 PDF-specific questions are authored per dataset.
4. **Downstream Check:** Use the questions to probe RAG/retrieval performance against each parser’s Markdown.

---

## Repository Layout

```
pdf-to-markdown/
├─ docs/                      # Published as GitHub Pages (deploy from /docs)
│  ├─ index.html              # Landing page (dataset cards, links)
│  ├─ pdfs/                   # Original PDFs and (optionally) rendered reports
│  ├─ md/                     # Parser outputs (Markdown)
│  │  └─ <parser>/<doc_id>/   # Either many per-page .md or a single .md
│  └─ questions/              # One JSONL file per dataset (up to 100 Qs)
├─ report/                    # (Optional) LaTeX source for a printable evaluation report
└─ .github/
   └─ workflows/              # (Optional) CI for LaTeX & site checks
```

**Naming conventions**

* `doc_id`: short, URL-friendly identifier for a PDF (e.g., `TP-MVD8MV2-rotated`).
* Parser folder names are free-form (e.g., `mathpix`, `textin`, `reducto`, `marker`, `internal`), but be consistent.

---

## Quick Start

1. **Clone** this repository.
2. **Add PDFs** to `docs/pdfs/` (e.g., `docs/pdfs/<doc_id>.pdf`).
3. **Add Markdown outputs** for each parser to `docs/md/<parser>/<doc_id>/`.

   * Prefer **one file per PDF page**: `001.md`, `002.md`, … (recommended for page-level debugging).
   * Single-file Markdown is also supported (e.g., `full.md`).
4. **Create questions** for the dataset in `docs/questions/<doc_id>.jsonl` (see format below).
5. **Commit & push**. If GitHub Pages is enabled for `/docs`, your site updates automatically.

---

## Add a New PDF Dataset

1. Copy your PDF to:

   ```
   docs/pdfs/<doc_id>.pdf
   ```
2. Drop parser outputs here (repeat for each parser you evaluate):

   ```
   docs/md/<parser>/<doc_id>/001.md
   docs/md/<parser>/<doc_id>/002.md
   ...
   ```

   or as a single file:

   ```
   docs/md/<parser>/<doc_id>/full.md
   ```
3. Author up to 100 questions about this PDF:

   ```
   docs/questions/<doc_id>.jsonl
   ```
4. Commit with a clear message, e.g.:

   ```
   git add docs/pdfs/<doc_id>.pdf docs/md/** docs/questions/<doc_id>.jsonl
   git commit -m "docs: add <doc_id> (PDF, parser MD, 100 Qs)"
   git push
   ```

---

## Question Set (JSONL) Format

A simple, line-delimited JSON file. **One question per line.**

**Canonical schema**

```json
{"id": "Q001", "q": "What is the main hypothesis stated in Section 2?"}
{"id": "Q002", "q": "Report the value of k in Eq. (7)."}
```

**Compatibility note**
If you already have `{ "qid": 1, "question": "..." }`, that’s fine—loaders can map it to `id/q`. Pick one style and use it consistently going forward.

**Helper: generate JSONL from plain text (stdin)**

```bash
python - <<'PY'
import sys, json
n = 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    n += 1
    print(json.dumps({"id": f"Q{n:03d}", "q": line}, ensure_ascii=False))
PY
```

---

## Parsers & Outputs

Place each parser’s output under `docs/md/<parser>/<doc_id>/`. Examples:

```
docs/md/mathpix/TP-MVD8MV2-rotated/001.md
docs/md/textin/TP-MVD8MV2-rotated/001.md
docs/md/reducto/TP-MVD8MV2-rotated/full.md
docs/md/marker/TP-MVD8MV2-rotated/full.md
docs/md/internal/TP-MVD8MV2-rotated/001.md
```

**Tips**

* When a parser converts **tables into images**, retrieval performance may drop (no cells to index).
* Keep **figures’ captions and references** as text near the figure so RAG can ground answers.
* Normalize headings (`#`, `##`, `###`) and math (`$...$`, `$$...$$`) to ease downstream parsing.

---

## Evaluation Methods

This repo is model-agnostic. You can run your own RAG pipeline or use any grader. A common setup:

1. **Chunking/Indexing**

   * Chunk each parser’s Markdown separately.
   * Build an embedding index per parser × dataset.

2. **QA Execution**

   * For each dataset’s JSONL questions, retrieve across that **parser’s** chunks.
   * Answer with your LLM (closed/open-book). Keep the original PDF available for final grading if needed.

3. **Scoring (two layers)**

   * **Intrinsic (structure-aware):**

     * Structural fidelity (headings, lists, math blocks)
     * Formatting accuracy (inline styles)
     * Special content handling (tables, figures, footnotes, references)
     * Content cleanliness (noise removal, artifacts)
     * Ease of post-processing (markdown simplicity, minimal HTML)
     * Automation readiness (predictable structure across pages/files)
   * **Extrinsic (downstream):**

     * Retrieval hit rate / MRR / Recall\@k
     * QA accuracy vs. **gold** (human-checked answers or PDF-grounded grader)
     * Error types (table values wrong, units missing, figure references lost)

> Store your raw run logs anywhere (e.g., `runs/<parser>/<doc_id>/answers.jsonl`) if you want to keep artifacts next to the data.

---

## Publishing with GitHub Pages

This repo is designed to be published from the `/docs` folder.

1. In **GitHub → Settings → Pages**, set:

   * **Source:** “Deploy from a branch”
   * **Branch:** `main` (or `master`)
   * **Folder:** `/docs`
2. Commit your data to `/docs` and push—GitHub Pages will serve them.
3. Link to:

   * `docs/pdfs/` for original PDFs and reports
   * `docs/questions/` for JSONL question sets
   * `docs/md/` for parser outputs

> If you want a custom homepage, edit `docs/index.html` to list datasets, parsers, and counts (e.g., number of `*.md` files per parser).

---

## Optional: Build a PDF Report via LaTeX + CI

If you want a nicely formatted evaluation report (PDF) compiled on every push:

1. Put your LaTeX sources under:

   ```
   report/main.tex
   report/assets/...
   ```
2. Add a GitHub Actions workflow (example):

```yaml
# .github/workflows/latex.yml
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

This will publish `docs/pdfs/evaluation-report.pdf`, which becomes available on your Pages site.

---

## Roadmap

* Side-by-side **PDF vs. Markdown** diff/preview in the site.
* Built-in **retrieval test harness** with simple configs per parser.
* Light **question harvesting** helpers (tables → value questions, figure → caption questions).
* Optional **weighted scoring** profiles (e.g., table-heavy vs. math-heavy documents).
* Dataset “cards” (JSON) to drive the homepage automatically.

---

## FAQ

**Do I have to export one Markdown file per page?**
No. Per-page files help with debugging and page-level analysis, but single-file exports also work. The site logic can count `*.md` files either way.

**What if a parser emits lots of HTML (e.g., `<table>`, inline styles)?**
It’s acceptable, but consider a cleanup pass if it hurts readability or indexing. Favor clean Markdown tables for retrieval and editing.

**Why do QA results differ between parsers on the same PDF?**
Structural losses (e.g., tables turned into images, math dropped, headings flattened) often degrade retrieval and precision.

**Where should I put answers and grader outputs?**
Anywhere outside `docs/` to avoid publishing by default—for example, `runs/<parser>/<doc_id>/…`. Publish only what you intend to share.

---

## Contributing

* Add a new dataset by following **Add a New PDF Dataset**.
* Add a new parser by creating `docs/md/<parser>/<doc_id>/` and placing its Markdown there.
* Open issues/PRs for improvements to the homepage, evaluation criteria, or CI.

---

## License

* Code & configuration: **MIT** (see `LICENSE`).
* Datasets & generated content: provide or respect an appropriate content license (e.g., CC BY 4.0) depending on source material.

---

## Citation

```bibtex
@misc{pdf_to_markdown_eval,
  title  = {PDF-to-Markdown Evaluation},
  author = {Repository Contributors},
  year   = {2025},
  howpublished = {\url{https://github.com/jiyouhai/pdf-to-markdown}}
}
```

---

> *Tip:* Keep the repo small and auditable. Treat `docs/` as the public snapshot; everything else is for your experiments and can evolve without breaking the published site.
