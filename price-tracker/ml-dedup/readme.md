# Guide: Implementing a Robust Cross-Encoder Pipeline for Product Deduplication

## Overview and Context

You maintain a large database of product titles scraped from various websites. Many products are semantically identical but have wildly different titles; other titles look similar but refer to distinct items (e.g., **RTX 5070** vs **RTX 5080**, **Corsair Vengeance 16 GB (1×16)** vs **2×8**). Traditional heuristic methods (brand lookups, spec comparisons, fuzzy rules, regex hacks) invariably encounter a **precision–recall battle**:

- Loosen rules → false merges skyrocket (RTX 5070 + 5080 are merged).
- Tighten rules → legitimate duplicates fail to cluster (Rapoo X130Pro variants remain separate).

This document presents a **learned**, **data-driven** approach using a fine-tuned cross-encoder that:

1. **Learns domain-specific distinctions** from labeled examples.
2. **Automatically down-weights noise** (colors, filler words, parentheses) without explicit lists.
3. **Scales** efficiently via a bi-encoder + FAISS blocking layer.
4. **Maintains** accuracy through continuous evaluation, augmentation, and retraining.
5. **Provides explainability** via attention visualization for debugging.

The guide is comprehensive enough for a junior engineer to implement, deploy, and iterate on the system.

