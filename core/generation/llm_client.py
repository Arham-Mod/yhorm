import os
from groq import Groq
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(prompt: str) -> str:
    """
    sends a prompt to the LLM and returns the generated answer.
    """
    logger.info("Sending prompt to Groq Llm...")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=500
    )

    answer = response.choices[0].message.content
    return answer