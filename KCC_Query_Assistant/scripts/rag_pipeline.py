import faiss
import pickle
import numpy as np
import requests
from sentence_transformers import SentenceTransformer
import torch
from duckduckgo_search import ddg

# --- Configuration ---
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma:2b"
RELEVANCE_THRESHOLD = 10.0  # FAISS distance threshold
TOP_K = 5

# --- Load Index & Embeddings ---
print("🔁 Loading FAISS index and chunk mapping...")
index = faiss.read_index("embeddings/faiss_index.index")
with open("embeddings/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

# --- Load Embedding Model ---
print("⚙️ Loading multilingual embedding model...")
model = SentenceTransformer("distiluse-base-multilingual-cased-v1", device='cuda' if torch.cuda.is_available() else 'cpu')

# --- Helper Functions ---

def embed_query(query: str):
    return model.encode([query], convert_to_numpy=True)[0]

def search_index(query_embedding):
    D, I = index.search(np.array([query_embedding]), TOP_K)
    return D[0], I[0]

def ask_ollama(prompt: str):
    response = requests.post(
        OLLAMA_URL,
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    )
    return response.json().get("response", "").strip()

def is_generic(chunk):
    lower = chunk.lower()
    return any(phrase in lower for phrase in [
        "given necessary information",
        "farmer asked query",
        "query on weather",
        "information regarding"
    ])

def search_web(query: str):
    try:
        results = ddg(query, max_results=3)
        if not results:
            return None
        return "\n\n".join([
            f"{r['title']}\n{r['body']}\nLink: {r['href']}" for r in results
        ])
    except Exception:
        return None

# --- Main Handler Function ---

def handle_query(user_query: str):
    query_vector = embed_query(user_query)
    distances, indices = search_index(query_vector)

    # Collect relevant KCC chunks
    results = [(d, chunks[i]) for d, i in zip(distances, indices) if i != -1 and d < RELEVANCE_THRESHOLD]
    candidate_chunks = list(dict.fromkeys([c for _, c in results]))
    specific_chunks = [c for c in candidate_chunks if not is_generic(c)]

    # ✅ 1. Answer from KCC + LLM
    if specific_chunks:
        context = "\n---\n".join(specific_chunks)
        prompt = (
            f"You are an expert agricultural assistant. Based on the following advisory data, answer the farmer's question in fluent English. Limit your response to a maximum of 5 bullet points.\n\n"
            f"---\nContext:\n{context}\n---\n"
            f"Question:\n{user_query}\n\nAnswer:"
        )
        return {
            "source": "KCC",
            "context": specific_chunks,
            "answer": ask_ollama(prompt)
        }

    # 🌐 2. Fallback: Internet + LLM
    internet_result = search_web(user_query)
    if internet_result:
        internet_prompt = (
            f"You are an agricultural assistant. Summarize and explain the following web results in fluent English, as a direct answer to the user's question.\n\n"
            f"---\nWeb Search Results:\n{internet_result}\n---\n"
            f"Question:\n{user_query}\n\nAnswer:"
        )
        return {
            "source": "Internet + LLM",
            "context": [],
            "answer": ask_ollama(internet_prompt)
        }

    # 🧠 3. Final fallback: LLM only
    fallback_prompt = (
        f"You are an expert agricultural assistant. No data was found in the dataset or online. Based on your general agricultural knowledge, provide a helpful answer in fluent English. Limit to 5 bullet points.\n\n"
        f"Question:\n{user_query}\n\nAnswer:"
    )
    return {
        "source": "LLM",
        "context": [],
        "answer": ask_ollama(fallback_prompt)
    }
