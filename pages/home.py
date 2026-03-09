import streamlit as st
from modules.skill_analyzer import get_all_roles, get_role_info, analyze_skills
from modules.demand_score import get_trending_skills

user_name = st.session_state.get("user_name", "")

# ── HERO ──────────────────────────────────────────────
col_left, col_right = st.columns([1.1, 1], gap="large")

with col_left:
    greeting = f"— {user_name.split()[0]}'s workspace" if user_name else "— Career Intelligence"
    st.markdown(f"""
    <div style="padding: 1rem 0 3rem;">
        <div style="font-size:0.68rem; font-weight:500; letter-spacing:3px;
                    text-transform:uppercase; color:rgba(26,60,35,0.38);
                    margin-bottom:2.5rem; font-family:'Inter',sans-serif;">{greeting}</div>
        <div style="font-family:'Fraunces',serif; font-size:4.8rem; font-weight:300;
                    color:#1A3C23; line-height:1.0; margin-bottom:2rem; letter-spacing:-1px;">
            Know<br>
            <em style="font-weight:600;">exactly</em><br>
            where you<br>
            stand.
        </div>
        <div style="width:48px; height:2px; background:#1A3C23; margin-bottom:2rem; opacity:0.25;"></div>
        <div style="font-size:0.95rem; color:rgba(26,60,35,0.5); line-height:1.8;
                    max-width:400px; font-family:'Inter',sans-serif; font-weight:300;">
            SkillLens compares your skills to any tech role,
            pinpoints exactly what's missing, and builds
            a step-by-step learning plan.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1.2, 1])
    with c1:
        if st.button("Start Analysis →", type="primary", use_container_width=True):
            st.session_state.current_page = "Analyze"
            st.rerun()
    with c2:
        if st.button("Browse Roles", use_container_width=True):
            st.session_state.current_page = "Explorer"
            st.rerun()

with col_right:
    st.markdown('<div style="padding:0 0 0 3rem; border-left:1px solid rgba(26,60,35,0.1);">', unsafe_allow_html=True)
    for val, lbl, has_border in [
        ("30+",  "Tech Roles Covered", True),
        ("80+",  "Skills Tracked",     True),
        ("Free", "Always & Forever",   False),
    ]:
        bb = "border-bottom:1px solid rgba(26,60,35,0.08);" if has_border else ""
        st.markdown(f"""
        <div style="padding:2.2rem 0; {bb}">
            <div style="font-family:'Fraunces',serif; font-size:3.5rem; font-weight:600;
                        color:#1A3C23; line-height:1; letter-spacing:-1px;">{val}</div>
            <div style="font-size:0.68rem; color:rgba(26,60,35,0.38); letter-spacing:2px;
                        text-transform:uppercase; margin-top:0.6rem;
                        font-family:'Inter',sans-serif;">{lbl}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:3.5rem 0;"></div>', unsafe_allow_html=True)

# ── QUICK ROLE MATCH FINDER ───────────────────────────
st.markdown('<div style="font-size:0.68rem; font-weight:500; letter-spacing:3px; text-transform:uppercase; color:rgba(26,60,35,0.35); margin-bottom:0.5rem; font-family:Inter,sans-serif;">Quick Match</div>', unsafe_allow_html=True)

col_h, col_sub = st.columns([1, 2])
with col_h:
    st.markdown("""
    <div style="font-family:'Fraunces',serif; font-size:2rem; font-weight:600;
                color:#1A3C23; line-height:1.2; margin-bottom:0.5rem;">
        Which roles suit<br>your skills?
    </div>
    """, unsafe_allow_html=True)
with col_sub:
    st.markdown("""
    <div style="font-size:0.85rem; color:rgba(26,60,35,0.45); line-height:1.7;
                font-family:'Inter',sans-serif; font-weight:300; padding-top:0.5rem;">
        Type a few skills below and instantly see which tech roles you match best.
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="margin-bottom:1rem;"></div>', unsafe_allow_html=True)

quick_input = st.text_input(
    "skills",
    placeholder="e.g. Python, SQL, Excel, Machine Learning, Docker...",
    key="quick_match_input",
    label_visibility="collapsed"
)

if quick_input.strip():
    quick_skills = [s.strip() for s in quick_input.split(",") if s.strip()]
    roles        = get_all_roles()
    results      = []
    for role in roles:
        r = analyze_skills(quick_skills, role)
        results.append((role, r["score"], r["matched"], r["missing"], r["readiness"], r["salary"], r["difficulty"]))
    results.sort(key=lambda x: x[1], reverse=True)
    top5 = results[:5]

    st.markdown('<div style="margin-top:1.5rem;">', unsafe_allow_html=True)
    for rank, (role, score, matched, missing, readiness, salary, diff) in enumerate(top5):
        score_color = "#2A6B3A" if score >= 70 else "#7A5C10" if score >= 40 else "#7A2A2A"
        bar_color   = "#1A3C23" if score >= 70 else "rgba(26,60,35,0.3)"
        border_top  = "border-top:1px solid rgba(26,60,35,0.07);" if rank > 0 else ""

        c1, c2, c3, c4 = st.columns([0.3, 2, 1.5, 1])
        with c1:
            st.markdown(f"""
            <div style="padding:1.1rem 0; {border_top}">
                <span style="font-family:'Fraunces',serif; font-size:0.85rem;
                             color:rgba(26,60,35,0.3); font-weight:400;">0{rank+1}</span>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style="padding:1.1rem 0; {border_top}">
                <div style="font-family:'Fraunces',serif; font-weight:600; font-size:1rem;
                            color:#1A3C23; margin-bottom:0.5rem;">{role}</div>
                <div style="background:rgba(26,60,35,0.08); border-radius:2px; height:3px; width:100%;">
                    <div style="background:{bar_color}; width:{score}%; height:3px; border-radius:2px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            matched_html = " ".join([
                f'<span style="background:rgba(42,107,58,0.08); color:#2A6B3A; '
                f'border:1px solid rgba(42,107,58,0.15); padding:0.15rem 0.6rem; border-radius:2px; '
                f'font-size:0.7rem; font-family:Inter,sans-serif; display:inline-block; margin:0.1rem;">{s}</span>'
                for s in matched[:3]
            ])
            st.markdown(f'<div style="padding:1.1rem 0; {border_top} line-height:2.2;">{matched_html if matched_html else "<span style=\'color:rgba(26,60,35,0.3);font-size:0.8rem;\'>No matches yet</span>"}</div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
            <div style="padding:0.6rem 0; {border_top} text-align:right;">
                <div style="font-family:'Fraunces',serif; font-size:1.6rem; font-weight:600;
                            color:{score_color};">{score}%</div>
                <div style="font-size:0.62rem; color:rgba(26,60,35,0.3); letter-spacing:1px;
                            text-transform:uppercase; font-family:Inter,sans-serif; margin-bottom:0.5rem;">match</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Analyze →", key=f"qm_{rank}", use_container_width=True):
                st.session_state.current_page = "Analyze"
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:3.5rem 0;"></div>', unsafe_allow_html=True)

