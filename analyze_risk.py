import csv
from collections import defaultdict

FILE = "output/student_risk_analytics_noheader.csv"

rows = []

with open(FILE, "r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(
        f,
        fieldnames=[
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
    )

    rows = list(reader)


def num(r, field):
    try:
        return float(r[field])
    except:
        return 0


print("\n======================================")
print("STUDENT RISK ANALYTICS")
print("======================================")

# ------------------------------------------------------------
# 1. RISK DISTRIBUTION
# ------------------------------------------------------------

risk_counts = defaultdict(int)

for r in rows:
    risk_counts[r["risk_level"]] += 1

print("\n1. RISK DISTRIBUTION")
print("--------------------")

for risk in ["High", "Medium", "Low"]:
    print(f"{risk:8}: {risk_counts[risk]}")


# ------------------------------------------------------------
# 2. AVERAGE METRICS BY RISK
# ------------------------------------------------------------

groups = defaultdict(list)

for r in rows:
    groups[r["risk_level"]].append(r)

metrics = [
    ("Attendance", "avg_attendance"),
    ("Assignment Completion", "assignment_completion_percentage"),
    ("Assignment Score", "avg_assignment_score"),
    ("GPA", "previous_gpa"),
    ("Study Hours/Day", "study_hours_per_day"),
    ("Study Consistency", "avg_study_consistency"),
    ("Distraction Hours", "total_distraction_hours"),
    ("LMS Logins", "total_logins"),
    ("Video Minutes", "total_video_minutes"),
    ("Quiz Attempts", "total_quiz_attempts")
]

print("\n2. AVERAGES BY RISK LEVEL")
print("-------------------------")

for risk in ["High", "Medium", "Low"]:

    print(f"\n{risk} Risk:")

    for label, field in metrics:

        values = [
            num(r, field)
            for r in groups[risk]
        ]

        avg = sum(values) / len(values)

        print(
            f"  {label:25}: {avg:.2f}"
        )


# ------------------------------------------------------------
# 3. HIGH-RISK STUDENTS
# ------------------------------------------------------------

high_risk = [
    r for r in rows
    if r["risk_level"] == "High"
]

print("\n3. HIGH-RISK STUDENTS")
print("--------------------")
print("Total:", len(high_risk))

for r in high_risk[:20]:

    print(
        f"{r['student_id']:10} "
        f"Attendance={num(r,'avg_attendance'):.2f} "
        f"GPA={num(r,'previous_gpa'):.2f} "
        f"Assignment={num(r,'assignment_completion_percentage'):.2f}% "
        f"Study={num(r,'study_hours_per_day'):.2f} "
        f"Risk={r['risk_level']}"
    )


# ------------------------------------------------------------
# 4. LOWEST ATTENDANCE
# ------------------------------------------------------------

lowest_attendance = sorted(
    rows,
    key=lambda r: num(r, "avg_attendance")
)

print("\n4. 10 STUDENTS WITH LOWEST ATTENDANCE")
print("--------------------------------------")

for r in lowest_attendance[:10]:

    print(
        f"{r['student_id']:10} "
        f"Attendance={num(r,'avg_attendance'):.2f}% "
        f"Risk={r['risk_level']}"
    )


# ------------------------------------------------------------
# 5. LOWEST GPA
# ------------------------------------------------------------

lowest_gpa = sorted(
    rows,
    key=lambda r: num(r, "previous_gpa")
)

print("\n5. 10 STUDENTS WITH LOWEST GPA")
print("------------------------------")

for r in lowest_gpa[:10]:

    print(
        f"{r['student_id']:10} "
        f"GPA={num(r,'previous_gpa'):.2f} "
        f"Risk={r['risk_level']}"
    )


# ------------------------------------------------------------
# 6. LOWEST ASSIGNMENT COMPLETION
# ------------------------------------------------------------

lowest_assignment = sorted(
    rows,
    key=lambda r: num(
        r,
        "assignment_completion_percentage"
    )
)

print("\n6. 10 STUDENTS WITH LOWEST ASSIGNMENT COMPLETION")
print("------------------------------------------------")

for r in lowest_assignment[:10]:

    print(
        f"{r['student_id']:10} "
        f"Completion="
        f"{num(r,'assignment_completion_percentage'):.2f}% "
        f"Risk={r['risk_level']}"
    )


# ------------------------------------------------------------
# 7. HIGHEST DISTRACTION
# ------------------------------------------------------------

highest_distraction = sorted(
    rows,
    key=lambda r: num(
        r,
        "total_distraction_hours"
    ),
    reverse=True
)

print("\n7. 10 STUDENTS WITH HIGHEST DISTRACTION")
print("---------------------------------------")

for r in highest_distraction[:10]:

    print(
        f"{r['student_id']:10} "
        f"Distraction="
        f"{num(r,'total_distraction_hours'):.2f} hrs "
        f"Risk={r['risk_level']}"
    )


print("\n======================================")
print("ANALYSIS COMPLETE")
print("======================================")
