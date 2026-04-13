from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_profile(name, degree, skills, goal):
    prompt = f"""
    Create a structured student profile.

    Name: {name}
    Degree: {degree}
    Skills: {skills}
    Career Goal: {goal}

    Give a clean summary.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content