# ── SKILL QUIZ (checkboxes — no navbar conflict) ──────
st.markdown('<div style="font-size:0.68rem; font-weight:500; letter-spacing:3px; text-transform:uppercase; color:rgba(26,60,35,0.35); margin-bottom:0.5rem; font-family:Inter,sans-serif;">Skill Quiz</div>', unsafe_allow_html=True)
st.markdown("""
<div style="font-family:'Fraunces',serif; font-size:2rem; font-weight:600;
            color:#1A3C23; line-height:1.2; margin-bottom:0.4rem;">
    Not sure what skills you have?
</div>
<div style="font-size:0.85rem; color:rgba(26,60,35,0.45); font-family:'Inter',sans-serif;
            font-weight:300; margin-bottom:2rem; line-height:1.7;">
    Tick everything that applies — we'll detect your skill profile automatically.
</div>
""", unsafe_allow_html=True)

quiz_questions = [
    ("Can write and run Python scripts",                 "Python"),
    ("Comfortable querying databases with SQL",          "SQL"),
    ("Built or deployed a machine learning model",       "Machine Learning"),
    ("Use Git for version control regularly",            "Git"),
    ("Can build UIs with React or similar",              "React"),
    ("Worked with cloud platforms (AWS/GCP/Azure)",      "Cloud"),
    ("Understand Docker or containerisation",            "Docker"),
    ("Create dashboards in Tableau or Power BI",         "Tableau"),
    ("Familiar with APIs and REST architecture",         "APIs"),
    ("Use Excel for data analysis regularly",            "Excel"),
    ("Experience with deep learning frameworks",         "Deep Learning"),
    ("Written Kubernetes or CI/CD pipelines",            "Kubernetes"),
]

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

