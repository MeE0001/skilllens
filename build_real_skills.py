"""
Run from your project root:
    python build_real_skills.py

Requires:
    /Users/rugved/Downloads/survey_results_public.csv  (Stack Overflow 2024)
    /Users/rugved/Downloads/postings.csv               (LinkedIn Job Postings)

Outputs: data/job_skills.csv
"""

import pandas as pd
import os
import re
from collections import Counter

SO_PATH  = "/Users/rugved/Downloads/survey_results_public.csv"
LI_PATH  = "/Users/rugved/Downloads/postings.csv"

# ── SkillLens role → Stack Overflow DevType keywords ─────────────────────
SO_ROLE_MAP = {
    "Data Scientist":            ["Data scientist"],
    "Data Analyst":              ["Data or business analyst"],
    "Data Engineer":             ["Data engineer"],
    "Machine Learning Engineer": ["Machine learning"],
    "AI Engineer":               ["Machine learning", "AI"],
    "Backend Developer":         ["Back-end developer"],
    "Frontend Developer":        ["Front-end developer"],
    "Full Stack Developer":      ["Full-stack developer"],
    "DevOps Engineer":           ["DevOps"],
    "Cloud Engineer":            ["Cloud infrastructure", "DevOps"],
    "Cybersecurity Analyst":     ["Security professional"],
    "Security Engineer":         ["Security professional"],
    "Software Engineer":         ["Developer, desktop", "Engineer, software"],
    "Mobile Developer":          ["Mobile developer"],
    "Database Administrator":    ["Database administrator"],
    "QA Engineer":               ["QA", "tester"],
    "Game Developer":            ["Game", "developer"],
    "Engineering Manager":       ["Engineering manager"],
    "Embedded Systems Engineer": ["Embedded"],
    "Site Reliability Engineer": ["Site reliability"],
    "Blockchain Developer":      ["Blockchain"],
    "Quantitative Analyst":      ["Data scientist", "Data or business analyst"],
}

# ── SkillLens role → LinkedIn title keywords ─────────────────────────────
LI_ROLE_MAP = {
    "Data Scientist":            ["data scientist"],
    "Data Analyst":              ["data analyst"],
    "Data Engineer":             ["data engineer"],
    "Machine Learning Engineer": ["machine learning engineer", "ml engineer"],
    "AI Engineer":               ["ai engineer", "artificial intelligence"],
    "Backend Developer":         ["backend developer", "back-end developer", "backend engineer"],
    "Frontend Developer":        ["frontend developer", "front-end developer", "frontend engineer"],
    "Full Stack Developer":      ["full stack", "fullstack"],
    "DevOps Engineer":           ["devops engineer", "devops"],
    "Cloud Engineer":            ["cloud engineer", "cloud architect"],
    "Cybersecurity Analyst":     ["cybersecurity analyst", "security analyst", "information security"],
    "Security Engineer":         ["security engineer"],
    "Software Engineer":         ["software engineer", "software developer"],
    "Mobile Developer":          ["mobile developer", "ios developer", "android developer"],
    "Database Administrator":    ["database administrator", "dba"],
    "Data Architect":            ["data architect"],
    "Network Engineer":          ["network engineer"],
    "QA Engineer":               ["qa engineer", "quality assurance", "test engineer"],
    "Game Developer":            ["game developer", "game engineer"],
    "Engineering Manager":       ["engineering manager"],
    "Product Manager":           ["product manager"],
    "Business Analyst":          ["business analyst"],
    "UX Designer":               ["ux designer", "ui designer", "ux/ui"],
    "Blockchain Developer":      ["blockchain developer", "blockchain engineer"],
    "Site Reliability Engineer": ["site reliability", "sre"],
    "Solutions Architect":       ["solutions architect", "solution architect"],
    "Scrum Master":              ["scrum master", "agile coach"],
    "Technical Writer":          ["technical writer"],
    "IT Project Manager":        ["it project manager", "technology project manager"],
    "Quantitative Analyst":      ["quantitative analyst", "quant analyst"],
    "Prompt Engineer":           ["prompt engineer"],
    "NLP Engineer":              ["nlp engineer", "natural language"],
    "Computer Vision Engineer":  ["computer vision"],
    "Robotics Engineer":         ["robotics engineer"],
    "Embedded Systems Engineer": ["embedded engineer", "embedded systems"],
    "IT Support Specialist":     ["it support", "technical support", "help desk"],
}

