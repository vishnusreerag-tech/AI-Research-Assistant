from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def retrieve_chunks(query_embedding, embeddings, chunks, top_k=3):

    similarities = cosine_similarity(query_embedding, embeddings)[0]

    top_indices = np.argsort(similarities)[-top_k:]

    relevant_chunks = [chunks[i] for i in top_indices]

    return relevant_chunks