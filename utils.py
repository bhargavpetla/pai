# utils.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(query_embedding, data_embeddings):
    query_embedding = np.array(query_embedding).reshape(1, -1)
    data_embeddings = np.array([item['embedding'] for item in data_embeddings])
    similarities = cosine_similarity(query_embedding, data_embeddings)[0]
    return similarities