# ── Fallback skills if SO data thin ──────────────────────────────────────
FALLBACK_SKILLS = {
    "Data Scientist":            ["Python", "SQL", "Machine Learning", "Statistics", "TensorFlow", "Pandas", "Scikit-learn"],
    "Data Analyst":              ["SQL", "Excel", "Python", "Tableau", "Power BI", "Statistics"],
    "Data Engineer":             ["Python", "SQL", "Spark", "Airflow", "AWS", "Kafka", "dbt"],
    "Machine Learning Engineer": ["Python", "TensorFlow", "PyTorch", "MLOps", "Docker", "AWS"],
    "AI Engineer":               ["Python", "PyTorch", "TensorFlow", "LLMs", "APIs", "Deep Learning"],
    "Backend Developer":         ["Python", "Node.js", "SQL", "APIs", "Docker", "PostgreSQL", "Redis"],
    "Frontend Developer":        ["JavaScript", "React", "TypeScript", "HTML", "CSS", "Figma"],
    "Full Stack Developer":      ["JavaScript", "React", "Node.js", "Python", "SQL", "Docker"],
    "DevOps Engineer":           ["Docker", "Kubernetes", "AWS", "Terraform", "Linux", "CI/CD"],
    "Cloud Engineer":            ["AWS", "Azure", "GCP", "Terraform", "Docker", "Kubernetes"],
    "Cybersecurity Analyst":     ["Network Security", "Linux", "Python", "Penetration Testing", "SIEM"],
    "Security Engineer":         ["Network Security", "Linux", "Python", "Cloud Security", "Zero Trust"],
    "Software Engineer":         ["Python", "Java", "Data Structures", "Algorithms", "Git", "SQL"],
    "Mobile Developer":          ["Swift", "Kotlin", "React Native", "Flutter", "Firebase"],
    "Database Administrator":    ["SQL", "PostgreSQL", "MongoDB", "Redis", "Performance Tuning"],
    "Data Architect":            ["SQL", "Data Modeling", "ETL", "AWS", "Spark", "Kafka"],
    "Network Engineer":          ["Networking", "Linux", "Cisco", "Firewalls", "TCP/IP"],
    "QA Engineer":               ["Test Automation", "Selenium", "Python", "API Testing", "CI/CD"],
    "Game Developer":            ["C++", "Unity", "Unreal Engine", "C#", "OpenGL"],
    "Engineering Manager":       ["Leadership", "Agile", "System Design", "Roadmapping"],
    "Product Manager":           ["Agile", "Scrum", "Roadmapping", "User Research", "Jira"],
    "Business Analyst":          ["SQL", "Excel", "Requirements Gathering", "Agile", "Tableau"],
    "UX Designer":               ["Figma", "User Research", "Prototyping", "Wireframing", "Adobe XD"],
    "Blockchain Developer":      ["Solidity", "Web3.js", "Smart Contracts", "Ethereum", "Python"],
    "Site Reliability Engineer": ["Linux", "Docker", "Kubernetes", "Python", "Monitoring", "AWS"],
    "Solutions Architect":       ["AWS", "System Design", "Microservices", "Docker", "Cloud"],
    "Scrum Master":              ["Scrum", "Agile", "Jira", "Facilitation", "Kanban"],
    "Technical Writer":          ["Technical Writing", "Documentation", "Markdown", "APIs", "Git"],
    "IT Project Manager":        ["Project Management", "Agile", "Scrum", "JIRA", "Risk Management"],
    "Quantitative Analyst":      ["Python", "R", "Statistics", "Financial Modeling", "SQL"],
    "Prompt Engineer":           ["LLMs", "Python", "Prompt Design", "APIs", "LangChain"],
    "NLP Engineer":              ["Python", "NLP", "PyTorch", "Hugging Face", "LLMs", "BERT"],
    "Computer Vision Engineer":  ["Python", "OpenCV", "PyTorch", "CNNs", "TensorFlow", "YOLO"],
    "Robotics Engineer":         ["Python", "C++", "ROS", "Control Systems", "Computer Vision"],
    "Embedded Systems Engineer": ["C", "C++", "RTOS", "Microcontrollers", "Linux", "FPGA"],
    "IT Support Specialist":     ["Windows", "Linux", "Networking", "Troubleshooting", "Active Directory"],
}

