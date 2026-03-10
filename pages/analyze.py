import streamlit as st
from modules.skill_analyzer import load_job_data, get_all_roles, get_role_info, analyze_skills

# ── HEADER ────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:2.5rem;">
    <div style="font-size:0.68rem; font-weight:500; letter-spacing:3px; text-transform:uppercase;
                color:rgba(26,60,35,0.35); margin-bottom:0.6rem; font-family:'Inter',sans-serif;">
        Skill Analysis
    </div>
    <div style="font-family:'Fraunces',serif; font-size:2.8rem; font-weight:300; color:#1A3C23;
                letter-spacing:-0.5px; line-height:1.1; margin-bottom:0.8rem;">
        What's your <em style="font-weight:600;">target role?</em>
    </div>
    <div style="font-size:0.88rem; color:rgba(26,60,35,0.45); font-family:'Inter',sans-serif;
                font-weight:300; line-height:1.7; max-width:520px;">
        Select a role, check off your skills, and get your match score instantly.
    </div>
</div>
<div style="height:1px; background:rgba(26,60,35,0.08); margin-bottom:2.5rem;"></div>
""", unsafe_allow_html=True)

# ── SESSION INIT ──────────────────────────────────────
if "selected_tags" not in st.session_state:
    st.session_state.selected_tags = []
if "last_role" not in st.session_state:
    st.session_state.last_role = None

# Prefill from quiz or explorer
if "prefilled_skills" in st.session_state and st.session_state.prefilled_skills:
    for s in st.session_state.prefilled_skills:
        if s not in st.session_state.selected_tags:
            st.session_state.selected_tags.append(s)
    st.session_state.prefilled_skills = []

roles = get_all_roles()

# Prefill role from explorer
prefill_role = st.session_state.pop("prefill_role", None)
default_role_index = roles.index(prefill_role) if prefill_role and prefill_role in roles else 0

# ── STEP 1: ROLE SELECTION ────────────────────────────
st.markdown('<div style="font-size:0.68rem; font-weight:500; letter-spacing:3px; text-transform:uppercase; color:rgba(26,60,35,0.35); margin-bottom:1rem; font-family:Inter,sans-serif;">Step 01 — Choose a Role</div>', unsafe_allow_html=True)

col_sel, col_info = st.columns([1.2, 2], gap="large")

with col_sel:
    selected_role = st.selectbox(
        "Role",
        roles,
        index=default_role_index,
        label_visibility="collapsed",
        key="role_select"
    )

if selected_role != st.session_state.last_role:
    st.session_state.selected_tags = []
    st.session_state.last_role = selected_role

role_info = get_role_info(selected_role)

with col_info:
    diff       = role_info["difficulty"]
    diff_color = "#2A6B3A" if diff == "Beginner" else "#7A5C10" if diff == "Intermediate" else "#7A2A2A"
    n_skills   = len(role_info["required_skills"])

    st.markdown(f"""
    <div style="display:flex; gap:1rem; flex-wrap:wrap; align-items:center; padding-top:0.2rem;">
        <div style="background:rgba(255,255,255,0.5); border:1px solid rgba(26,60,35,0.1);
                    border-radius:3px; padding:0.7rem 1.2rem;">
            <div style="font-size:0.6rem; letter-spacing:1.5px; text-transform:uppercase;
                        color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.3rem;">Salary</div>
            <div style="font-family:'Fraunces',serif; font-weight:600; font-size:1.1rem;
                        color:#1A3C23;">{role_info['salary']}</div>
        </div>
        <div style="background:rgba(255,255,255,0.5); border:1px solid rgba(26,60,35,0.1);
                    border-radius:3px; padding:0.7rem 1.2rem;">
            <div style="font-size:0.6rem; letter-spacing:1.5px; text-transform:uppercase;
                        color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.3rem;">Difficulty</div>
            <div style="font-family:'Fraunces',serif; font-weight:600; font-size:1.1rem;
                        color:{diff_color};">{diff}</div>
        </div>
        <div style="background:rgba(255,255,255,0.5); border:1px solid rgba(26,60,35,0.1);
                    border-radius:3px; padding:0.7rem 1.2rem;">
            <div style="font-size:0.6rem; letter-spacing:1.5px; text-transform:uppercase;
                        color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.3rem;">Skills Needed</div>
            <div style="font-family:'Fraunces',serif; font-weight:600; font-size:1.1rem;
                        color:#1A3C23;">{n_skills}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2.5rem 0;"></div>', unsafe_allow_html=True)

