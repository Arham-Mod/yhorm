import os
import time
from utils.logging.logger import setup_logging
import logging

from core.ingestion.repo_loader import load_repository
from core.parsing.ast_parser import ASTParser
from core.indexing.embedder import Embedder
from core.indexing.faiss_store import FaissVectorStore
from core.indexing.metadata_store import MetadataStore


def main():

    # -----------------------------
    # Setup Logging
    # -----------------------------
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting Repository Intelligence System Test")

    # -----------------------------
    # Load Repository
    # -----------------------------
    repo_path = "data/raw/"   # Change this path
    # `load_repository` returns a list of file paths, not a loader object.
    # Use the returned list directly.
    files = load_repository(repo_path)

    logger.info(f"Loaded {len(files)} Python files")

    # -----------------------------
    # Parse Code into Chunks
    # -----------------------------
    parser = ASTParser()
    code_chunks = []

    for file_path in files:
        chunks = parser.parse_file(file_path)
        code_chunks.extend(chunks)

    logger.info(f"Extracted {len(code_chunks)} code chunks")

    if len(code_chunks) == 0:
        logger.error("No chunks extracted. Exiting.")
        return

    # -----------------------------
    # Embedding + Indexing
    # -----------------------------
    logger.info("Generating embeddings...")

    embedder = Embedder()

    texts = [
        f"{chunk.name}\n{chunk.source_code}"
        for chunk in code_chunks
    ]

    start_time = time.time()
    vectors = embedder.embed_batch(texts)
    logger.info(f"Generated {len(vectors)} embeddings")

    dimension = vectors[0].shape[0]
    vector_store = FaissVectorStore(dimension)
    metadata_store = MetadataStore()

    vector_store.add_vectors(vectors)

    for idx, chunk in enumerate(code_chunks):
        metadata_store.add(idx, {
            "name": chunk.name,
            "file_path": chunk.file_path,
            "start_line": chunk.start_line,
            "end_line": chunk.end_line,
            "source_code": chunk.source_code,
            "called_functions": chunk.calls
        })

    logger.info("Indexing complete")

    # -----------------------------
    # Test Query
    # -----------------------------
    test_query = "In what files is the multiply logic present"

    logger.info(f"Running test query: {test_query}")

    query_vector = embedder.embed_text(test_query)
    scores, indices = vector_store.search(query_vector, top_k=5)

    logger.info("Top results:")

    for rank, (idx, score) in enumerate(zip(indices, scores), start=1):
        metadata = metadata_store.get(idx)

        logger.info(
            f"\nRank {rank}\n"
            f"Score: {score:.4f}\n"
            f"Function: {metadata['name']}\n"
            f"File: {metadata['file_path']}\n"
            f"Lines: {metadata['start_line']} - {metadata['end_line']}\n"
        )

    end_time = time.time()
    logger.info(f"Total execution time: {end_time - start_time:.2f}s")

    logger.info("Test completed successfully.")


if __name__ == "__main__":
    main()




#TODO
"""
find out the working of sentence transformer and how to run it for this project as it is showing error
"""