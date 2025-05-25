
# KCC Query Assistant

**KCC Query Assistant** is an offline-ready, AI-powered chatbot designed to help farmers, agricultural officers, and rural citizens easily access reliable information from the **Kisan Call Center (KCC)** dataset. The assistant can understand queries in plain language and respond with useful advice from government datasets or generate relevant explanations using AI.

---

## What is This Project?

Farmers in India often face challenges in getting real-time, region-specific agricultural advice. The KCC Query Assistant solves this by using:

- A cleaned dataset from real queries answered by Kisan Call Centers
- Smart semantic search to match the most relevant advice
- Local AI models that can explain and simplify responses
- A fallback system that uses the internet to find missing answers
- A simple user interface made for easy usage in rural or low-tech environments

This assistant is multilingual and lightweight, making it ideal for use in village-level computer centers, agricultural kiosks, and mobile devices.


## How Does It Work?

```
User types a question
     ↓
Search KCC dataset using semantic similarity
     ↓
If good match found:
    → Use AI model to summarize the result
Else:
    → Search the web using DuckDuckGo
    → Summarize findings using LLM
If nothing found:
    → Use general agricultural AI response
```

---

## ⚠️ Note on Dataset & Embedding Files

Due to file size limitations on GitHub, some core assets are **not included directly in this repository**:

### 1 KCC Dataset:
-  The full CSV dataset (`kcc_raw.csv`) is approximately **800 MB** and with **1.4 Million Data** is hosted externally.

- **Download Raw Dataset**
- 
   You can download the raw KCC dataset from this Google Drive link:
  
 **[Download Dataset from Google Drive](https://drive.google.com/file/d/1MtACzq796TaVxs0kCe1ydZFpmHUi6-Rf/view?usp=sharing)**


### 2 Embeddings + FAISS Index:
- The precomputed `chunks.pkl` and `faiss_index.index` files are **around 2.7 GB** and must be generated locally.

**Generate Embeddings Locally**

To generate embeddings and build the FAISS index on your own machine:

1. **Preprocess the dataset**  
   ```bash
   python scripts/preprocess_data.py

1. **Generate embeddings and index**
   ```bash
   python scripts/generate_embeddings.py


## Quick Start Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/PriyanshuKanyal37/PriyanshuKanyal_KCCQueryAssistant.git
cd PriyanshuKanyal_KCCQueryAssistant
```

### 2. Install the Required Packages

```bash
pip install -r requirements.txt
```

### 3. Start the Ollama LLM Engine

```bash
ollama run gemma:2b
```

### 4. Launch the Chatbot

```bash
streamlit run scripts/app.py
```

---

## Sample Queries to Try

Some questions that work well:

1. How to increase yield in organic turmeric farming?
2. How to control whiteflies in cotton crops?
3. What is the PM-Kisan Yojana?
4. How to manage drought stress in groundnut cultivation?
5. Best crop for dry soil in Rajasthan?
6. What are pest control methods for paddy in Tamil Nadu?
7. How to protect banana crops from strong winds?
8. What diseases affect tomato plants?
9. How to get subsidy for solar pumps?
10. How to identify zinc deficiency in rice?
---

## Technology Stack

| Component         | Tool / Framework         |
|------------------|--------------------------|
| Dataset           | Kisan Call Center (CSV)  |
| Embeddings        | Sentence Transformers    |
| Vector Database   | FAISS                    |
| Local AI Model    | Ollama + Gemma 2B        |
| Web Search        | DuckDuckGo API           |
| Frontend UI       | Streamlit                |

---

## Performance and Caching

- Uses `@st.cache_resource` to avoid reloading models, index, and data
- Ideal for systems with limited internet or computing power
- Works on CPU or GPU with quantized models

---

## Folder Structure

```
KCC_Query_Assistant/
├── scripts/
│   ├── app.py               # Streamlit frontend
│   ├── rag_pipeline.py      # Core logic and LLM interaction
│   ├── preprocess_kcc.py    # Data cleaning and chunking
|   ├── generate_embeddings.py 
├── embeddings/
│   ├── faiss_index.index
│   ├── chunks.pkl
├── data/
│   └── kcc_data.csv
├── sample_queries.txt
├── requirements.txt
└── README.md
```

---

## Demo Video

You can watch a short walkthrough demo on Google Drive:

[Demo Video](https://drive.google.com/your-demo-link-here)

---

## Author

Created by Priyanshu Kanyal


## Why This Matters

More than 60% of India's population depends on agriculture, yet timely advice is hard to come by in remote areas. KCC Query Assistant uses open data and AI to bridge that gap and empower rural communities with accurate, fast, and local language support.
