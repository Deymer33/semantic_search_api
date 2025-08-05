import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Cargar modelo y embeddings precalculados
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

with open('embeddings.pkl', 'rb') as f:
    df, embeddings = pickle.load(f)

def search_tools(query, top_k=3):
    query_embedding = model.encode([query])
    scores = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = np.argsort(scores)[::-1]

    seen = set()
    results = []

    for idx in top_indices:
        row = df.iloc[idx]
        if row['link'] not in seen:
            seen.add(row['link'])
            results.append({
                "tool": row['description'],
                "link": row['link'],
                "name": row['name'],
                "suggestion": f"Te recomendamos esta herramienta para: {row['description'][:80]}..."
            })
        if len(results) == top_k:
            break

    return results