---
## Table of Contents
- [Guide: Implementing a Robust Cross-Encoder Pipeline for Product Deduplication](#guide-implementing-a-robust-cross-encoder-pipeline-for-product-deduplication)
  - [Overview and Context](#overview-and-context)
  - [Table of Contents](#table-of-contents)
  - [System Requirements \& Dependencies](#system-requirements--dependencies)
  - [Constraints \& Requirements](#constraints--requirements)
  - [High-Level Solution Architecture](#high-level-solution-architecture)
  - [Detailed Implementation Steps](#detailed-implementation-steps)
    - [Data Preparation \& Labeling](#data-preparation--labeling)
    - [Synthetic Data Augmentation](#synthetic-data-augmentation)
    - [Fine-Tuning the Cross-Encoder](#fine-tuning-the-cross-encoder)
    - [Blocking with Bi-Encoder + FAISS](#blocking-with-bi-encoder--faiss)
    - [Clustering via Cross-Encoder \& Graph Components](#clustering-via-cross-encoder--graph-components)
    - [Evaluation \& Metrics](#evaluation--metrics)
    - [Iterative Refinement \& Automated Retraining](#iterative-refinement--automated-retraining)
    - [Explainability \& Debugging](#explainability--debugging)
  - [Code Organization \& Deployment](#code-organization--deployment)
  - [Why This Is the Best Solution](#why-this-is-the-best-solution)
  - [Next Steps \& Milestones](#next-steps--milestones)

## System Requirements & Dependencies

- **Python 3.8+**
- **Libraries**:
    - `sentence-transformers` (for bi-encoder and cross-encoder)
    - `faiss` (for approximate nearest neighbor search)
    - `scikit-learn` (for metrics, optionally HDBSCAN)
    - `pandas` (for dataset management)
    - `captum` or similar (for attention/gradient visualization)
- **Infrastructure**:
    - GPU for model fine-tuning (NVIDIA T4 or better recommended)
    - CPU for inference + blocking layer
- **Version control**: Git repository with separate branches for prototype, staging, and production.

---

## Constraints & Requirements

- **No brand/category lists**: Too numerous and dynamic.
- **No spec-based rules**: Technical specs overlap across models.
- **No brittle regex/stopword tables**: Maintenance nightmare as product categories expand.
- **High precision target**: ≥ 95 % to avoid false merges.
- **High recall target**: ≥ 90 % to catch legitimate duplicates.
- **Scalable**: Support millions of titles via approximate search.
- **Maintainable by junior engineers**: Clear scripts and documentation.

---

## High-Level Solution Architecture

```
                    +---------------------+                 +---------------------+
                    |   Scraped Titles    |                 |   Labeled Pairs     |
                    +----------+----------+                 +----------+----------+
                               |                                    |
                [Preprocess ─┬─┘                                    |
                            \/                                      |
                  +---------------------+                           |
                  |   Bi-Encoder Model  |                           |
                  |  (SentenceTransformer) ─┐                      |
                  +---------------------+  |                       |
                            | Embeddings    |                       |
                            v               |                       |
                     +-------------+        |                       |
                     |   FAISS     |        |                       |
                     +-------------+        |                       |
                            | Neighbors     |                       v
                            v               +------------+    +-------------------+
                  +---------------------+                |    |  Cross-Encoder    |
                  | Retrieve top-K per  |                |    | (Fine-tuned on    |
                  | title via FAISS     |                |    |  in-domain pairs) |
                  +---------------------+                |    +--------+----------+
                            |                              |             |
                            v                              |   Score each pair
                +-------------------------+                |             v
                | Cluster via connected   |<---------------+   +----------------+
                | components on edges     |                    |  Thresholding   |
                +-------------------------+                    +----------------+
                            |
                            v
                +-------------------------+
                |  Final deduplicated     |
                |  product clusters       |
                +-------------------------+

```

This diagram shows how the system processes product titles through both a bi-encoder and cross-encoder pipeline to create deduplicated clusters. The bi-encoder with FAISS handles efficient retrieval of similar titles, while the cross-encoder performs precise similarity scoring on candidate pairs.

---

## Detailed Implementation Steps

### Data Preparation & Labeling

1. **Source Titles**: Extract a representative subset (~50 000) of your full catalog.
2. **Pair Sampling**:
    - **Positives**: For each known duplicate group, randomly sample 2–3 title pairs.
    - **Hard Negatives**: For each cluster, select near-miss pairs (e.g. RTX 5070 vs 5080, 1×16 vs 2×8).
3. **Format**: Create a CSV or JSONL with columns `title_1`, `title_2`, and `label` (1.0 or 0.0).
4. **Split**: Use an 80/10/10 split for train/validation/test.
5. **Storage**: Commit the labeled file to `data/labels/` in your repo.

### Synthetic Data Augmentation

- **Purpose**: Teach the model invariance to noise: reordering, filler insertion, and punctuation.
- **Implementation**:
    - Write `scripts/augment.py` that reads positive pairs and for each:
        1. **Shuffle non-core tokens** (using random permutations on stopword lists).
        2. **Inject random filler phrases** from a small pool (`edition speciale`, `bulk memory`, etc.).
        3. **Randomly remove parentheses** or punctuation.
    - Append these synthetic pairs (with `label=1`) to `train.csv`, ensuring balance with negatives.

### Fine-Tuning the Cross-Encoder

File: `models/train_cross_encoder.py`

```python
from sentence_transformers import CrossEncoder
import pandas as pd

def load_samples(path):
    df = pd.read_csv(path)
    return [(r.title_1, r.title_2, float(r.label)) for _, r in df.iterrows()]

if __name__ == '__main__':
    train_samples = load_samples('data/labels/train.csv')
    model = CrossEncoder(
        'cross-encoder/ms-marco-MiniLM-L-6-v2',
        num_labels=1,
        device='cuda'
    )
    model.fit(
        train_dataloader=train_samples,
        loss_fct='mse',
        epochs=2,
        warmup_steps=int(len(train_samples) * 0.1),
        output_path='models/product-cross-encoder'
    )

```

- **Hyperparameters**: 2 epochs, warmup = 10 % of steps, MSE loss for regression to [0–1] similarity.
- **Outputs**: `models/product-cross-encoder/` containing model weights and config.

### Blocking with Bi-Encoder + FAISS

File: `scripts/build_faiss_index.py`

```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Load data\ ntitles = open('data/all_titles.txt').read().splitlines()

# Encode\ nmodel = SentenceTransformer('all-MiniLM-L6-v2')
embs = model.encode(ntitles, convert_to_numpy=True, batch_size=64)
faiss.normalize_L2(embs)

# Build index\ ndim = embs.shape[1]
index = faiss.IndexFlatIP(ndim)
index.add(embs)

# Persist\ nfaiss.write_index(index, 'models/faiss_index.idx')
pickle.dump(ntitles, open('models/all_titles.pkl', 'wb'))

```

- **Index Type**: Flat index for simplicity; can upgrade to IVF or HNSW for very large corpora.
- **Normalization**: L2-normalize embeddings for inner-product cosine sim.

### Clustering via Cross-Encoder & Graph Components

File: `scripts/cluster_products.py`

```python
import faiss
import pickle
from sentence_transformers import CrossEncoder
from sklearn.metrics.pairwise import cosine_similarity
from collections import deque, defaultdict

# Load index and data\ nindex = faiss.read_index('models/faiss_index.idx')
titles = pickle.load(open('models/all_titles.pkl', 'rb'))
embs = ... # reload embeddings or recompute

# Load cross-encoder\ ncross = CrossEncoder('models/product-cross-encoder', device='cuda')

threshold = 0.85
k = 50  # top-K neighbors
used = set()
clusters = []

for i, title in enumerate(titles):
    if i in used: continue
    group = [i]
    used.add(i)
    # 1) Retrieve neighbors via FAISS
    D, I = index.search(embs[i:i+1], k)
    # 2) Rerank and filter using cross-encoder
    for j in I[0]:
        if j == i or j in used: continue
        score = cross.predict([(title, titles[j])])[0]
        if score >= threshold:
            group.append(j)
            used.add(j)
    clusters.append([titles[x] for x in group])

# Save clusters\ nimport json
json.dump(clusters, open('output/clusters.json', 'w'), indent=2)

```

- **Graph clustering**: Here we use sequential assignment; for global merging, build an edge list and extract connected components via NetworkX or Union-Find.

### Evaluation & Metrics

File: `scripts/evaluate.py`

```python
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support, roc_auc_score

def load_pairs(path):
    return pd.read_csv(path)

if __name__ == '__main__':
    test = load_pairs('data/labels/test.csv')
    preds, trues = [], []
    for _, row in test.iterrows():
        score = cross.predict([(row.title_1, row.title_2)])[0]
        preds.append(score >= 0.85)
        trues.append(row.label == 1)
    precision, recall, f1, _ = precision_recall_fscore_support(trues, preds, average='binary')
    auc = roc_auc_score(trues, preds)
    print(f"Precision: {precision:.3f}\nRecall: {recall:.3f}\nF1: {f1:.3f}\nAUC: {auc:.3f}")

```

- **Metrics**: Precision, Recall, F1, AUC.
- **Threshold tuning**: Evaluate multiple cutoffs via a PR curve to select the optimal balance.

### Iterative Refinement & Automated Retraining

1. **Logging**: During production inference, log all pairs with scores in the “gray zone” (e.g., 0.75–0.9).
2. **Error Review**: Weekly, sample 100 logged pairs and label them manually.
3. **Data Update**: Append these new labels to `data/labels/train.csv`.
4. **Retraining**: Schedule a cron job or CI pipeline to retrain the cross-encoder monthly on the expanded dataset.
5. **Versioning**: Tag each model release (`v1.0`, `v1.1`, …) and store metrics in a central dashboard (e.g. MLflow).

### Explainability & Debugging

- **Attention Visualization**: Use Captum’s `LayerIntegratedGradients` or built-in model heads to compute token importance scores.
- **UI**: In your admin dashboard, display the input pair with color‐coded tokens indicating contribution to the similarity decision.
- **Traceability**: For any cluster, allow drilling down to view pairwise scores and model logs (attention maps, gradient attributions).

---

## Code Organization & Deployment

```
project-root/
├── data/
│   ├── all_titles.txt
│   └── labels/
│       ├── train.csv
│       ├── valid.csv
│       └── test.csv
├── models/
│   ├── product-cross-encoder/
│   └── faiss_index.idx
├── scripts/
│   ├── augment.py
│   ├── build_faiss_index.py
│   ├── cluster_products.py
│   └── evaluate.py
├── services/
│   └── api.py        # Flask/FastAPI endpoint for real-time deduplication
└── docs/
    └── CrossEncoder_Product_Deduplication_Guide.md

```

- **CI/CD**: On merge to `main`, run linting, tests (on a small sample), and rebuild FAISS index if needed.
- **Containerization**: Dockerfile with CUDA support for training; separate inference container without GPU.

---

## Why This Is the Best Solution

- **Data-driven**: Learns your actual duplicate definitions, not brittle heuristics.
- **One threshold**: No more endless tuning loops.
- **Scalable**: FAISS + batching handles millions of titles.
- **Maintainable**: Adding new examples automatically improves performance.
- **Explainable**: Attention maps clarify edge-case decisions.

Alternative approaches collapse under real-world noise or require constant rule maintenance.

---

## Next Steps & Milestones

1. **Step 1**: Label ~1 000 pairs, implement augmentation script.
2. **Step 2**: Fine-tune cross-encoder, evaluate on test set, choose threshold.
3. **Step 3**: Build FAISS index, run initial clustering, compare to ground truth.
4. **Step  4**: Deploy inference API, set up logging of gray-zone scores.
5. **Step 5+**: Monthly error review and retraining; integrate explainability in dashboard.