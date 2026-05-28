from groq import Groq
import os

from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(query, documents):

    context = "\n".join(documents)

    prompt = f"""
You are a document-based AI assistant.

Answer ONLY using the provided context.

If the answer is not present in the context,
say:
"Answer not found in provided documents."

Context:
{context}

Question:
{query}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Error: {str(e)}"