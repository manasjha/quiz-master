import fitz  # PyMuPDF

PDF_PATH = "1649674601_03 Polity Ques..pdf"  # Update this if needed

doc = fitz.open(PDF_PATH)
for page_num, page in enumerate(doc):
    print(f"\n--- Page {page_num + 1} ---\n")
    print(page.get_text("text"))  # Print extracted text

print("\n✅ Text extraction complete!")