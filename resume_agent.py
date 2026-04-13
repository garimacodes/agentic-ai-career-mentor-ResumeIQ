from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_resume(resume_text, goal):
    prompt = f"""
    Analyze this resume for a {goal} role.

    Resume:
    {resume_text}

    Give:
    - ATS score (out of 100)
    - Missing keywords
    - Formatting issues
    - Suggestions
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # 🔥 safer model
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content