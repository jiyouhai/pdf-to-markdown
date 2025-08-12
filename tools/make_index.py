import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
pdf_dir = ROOT/"docs/pdfs"
md_root = ROOT/"docs/md"
parsers = []
if md_root.exists():
    parsers = [p.name for p in md_root.iterdir() if p.is_dir()]

index = {}
for pdf in sorted(pdf_dir.glob("*.pdf")):
    doc_id = pdf.stem
    md_map = {}
    for parser in parsers:
        p = md_root/parser/doc_id
        md_map[parser] = str(p.relative_to(ROOT)).replace("\\","/") if p.exists() else ""
    index[doc_id] = {"pdf": str(pdf.relative_to(ROOT)).replace("\\","/"), "md": md_map}

out = ROOT/"questions/index.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
print("Wrote", out)
