import csv
import random
from pathlib import Path

OUTPUT_FILE = Path(__file__).parent / "assignments.csv"

subjects = [
    "Big Data Analytics",
    "Computer Networks",
    "Database Management",
    "Machine Learning",
    "Operating Systems"
]

rows = []
assignment_id = 1

for student_num in range(1, 501):
    student_id = f"STU{student_num:05d}"

    for subject in subjects:
        total_assignments = random.randint(8, 12)
        submitted_assignments = random.randint(
            3,
            total_assignments
        )

        completion_percentage = round(
            (submitted_assignments / total_assignments) * 100,
            2
        )

        average_score = round(
            random.uniform(35, 100),
            2
        )

        rows.append([
            f"ASG{assignment_id:05d}",
            student_id,
            subject,
            total_assignments,
            submitted_assignments,
            completion_percentage,
            average_score
        ])

        assignment_id += 1

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "assignment_id",
        "student_id",
        "subject",
        "total_assignments",
        "submitted_assignments",
        "completion_percentage",
        "average_assignment_score"
    ])

    writer.writerows(rows)

print(f"Dataset created successfully: {OUTPUT_FILE}")
print(f"Total assignment records: {len(rows)}")
