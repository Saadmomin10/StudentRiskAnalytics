import csv
import random
from datetime import date, timedelta
from pathlib import Path

OUTPUT_FILE = Path(__file__).parent / "lms_activity.csv"

rows = []

start_date = date(2026, 1, 1)

activity_id = 1

for student_num in range(1, 501):
    student_id = f"STU{student_num:05d}"

    for _ in range(20):

        activity_date = start_date + timedelta(
            days=random.randint(0, 180)
        )

        login_count = random.randint(0, 8)

        video_minutes = random.randint(0, 180)

        resources_viewed = random.randint(0, 15)

        quiz_attempts = random.randint(0, 5)

        forum_posts = random.randint(0, 5)

        session_minutes = random.randint(0, 240)

        rows.append([
            f"LMS{activity_id:06d}",
            student_id,
            activity_date,
            login_count,
            video_minutes,
            resources_viewed,
            quiz_attempts,
            forum_posts,
            session_minutes
        ])

        activity_id += 1


with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "activity_id",
        "student_id",
        "activity_date",
        "login_count",
        "video_minutes",
        "resources_viewed",
        "quiz_attempts",
        "forum_posts",
        "session_minutes"
    ])

    writer.writerows(rows)


print(f"Dataset created successfully: {OUTPUT_FILE}")
print(f"Total LMS activity records: {len(rows)}")