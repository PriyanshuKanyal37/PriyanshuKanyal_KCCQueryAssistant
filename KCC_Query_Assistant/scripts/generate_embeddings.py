import pandas as pd
import os
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
import faiss
import torch

MODEL_NAME = 'distiluse-base-multilingual-cased-v1'
BATCH_SIZE = 10000
DATA_PATH = "data/cleaned_kcc_data.csv"
INDEX_PATH = "embeddings/faiss_index.index"
CHUNKS_PATH = "embeddings/chunks.pkl"
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

df = pd.read_csv(DATA_PATH)
chunks = df['chunk'].tolist()

print(f"Loading model '{MODEL_NAME}' on device: {DEVICE}")
model = SentenceTransformer(MODEL_NAME, device=DEVICE)
embedding_dim = model.get_sentence_embedding_dimension()

if os.path.exists(INDEX_PATH) and os.path.exists(CHUNKS_PATH):
    print("Found existing index — loading...")
    index = faiss.read_index(INDEX_PATH)
    with open(CHUNKS_PATH, "rb") as f:
        all_chunks = pickle.load(f)
else:
    print("Creating new FAISS index...")
    index = faiss.IndexFlatL2(embedding_dim)
    all_chunks = []

start = len(all_chunks)  # Resume support
for i in range(start, len(chunks), BATCH_SIZE):
    batch_chunks = chunks[i:i + BATCH_SIZE]
    print(f"\nEncoding batch {i // BATCH_SIZE + 1} | Records {i} to {i + len(batch_chunks)}")

    embeddings = model.encode(batch_chunks,
                              show_progress_bar=True,
                              convert_to_numpy=True,
                              device=DEVICE)

    index.add(embeddings)
    all_chunks.extend(batch_chunks)

    os.makedirs("embeddings", exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(all_chunks, f)

    print(f"Batch {i // BATCH_SIZE + 1} saved.")

print(f"\nCompleted! Total indexed chunks: {len(all_chunks)}")
print(f"Index saved at: {INDEX_PATH}")
