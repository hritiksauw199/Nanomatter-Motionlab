import fitz  # PyMuPDF
import tabula

pdf_path = "/content/1-s2.0-S0079672722000751-main.pdf"
output_text_file = "199.md"

def detect_super_subscripts(spans):
    formatted_text, prev_span = "", None

    for span in spans:
        text, bbox, font_size = span["text"], span["bbox"], span["size"]

        if prev_span:
            prev_y0, prev_size = prev_span["bbox"][1], prev_span["size"]

            if text.isdigit() and font_size < prev_size:
                formatted_text += f"^{text}" if bbox[1] < prev_y0 else f"_{text}"
                continue

        formatted_text += text
        prev_span = span

    return formatted_text.strip()

full_markdown = ""

# Extract text and detect superscripts/subscripts
with fitz.open(pdf_path) as doc:
    for page_num, page in enumerate(doc, start=1):
        formatted_text = " ".join(
            detect_super_subscripts([{k: span[k] for k in ["text", "bbox", "size"]} for span in line["spans"]])
            for block in page.get_text("dict")["blocks"] if "lines" in block
            for line in block["lines"]
        )
        full_markdown += f"### Page {page_num} - Text\n{formatted_text}\n\n"

# Extract tables
for i, table in enumerate(tabula.read_pdf(pdf_path, pages="all", multiple_tables=True), start=1):
    full_markdown += f"\n### Table {i}\n{table.to_markdown(index=False)}\n\n"

# Save to file
with open(output_text_file, "w", encoding="utf-8") as output_file:
    output_file.write(full_markdown)

print(f"Extraction completed! Text & tables saved in '{output_text_file}'")
