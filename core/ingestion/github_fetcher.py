import os
import requests
import logging
from pathlib import Path

from utils.logging.logger import setup_logging

logger = logging.getLogger(__name__)

GITHUB_API_BASE = "https://api.github.com/repos"


def extract_repo_info(repo_url: str):
    """
    Extract owner and repo name from GitHub URL.
    """
    parts = repo_url.rstrip("/").split("/")
    owner = parts[-2]
    repo = parts[-1]
    return owner, repo


def fetch_repository(repo_url: str, save_dir: str, token: str):
    """
    Fetch repository contents using GitHub API and save locally.
    """
    owner, repo = extract_repo_info(repo_url)

    target_path = Path(save_dir) / repo
    target_path.mkdir(parents=True, exist_ok=True)

    logger.info(f"Fetching repository: {owner}/{repo}")

    _fetch_directory(owner, repo, "", target_path, token)

    logger.info(f"Repository saved to {target_path}")

    return str(target_path)


def _fetch_directory(owner: str, repo: str, path: str, local_dir: Path, token: str):
    """
    Recursively fetch directory contents from GitHub API.
    """
    url = f"{GITHUB_API_BASE}/{owner}/{repo}/contents/{path}"

    headers = {"Authorization": f"token {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.json()}")

    items = response.json()

    for item in items:
        if item["type"] == "dir":
            sub_dir = local_dir / item["name"]
            sub_dir.mkdir(exist_ok=True)
            _fetch_directory(owner, repo, item["path"], sub_dir, token)

        elif item["type"] == "file":
            if item["name"].endswith(".py"):
                file_response = requests.get(item["download_url"], headers=headers)

                file_path = local_dir / item["name"]

                with open(file_path, "wb") as f:
                    f.write(file_response.content)

                logger.info(f"Saved: {file_path}")

"""
usage:

local_repo_path = fetch_repository(
    repo_url=args.repo_url,
    save_dir="data/raw",
    token = github_token
)

use a parser to extract repo code and feed it to fetch_repo function to save the repo locally.
"""