import csv
import os
from collections import defaultdict

# ============================================================
# PATHS
# ============================================================

BASE = "/mnt/c/StudentRiskAnalytics"
DATA = os.path.join(BASE, "data")
OUTPUT = os.path.join(BASE, "output")

os.makedirs(OUTPUT, exist_ok=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def read_csv(filename):
    path = os.path.join(DATA, filename)

    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def to_int(value):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return 0


def average(values):
    if not values:
        return 0.0

    return sum(values) / len(values)


def write_csv(filename, rows, fields):
    path = os.path.join(OUTPUT, filename)

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created: {path} ({len(rows)} rows)")


# ============================================================
# LOAD SOURCE DATA
# ============================================================

print()
print("======================================")
print("LOADING SOURCE DATA")
print("======================================")

students = read_csv("students.csv")
attendance = read_csv("attendance.csv")
assignments = read_csv("assignments.csv")
marks = read_csv("marks.csv")
lms = read_csv("lms_activity.csv")
study = read_csv("study_behavior.csv")

print()
print("SOURCE RECORDS")
print("students       :", len(students))
print("attendance     :", len(attendance))
print("assignments    :", len(assignments))
print("marks          :", len(marks))
print("lms_activity   :", len(lms))
print("study_behavior :", len(study))
print()


# ============================================================
# ATTENDANCE SUMMARY
# ============================================================

print("Generating attendance summary...")

att = defaultdict(lambda: {
    "total_classes": 0,
    "attended_classes": 0,
    "percentages": []
})

for r in attendance:
    sid = r["student_id"]

    att[sid]["total_classes"] += to_int(
        r["total_classes"]
    )

    att[sid]["attended_classes"] += to_int(
        r["attended_classes"]
    )

    att[sid]["percentages"].append(
        to_float(r["attendance_percentage"])
    )


attendance_summary = []

for s in students:
    sid = s["student_id"]
    x = att[sid]

    avg_attendance = average(
        x["percentages"]
    )

    attendance_summary.append({
        "student_id": sid,
        "avg_attendance": round(avg_attendance, 2),
        "attended_classes": x["attended_classes"],
        "total_classes": x["total_classes"]
    })


write_csv(
    "attendance_summary.csv",
    attendance_summary,
    [
        "student_id",
        "avg_attendance",
        "attended_classes",
        "total_classes"
    ]
)


# ============================================================
# ASSIGNMENT SUMMARY
# ============================================================

print("Generating assignment summary...")

asg = defaultdict(lambda: {
    "completion": [],
    "scores": [],
    "submitted": 0,
    "total": 0
})

for r in assignments:
    sid = r["student_id"]

    asg[sid]["completion"].append(
        to_float(r["completion_percentage"])
    )

    asg[sid]["scores"].append(
        to_float(r["average_assignment_score"])
    )

    asg[sid]["submitted"] += to_int(
        r["submitted_assignments"]
    )

    asg[sid]["total"] += to_int(
        r["total_assignments"]
    )


assignment_summary = []

for s in students:
    sid = s["student_id"]
    x = asg[sid]

    avg_completion = average(
        x["completion"]
    )

    avg_score = average(
        x["scores"]
    )

    assignment_summary.append({
        "student_id": sid,
        "assignment_completion_percentage":
            round(avg_completion, 2),

        "avg_assignment_completion":
            round(avg_completion, 2),

        "avg_assignment_score":
            round(avg_score, 2),

        "submitted_assignments":
            x["submitted"],

        "total_assignments":
            x["total"]
    })


write_csv(
    "assignments_summary.csv",
    assignment_summary,
    [
        "student_id",
        "assignment_completion_percentage",
        "avg_assignment_completion",
        "avg_assignment_score",
        "submitted_assignments",
        "total_assignments"
    ]
)


# ============================================================
# MARKS SUMMARY
# ============================================================

print("Generating marks summary...")

mk = defaultdict(lambda: {
    "internal": [],
    "midterm": [],
    "final": [],
    "total": []
})

for r in marks:
    sid = r["student_id"]

    mk[sid]["internal"].append(
        to_float(r["internal_marks"])
    )

    mk[sid]["midterm"].append(
        to_float(r["midterm_marks"])
    )

    mk[sid]["final"].append(
        to_float(r["final_exam_marks"])
    )

    mk[sid]["total"].append(
        to_float(r["total_marks"])
    )


marks_summary = []

for s in students:
    sid = s["student_id"]

    # IMPORTANT:
    # Use sid here, not s.
    x = mk[sid]

    marks_summary.append({
        "student_id": sid,

        "internal_marks":
            to_float(s["internal_marks"]),

        "avg_internal_marks":
            round(average(x["internal"]), 2),

        "avg_midterm_marks":
            round(average(x["midterm"]), 2),

        "avg_final_exam_marks":
            round(average(x["final"]), 2),

        "avg_total_marks":
            round(average(x["total"]), 2),

        "previous_gpa":
            to_float(s["previous_gpa"])
    })


write_csv(
    "marks_summary.csv",
    marks_summary,
    [
        "student_id",
        "internal_marks",
        "avg_internal_marks",
        "avg_midterm_marks",
        "avg_final_exam_marks",
        "avg_total_marks",
        "previous_gpa"
    ]
)


# ============================================================
# LMS SUMMARY
# ============================================================

print("Generating LMS summary...")

lm = defaultdict(lambda: {
    "login_count": 0,
    "video_minutes": 0,
    "resources_viewed": 0,
    "quiz_attempts": 0,
    "forum_posts": 0,
    "session_minutes": 0
})


for r in lms:
    sid = r["student_id"]

    lm[sid]["login_count"] += to_int(
        r["login_count"]
    )

    lm[sid]["video_minutes"] += to_int(
        r["video_minutes"]
    )

    lm[sid]["resources_viewed"] += to_int(
        r["resources_viewed"]
    )

    lm[sid]["quiz_attempts"] += to_int(
        r["quiz_attempts"]
    )

    lm[sid]["forum_posts"] += to_int(
        r["forum_posts"]
    )

    lm[sid]["session_minutes"] += to_int(
        r["session_minutes"]
    )


lms_summary = []

for s in students:
    sid = s["student_id"]
    x = lm[sid]

    lms_summary.append({
        "student_id": sid,

        "total_logins":
            x["login_count"],

        "total_video_minutes":
            x["video_minutes"],

        "total_resources_viewed":
            x["resources_viewed"],

        "total_quiz_attempts":
            x["quiz_attempts"],

        "total_forum_posts":
            x["forum_posts"],

        "total_session_minutes":
            x["session_minutes"]
    })


write_csv(
    "lms_summary.csv",
    lms_summary,
    [
        "student_id",
        "total_logins",
        "total_video_minutes",
        "total_resources_viewed",
        "total_quiz_attempts",
        "total_forum_posts",
        "total_session_minutes"
    ]
)


# ============================================================
# STUDY BEHAVIOR SUMMARY
# ============================================================

print("Generating study behavior summary...")

sb = defaultdict(lambda: {
    "study_hours": [],
    "sleep_hours": 0,
    "library_hours": 0,
    "self_study_hours": 0,
    "distraction_hours": 0,
    "practice_questions": 0,
    "consistency": []
})


for r in study:
    sid = r["student_id"]

    sb[sid]["study_hours"].append(
        to_float(r["study_hours"])
    )

    sb[sid]["sleep_hours"] += to_float(
        r["sleep_hours"]
    )

    sb[sid]["library_hours"] += to_float(
        r["library_hours"]
    )

    sb[sid]["self_study_hours"] += to_float(
        r["self_study_hours"]
    )

    sb[sid]["distraction_hours"] += to_float(
        r["distraction_hours"]
    )

    sb[sid]["practice_questions"] += to_int(
        r["practice_questions"]
    )

    sb[sid]["consistency"].append(
        to_float(r["study_consistency"])
    )


study_summary = []

for s in students:
    sid = s["student_id"]
    x = sb[sid]

    avg_consistency = average(
        x["consistency"]
    )

    study_summary.append({
        "student_id": sid,

        "total_study_hours":
            round(sum(x["study_hours"]), 2),

        "total_sleep_hours":
            round(x["sleep_hours"], 2),

        "total_library_hours":
            round(x["library_hours"], 2),

        "total_self_study_hours":
            round(x["self_study_hours"], 2),

        "total_distraction_hours":
            round(x["distraction_hours"], 2),

        "total_practice_questions":
            x["practice_questions"],

        "avg_study_consistency":
            round(avg_consistency, 2)
    })


write_csv(
    "study_summary.csv",
    study_summary,
    [
        "student_id",
        "total_study_hours",
        "total_sleep_hours",
        "total_library_hours",
        "total_self_study_hours",
        "total_distraction_hours",
        "total_practice_questions",
        "avg_study_consistency"
    ]
)


# ============================================================
# CREATE LOOKUP MAPS
# ============================================================

print("Joining all summaries...")

att_map = {
    r["student_id"]: r
    for r in attendance_summary
}

asg_map = {
    r["student_id"]: r
    for r in assignment_summary
}

mk_map = {
    r["student_id"]: r
    for r in marks_summary
}

lm_map = {
    r["student_id"]: r
    for r in lms_summary
}

sb_map = {
    r["student_id"]: r
    for r in study_summary
}


# ============================================================
# FINAL STUDENT RISK ANALYTICS DATASET
# ============================================================

final_rows = []

for s in students:

    sid = s["student_id"]

    a = att_map[sid]
    g = asg_map[sid]
    m = mk_map[sid]
    l = lm_map[sid]
    b = sb_map[sid]

    final_rows.append({

        # -------------------------
        # Student
        # -------------------------

        "student_id":
            sid,

        # -------------------------
        # Attendance
        # -------------------------

        "avg_attendance":
            a["avg_attendance"],

        "attended_classes":
            a["attended_classes"],

        "total_classes":
            a["total_classes"],

        # -------------------------
        # Assignments
        # -------------------------

        "assignment_completion_percentage":
            g["assignment_completion_percentage"],

        "avg_assignment_completion":
            g["avg_assignment_completion"],

        "avg_assignment_score":
            g["avg_assignment_score"],

        "submitted_assignments":
            g["submitted_assignments"],

        "total_assignments":
            g["total_assignments"],

        # -------------------------
        # Marks
        # -------------------------

        "internal_marks":
            m["internal_marks"],

        "avg_internal_marks":
            m["avg_internal_marks"],

        "avg_midterm_marks":
            m["avg_midterm_marks"],

        "avg_final_exam_marks":
            m["avg_final_exam_marks"],

        "avg_total_marks":
            m["avg_total_marks"],

        "previous_gpa":
            m["previous_gpa"],

        # -------------------------
        # Study Behavior
        # -------------------------

        "study_hours_per_day":
            to_float(s["study_hours_per_day"]),

        "total_study_hours":
            b["total_study_hours"],

        "total_sleep_hours":
            b["total_sleep_hours"],

        "total_library_hours":
            b["total_library_hours"],

        "total_self_study_hours":
            b["total_self_study_hours"],

        "total_distraction_hours":
            b["total_distraction_hours"],

        "total_practice_questions":
            b["total_practice_questions"],

        "avg_study_consistency":
            b["avg_study_consistency"],

        # -------------------------
        # LMS
        # -------------------------

        "total_logins":
            l["total_logins"],

        "total_video_minutes":
            l["total_video_minutes"],

        "total_resources_viewed":
            l["total_resources_viewed"],

        "total_quiz_attempts":
            l["total_quiz_attempts"],

        "total_forum_posts":
            l["total_forum_posts"],

        "total_session_minutes":
            l["total_session_minutes"],

        # -------------------------
        # Risk
        # -------------------------

        "risk_level":
            s["risk_level"]
    })


# ============================================================
# FINAL CSV
# ============================================================

final_fields = [

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


write_csv(
    "student_risk_analytics.csv",
    final_rows,
    final_fields
)


# ============================================================
# VALIDATION
# ============================================================

print()
print("======================================")
print("VALIDATING OUTPUT FILES")
print("======================================")

output_files = [
    "attendance_summary.csv",
    "assignments_summary.csv",
    "marks_summary.csv",
    "lms_summary.csv",
    "study_summary.csv",
    "student_risk_analytics.csv"
]


for filename in output_files:

    path = os.path.join(
        OUTPUT,
        filename
    )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        line_count = sum(
            1 for _ in f
        )

    data_rows = line_count - 1

    print(
        f"{filename:35} "
        f"{data_rows} records"
    )


# ============================================================
# FINISHED
# ============================================================

print()
print("======================================")
print("SUMMARY GENERATION COMPLETE")
print("======================================")
print()
print("Final dataset:")
print(
    os.path.join(
        OUTPUT,
        "student_risk_analytics.csv"
    )
)
print()
