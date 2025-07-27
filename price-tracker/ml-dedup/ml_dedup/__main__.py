import argparse
from ml_dedup.scripts.extract_titles import run as extract_titles
from ml_dedup.scripts.preprocess_titles import run as preprocess
from ml_dedup.scripts.label_pairs import run as start_labeling


def main():
    parser = argparse.ArgumentParser(description="ML Deduplication Pipeline CLI")
    
    parser.add_argument('--extract', action='store_true', help="Extract and process product names from database")
    parser.add_argument('--labeling', action='store_true', help="Start a labeling session")

    args = parser.parse_args()

    if args.extract:
        print("[✓] Extracting product titles...")
        extract_titles()
        print("[✓] Preprocessing titles...")
        preprocess()

    if args.labeling:
        print("[✓] Starting labeling session...")
        start_labeling()

if __name__ == "__main__":
    main()