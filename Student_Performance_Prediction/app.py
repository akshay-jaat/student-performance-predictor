from pathlib import Path
import joblib
import pandas as pd
from flask import Flask, render_template, request

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "student_model.joblib"
FEATURES = ["study_hours", "attendance", "previous_marks", "assignment_score", "sleep_hours"]

app = Flask(__name__)

def load_model():
    if not MODEL_PATH.exists():
        from train_model import train
        train()
    return joblib.load(MODEL_PATH)

model = load_model()

def category(score):
    if score >= 85:
        return "Excellent", "excellent"
    if score >= 70:
        return "Good", "good"
    if score >= 50:
        return "Average", "average"
    return "Needs Improvement", "improve"

def advice(data, score):
    tips = []
    if data["study_hours"] < 2:
        tips.append("Try building a consistent study routine of at least 2–3 focused hours daily.")
    if data["attendance"] < 75:
        tips.append("Improve class attendance and revise missed topics.")
    if data["previous_marks"] < 50:
        tips.append("Revise foundational concepts and practise topic-wise questions.")
    if data["assignment_score"] < 60:
        tips.append("Complete assignments on time and use feedback to improve.")
    if data["sleep_hours"] < 6:
        tips.append("Aim for a regular, healthy sleep schedule.")
    if not tips:
        tips.append("Keep your current routine, practise mock tests and review weak topics regularly.")
    if score < 50:
        tips.append("Discuss a focused improvement plan with a teacher or academic mentor.")
    return tips

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = {
            "study_hours": float(request.form["study_hours"]),
            "attendance": float(request.form["attendance"]),
            "previous_marks": float(request.form["previous_marks"]),
            "assignment_score": float(request.form["assignment_score"]),
            "sleep_hours": float(request.form["sleep_hours"]),
        }
        limits = {
            "study_hours": (0, 16), "attendance": (0, 100),
            "previous_marks": (0, 100), "assignment_score": (0, 100),
            "sleep_hours": (0, 24)
        }
        for key, value in data.items():
            low, high = limits[key]
            if not low <= value <= high:
                raise ValueError(f"{key.replace('_', ' ').title()} must be between {low} and {high}.")
        input_df = pd.DataFrame([data], columns=FEATURES)
        score = round(float(model.predict(input_df)[0]), 1)
        score = max(0, min(100, score))
        label, css_class = category(score)
        return render_template(
            "result.html", score=score, label=label, css_class=css_class,
            data=data, tips=advice(data, score)
        )
    except (ValueError, KeyError) as exc:
        return render_template("index.html", error=str(exc)), 400

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