cols = st.columns(3, gap="large")
for i, (question, skill) in enumerate(quiz_questions):
    with cols[i % 3]:
        checked = st.checkbox(question, key=f"quiz_{i}")
        st.session_state.quiz_answers[skill] = checked

detected = [skill for skill, yes in st.session_state.quiz_answers.items() if yes]

if detected:
    chips = "".join([
        f'<span style="background:#1A3C23; color:#EDEADE; padding:0.3rem 0.9rem; '
        f'border-radius:2px; font-size:0.78rem; font-family:Inter,sans-serif; '
        f'display:inline-block; margin:0.2rem;">{s}</span>'
        for s in detected
    ])
    st.markdown(f"""
    <div style="background:rgba(26,60,35,0.04); border:1px solid rgba(26,60,35,0.1);
                border-radius:4px; padding:1.5rem 2rem; margin-top:1.5rem;">
        <div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase;
                    color:rgba(26,60,35,0.4); font-family:Inter,sans-serif; margin-bottom:0.8rem;">
            Detected — {len(detected)} skills
        </div>
        <div style="line-height:2.5;">{chips}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div style="margin-top:1.2rem;"></div>', unsafe_allow_html=True)
    if st.button("Use These Skills in Full Analysis →", type="primary"):
        st.session_state.prefilled_skills = detected
        st.session_state.current_page = "Analyze"
        st.rerun()

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:3.5rem 0;"></div>', unsafe_allow_html=True)

# ── PROCESS ───────────────────────────────────────────
st.markdown('<div style="font-size:0.68rem; font-weight:500; letter-spacing:3px; text-transform:uppercase; color:rgba(26,60,35,0.35); margin-bottom:2.5rem; font-family:Inter,sans-serif;">The Process</div>', unsafe_allow_html=True)

steps = [
    ("Pick a role",      "Choose from 30+ tech roles including Data, Engineering, and Product."),
    ("Add your skills",  "Click to select or type in your current skill set."),
    ("See the gap",      "Get a precise match score and breakdown of what's missing."),
    ("Follow the plan",  "A curated, prioritized roadmap to bridge every gap."),
]

cols = st.columns(4, gap="medium")
for i, (col, (title, desc)) in enumerate(zip(cols, steps)):
    with col:
        st.markdown(f"""
        <div style="padding:1.5rem 1.2rem; background:rgba(255,255,255,0.35);
                    border:1px solid rgba(26,60,35,0.09); border-radius:2px;">
            <div style="font-family:'Fraunces',serif; font-size:0.72rem;
                        color:rgba(26,60,35,0.25); margin-bottom:1rem; letter-spacing:1px;">0{i+1}</div>
            <div style="font-family:'Fraunces',serif; font-size:1.05rem; font-weight:600;
                        color:#1A3C23; margin-bottom:0.6rem; line-height:1.3;">{title}</div>
            <div style="font-size:0.82rem; color:rgba(26,60,35,0.45); line-height:1.7;
                        font-family:'Inter',sans-serif; font-weight:300;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:3.5rem 0;"></div>', unsafe_allow_html=True)

# ── TESTIMONIALS ──────────────────────────────────────
st.markdown('<div style="font-size:0.68rem; font-weight:500; letter-spacing:3px; text-transform:uppercase; color:rgba(26,60,35,0.35); margin-bottom:2rem; font-family:Inter,sans-serif;">What people say</div>', unsafe_allow_html=True)

testimonials = [
    ("Priya S.",  "Data Analyst → Data Scientist",  "I had no idea I was just 2 skills away from qualifying for senior DS roles. SkillLens showed me exactly what to learn next."),
    ("Arjun M.",  "Fresher → Backend Developer",    "The roadmap was more useful than any YouTube playlist. I got my first dev job 4 months after using it."),
    ("Sneha R.",  "MBA → Product Manager",           "Switching careers felt overwhelming until I saw my actual skill match. 68% on day one — way better than I expected."),
    ("Rahul T.",  "Student → ML Engineer",           "The market demand scores helped me prioritize. Didn't waste time on low-value certifications."),
]

cols = st.columns(4, gap="medium")
for col, (name, role_change, quote) in zip(cols, testimonials):
    with col:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.4); border:1px solid rgba(26,60,35,0.09);
                    border-radius:2px; padding:1.5rem; height:100%;">
            <div style="font-size:2rem; color:rgba(26,60,35,0.15); font-family:'Fraunces',serif;
                        margin-bottom:0.8rem; line-height:1;">"</div>
            <div style="font-size:0.85rem; color:rgba(26,60,35,0.6); line-height:1.75;
                        font-family:'Inter',sans-serif; font-weight:300; margin-bottom:1.5rem;
                        font-style:italic;">"{quote}"</div>
            <div style="border-top:1px solid rgba(26,60,35,0.08); padding-top:1rem;">
                <div style="font-family:'Fraunces',serif; font-weight:600; font-size:0.9rem;
                            color:#1A3C23; margin-bottom:0.2rem;">{name}</div>
                <div style="font-size:0.72rem; color:rgba(26,60,35,0.38); letter-spacing:0.5px;
                            font-family:'Inter',sans-serif;">{role_change}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:3.5rem 0;"></div>', unsafe_allow_html=True)

