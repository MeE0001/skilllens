import pandas as pd
import os

def load_job_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base_dir, "data", "job_skills.csv")
    df = pd.read_csv(path)
    return df

def get_all_roles():
    df = load_job_data()
    return df["role"].tolist()

def get_role_info(role_name):
    df = load_job_data()
    row = df[df["role"] == role_name].iloc[0]
    return {
        "role": row["role"],
        "required_skills": [s.strip() for s in row["required_skills"].split(",")],
        "salary": row["salary"],
        "difficulty": row["difficulty"]
    }

def analyze_skills(user_skills, target_role):
    # Clean up user input
    user_skills_clean = [s.strip().lower() for s in user_skills]

    # Get role info
    role_info = get_role_info(target_role)
    required = role_info["required_skills"]
    required_clean = [s.lower() for s in required]

    # Compare
    matched = []
    missing = []

    for i, skill in enumerate(required_clean):
        if skill in user_skills_clean:
            matched.append(required[i])
        else:
            missing.append(required[i])

    # Calculate score
    total = len(required)
    score = round((len(matched) / total) * 100) if total > 0 else 0

    # Readiness level
    if score >= 80:
        readiness = "Job Ready"
    elif score >= 60:
        readiness = "Almost Ready"
    elif score >= 40:
        readiness = "Needs Improvement"
    else:
        readiness = "Beginner"

    return {
        "matched": matched,
        "missing": missing,
        "score": score,
        "readiness": readiness,
        "total_required": total,
        "salary": role_info["salary"],
        "difficulty": role_info["difficulty"]
    }