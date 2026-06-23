import fitz

def extract_text_from_pdf(pdf_path):
    """
    Extracts embedded digital text from PDF layers using PyMuPDF (fitz).
    """
    extracted_content = []
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text = page.get_text("text")
                if text:
                    extracted_content.append(text)
    except Exception as e:
        print(f"[ERROR] Native extraction failed for {pdf_path}: {e}")
    
    return "\n".join(extracted_content).strip()