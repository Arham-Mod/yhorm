def build_context(chunks, max_chunks=5):

    if not chunks:
        return "No relevant code found."

    selected_chunks = chunks[:max_chunks]

    context_blocks = []

    for chunk in selected_chunks:

        block = f"""
File: {chunk.file_path}
Function/Class: {chunk.name}
Lines: {chunk.start_line}-{chunk.end_line}

code:
{chunk.source_code}
"""

        context_blocks.append(block.strip())

    context = "\n\n----------------------------------------\n\n".join(context_blocks)

    return context