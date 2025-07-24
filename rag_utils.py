import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
import groq

load_dotenv(dotenv_path=r"C:\Users\tibde\Desktop\Projects\h_rag\.env")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print("KEY:", GROQ_API_KEY)

# Groq client (used to call the llm to generate the answers)
client = groq.Groq(api_key=GROQ_API_KEY) #initialize commuincation with the groq llm llama3.1

# Vector DB path faiss vector 
VECTOR_DB_PATH = "model_store/vector_db"

# HuggingFace Embedding Model 
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def build_faiss_index(chunks):
    docs = [Document(page_content=chunk["text"], metadata=chunk["metadata"]) for chunk in chunks]
    vectorstore = FAISS.from_documents(docs, embedding_model)
    vectorstore.save_local(VECTOR_DB_PATH)
    print(f"FAISS index saved at: {VECTOR_DB_PATH}")


def search(query, top_k=5):
    """
    Retrieve top-k relevant chunks from FAISS store.
    """
    vectorstore = FAISS.load_local(VECTOR_DB_PATH, embedding_model, allow_dangerous_deserialization=True)
    results = vectorstore.similarity_search(query, k=top_k)
    return [doc.page_content for doc in results]


def generate_answer_with_groq(query, top_chunks):

    try:
        
        context = "\n\n".join(top_chunks)

        system_prompt =  "You are a highly accurate and intelligent assistant. Your job is to answer the user's question using only the  information provided in the context. Carefully read all the context chunks and extract relevant facts to form a clear, complete, and precise answer. If multiple chunks contribute to the answer, combine them logically without repeating content. Do not guess or add any information that is not supported by the context. If the context does not contain enough information, respond with 'Not enough information in the context to answer this question. Do not include any asterisks, markdown, or formatting — just return clean text in a formal tone. Avoid summarizing the context — focus only on answering the question directly based on the facts given."

        full_prompt = f"""[Context]\n{context}\n\n[User Question]\n{query}\n\n[Answer]"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.3, #lower value for more deterministic answers and factual answers
            max_tokens=2000 #limit of the response length to avoid excessive output
        )

        # print("Response:\n", response.choices[0].message.content)
        return response.choices[0].message.content

    except Exception as e:
        print("Error while calling Groq API:", e)
        return None