DIFFICULTY_MAP = {
    "Data Scientist":            "Advanced",
    "Data Analyst":              "Intermediate",
    "Data Engineer":             "Advanced",
    "Machine Learning Engineer": "Advanced",
    "AI Engineer":               "Advanced",
    "Backend Developer":         "Intermediate",
    "Frontend Developer":        "Intermediate",
    "Full Stack Developer":      "Advanced",
    "DevOps Engineer":           "Advanced",
    "Cloud Engineer":            "Advanced",
    "Cybersecurity Analyst":     "Advanced",
    "Security Engineer":         "Advanced",
    "Software Engineer":         "Intermediate",
    "Mobile Developer":          "Intermediate",
    "Database Administrator":    "Intermediate",
    "Data Architect":            "Advanced",
    "Network Engineer":          "Intermediate",
    "QA Engineer":               "Intermediate",
    "Game Developer":            "Intermediate",
    "Engineering Manager":       "Advanced",
    "Product Manager":           "Intermediate",
    "Business Analyst":          "Beginner",
    "UX Designer":               "Intermediate",
    "Blockchain Developer":      "Advanced",
    "Site Reliability Engineer": "Advanced",
    "Solutions Architect":       "Advanced",
    "Scrum Master":              "Intermediate",
    "Technical Writer":          "Beginner",
    "IT Project Manager":        "Intermediate",
    "Quantitative Analyst":      "Advanced",
    "Prompt Engineer":           "Intermediate",
    "NLP Engineer":              "Advanced",
    "Computer Vision Engineer":  "Advanced",
    "Robotics Engineer":         "Advanced",
    "Embedded Systems Engineer": "Advanced",
    "IT Support Specialist":     "Beginner",
}

# ── Step 1: Extract skills from Stack Overflow ────────────────────────────
print("Loading Stack Overflow survey...")
so = pd.read_csv(SO_PATH, low_memory=False)

# Columns that contain tech skills (semicolon-separated)
SKILL_COLS = [
    "LanguageHaveWorkedWith",
    "DatabaseHaveWorkedWith",
    "WebframeHaveWorkedWith",
    "PlatformHaveWorkedWith",
]

def get_so_skills(df, keywords, top_n=12):
    """Filter rows matching DevType keywords, extract top skills."""
    mask = df["DevType"].fillna("").str.lower().apply(
        lambda x: any(k.lower() in x for k in keywords)
    )
    subset = df[mask]
    if len(subset) < 10:
        return []

    skill_counter = Counter()
    for col in SKILL_COLS:
        for val in subset[col].dropna():
            for skill in str(val).split(";"):
                s = skill.strip()
                if s and s != "nan":
                    skill_counter[s] += 1

    return [s for s, _ in skill_counter.most_common(top_n)]

so_skills = {}
for role, keywords in SO_ROLE_MAP.items():
    skills = get_so_skills(so, keywords)
    so_skills[role] = skills
    print(f"  {role}: {len(skills)} SO skills found")

# ── Step 2: Extract India salaries from LinkedIn ──────────────────────────
print("\nLoading LinkedIn postings...")

# Load only needed columns to save memory
LI_COLS = ["title", "location", "normalized_salary", "currency", "min_salary", "max_salary", "med_salary"]
li = pd.read_csv(LI_PATH, usecols=LI_COLS, low_memory=False)

# Filter India jobs
india = li[
    li["location"].fillna("").str.contains("India", case=False)
]
print(f"  India postings found: {len(india)}")

def get_india_salary(df, keywords):
    """Get median salary range for a role from Indian postings."""
    mask = df["title"].fillna("").str.lower().apply(
        lambda x: any(k.lower() in x for k in keywords)
    )
    subset = df[mask].dropna(subset=["normalized_salary"])

    if len(subset) < 3:
        return None

    # normalized_salary is yearly USD — convert to INR lakhs
    # If currency is already INR keep as is, else convert
    inr_rows = subset[subset["currency"].fillna("").str.upper() == "INR"]
    usd_rows = subset[subset["currency"].fillna("").str.upper() != "INR"]

    salaries_inr = []
    for _, row in inr_rows.iterrows():
        salaries_inr.append(row["normalized_salary"])
    for _, row in usd_rows.iterrows():
        salaries_inr.append(row["normalized_salary"] * 84)

    if not salaries_inr:
        return None

    s = pd.Series(salaries_inr)
    p25 = s.quantile(0.25) / 100000
    p75 = s.quantile(0.75) / 100000

    lo = max(1, round(p25))
    hi = round(p75)
    if hi <= lo:
        hi = lo + 10

    return f"Rs.{lo}L-Rs.{hi}L"

