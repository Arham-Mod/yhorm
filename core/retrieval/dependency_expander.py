def expand_dependencies(initial_chunks, metadata_store):
    """
    Expand retrieved chunks by including functions they call.
    Only expands 1 level.
    """

    expanded = {}

    # add initial chunks
    for chunk in initial_chunks:
        expanded[chunk.chunk_id] = chunk

    # expand dependencies
    for chunk in initial_chunks:

        for called_name in chunk.called_functions:

            dependent_chunks = metadata_store.get_chunks_by_name(called_name)

            for dep_chunk in dependent_chunks:
                expanded[dep_chunk.chunk_id] = dep_chunk

    return list(expanded.values())