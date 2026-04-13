from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_built_resume(resume_text, goal):
    prompt = f"""
    You are a professional resume consultant and ATS expert.

    The user has built the following resume and wants to target the role of: {goal}

    Resume:
    {resume_text}

    Analyze the resume and provide:

    1. **Overall Quality Score** (out of 100) — based on ATS compatibility, formatting, and content
    2. **Missing Keywords** — List specific keywords/phrases that are important for a {goal} role but missing from this resume
    3. **Section-by-Section Feedback**:
       - Professional Summary: Is it strong? Suggestions?
       - Experience: Are bullet points impact-driven? Using action verbs and metrics?
       - Skills: Any critical skills missing for this role?
       - Projects: Are they relevant? Do they demonstrate required skills?
       - Education: Any relevant coursework or honors to add?
    4. **ATS Compatibility Issues** — formatting problems, missing sections, keyword density
    5. **Top 5 Immediate Improvements** — ranked by impact

    Format your response with clear headings and bullet points.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
