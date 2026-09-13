import csv
import random
from pathlib import Path

OUTPUT_FILE = Path(__file__).parent / "marks.csv"

subjects = [
    "Big Data Analytics",
    "Computer Networks",
    "Database Management",
    "Machine Learning",
    "Operating Systems"
]

rows = []

for student_num in range(1, 501):
    student_id = f"STU{student_num:05d}"

    for subject in subjects:
        internal = random.randint(20, 40)
        midterm = random.randint(15, 30)
        final_exam = random.randint(20, 30)

        total = internal + midterm + final_exam

        if total >= 85:
            grade = "A"
        elif total >= 70:
            grade = "B"
        elif total >= 55:
            grade = "C"
        elif total >= 40:
            grade = "D"
        else:
            grade = "F"

        rows.append([
            student_id,
            subject,
            internal,
            midterm,
            final_exam,
            total,
            grade
        ])

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "student_id",
        "subject",
        "internal_marks",
        "midterm_marks",
        "final_exam_marks",
        "total_marks",
        "grade"
    ])

    writer.writerows(rows)

print(f"Dataset created successfully: {OUTPUT_FILE}")
print(f"Total marks records: {len(rows)}")