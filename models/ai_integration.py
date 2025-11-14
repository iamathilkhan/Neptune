import os, pickle, time
import numpy as np
import pandas as pd
from .train_and_load import ensure_models_exist
from .fishing_model import predict_fishing
from .disaster_model import predict_disaster

from sentence_transformers import SentenceTransformer
import faiss

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

BASE = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE, "..", "data", "output.csv")
VECTOR_DIR = os.path.join(BASE, "..", "vectorstore")
os.makedirs(VECTOR_DIR, exist_ok=True)
FAISS_PATH = os.path.join(VECTOR_DIR, "index.faiss")
META_PATH = os.path.join(VECTOR_DIR, "meta.pkl")
EMB_PATH = os.path.join(VECTOR_DIR, "embeddings.npy")

_EMBED_NAME = "all-MiniLM-L6-v2"
_LM_NAME = "distilgpt2"

_embedder = None
_index = None
_meta = None
_tokenizer = None
_lm = None

def _lazy_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(_EMBED_NAME)
    return _embedder

def _lazy_lm():
    global _tokenizer, _lm
    if _lm is None:
        _tokenizer = AutoTokenizer.from_pretrained(_LM_NAME)
        _lm = AutoModelForCausalLM.from_pretrained(_LM_NAME)
        _lm.eval()
    return _tokenizer, _lm

def build_index_if_missing(sample_rows=50000):
    if os.path.exists(FAISS_PATH) and os.path.exists(META_PATH) and os.path.exists(EMB_PATH):
        return
    print("Building FAISS index (this may take a minute)...")
    df = pd.read_csv(DATA_PATH, low_memory=False).fillna("")
    numeric_cols = ['tdrop','tbar','tskinice','rainocn','delts','latitude','longitude','time']
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^0-9\.\-]', '', regex=True), errors='coerce').fillna(0.0)
    if len(df) > sample_rows:
        df = df.sample(n=sample_rows, random_state=42).reset_index(drop=True)
    texts = df.apply(lambda r: f"Lat:{r.latitude} Lon:{r.longitude} Tdrop:{r.tdrop} Tbar:{r.tbar} Tskinice:{r.tskinice} Rain:{r.rainocn}", axis=1).astype(str).tolist()
    embedder = _lazy_embedder()
    embs = embedder.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    np.save(EMB_PATH, embs)
    d = embs.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embs)
    faiss.write_index(index, FAISS_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump({"texts": texts}, f)
    print("Index built and saved.")

def _load_index():
    global _index, _meta
    if _index is not None and _meta is not None:
        return _index, _meta
    if not (os.path.exists(FAISS_PATH) and os.path.exists(META_PATH) and os.path.exists(EMB_PATH)):
        build_index_if_missing()
    index = faiss.read_index(FAISS_PATH)
    with open(META_PATH, "rb") as f:
        meta = pickle.load(f)
    _index = index
    _meta = meta
    return _index, _meta

def build_all_if_missing():
    ensure_models_exist()
    build_index_if_missing()

def retrieve_context(query, top_k=3):
    index, meta = _load_index()
    embedder = _lazy_embedder()
    q_emb = embedder.encode([query], convert_to_numpy=True)
    D, I = index.search(q_emb, top_k)
    texts = [meta["texts"][int(i)] for i in I[0]]
    return texts

def ai_query_handler(user_query: str, context_data: dict):
    ensure_models_exist()
    fish_p = predict_fishing(context_data)
    dis_p = predict_disaster(context_data)
    fish_pct = (fish_p*100.0) if fish_p <= 1.0 else fish_p
    dis_pct = (dis_p*100.0) if dis_p <= 1.0 else dis_p

    retrieved = retrieve_context(user_query, top_k=3)
    retrieved_text = "\n".join(retrieved)

    if dis_pct > 50:
        safety = f"High disaster risk: {dis_pct:.1f}%. Follow official guidance."
    else:
        safety = f"Low disaster risk: {dis_pct:.1f}%."

    if fish_pct > 70:
        fish_msg = f"Great fishing conditions: {fish_pct:.1f}% — try nearby coords below."
    elif fish_pct > 40:
        fish_msg = f"Moderate fishing chance: {fish_pct:.1f}%."
    else:
        fish_msg = f"Low fishing probability: {fish_pct:.1f}%."

    deterministic = f"{fish_msg} {safety}\nRelevant records:\n{retrieved_text}"

    try:
        tokenizer, lm = _lazy_lm()
        prompt = f"You are a friendly ocean guide. User asked: \"{user_query}\".\n{deterministic}\nAnswer concisely and friendly."
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = lm.generate(**inputs, max_new_tokens=120, do_sample=True, top_p=0.9, temperature=0.7, pad_token_id=tokenizer.eos_token_id)
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        if text.strip().startswith(prompt.strip()):
            gen = text[len(prompt):].strip()
            if not gen:
                gen = deterministic
        else:
            gen = text.strip()
        return {"response": gen}
    except Exception:
        return {"response": deterministic}
