import os
import argparse
from dotenv import load_dotenv

from utils.logging.logger import setup_logging
from core.ingestion.github_fetcher import fetch_repository
from core.ingestion.repo_loader import load_repository

def main():
    load_dotenv()
    setup_logging()
    github_token = os.getenv("GITHUB_TOKEN")
    


    parser = argparse.ArgumentParser()
    parser.add_argument("--repo_url", type=str, required=True)

    args = parser.parse_args()


    if not github_token:
        raise ValueError("GITHUB_TOKEN not found in environment variables.")

    # Step 1: Fetch repository
    local_repo_path = fetch_repository(
        repo_url=args.repo_url,
        save_dir="data/raw",
        token=github_token
    )

    # Step 2: Load repository files
    files = load_repository(local_repo_path)

    print("\nFiles ready for parsing:")
    for f in files:
        print(f)



if __name__ == "__main__":
    main()
