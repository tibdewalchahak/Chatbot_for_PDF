INDEX_PATH = "app/model_store/index.faiss"
# CHUNKS_PATH = "app/model_store/chunks.pkl"

# def build_faiss_index(chunks):
#     embeddings = model.encode(chunks)
#     dim = embeddings.shape[1]
#     index = faiss.IndexFlatL2(dim)
#     index.add(embeddings)
    
#     os.makedirs("app/model_store", exist_ok=True)
#     faiss.write_index(index, INDEX_PATH)

#     with open(CHUNKS_PATH, "wb") as f:
#         pickle.dump(chunks, f)

# def search(query, top_k=3):
#     index = faiss.read_index(INDEX_PATH)
#     with open(CHUNKS_PATH, "rb") as f:
#         chunks = pickle.load(f)

#     query_embedding = model.encode([query])
#     D, I = index.search(query_embedding, top_k)
    
#     return [chunks[i] for i in I[0]]