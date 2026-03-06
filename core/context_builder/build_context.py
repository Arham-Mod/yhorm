import logging

from utils.logging.logger import setup_logging
def build_context(chunks, max_chunks=5):

    if not chunks:
        return "No relevant code found."

    selected_chunks = chunks[:max_chunks]

    context_blocks = []

    for rank, chunk in enumerate(selected_chunks, start=1):

        block = f"""
Rank: {rank}
File: {chunk.file_path}
Function/Class: {chunk.name}
Lines: {chunk.start_line}-{chunk.end_line}

code:
{chunk.source_code}

"""

        context_blocks.append(block.strip())

    context = "\n\n----------------------------------------\n\n".join(context_blocks)

    return context

def log_clean_context(context: str):
    """
    Logs only Rank, File, Function/Class and Lines from the context.
    Removes the source code for clean logging.
    """
    logger = logging.getLogger(__name__)

    filtered_lines = []

    for line in context.split("\n"):

        line = line.strip()

        if (
            line.startswith("Rank:")
            or line.startswith("File:")
            or line.startswith("Function/Class:")
            or line.startswith("Lines:")
        ):
            filtered_lines.append(line)

        elif line.startswith("----------------------------------------"):
            filtered_lines.append(line)

    clean_log = "\n".join(filtered_lines)

    logger.info("\n===== RETRIEVED CONTEXT (CLEAN LOG) =====\n")
    logger.info(clean_log)