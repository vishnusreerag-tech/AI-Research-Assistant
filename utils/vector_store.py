import chromadb
from sentence_transformers import SentenceTransformer

# Create persistent ChromaDB client
client = chromadb.PersistentClient(path="chroma_db")

# Create collection
collection = client.get_or_create_collection(
    name="research_assistant"
)

# Load embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ---------------- CLEAR DATABASE ----------------

def clear_database():

    client.delete_collection("research_assistant")

    global collection

    collection = client.get_or_create_collection(
        name="research_assistant"
    )


# ---------------- STORE EMBEDDINGS ----------------
def store_embeddings(chunks, source_name):

    embeddings = embedding_model.encode(chunks)

    ids = [
        f"{source_name}_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "source": source_name,
            "page": i + 1
        }
        for i, _ in enumerate(chunks)
    ]

    collection.add(
        embeddings=embeddings.tolist(),
        documents=chunks,
        metadatas=metadatas,
        ids=ids
    )

# ---------------- RETRIEVE CHUNKS ----------------

def retrieve_chunks(query, top_k=5):

    query_embedding = embedding_model.encode([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return (
        results["documents"][0],
        results["metadatas"][0]
    )