from flask import Flask, jsonify, request
from flask_cors import CORS
import csv
from pathlib import Path

app = Flask(__name__)
CORS(app)

DATA_FILE = Path(__file__).resolve().parent / "student_risk_analytics_noheader.csv"
FIELDS = [
    "student_id",
    "avg_attendance",
    "attended_classes",
    "total_classes",
    "assignment_completion_percentage",
    "avg_assignment_completion",
    "avg_assignment_score",
    "submitted_assignments",
    "total_assignments",
    "internal_marks",
    "avg_internal_marks",
    "avg_midterm_marks",
    "avg_final_exam_marks",
    "avg_total_marks",
    "previous_gpa",
    "study_hours_per_day",
    "total_study_hours",
    "total_sleep_hours",
    "total_library_hours",
    "total_self_study_hours",
    "total_distraction_hours",
    "total_practice_questions",
    "avg_study_consistency",
    "total_logins",
    "total_video_minutes",
    "total_resources_viewed",
    "total_quiz_attempts",
    "total_forum_posts",
    "total_session_minutes",
    "risk_level"
]

NUMERIC_FIELDS = set(FIELDS[1:-1])


def load_students():
    with open(DATA_FILE, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, fieldnames=FIELDS))


def clean_student(row):
    result = {}

    for key, value in row.items():
        if key in NUMERIC_FIELDS:
            try:
                number = float(value)
                result[key] = int(number) if number.is_integer() else number
            except (ValueError, TypeError):
                result[key] = value
        else:
            result[key] = value.strip()

    return result


@app.get("/")
def home():
    return jsonify({
        "application": "Student Risk Analytics API",
        "status": "running",
        "data_source": str(DATA_FILE),
        "endpoints": [
            "/api/summary",
            "/api/risk-distribution",
            "/api/risk-analysis",
            "/api/students",
            "/api/students/<student_id>"
        ]
    })


@app.get("/api/summary")
def summary():
    students = load_students()

    counts = {
        "High": 0,
        "Medium": 0,
        "Low": 0
    }

    for student in students:
        risk = student["risk_level"].strip()

        if risk in counts:
            counts[risk] += 1

    total = len(students)
    attention = counts["High"] + counts["Medium"]

    return jsonify({
        "total_students": total,
        "high_risk": counts["High"],
        "medium_risk": counts["Medium"],
        "low_risk": counts["Low"],
        "high_medium_risk": attention,
        "high_medium_percentage": round(
            attention / total * 100, 2
        ) if total else 0
    })


@app.get("/api/risk-distribution")
def risk_distribution():
    students = load_students()

    counts = {
        "High": 0,
        "Medium": 0,
        "Low": 0
    }

    for student in students:
        risk = student["risk_level"].strip()

        if risk in counts:
            counts[risk] += 1

    total = len(students)

    return jsonify([
        {
            "risk": risk,
            "students": counts[risk],
            "percentage": round(
                counts[risk] / total * 100, 2
            ) if total else 0
        }
        for risk in ["High", "Medium", "Low"]
    ])


@app.get("/api/risk-analysis")
def risk_analysis():
    students = load_students()

    groups = {
        "High": [],
        "Medium": [],
        "Low": []
    }

    for student in students:
        risk = student["risk_level"].strip()

        if risk in groups:
            groups[risk].append(student)

    metrics = {
        "avg_attendance": "attendance",
        "avg_assignment_completion": "assignment_completion",
        "avg_assignment_score": "assignment_score",
        "previous_gpa": "gpa",
        "study_hours_per_day": "study_hours_per_day",
        "avg_study_consistency": "study_consistency",
        "total_distraction_hours": "distraction_hours",
        "total_logins": "lms_logins",
        "total_video_minutes": "video_minutes",
        "total_quiz_attempts": "quiz_attempts"
    }

    result = []

    for risk in ["High", "Medium", "Low"]:

        item = {
            "risk": risk,
            "students": len(groups[risk])
        }

        for source, output in metrics.items():

            values = [
                float(student[source])
                for student in groups[risk]
            ]

            item[output] = round(
                sum(values) / len(values), 2
            ) if values else 0

        result.append(item)

    return jsonify(result)


@app.get("/api/students")
def student_list():

    students = [
        clean_student(student)
        for student in load_students()
    ]

    risk = request.args.get("risk", "").strip()
    search = request.args.get("search", "").strip().lower()

    try:
        limit = min(
            int(request.args.get("limit", 100)),
            500
        )
    except ValueError:
        limit = 100

    if risk:
        students = [
            student
            for student in students
            if student["risk_level"] == risk
        ]

    if search:
        students = [
            student
            for student in students
            if search in student["student_id"].lower()
        ]

    return jsonify({
        "count": len(students),
        "students": students[:limit]
    })


@app.get("/api/students/<student_id>")
def student_detail(student_id):

    student_id = student_id.strip().upper()

    students = [
        clean_student(student)
        for student in load_students()
    ]

    student = next(
        (
            student
            for student in students
            if student["student_id"] == student_id
        ),
        None
    )

    if not student:
        return jsonify({
            "error": "Student not found"
        }), 404

    return jsonify(student)


if __name__ == "__main__":

    print()
    print("=" * 50)
    print("STUDENT RISK ANALYTICS - FLASK API")
    print("=" * 50)
    print(f"Data file: {DATA_FILE}")
    print("API: http://127.0.0.1:5000")
    print("=" * 50)
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
