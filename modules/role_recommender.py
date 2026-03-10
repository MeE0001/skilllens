"""
modules/role_recommender.py
===========================
ML-powered role recommendation using TF-IDF vectorization + cosine similarity.

How it works:
1. Each role's required skills are treated as a "document"
2. TF-IDF vectorizes all roles into skill-weighted vectors
3. User's skills are vectorized the same way
4. Cosine similarity finds which roles are closest to the user's profile
5. Returns top N alternative roles with match % and gap analysis
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from modules.skill_analyzer import get_all_roles, get_role_info


def _build_model():
    """Build TF-IDF model over all roles. Cached after first call."""
    roles = get_all_roles()
    # Each role becomes a "document" of its skills joined as text
    role_docs = []
    for role in roles:
        info = get_role_info(role)
        # Repeat high-value skills to boost their TF-IDF weight
        skills = info["required_skills"]
        doc = " ".join(s.lower().replace(" ", "_").replace("/", "_") for s in skills)
        role_docs.append(doc)

    vectorizer = TfidfVectorizer(analyzer="word", token_pattern=r"[^\s]+")
    role_matrix = vectorizer.fit_transform(role_docs)

    return vectorizer, role_matrix, roles


# Module-level cache so we only build once per session
_vectorizer = None
_role_matrix = None
_roles = None


def _get_model():
    global _vectorizer, _role_matrix, _roles
    if _vectorizer is None:
        _vectorizer, _role_matrix, _roles = _build_model()
    return _vectorizer, _role_matrix, _roles


def get_similar_roles(user_skills: list, current_role: str, top_n: int = 3) -> list:
    """
    Given a list of user skill strings and their target role,
    return top_n similar roles (excluding current_role) with:
      - role name
      - similarity score (0-100)
      - match % (how many required skills user has)
      - missing skills list
      - readiness label
    """
    if not user_skills:
        return []

    vectorizer, role_matrix, roles = _get_model()

    # Vectorize user skills the same way
    user_doc = " ".join(s.lower().replace(" ", "_").replace("/", "_") for s in user_skills)

    try:
        user_vec = vectorizer.transform([user_doc])
    except Exception:
        return []

    # Cosine similarity between user and every role
    sims = cosine_similarity(user_vec, role_matrix)[0]

    # Build scored list, exclude current target role
    scored = []
    for i, role in enumerate(roles):
        if role == current_role:
            continue
        sim_score = float(sims[i])

        info = get_role_info(role)
        required = info["required_skills"]
        user_set  = set(s.lower() for s in user_skills)
        matched   = [s for s in required if s.lower() in user_set]
        missing   = [s for s in required if s.lower() not in user_set]
        match_pct = round(len(matched) / max(len(required), 1) * 100)

        # Blend cosine similarity + direct match % for final score
        # 60% cosine (skill profile similarity) + 40% direct match
        blended = round(sim_score * 60 + match_pct * 0.4)

        if match_pct < 5:  # Skip roles where user has almost nothing
            continue

        readiness = (
            "Ready" if match_pct >= 75 else
            "Almost Ready" if match_pct >= 50 else
            "Good Fit" if match_pct >= 30 else
            "Stretch Goal"
        )

        scored.append({
            "role":       role,
            "similarity": round(sim_score * 100),
            "match_pct":  match_pct,
            "blended":    blended,
            "matched":    matched,
            "missing":    missing[:6],   # top 6 missing skills
            "salary":     info["salary"],
            "difficulty": info["difficulty"],
            "readiness":  readiness,
        })

    # Sort by blended score descending
    scored.sort(key=lambda x: x["blended"], reverse=True)

    return scored[:top_n]


def get_skill_clusters(user_skills: list) -> list:
    """
    Identify which skill clusters the user belongs to based on
    their skill overlap with common tech stacks.
    Returns list of (cluster_name, overlap_pct) tuples.
    """
    CLUSTERS = {
        "Data & ML":       ["Python", "SQL", "Pandas", "NumPy", "Scikit-learn",
                            "Machine Learning", "TensorFlow", "PyTorch", "Statistics"],
        "Cloud & DevOps":  ["AWS", "Docker", "Kubernetes", "Terraform", "CI/CD",
                            "Linux", "Git", "GitHub Actions", "Azure"],
        "Web Development": ["JavaScript", "React", "Node.js", "HTML", "CSS",
                            "TypeScript", "Next.js", "REST APIs"],
        "Data Engineering":["SQL", "Spark", "Kafka", "Airflow", "dbt",
                            "Snowflake", "Python", "ETL"],
        "Security":        ["Cybersecurity", "Network Security", "Linux",
                            "Penetration Testing", "Python"],
        "Mobile":          ["Flutter", "React Native", "Swift", "Kotlin", "Git"],
    }

    user_set = set(s.lower() for s in user_skills)
    results = []
    for cluster, skills in CLUSTERS.items():
        skill_set = set(s.lower() for s in skills)
        overlap   = len(user_set & skill_set)
        pct       = round(overlap / len(skill_set) * 100)
        if pct >= 20:
            results.append({"cluster": cluster, "pct": pct, "overlap": overlap, "total": len(skill_set)})

    results.sort(key=lambda x: x["pct"], reverse=True)
    return results[:3]