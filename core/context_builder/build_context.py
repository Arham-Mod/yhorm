from typing import List

def build_context(cohunks: List, max_chunks: int=5) -> str:
    """
    Converts retrieved chunks into a structed prompt context
    """
    # Removing du[lictae chunks based on chunk id
    unique_chunks = {}

    for chunk in cohunks:
        unique_chunks[chunk.chunk_id] = chunk
    
    chunks = list(unique_chunks.values)

    # Limiting number of chunks 

    chunks = chunks[:max_chunks]

    context_blocks = []

    for chunk in chunks:

        block = f"""
File: {chunk.file_path}
Function/Class: {chunk.name}
Lines: {chunk.start_line}-{chunk.end_line}

code:
{chunk.source_code}
        """

        context_blocks.append(block)

        # Join blocks
        context = "\n\n----------------------------------------\n\n".join(context_blocks)

        return context