# ── STEP 2: SKILL SELECTION ───────────────────────────
st.markdown('<div style="font-size:0.68rem; font-weight:500; letter-spacing:3px; text-transform:uppercase; color:rgba(26,60,35,0.35); margin-bottom:0.5rem; font-family:Inter,sans-serif;">Step 02 — Select Your Skills</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size:0.85rem; color:rgba(26,60,35,0.45); font-family:Inter,sans-serif; margin-bottom:1.5rem;">Click to toggle skills you already have.</div>', unsafe_allow_html=True)

required_skills = role_info["required_skills"]

extra_skills = [
    "Python", "SQL", "Excel", "Git", "Docker", "Kubernetes", "Linux",
    "JavaScript", "React", "Node.js", "HTML", "CSS", "TypeScript",
    "Machine Learning", "Deep Learning", "Statistics", "R", "Spark",
    "Tableau", "Power BI", "AWS", "Azure", "GCP", "Terraform",
    "Agile", "Scrum", "Communication", "APIs", "Flask", "FastAPI",
    "MongoDB", "PostgreSQL", "Redis", "Kafka", "Airflow", "NLP",
    "PyTorch", "TensorFlow", "OpenCV", "Figma", "Swift", "Kotlin",
]
all_skills = list(dict.fromkeys(required_skills + [s for s in extra_skills if s not in required_skills]))

# Required skills
st.markdown('<div style="font-size:0.72rem; color:rgba(26,60,35,0.4); font-family:Inter,sans-serif; letter-spacing:0.5px; margin-bottom:0.8rem;">Required for this role:</div>', unsafe_allow_html=True)

req_cols = st.columns(6, gap="small")
for i, skill in enumerate(required_skills):
    with req_cols[i % 6]:
        is_selected = skill in st.session_state.selected_tags
        if st.button(
            f"✓ {skill}" if is_selected else skill,
            key=f"req_{skill}",
            use_container_width=True,
            type="primary" if is_selected else "secondary"
        ):
            if skill in st.session_state.selected_tags:
                st.session_state.selected_tags.remove(skill)
            else:
                st.session_state.selected_tags.append(skill)
            st.rerun()

st.markdown('<div style="margin:1.5rem 0 0.8rem;"><span style="font-size:0.72rem; color:rgba(26,60,35,0.4); font-family:Inter,sans-serif; letter-spacing:0.5px;">Other common skills:</span></div>', unsafe_allow_html=True)

other_skills = [s for s in extra_skills if s not in required_skills]
oth_cols = st.columns(6, gap="small")
for i, skill in enumerate(other_skills[:24]):
    with oth_cols[i % 6]:
        is_selected = skill in st.session_state.selected_tags
        if st.button(
            f"✓ {skill}" if is_selected else skill,
            key=f"oth_{skill}",
            use_container_width=True,
            type="primary" if is_selected else "secondary"
        ):
            if skill in st.session_state.selected_tags:
                st.session_state.selected_tags.remove(skill)
            else:
                st.session_state.selected_tags.append(skill)
            st.rerun()

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2.5rem 0;"></div>', unsafe_allow_html=True)

# ── STEP 3: MANUAL INPUT ──────────────────────────────
st.markdown('<div style="font-size:0.68rem; font-weight:500; letter-spacing:3px; text-transform:uppercase; color:rgba(26,60,35,0.35); margin-bottom:0.5rem; font-family:Inter,sans-serif;">Step 03 — Add More Skills</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size:0.85rem; color:rgba(26,60,35,0.45); font-family:Inter,sans-serif; margin-bottom:1rem;">Not in the list above? Type them here.</div>', unsafe_allow_html=True)

col_in, col_btn = st.columns([3, 1], gap="medium")
with col_in:
    manual_input = st.text_input(
        "Extra skills",
        placeholder="e.g. Solidity, Flutter, Prompt Engineering...",
        label_visibility="collapsed",
        key="manual_skills"
    )
with col_btn:
    if st.button("Add Skills", use_container_width=True):
        if manual_input:
            new_skills = [s.strip() for s in manual_input.split(",") if s.strip()]
            for s in new_skills:
                if s not in st.session_state.selected_tags:
                    st.session_state.selected_tags.append(s)
            st.rerun()

