# PDF-to-Markdown Evaluation

This repository showcases the results of our **PDF → Markdown** evaluation.  
It hosts **all final PDFs** and **Markdown outputs** on GitHub Pages.

- **Live site:** https://jiyouhai.github.io/pdf-to-markdown/
- **PDFs:** under `docs/pdfs/` (entire folder mirrored)
- **Markdown outputs:** under `docs/md/`

## What’s inside
- End-to-end perspective: judge utility by **QA over parsed Markdown**, not only formatting.
- Reproducible structure: simple static publishing now, room for LaTeX + CI later.
- Clear separation of artifacts (PDFs vs. Markdown vs. LaTeX sources).

## Repository layout
```
pdf-to-markdown/
├─ docs/              # Published site (GitHub Pages)
│  ├─ index.html      # Landing page
│  ├─ pdfs/           # ALL PDFs (mirrored from your local folder)
│  └─ md/             # Markdown outputs (mirrored from your local folder)
├─ report/            # LaTeX sources (placeholder, add Overleaf export here)
│  ├─ .gitignore
│  └─ README.md
└─ .github/
   └─ workflows/
      └─ latex.yml    # Reserved (only runs if .tex exists)
```

## How to update
- Replace files under `docs/pdfs/` or `docs/md/` and commit; **or**
- Re-run the bootstrap script with your local folders to refresh the mirror.

## Add LaTeX later (optional)
1. Export sources from Overleaf and put them into `report/`.
2. The reserved workflow `latex.yml` will **auto-skip** unless `.tex` files exist.
3. We can extend CI to publish the compiled PDF to `docs/pdfs/` on every push.

## License
- Code/scripts: MIT (see `LICENSE`).
- Report content: choose your own (e.g., CC BY 4.0) — update as needed.

## Citation (example)
```
@misc{pdf_to_md_eval_2025,
  title  = {PDF-to-Markdown Evaluation},
  author = {Xiaoxiao},
  year   = {2025},
  url    = {https://github.com/jiyouhai/pdf-to-markdown}
}
```
