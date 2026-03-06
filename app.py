import time
import logging

from utils.logging.logger import setup_logging

from core.ingestion.repo_loader import load_repository
from core.parsing.ast_parser import ASTParser
from core.indexing.embedder import Embedder
from core.indexing.faiss_store import FaissVectorStore
from core.indexing.metadata_store import MetadataStore
from core.retrieval.retriever import expand_dependencies
from core.context_builder.build_context import build_context, log_clean_context
from core.generation.prompt_builder import build_prompt
from core.generation.llm_client import generate_answer



def main():

    # Setup Logging
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting Repository System Test")

    # Load Repository
    repo_path = "data/raw/"
    files = load_repository(repo_path)

    logger.info(f"Loaded {len(files)} Python files")

    # Parse Code into Chunks
    parser = ASTParser()
    code_chunks = []

    for file_path in files:
        chunks = parser.parse_file(file_path)
        code_chunks.extend(chunks)

    logger.info(f"Extracted {len(code_chunks)} code chunks")

    if len(code_chunks) == 0:
        logger.error("No chunks extracted. Exiting.")
        return

    # Embedding + Indexing
    logger.info("Generating embeddings...")

    embedder = Embedder()

    texts = [
        f"{chunk.name}\n{chunk.source_code}"
        for chunk in code_chunks
    ]

    start_time = time.time()

    vectors = embedder.embed_batch(texts)

    logger.info(f"Generated {len(vectors)} embeddings")

    # Initialize Stores
    metadata_store = MetadataStore()
    vector_store = FaissVectorStore(metadata_store)

    # Add vectors to FAISS
    vector_store.add_vectors(vectors)

    # Register metadata
    for idx, chunk in enumerate(code_chunks):
        metadata_store.add(idx, chunk)

    logger.info("Indexing complete")

    # Test Query
    test_query = "WHICH LLM MODEL IS USED IN THE CODEBASE? is it any good?"

    logger.info(f"Running test query: {test_query}")

    query_vector = embedder.embed_text(test_query)

    # FAISS Search
    scores, indices = vector_store.search(query_vector, top_k=5)

    # Convert FAISS ids → CodeChunk objects
    initial_chunks = [
        metadata_store.get_chunk(i)
        for i in indices
    ]

    # Dependency expansion
    expanded_chunks = expand_dependencies(
        initial_chunks,
        metadata_store
    )
    logger.info(f"Chunks after dependency expansion: {len(expanded_chunks)}")

    # Build safe context (prevents token overflow)
    logger.info(f"Chunks received by context builder: {len(expanded_chunks)}")

    context = build_context(expanded_chunks)


    # Show retrieved chunks
    logger.info("Top results (after dependency expansion):")

    for rank, chunk in enumerate(expanded_chunks, start=1):

        logger.info(
            f"\nRank {rank}\n"
            f"Function: {chunk.name}\n"
            f"File: {chunk.file_path}\n"
            f"Lines: {chunk.start_line}-{chunk.end_line}\n"
        )

    end_time = time.time()

    logger.info("\n===== FINAL CONTEXT SENT TO LLM =====\n")
    print(context)
    logger.info(f"Total execution time: {end_time - start_time:.2f}s")

    logger.info("Test completed successfully.")

    log_clean_context(context)

    # Prompt Building
    prompt = build_prompt(test_query, context)
    logger.info("\nFinal Prompt Sent to LLM\n")

    answer = generate_answer(prompt)

    print(answer)
    logger.info("Answer generation complete.")


if __name__ == "__main__":
    main()