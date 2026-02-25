import os

from sklearn import tree
from core.parsing.ast_parser import ASTParser  # adjust import path
from core.parsing.chunk_model import CodeChunk
import ast

def collect_python_files(repo_root):
    python_files = []
    for root, _, files in os.walk(repo_root):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files


def main():
    repo_root = "./tests"  # or path to your test repo
    print(f"Scanning repository: {repo_root}")

    files = collect_python_files(repo_root)
    print(f"Total Python files found: {len(files)}")

    parser = ASTParser()

    chunks = parser.parse_repository(files)

    print("\n===== PARSER RESULTS =====")
    print(f"Total Chunks Extracted: {len(chunks)}")

    # Print first 5 chunks for inspection
    for i, chunk in enumerate(chunks[:5]):
        print("\n------------------------")
        print(f"Chunk #{i+1}")
        print(f"ID: {chunk.id}")
        print(f"File: {chunk.file_path}")
        print(f"Name: {chunk.name}")
        print(f"Type: {chunk.type}")
        print(f"Lines: {chunk.start_line} - {chunk.end_line}")
        print(f"Calls: {chunk.calls}")
        print("\nSource Preview:")
        print(chunk.source_code[:300])  # first 300 chars


    # Optional: Build registry test
    registry = {chunk.name: chunk for chunk in chunks}
    print("\n===== REGISTRY TEST =====")
    print(f"Total registry entries: {len(registry)}")

    # Optional: Check internal resolution
    print("\n===== INTERNAL CALL CHECK =====")
    for chunk in chunks[:5]:
        resolved = [call for call in chunk.calls if call in registry]
        print(f"{chunk.name} → {resolved}")



if __name__ == "__main__":
    main()