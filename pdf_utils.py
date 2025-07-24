# pdf_utils.py

from langchain.text_splitter import RecursiveCharacterTextSplitter

import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    Extracts full text from a PDF file using PyMuPDF.
    """
    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        if text.strip():
            full_text += f"\n\n--- Page {page_num} ---\n{text.strip()}"

    doc.close()
    return full_text


def chunk_text(full_text, chunk_size=1000, chunk_overlap=250):
    """
    Splits the full extracted PDF text into overlapping chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""]
    )

    split_chunks = splitter.split_text(full_text)

    chunks = []
    for i, chunk in enumerate(split_chunks):
        chunks.append({
            "text": chunk.strip(),
            "metadata": {"chunk_id": i + 1}
        })

    return chunks
