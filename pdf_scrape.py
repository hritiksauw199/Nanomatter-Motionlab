import fitz  # PyMuPDF
import tabula

pdf_path = '/content/1-s2.0-S0167577X96002157-main.pdf'
full_markdown = ""

# Extract text
with fitz.open(pdf_path) as doc:
    for page_num in range(len(doc)):
        full_markdown += f"### Page {page_num + 1} - Text\n{doc[page_num].get_text('text')}\n\n"

# Extract table
for i, table in enumerate(tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)):
    full_markdown += f"\n### Table {i + 1}\n{table.to_markdown(index=False)}\n\n"


with open("333.md", "w", encoding="utf-8") as output_file:
    output_file.write(full_markdown)

print("Done")
