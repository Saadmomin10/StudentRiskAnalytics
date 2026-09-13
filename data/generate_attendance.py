import csv
import random
from pathlib import Path

OUTPUT_FILE = Path(__file__).parent / "attendance.csv"

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
        total_classes = random.randint(35, 50)
        attended_classes = random.randint(
            int(total_classes * 0.50),
            total_classes
        )

        attendance_percentage = round(
            (attended_classes / total_classes) * 100, 2
        )

        rows.append([
            student_id,
            subject,
            total_classes,
            attended_classes,
            attendance_percentage
        ])

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "student_id",
        "subject",
        "total_classes",
        "attended_classes",
        "attendance_percentage"
    ])

    writer.writerows(rows)

print(f"Dataset created successfully: {OUTPUT_FILE}")
print(f"Total attendance records: {len(rows)}")