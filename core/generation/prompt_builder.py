def build_prompt(query: str, context: str) -> str:
    """
    Building final prompt for the LLm using the query and retrieved context.
    """

    system_instruction ="""
You are a repository analysis assistant.

Your task is to answer questions about a code repository.

Rules:
1. Use ONLY the provided repository context.
2. If the answer is not present in the context, say:
   "Insufficient information found in the repository."
3. Cite the file and function names when explaining code.
4. Be concise and technical.
"""

    prompt = f"""
{system_instruction}

Question: 
{query}

Repository Context:
{context}

Answer:
"""
    
    return prompt.strip()