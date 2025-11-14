# Neptune

Neptune is a small Flask app that provides an ocean-focused chat UI and simple ML models for fishing/disaster prediction. This repo contains lightweight example models and a FAISS vectorstore built from a CSV dataset.

Important: the project will download and/or build some models and a FAISS index on first run. That can be heavy and may require extra build steps on Windows (see notes below).

## Quick start (Windows PowerShell)

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

Note: `faiss-cpu` may not have an official wheel for your Windows/Python version. If `pip install faiss-cpu` fails, consider using conda:

```powershell
conda create -n neptune python=3.11
conda activate neptune
conda install -c conda-forge faiss-cpu
pip install -r requirements.txt --no-deps
```

3. (Optional) Skip heavy building on startup

Set an environment variable to skip building the Keras models and FAISS index during startup. Useful for development, tests, and CI.

```powershell
$env:NEPTUNE_SKIP_BUILD = "1"
```

4. Run the app

```powershell
python app.py
```

Open http://127.0.0.1:5000/ in your browser and try the chat page.

## Tests

A very small test is included that uses the Flask test client and sets `NEPTUNE_SKIP_BUILD` to avoid heavy downloads/builds.

Install `pytest` then run:

```powershell
pip install pytest
pytest -q
```

## Files of interest

- `app.py` — Flask entrypoint
- `routes/api.py` — API endpoints; starts resource build unless skipped
- `models/*` — small model wrappers and a training helper
- `templates/*` — basic UI
- `data/output.csv` — source dataset used to build embeddings and train toy models
- `vectorstore/*` — FAISS index and embeddings (built on demand)

## Notes & Troubleshooting

- If TensorFlow install is problematic, consider using `tensorflow-cpu` or a compatible wheel for your Python version.
- The repo includes `models/*.h5` as pre-saved examples; if they are missing, the app will train small models from `data/output.csv` (this may take several minutes).
- FAISS and Sentence Transformers will download model weights the first time they run — ensure you have network access.

If you'd like, I can:
- Add a small CI config (GitHub Actions) to run the tests on push.
- Add more tests around predictions.
- Make the UI fancier.

