import pandas as pd 
from ml_dedup.pipeline.tokenizer import preprocess

def run():
    df = pd.read_csv("data/raw/products.csv")
    df['cleaned'] = df['name'].map(preprocess)
    df.to_csv("data/processed/cleaned_products_for_labeling.csv", index=False)