from ml_dedup.pipeline.db import fetch_sorted_titles

def run():
    df = fetch_sorted_titles()
    df.to_csv("data/raw/products.csv", index=False)