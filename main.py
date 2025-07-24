from pdf_utils import extract_text_from_pdf, chunk_text
from rag_utils import build_faiss_index, search, generate_answer_with_groq

def main():
    print("Welcome to the Document Q&A Agent\n\n")

    doc_path = input("Enter the path to your PDF file: ").strip()
    print(f"Loading and processing document: {doc_path}")

    text = extract_text_from_pdf(doc_path)
    chunks = chunk_text(text)
    build_faiss_index(chunks)

    print("\nDocument loaded. Ask your questions (type 'exit' to quit):\n")

    while True:
        query = input("Ask: ")
        if query.lower() in ['exit', 'quit']:
            print("Exiting.")
            break
        try:
            top_chunks = search(query)
            answer = generate_answer_with_groq(query, top_chunks)
            print("\nAnswer:\n", answer, "\n")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
