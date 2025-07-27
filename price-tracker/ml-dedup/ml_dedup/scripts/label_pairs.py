import pandas as pd
import os
import json
from itertools import combinations
from tqdm import tqdm
from rapidfuzz import process, fuzz

SIMILARITY_THRESHOLD = 80
PROGRESS_PATH = "data/labeled/progress.json"
OUTPUT_PATH = "data/labeled/labeled_pairs.jsonl"

def find_similar(title, titles, limit=10):
    return process.extract(title, titles, scorer=fuzz.token_sort_ratio, limit=limit)

def save_labeled(pairs, path):
    with open(path, "a", encoding="utf-8") as f:
        for pair in pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")

def load_progress():
    if not os.path.exists(PROGRESS_PATH):
        return 0
    with open(PROGRESS_PATH, "r") as f:
        return json.load(f).get("last_index", 0)

def save_progress(index):
    with open(PROGRESS_PATH, "w") as f:
        json.dump({"last_index": index}, f)

def labeling_session(df, output_path, start_index):
    already_seen = set()
    titles = df['cleaned'].dropna().unique().tolist()
    ids = df['id'].tolist()
    labeled = []

    total = len(titles)
    for i in tqdm(range(start_index, total), total=total - start_index, desc="Labeling"):
        save_progress(i)
        
        base_id = ids[i]
        base_title = titles[i]

        similar = find_similar(base_title, titles)
        filtered = [
            (idx, score) for (match, score, idx) in similar 
            if score >= SIMILARITY_THRESHOLD and idx != i
        ]

        if not filtered:
            continue

        for idx, score in filtered:
            pair = tuple(sorted([base_id, ids[idx]]))
            if pair in already_seen:
                continue
            already_seen.add(pair)

            print("\n🔗 Possible Duplicate:")
            print(f"1. {base_title}")
            print(f"2. {titles[idx]}")
            print(f"Similarity Score: {score}")
            label = input("Are these duplicates? (1 = yes, 2 = no, s = skip, q = quit): ")
            if label == 'q':
                save_labeled(labeled, output_path)
                save_progress(i)
                return
            elif label == 's':
                continue
            elif label in ('1', '2'):
                labeled.append({
                    "product1": base_title,
                    "product2": titles[idx],
                    "label": 1 if label == '1' else 0
                })
        

    save_labeled(labeled, output_path)
    save_progress(total)


def run():
    df = pd.read_csv("data/processed/cleaned_products_for_labeling.csv")
    start_index = load_progress()
    labeling_session(df, OUTPUT_PATH, start_index)
            
if __name__ == "__main__":
    run()

    