li_salaries = {}
for role, keywords in LI_ROLE_MAP.items():
    sal = get_india_salary(india, keywords)
    li_salaries[role] = sal
    status = sal if sal else "not found — using fallback"
    print(f"  {role}: {status}")

# ── Fallback salaries ─────────────────────────────────────────────────────
FALLBACK_SALARY = {
    "Data Scientist":            "Rs.80L-Rs.134L",
    "Data Analyst":              "Rs.50L-Rs.92L",
    "Data Engineer":             "Rs.84L-Rs.134L",
    "Machine Learning Engineer": "Rs.101L-Rs.151L",
    "AI Engineer":               "Rs.101L-Rs.160L",
    "Backend Developer":         "Rs.80L-Rs.130L",
    "Frontend Developer":        "Rs.71L-Rs.122L",
    "Full Stack Developer":      "Rs.76L-Rs.130L",
    "DevOps Engineer":           "Rs.84L-Rs.139L",
    "Cloud Engineer":            "Rs.88L-Rs.139L",
    "Cybersecurity Analyst":     "Rs.76L-Rs.126L",
    "Security Engineer":         "Rs.84L-Rs.143L",
    "Software Engineer":         "Rs.84L-Rs.139L",
    "Mobile Developer":          "Rs.80L-Rs.130L",
    "Database Administrator":    "Rs.67L-Rs.109L",
    "Data Architect":            "Rs.92L-Rs.147L",
    "Network Engineer":          "Rs.63L-Rs.109L",
    "QA Engineer":               "Rs.50L-Rs.92L",
    "Game Developer":            "Rs.63L-Rs.113L",
    "Engineering Manager":       "Rs.126L-Rs.210L",
    "Product Manager":           "Rs.80L-Rs.139L",
    "Business Analyst":          "Rs.55L-Rs.92L",
    "UX Designer":               "Rs.63L-Rs.113L",
    "Blockchain Developer":      "Rs.84L-Rs.143L",
    "Site Reliability Engineer": "Rs.97L-Rs.147L",
    "Solutions Architect":       "Rs.101L-Rs.168L",
    "Scrum Master":              "Rs.71L-Rs.118L",
    "Technical Writer":          "Rs.46L-Rs.80L",
    "IT Project Manager":        "Rs.76L-Rs.130L",
    "Quantitative Analyst":      "Rs.92L-Rs.168L",
    "Prompt Engineer":           "Rs.76L-Rs.134L",
    "NLP Engineer":              "Rs.97L-Rs.147L",
    "Computer Vision Engineer":  "Rs.97L-Rs.147L",
    "Robotics Engineer":         "Rs.76L-Rs.130L",
    "Embedded Systems Engineer": "Rs.71L-Rs.118L",
    "IT Support Specialist":     "Rs.34L-Rs.63L",
}

# ── Step 3: Combine and build CSV ─────────────────────────────────────────
print("\nBuilding job_skills.csv...")
all_roles = set(list(SO_ROLE_MAP.keys()) + list(LI_ROLE_MAP.keys()) + list(FALLBACK_SKILLS.keys()))

rows = []
for role in sorted(all_roles):
    # Skills: SO skills first, fill with fallback
    so_s   = so_skills.get(role, [])
    fall_s = FALLBACK_SKILLS.get(role, [])
    combined = list(dict.fromkeys(so_s + [s for s in fall_s if s not in so_s]))[:15]

    # Salary: LinkedIn India first, fallback if not found
    salary = li_salaries.get(role) or FALLBACK_SALARY.get(role, "Rs.50L-Rs.100L")

    rows.append({
        "role":          role,
        "required_skills": ", ".join(combined),
        "salary":        salary,
        "difficulty":    DIFFICULTY_MAP.get(role, "Intermediate"),
    })

df = pd.DataFrame(rows)
os.makedirs("data", exist_ok=True)
df.to_csv("data/job_skills.csv", index=False)

print(f"\nDone! {len(df)} roles written to data/job_skills.csv")
print(df[["role", "salary", "difficulty"]].to_string(index=False))
