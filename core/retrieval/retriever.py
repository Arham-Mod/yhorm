from core.retrieval.dependency_expander import expand_dependencies

def retrieve(query, embedder, vector_store, metadata_store, top_k=5):

    # 1. Embed query
    query_embedding = embedder.embed_text(query)

    # 2. Semantic retrieval
    top_ids, scores = vector_store.search(query_embedding, top_k)

    initial_chunks = [
        metadata_store.get_chunk(i)
        for i in top_ids
    ]

    # 3. Structural expansion
    expanded_chunks = expand_dependencies(
        initial_chunks,
        metadata_store
    )

    return expanded_chunks