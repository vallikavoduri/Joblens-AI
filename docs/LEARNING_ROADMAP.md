# AI/ML Learning Roadmap (free-only)

Two parallel tracks:

- **Track A — Just-in-time learning during the build (June 16–29).** Every concept is tied to a Phase in `PROJECT_PLAN.md`. Don't pre-study — learn the moment you need it. This is how concepts actually stick.
- **Track B — Long-term foundations (post-June 30, 3–6 months).** Builds the depth recruiters and interviewers expect. Do this AFTER the project ships.
- **Track C — Interview prep (parallel to B).** Specific to data science / ML engineer / data analyst interviews.

> **Rule:** every resource below is **free** (some via Coursera "audit" option, which gives free access to all videos and quizzes — you only pay if you want a certificate, which you don't need).

---

## Track A — Just-in-time during the build

### Phase 1 — Core CRUD & Dashboard (Days 2–5)
**No ML needed.** But brush up on these if rusty:

| Topic | Resource | Time |
|---|---|---|
| FastAPI basics | [FastAPI official tutorial](https://fastapi.tiangolo.com/tutorial/) | 2 hrs |
| React + Vite intro | [React docs — Quick Start](https://react.dev/learn) | 1 hr |
| Tailwind CSS | [Tailwind docs — Utility-first](https://tailwindcss.com/docs/utility-first) | 30 min |
| SQLAlchemy basics | [SQLAlchemy 2.0 ORM tutorial](https://docs.sqlalchemy.org/en/20/orm/quickstart.html) | 1 hr |

### Phase 2 — Email classifier (Days 6–8)

These four concepts are interview gold. **Watch in this order:**

| Topic | Resource | Time | Why it matters |
|---|---|---|---|
| What is supervised learning | [StatQuest — ML fundamentals playlist (videos 1–4)](https://www.youtube.com/playlist?list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF) | 40 min | Asked in EVERY ML interview |
| Train/test split, overfitting | [StatQuest — Cross Validation](https://www.youtube.com/watch?v=fSytzGwwBVw) | 7 min | Asked in EVERY ML interview |
| Precision / Recall / F1 / Confusion matrix | [StatQuest — Confusion Matrix + Sensitivity & Specificity](https://www.youtube.com/watch?v=Kdsp6soqA7o) | 12 min | Always asked when classifier is involved |
| What is a transformer (high-level) | [3Blue1Brown — But what is a GPT? (chapter 5)](https://www.youtube.com/watch?v=wjZofJX0v4M) | 27 min | Modern NLP must-know |
| Hugging Face pipelines (zero-shot, fine-tune) | [HF NLP Course Ch. 1 + Ch. 3](https://huggingface.co/learn/nlp-course) | 3 hrs | Direct hands-on — exactly what you'll build |

### Phase 3 — Resume↔JD matching (Days 9–10)

| Topic | Resource | Time |
|---|---|---|
| Word embeddings intuition | [3Blue1Brown — Word vectors visualized (Chapter 1 of "But what is a GPT?")](https://www.youtube.com/watch?v=wjZofJX0v4M) | covered above |
| Sentence embeddings & cosine similarity | [Sentence-Transformers official quick start](https://sbert.net/docs/quickstart.html) | 1 hr |
| Why semantic > keyword search | [Pinecone — What are embeddings (free article)](https://www.pinecone.io/learn/vector-embeddings/) | 20 min |

### Phase 4 — Telegram + NER [stretch]

| Topic | Resource | Time |
|---|---|---|
| Named Entity Recognition basics | [spaCy — NER tutorial](https://spacy.io/usage/linguistic-features#named-entities) | 30 min |
| Zero-shot NER with LLMs | [HF NLP Course Ch. 7 — Token Classification](https://huggingface.co/learn/nlp-course/chapter7/2) | 1 hr |

### Phase 5 — Deploy

| Topic | Resource | Time |
|---|---|---|
| Docker basics | [Docker — Get Started (Parts 1–3)](https://docs.docker.com/get-started/) | 2 hrs |
| Deploying FastAPI on Render | [Render docs — FastAPI quickstart](https://render.com/docs/deploy-fastapi) | 30 min |

---

## Track B — Long-term foundations (post June 30)

Plan this as a **3–6 month** journey alongside your job hunt. Don't try to consume it all at once.

### Month 1 — Math + ML core

| Course | Why | Time |
|---|---|---|
| **[Andrew Ng — Machine Learning Specialization (Coursera, audit free)](https://www.coursera.org/specializations/machine-learning-introduction)** | The gold standard. Modernised 2022 version. Linear regression → neural networks. | ~60 hrs |
| **[3Blue1Brown — Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)** | Visual math intuition. Watch all 16 videos. | ~3 hrs |
| **[3Blue1Brown — Neural Networks playlist](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)** | Best explanation of NN + backprop in existence | ~2 hrs |
| **[StatQuest — Statistics Fundamentals playlist](https://www.youtube.com/playlist?list=PLblh5JKOoLUK0FLuzwntyYI10UQFUhsY9)** | Stats intuition — bias/variance, p-values, distributions | ~5 hrs |

### Month 2 — Deep Learning

| Course | Why | Time |
|---|---|---|
| **[fast.ai — Practical Deep Learning for Coders (Part 1)](https://course.fast.ai/)** | Top-down, code-first. You'll train models in lesson 1. | ~40 hrs |
| **[Andrej Karpathy — Neural Networks: Zero to Hero](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ)** | Build GPT from scratch. THE modern DL course. Free YouTube. | ~25 hrs |

### Month 3 — Specialise: NLP (since your project is NLP-heavy)

| Course | Why | Time |
|---|---|---|
| **[Hugging Face NLP Course (full)](https://huggingface.co/learn/nlp-course)** | Modern, free, hands-on. Transformers + fine-tuning + datasets + tokenizers | ~30 hrs |
| **[Stanford CS224N (YouTube — 2023)](https://www.youtube.com/playlist?list=PLoROMvodv4rMFqRtEuo6SGjY4XbRIVRd4)** | Deep theoretical foundation. Watch 1.5x speed. | ~30 hrs |

### Month 4 — MLOps (huge differentiator for fresher resumes)

| Course | Why | Time |
|---|---|---|
| **[Made With ML — Goku Mohandas](https://madewithml.com/)** | THE free MLOps course. Project-based. Industry standard. | ~40 hrs |
| **[MLflow docs + tutorials](https://mlflow.org/docs/latest/getting-started/index.html)** | Hands-on with the tool you'll mention in interviews | ~3 hrs |
| **[DVC tutorial](https://dvc.org/doc/start)** | Data versioning — sounds fancy, learn it in an evening | ~2 hrs |

### Month 5–6 — Pick a vertical based on jobs you target

- **Data Engineering bent:** [Data Engineering Zoomcamp (DataTalks.Club, free)](https://github.com/DataTalksClub/data-engineering-zoomcamp) — 9 weeks, Spark, Airflow, dbt. Zero cost. Hugely respected.
- **ML Engineering bent:** [Full Stack Deep Learning](https://fullstackdeeplearning.com/) — free archive of all lectures.
- **Computer Vision bent:** [Stanford CS231n YouTube](https://www.youtube.com/playlist?list=PL3FW7Lu3i5JvHM8ljYj-zLfQRF3EO8sYv).

---

## Track C — Interview prep (parallel to B, start Month 1)

### Books (free online)

| Book | Why |
|---|---|
| **[Machine Learning Interviews — Chip Huyen (free)](https://huyenchip.com/ml-interviews-book/)** | THE book for ML interviews. Free online. Read once during Month 1, again before interviews. |
| **[Mathematics for Machine Learning — Deisenroth, Faisal, Ong (free PDF)](https://mml-book.github.io/)** | Reference book. Don't read cover-to-cover; look up topics as needed. |

### Question banks (do daily, 1–2 questions/day)

| Resource | Type |
|---|---|
| **[StrataScratch — Free SQL & Python questions](https://www.stratascratch.com/)** | Real DS interview questions from FAANG, Spotify, Airbnb |
| **[LeetCode — SQL 50 + Easy Python](https://leetcode.com/studyplan/top-sql-50/)** | Free tier is enough for fresher prep |
| **[Glassdoor — Search "[Company] data scientist interview"](https://www.glassdoor.com/)** | Specific past questions for companies you'll apply to |
| **[Interviewing.io — Free recorded mock interviews](https://interviewing.io/recordings)** | Watch real interviews to learn pacing & communication |

### Concepts you MUST be able to explain in 60 seconds (rapid-fire)

Make flashcards (Anki, free) for each:

- Bias-variance tradeoff
- Overfitting & underfitting (and 3 ways to fix each)
- Cross-validation (and why k-fold)
- Regularization — L1 vs L2, when to use which
- Logistic regression — loss function, why sigmoid
- Decision trees, random forests, gradient boosting (intuition)
- KNN — pros/cons, why curse of dimensionality
- K-means — algorithm, how to pick k, limitations
- Precision, recall, F1, ROC-AUC, when to use each
- Class imbalance — 4 ways to handle
- p-value, confidence interval (in plain English)
- Type I vs Type II errors
- A/B testing — sample size, p-value, power
- Gradient descent — batch vs stochastic vs mini-batch
- Backpropagation (one-line intuition)
- CNN, RNN, Transformer — when to use each
- Attention mechanism (one-paragraph explanation)
- Word2Vec vs BERT (one-paragraph each)
- Embeddings — why they work
- Train/val/test — why three sets, not two

### Behavioural / story bank

Prepare STAR-format stories (Situation, Task, Action, Result) for:

1. A bug you debugged that taught you something
2. A project you're proud of (use **JobLens** for this!)
3. A time you learned something fast under pressure
4. A time you disagreed with someone technical
5. A time you failed (real failure — interviewers can smell fake humility)

JobLens is your story #1 and #2. Practice telling it in **2 minutes** end-to-end.

---

## Communities (free)

| Community | What |
|---|---|
| [r/MachineLearning](https://reddit.com/r/MachineLearning) | Latest research, sometimes too academic |
| [r/datascience](https://reddit.com/r/datascience) | Career questions, pragmatic |
| [DataTalks.Club Slack](https://datatalks.club/) | Free Zoomcamps + active Slack — best DS community for freshers |
| [Hugging Face Discord](https://discord.gg/huggingface) | Help on transformers / models |
| [Kaggle](https://kaggle.com) | Free notebooks, free GPU, competitions, learn micro-courses |

---

## Cheat-sheets (free, save these)

- [scikit-learn algorithm cheat-sheet](https://scikit-learn.org/stable/machine_learning_map.html) — flowchart of which algo for which problem
- [Stanford CS229 cheatsheets (Shervine Amidi)](https://stanford.edu/~shervine/teaching/cs-229/) — best ML cheatsheets ever made
- [Distill.pub](https://distill.pub/) — visual ML papers; bookmark forever

---

## Anti-patterns to avoid

1. **Tutorial hell.** Pick *one* course, finish it, move on. Don't half-do five courses.
2. **Watching without coding.** Type out every example. If you only watch, you learn nothing.
3. **Skipping the math.** You don't need to derive backprop, but you should be able to explain *what gradient descent is doing geometrically*.
4. **Building model.fit() projects.** Every fresher has a Titanic notebook. JobLens already puts you ahead — keep it that way.
5. **Reading papers too early.** First make scikit-learn boring. Then HF Transformers boring. *Then* read papers.
6. **Comparing yourself to twitter.** Twitter ML is performance art. Stick to your roadmap.

---

## Suggested weekly cadence (post-internship)

| Day | What |
|---|---|
| Mon–Fri | 1 hr Track B (Andrew Ng / fast.ai) + 30 min Track C (1 question) |
| Sat | 3–4 hr deep work — extend JobLens with one new ML feature |
| Sun | 2 hr review + write a LinkedIn post about what you learned that week |

The LinkedIn weekly post is a non-negotiable resume hack. After 12 weeks of consistent posts, recruiters will start finding you.
