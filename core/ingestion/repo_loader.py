import logging
import os
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

# Directories to ignore during traversal
EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "env",
    "node_modules",
    "dist",
    "build"
}

# File extensions we want to index
ALLOWED_EXTENSIONS = {".py"}

def load_repository(repo_path:str) -> List[str]:
    """
    recursively scans a repository directory and returns a list of valid file paths.
    """

    repo_path = Path(repo_path)

    if not repo_path.exists():
        raise ValueError(f"Provided path '{repo_path}' does not exist")
    
    if not repo_path.is_dir():
        raise ValueError(f"Provided path '{repo_path}' is not a valid directory.")
    
    logger.info(f"Scanning repository at: {repo_path}")

    valid_files = []

    for root, dirs, files in os.walk(repo_path):
        # Remove excluded directories from traversal
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for file in files:
            file_path = Path(root) / file

            if file_path.suffix in ALLOWED_EXTENSIONS:
                valid_files.append(str(file_path.resolve()))
    
    logger.info(f"Found {len(valid_files)} valid files in the repository.")

    return valid_files