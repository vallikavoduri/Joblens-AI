# ml/ — Machine learning notebooks + scripts

All ML work lives here. The backend imports trained models from `ml/models/` at runtime.

## Layout (filled in across phases)

```
ml/
├── notebooks/
│   ├── 01_email_classifier.ipynb     # Phase 2 — DistilBERT / zero-shot
│   ├── 02_resume_jd_match.ipynb      # Phase 3 — sentence-transformers
│   └── 03_telegram_ner.ipynb         # Phase 4 — spaCy NER (stretch)
├── data/           # gitignored — raw datasets
├── models/         # gitignored — trained model artifacts
└── mlruns/         # gitignored — MLflow experiment logs
```

## Why a separate folder

Keeps notebooks + experimentation **out of the backend's dependency tree**. The backend stays slim — only loads the final saved models.

## Concepts you'll touch here

- **Supervised classification** — precision / recall / F1 / confusion matrix
- **Transformers** — DistilBERT fine-tuning vs zero-shot BART
- **Sentence embeddings** — cosine similarity, semantic vs lexical search
- **MLflow** — experiment tracking (a small but huge resume signal)

See `docs/LEARNING_ROADMAP.md` for the free resources tied to each.
