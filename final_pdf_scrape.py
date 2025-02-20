import fitz  # form PyMuPDF
import tabula
import os


pdf_path = "/content/1-s2.0-S0079672722000751-main.pdf"
output_text_file = "199.md"


full_markdown = ""

def detect_super_subscripts(spans):
    """Detect superscript and subscript numbers using font size and position."""
    formatted_text = ""
    prev_span = None

    for span in spans:
        text = span["text"]
        bbox = span["bbox"]  
        font_size = span["size"]  

        if prev_span:
            prev_y0 = prev_span["bbox"][1]  
            prev_size = prev_span["size"]  

            #  superscript 
            if text.isdigit() and font_size < prev_size and bbox[1] < prev_y0:
                formatted_text += f"^{text}"
                continue

            #  subscript
            elif text.isdigit() and font_size < prev_size and bbox[1] > prev_y0:
                formatted_text += f"_{text}"
                continue

        formatted_text += text
        prev_span = span

    return formatted_text.strip()

# Extract text using PyMuPDF 
with fitz.open(pdf_path) as doc:
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text_blocks = page.get_text("dict")["blocks"] 
        formatted_text = ""

        for block in text_blocks:
            if "lines" in block:
                for line in block["lines"]:
                    spans = [
                        {"text": span["text"], "bbox": span["bbox"], "size": span["size"]}
                        for span in line["spans"]
                    ]
                    formatted_text += detect_super_subscripts(spans) + " "

        # Markdown file
        full_markdown += f"### Page {page_num + 1} - Text\n"
        full_markdown += formatted_text + "\n\n"

# Step 2: Extract tables 
tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)

for i, table in enumerate(tables):
    full_markdown += f"\n### Table {i + 1}\n"
    markdown_table = table.to_markdown(index=False)
    full_markdown += markdown_table + "\n\n"


with open(output_text_file, "w", encoding="utf-8") as output_file:
    output_file.write(full_markdown)

print(f"Extraction completed!\n- Text & tables saved in '{output_text_file}'")
