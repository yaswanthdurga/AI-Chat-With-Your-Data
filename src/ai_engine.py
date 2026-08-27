import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")


client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    timeout=60.0,
    max_retries=2
)


MODEL = "gemini-3.7-flash"


def generate_sql(question, schema):

    prompt = f"""
You are an expert SQL analyst.

Convert the user's question into a DuckDB SQL query.

Database table:
sales

Columns:
{schema}

Rules:
- Return ONLY SQL.
- Do not use markdown.
- Do not explain the query.
- Use DuckDB-compatible SQL.
- Never modify data.
- Only use SELECT queries.
- Do not invent columns.
- Use only the columns provided above.

User question:
{question}
"""

    response = client.chat.completions.create(
        model=MODEL,
        reasoning_effort="low",
        messages=[
            {
                "role": "system",
                "content": "You generate safe DuckDB SQL queries."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()