# ── TRENDING ──────────────────────────────────────────
col1, col2 = st.columns([0.4, 1.6], gap="large")
with col1:
    st.markdown("""
    <div style="padding-top:0.3rem;">
        <div style="font-size:0.68rem; font-weight:500; letter-spacing:3px; text-transform:uppercase;
                    color:rgba(26,60,35,0.35); margin-bottom:1rem; font-family:'Inter',sans-serif;">Hot skills</div>
        <div style="font-family:'Fraunces',serif; font-size:1.6rem; font-weight:600;
                    color:#1A3C23; line-height:1.25; margin-bottom:0.8rem;">
            What the<br>market wants
        </div>
        <div style="font-size:0.82rem; color:rgba(26,60,35,0.4); line-height:1.7;
                    font-family:'Inter',sans-serif; font-weight:300;">
            Skills appearing most in tech job listings right now.
        </div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    trending   = get_trending_skills()
    chips_html = "".join([
        f'<span style="background:transparent; color:#1A3C23; border:1px solid rgba(26,60,35,0.2); '
        f'padding:0.45rem 1rem; border-radius:2px; font-size:0.78rem; font-weight:400; '
        f'display:inline-block; margin:0.2rem; font-family:Inter,sans-serif;">{s}</span>'
        for s in trending
    ])
    st.markdown(f'<div style="padding-top:0.3rem; line-height:2.8;">{chips_html}</div>', unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:3.5rem 0;"></div>', unsafe_allow_html=True)

# ── ROLE INDEX ────────────────────────────────────────
st.markdown('<div style="font-size:0.68rem; font-weight:500; letter-spacing:3px; text-transform:uppercase; color:rgba(26,60,35,0.35); margin-bottom:2rem; font-family:Inter,sans-serif;">Role Index</div>', unsafe_allow_html=True)

roles   = get_all_roles()
preview = roles[:12]

for i, role in enumerate(preview):
    info       = get_role_info(role)
    diff       = info["difficulty"]
    diff_color = "#2A6B3A" if diff == "Beginner" else "#7A5C10" if diff == "Intermediate" else "#7A2A2A"
    border_top = "border-top:1px solid rgba(26,60,35,0.07);" if i > 0 else ""

    c1, c2, c3, c4 = st.columns([2.5, 1.2, 1, 1])
    with c1:
        st.markdown(f'<div style="padding:1rem 0; {border_top}"><span style="font-family:Fraunces,serif; font-weight:500; font-size:1rem; color:#1A3C23;">{role}</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div style="padding:1rem 0; {border_top}"><span style="font-size:0.82rem; color:rgba(26,60,35,0.5); font-family:Inter,sans-serif;">{info["salary"]}</span></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div style="padding:1rem 0; {border_top}"><span style="font-size:0.75rem; color:{diff_color}; font-family:Inter,sans-serif;">{diff}</span></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div style="padding:0.5rem 0; {border_top}">', unsafe_allow_html=True)
        if st.button("Analyze →", key=f"role_{i}", use_container_width=True):
            st.session_state.current_page = "Analyze"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────
st.markdown("""
<div style="margin-top:5rem; padding-top:2rem; border-top:1px solid rgba(26,60,35,0.08);
            display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
    <div style="font-family:'Fraunces',serif; font-style:italic; font-size:1.1rem;
                font-weight:400; color:rgba(26,60,35,0.4);">SkillLens</div>
    <div style="font-size:0.72rem; color:rgba(26,60,35,0.25); letter-spacing:1px;
                font-family:'Inter',sans-serif; text-transform:uppercase;">
        Free · Instant · No credit card
    </div>
</div>
""", unsafe_allow_html=True)