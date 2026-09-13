import csv
import random
from pathlib import Path

OUTPUT_FILE = Path(__file__).parent / "students.csv"

departments = [
    "Computer Science",
    "Information Technology",
    "Electronics",
    "Mechanical",
    "Civil"
]

genders = ["Male", "Female"]

students = []

for i in range(1, 501):
    attendance = round(random.uniform(55, 100), 2)
    study_hours = round(random.uniform(1, 8), 2)
    assignment_completion = round(random.uniform(40, 100), 2)
    previous_gpa = round(random.uniform(4.5, 10.0), 2)

    # Generate marks with some relationship to academic behavior
    internal_marks = (
        attendance * 0.20
        + study_hours * 3
        + assignment_completion * 0.20
        + previous_gpa * 2
        + random.uniform(-10, 10)
    )

    internal_marks = round(max(20, min(100, internal_marks)), 2)

    # Determine risk level
    risk_score = (
        (100 - attendance) * 0.35
        + (100 - assignment_completion) * 0.25
        + (8 - study_hours) * 4
        + (7 - previous_gpa) * 5
        + (50 - internal_marks) * 0.20
    )

    if risk_score >= 30:
        risk_level = "High"
    elif risk_score >= 15:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    students.append([
        f"STU{i:05d}",
        f"Student_{i}",
        random.randint(18, 24),
        random.choice(genders),
        random.choice(departments),
        random.randint(1, 8),
        attendance,
        study_hours,
        assignment_completion,
        internal_marks,
        previous_gpa,
        risk_level
    ])

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "student_id",
        "name",
        "age",
        "gender",
        "department",
        "semester",
        "attendance_percentage",
        "study_hours_per_day",
        "assignment_completion_percentage",
        "internal_marks",
        "previous_gpa",
        "risk_level"
    ])

    writer.writerows(students)

print(f"Dataset created successfully: {OUTPUT_FILE}")
print(f"Total students: {len(students)}")