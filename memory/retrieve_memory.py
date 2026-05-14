from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

print("Loading retrieval model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

# Load saved FAISS index
index = faiss.read_index("memory/vector.index")

# Load saved documents
with open("memory/documents.txt", "r", encoding="utf-8") as f:
    documents = f.readlines()


def retrieve_relevant_memory(query, k=2):

    # Convert query into embedding
    query_embedding = model.encode([query])

    # Convert to numpy float32
    query_embedding = np.array(query_embedding).astype("float32")

    # Search similar vectors
    distances, indices = index.search(query_embedding, k)

    results = []

    for i in indices[0]:
        if i < len(documents):
            results.append(documents[i].strip())

    return "\n".join(results)