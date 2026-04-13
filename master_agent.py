from agents.profile_agent import generate_profile
from agents.resume_agent import analyze_resume
from agents.skill_gap_agent import find_skill_gaps
from agents.recommendation_agent import get_recommendations
from agents.roadmap_agent import generate_roadmap
from agents.improvement_agent import improve_resume


def generate_full_analysis(name, degree, skills, goal, resume_text):
    """
    Calls each individual agent and returns a dict with separate results.
    """
    results = {}

    results["profile"] = generate_profile(name, degree, skills, goal)
    results["resume_analysis"] = analyze_resume(resume_text, goal)
    results["skill_gaps"] = find_skill_gaps(skills, goal)
    results["recommendations"] = get_recommendations(goal)
    results["roadmap"] = generate_roadmap(goal)
    results["improvements"] = improve_resume(resume_text)

    return results