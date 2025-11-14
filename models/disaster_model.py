import os, joblib, pandas as pd, numpy as np
from tensorflow.keras.models import load_model

BASE = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE, "disaster_model.h5")
SCALER_PATH = os.path.join(BASE, "scaler_dis.pkl")

_model = None
_scaler = None

def _load():
    global _model, _scaler
    if _model is None:
        if os.path.exists(MODEL_PATH):
            _model = load_model(MODEL_PATH)
    if _scaler is None:
        if os.path.exists(SCALER_PATH):
            _scaler = joblib.load(SCALER_PATH)

def predict_disaster(inputs: dict) -> float:
    _load()
    numeric_cols = ['tdrop','tbar','tskinice','rainocn','delts','latitude','longitude']
    df = pd.DataFrame([inputs])
    for c in numeric_cols:
        if c not in df:
            df[c] = 0.0
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0.0)
    if _model is None or _scaler is None:
        ts = float(df['tskinice'].iloc[0])
        rain = float(df['rainocn'].iloc[0])
        score = 0.0
        if ts >= 30: score += 0.5
        if rain >= 0.6: score += 0.5
        return float(min(max(score, 0.0), 1.0))
    features = list(_scaler.feature_names_in_)
    df = df.reindex(columns=features, fill_value=0.0)
    X = _scaler.transform(df)
    p = _model.predict(X)[0][0]
    return float(min(max(p, 0.0), 1.0))
