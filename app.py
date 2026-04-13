from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from agents.master_agent import generate_full_analysis
from agents.interview_agent import generate_interview_questions, evaluate_answer, generate_interview_summary
from utils.pdf_parser import extract_text_from_pdf
from dotenv import load_dotenv
import markdown
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)


def md_to_html(text):
    """Convert markdown text to HTML."""
    if not text:
        return ""
    return markdown.markdown(text, extensions=["tables", "fenced_code"])


@app.route("/")
def home():
    return render_template("home.html", active_page="home")


@app.route("/builder")
def builder():
    return render_template("builder.html", active_page="builder")


@app.route("/use-built-resume", methods=["POST"])
def use_built_resume():
    """Receives resume text from the builder and redirects to analyze page."""
    resume_text = request.form.get("resume_text", "")
    session["built_resume"] = resume_text
    return redirect(url_for("analyze"))


@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "POST":
        name = request.form["name"]
        degree = request.form["degree"]
        skills = request.form["skills"]
        goal = request.form["goal"]

        # Check for uploaded PDF first, then fall back to built resume text
        resume_text = ""
        file = request.files.get("resume")
        if file and file.filename:
            resume_text = extract_text_from_pdf(file)
        elif request.form.get("resume_text"):
            resume_text = request.form["resume_text"]

        if not resume_text:
            return render_template(
                "analyze.html",
                active_page="analyze",
                error="Please upload a resume or build one first.",
            )

        # Run all agents
        raw_results = generate_full_analysis(name, degree, skills, goal, resume_text)

        # Convert markdown to HTML for each result
        results = {key: md_to_html(val) for key, val in raw_results.items()}

        # Clear the built resume from session after use
        session.pop("built_resume", None)

        return render_template("results.html", active_page="analyze", results=results)

    # GET — show the form
    built_resume = session.get("built_resume", "")
    return render_template(
        "analyze.html", active_page="analyze", built_resume=built_resume
    )


# ── Mock Interview Routes ──

@app.route("/interview")
def interview():
    return render_template("interview.html", active_page="interview")


@app.route("/api/interview/start", methods=["POST"])
def interview_start():
    """Generate interview questions for the given role."""
    data = request.get_json()
    role = data.get("role", "")
    difficulty = data.get("difficulty", "medium")
    num_questions = data.get("num_questions", 5)

    if not role:
        return jsonify({"error": "Please specify a role."}), 400

    try:
        questions = generate_interview_questions(role, difficulty, num_questions)
        return jsonify({"questions": questions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/interview/answer", methods=["POST"])
def interview_answer():
    """Evaluate a single interview answer."""
    data = request.get_json()
    question = data.get("question", "")
    answer = data.get("answer", "")
    role = data.get("role", "")

    try:
        feedback = evaluate_answer(question, answer, role)
        return jsonify({"feedback": feedback})
    except Exception as e:
        return jsonify({"feedback": f"Error: {str(e)}"}), 500


@app.route("/api/interview/summary", methods=["POST"])
def interview_summary():
    """Generate overall interview performance summary."""
    data = request.get_json()
    role = data.get("role", "")
    qa_pairs = data.get("qa_pairs", [])

    try:
        summary = generate_interview_summary(role, qa_pairs)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"summary": f"Error generating summary: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)