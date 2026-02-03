import sys, subprocess
try:
    from pypdf import PdfReader
except Exception:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "pypdf"])
    from pypdf import PdfReader

reader = PdfReader(r"docs\va-2025.pdf")
parts = []
for i, page in enumerate(reader.pages):
    txt = page.extract_text()
    parts.append(f"--- Page {i+1} ---\n")
    if txt:
        parts.append(txt)
    else:
        parts.append("[NO TEXT]\n")
with open(r"docs\va-2025.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(parts))
print("WROTE docs\\va-2025.txt")
