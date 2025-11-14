import os, joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam

BASE = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE, "..", "data", "output.csv")
FISH_MODEL = os.path.join(BASE, "fishing_model.h5")
DIS_MODEL = os.path.join(BASE, "disaster_model.h5")
SCALER_F = os.path.join(BASE, "scaler_fish.pkl")
SCALER_D = os.path.join(BASE, "scaler_dis.pkl")

SAMPLE_SIZE = 50000

def _read_and_clean(sample_size=SAMPLE_SIZE):
    df = pd.read_csv(DATA_PATH, low_memory=False)
    numeric_cols = ['tdrop','tbar','tskinice','rainocn','delts','latitude','longitude']
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^0-9\.\-]', '', regex=True), errors='coerce')
        else:
            df[c] = np.nan
    df = df.dropna(subset=numeric_cols)
    if len(df) > sample_size:
        df = df.sample(n=sample_size, random_state=42)
    df = df.reset_index(drop=True)
    return df

def train_and_save():
    df = _read_and_clean()
    y_fish = ((df['tdrop'] >= 28) & (df['rainocn'] <= 0.5)).astype(int)
    X_fish = df[['tdrop','tbar','rainocn','delts','latitude','longitude']].copy()
    scaler_f = StandardScaler().fit(X_fish)
    Xf_scaled = scaler_f.transform(X_fish)

    model_f = Sequential([
        Dense(64, activation='relu', input_shape=(Xf_scaled.shape[1],)),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model_f.compile(optimizer=Adam(learning_rate=1e-3), loss='binary_crossentropy', metrics=['accuracy'])
    model_f.fit(Xf_scaled, y_fish, epochs=5, batch_size=1024, validation_split=0.1, verbose=1)

    model_f.save(FISH_MODEL)
    joblib.dump(scaler_f, SCALER_F)

    y_dis = ((df['tskinice'] >= 29) & (df['rainocn'] >= 0.6)).astype(int)
    X_dis = df[['tdrop','tbar','tskinice','rainocn','delts','latitude','longitude']].copy()
    scaler_d = StandardScaler().fit(X_dis)
    Xd_scaled = scaler_d.transform(X_dis)

    model_d = Sequential([
        Dense(64, activation='relu', input_shape=(Xd_scaled.shape[1],)),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model_d.compile(optimizer=Adam(learning_rate=1e-3), loss='binary_crossentropy', metrics=['accuracy'])
    model_d.fit(Xd_scaled, y_dis, epochs=5, batch_size=1024, validation_split=0.1, verbose=1)

    model_d.save(DIS_MODEL)
    joblib.dump(scaler_d, SCALER_D)

    return True

def ensure_models_exist():
    if os.path.exists(FISH_MODEL) and os.path.exists(DIS_MODEL) and os.path.exists(SCALER_F) and os.path.exists(SCALER_D):
        return True
    print("Training ANN models (this will take a few minutes) ...")
    train_and_save()
    return True