# ── SELECTED PREVIEW ──────────────────────────────────
if st.session_state.selected_tags:
    chips = "".join([
        f'<span style="background:#1A3C23; color:#EDEADE; padding:0.3rem 0.9rem; '
        f'border-radius:2px; font-size:0.78rem; font-family:Inter,sans-serif; '
        f'display:inline-block; margin:0.2rem;">{s}</span>'
        for s in st.session_state.selected_tags
    ])
    st.markdown(f"""
    <div style="margin-top:1.5rem; background:rgba(26,60,35,0.03);
                border:1px solid rgba(26,60,35,0.09); border-radius:3px; padding:1.2rem 1.5rem;">
        <div style="font-size:0.62rem; letter-spacing:2px; text-transform:uppercase;
                    color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.8rem;">
            Selected — {len(st.session_state.selected_tags)} skills
        </div>
        <div style="line-height:2.4;">{chips}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2.5rem 0;"></div>', unsafe_allow_html=True)

# ── ANALYZE BUTTON ────────────────────────────────────
col1, col2, col3 = st.columns([1.5, 1, 2])
with col1:
    analyze_clicked = st.button(
        "Run Analysis →",
        type="primary",
        use_container_width=True,
        disabled=len(st.session_state.selected_tags) == 0
    )
with col2:
    if st.button("Clear All", use_container_width=True):
        st.session_state.selected_tags = []
        st.rerun()

if analyze_clicked:
    if not st.session_state.selected_tags:
        st.warning("Please select at least one skill.")
    else:
        with st.spinner("Analyzing..."):
            result = analyze_skills(st.session_state.selected_tags, selected_role)

        # ── Save to session state (used by Dashboard ML + Roadmap) ──
        st.session_state.result      = result
        st.session_state.role        = selected_role
        st.session_state.user_skills = st.session_state.selected_tags.copy()

        score       = result["score"]
        score_color = "#2A6B3A" if score >= 70 else "#7A5C10" if score >= 40 else "#7A2A2A"

        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.5); border:1px solid rgba(26,60,35,0.1);
                    border-radius:3px; padding:2rem 2.5rem; margin-top:2rem;">
            <div style="display:flex; justify-content:space-between; align-items:center;
                        flex-wrap:wrap; gap:1.5rem;">
                <div>
                    <div style="font-size:0.62rem; letter-spacing:2px; text-transform:uppercase;
                                color:rgba(26,60,35,0.35); font-family:Inter,sans-serif;
                                margin-bottom:0.5rem;">Analysis Complete</div>
                    <div style="font-family:'Fraunces',serif; font-size:1.5rem; font-weight:600;
                                color:#1A3C23; margin-bottom:0.3rem;">{selected_role}</div>
                    <div style="font-size:0.85rem; color:rgba(26,60,35,0.5); font-family:Inter,sans-serif;">
                        {len(result['matched'])} matched · {len(result['missing'])} missing · {result['readiness']}
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-family:'Fraunces',serif; font-size:3.5rem; font-weight:700;
                                color:{score_color}; line-height:1; letter-spacing:-1px;">{score}%</div>
                    <div style="font-size:0.62rem; color:rgba(26,60,35,0.35); text-transform:uppercase;
                                letter-spacing:1.5px; font-family:Inter,sans-serif;">match score</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="margin-top:1.5rem;"></div>', unsafe_allow_html=True)

        # ── ML SNEAK PEEK: top 2 alternative roles ────────────────
        try:
            from modules.role_recommender import get_similar_roles
            with st.spinner("Finding similar roles..."):
                recs = get_similar_roles(st.session_state.user_skills, selected_role, top_n=2)
            if recs:
                st.markdown("""
                <div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase;
                            color:rgba(26,60,35,0.35); font-family:Inter,sans-serif;
                            margin-bottom:0.8rem;">You might also fit</div>
                """, unsafe_allow_html=True)
                rec_cols = st.columns(len(recs), gap="medium")
                for col, rec in zip(rec_cols, recs):
                    with col:
                        st.markdown(f"""
                        <div style="background:rgba(255,255,255,0.4);
                                    border:1px solid rgba(26,60,35,0.1);
                                    border-radius:3px; padding:1rem 1.2rem;
                                    display:flex; justify-content:space-between;
                                    align-items:center;">
                            <div>
                                <div style="font-family:'Fraunces',serif; font-weight:600;
                                            font-size:0.95rem; color:#1A3C23;">{rec['role']}</div>
                                <div style="font-size:0.72rem; color:rgba(26,60,35,0.45);
                                            font-family:Inter,sans-serif; margin-top:0.2rem;">
                                    {rec['salary']} · {rec['readiness']}
                                </div>
                            </div>
                            <div style="font-family:'Fraunces',serif; font-weight:700;
                                        font-size:1.4rem; color:#1A3C23;">{rec['match_pct']}%</div>
                        </div>
                        """, unsafe_allow_html=True)
        except Exception:
            pass  # ML is optional — don't break the page if it fails

        st.markdown('<div style="margin-top:1.5rem;"></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("View Dashboard →", type="primary", use_container_width=True):
                st.session_state.current_page = "Dashboard"
                st.rerun()
        with c2:
            if st.button("View Roadmap →", use_container_width=True):
                st.session_state.current_page = "Roadmap"
                st.rerun()