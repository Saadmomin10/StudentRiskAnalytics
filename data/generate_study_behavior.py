import csv
import random
from datetime import date, timedelta
from pathlib import Path

OUTPUT_FILE = Path(__file__).parent / "study_behavior.csv"

rows = []

start_date = date(2026, 1, 1)

record_id = 1

for student_num in range(1, 501):
    student_id = f"STU{student_num:05d}"

    for _ in range(10):

        study_date = start_date + timedelta(
            days=random.randint(0, 180)
        )

        study_hours = round(random.uniform(0.5, 8), 2)

        sleep_hours = round(random.uniform(4.5, 9), 2)

        library_hours = round(random.uniform(0, 5), 2)

        self_study_hours = round(random.uniform(0.5, 6), 2)

        distraction_hours = round(random.uniform(0, 5), 2)

        practice_questions = random.randint(0, 50)

        study_consistency = random.randint(1, 10)

        rows.append([
            f"SB{record_id:06d}",
            student_id,
            study_date,
            study_hours,
            sleep_hours,
            library_hours,
            self_study_hours,
            distraction_hours,
            practice_questions,
            study_consistency
        ])

        record_id += 1


with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "record_id",
        "student_id",
        "study_date",
        "study_hours",
        "sleep_hours",
        "library_hours",
        "self_study_hours",
        "distraction_hours",
        "practice_questions",
        "study_consistency"
    ])

    writer.writerows(rows)


print(f"Dataset created successfully: {OUTPUT_FILE}")
print(f"Total study behavior records: {len(rows)}")