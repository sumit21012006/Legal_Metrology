import hashlib
from pathlib import Path
import fitz  # PyMuPDF
import pdfplumber

def calculate_sha256(file_path: Path) -> str:
    """Calculates SHA-256 hash of a file for integrity verification and deduplication."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def extract_text_from_pdf(pdf_path: Path) -> tuple[str, list[dict]]:
    """
    Extracts text page-by-page from PDF file using PyMuPDF (fitz), fallback to pdfplumber/pytesseract OCR.
    Returns full text string and a list of page objects: [{'page': 1, 'text': '...'}]
    """
    pages_data = []
    full_text_list = []

    try:
        doc = fitz.open(pdf_path)
        for page_num, page in enumerate(doc, start=1):
            page_text = page.get_text("text")
            
            # If PyMuPDF returned almost no text, try pdfplumber if available
            if not page_text or len(page_text.strip()) < 30:
                try:
                    import pdfplumber
                    with pdfplumber.open(pdf_path) as plumber_pdf:
                        if page_num <= len(plumber_pdf.pages):
                            plumber_page = plumber_pdf.pages[page_num - 1]
                            page_text = plumber_page.extract_text() or ""
                except Exception:
                    pass

            cleaned_text = page_text.strip()
            pages_data.append({
                "page": page_num,
                "text": cleaned_text
            })
            full_text_list.append(cleaned_text)
        doc.close()
    except Exception as e:
        print(f"Error parsing PDF {pdf_path}: {e}")

    full_text = "\n\n".join(full_text_list)
    return full_text, pages_data
