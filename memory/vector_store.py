from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("memory/documents.txt", "r", encoding="utf-8") as file:
    documents = file.readlines()

documents = [doc.strip() for doc in documents if doc.strip()]

embeddings = model.encode(documents)

embedding_dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(embedding_dimension)

index.add(np.array(embeddings))

faiss.write_index(index, "memory/vector.index")
print("Vector database created successfully.")

query = input("Enter your query: ")

query_embedding = model.encode([query])

distances, indices = index.search(
    np.array(query_embedding),
    k=2
)

print("\nTop Matching Documents:\n")

for i in indices[0]:
    print(documents[i])