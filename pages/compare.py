import streamlit as st
import plotly.graph_objects as go
from modules.skill_analyzer import get_all_roles, get_role_info

# ── HEADER ────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:2rem;">
    <div style="font-size:0.68rem; font-weight:500; letter-spacing:3px; text-transform:uppercase;
                color:rgba(26,60,35,0.35); margin-bottom:0.6rem; font-family:'Inter',sans-serif;">
        Compare
    </div>
    <div style="font-family:'Fraunces',serif; font-size:2.8rem; font-weight:300; color:#1A3C23;
                letter-spacing:-0.5px; line-height:1.1; margin-bottom:0.5rem;">
        Side-by-side <em style="font-weight:600;">role comparison</em>
    </div>
    <div style="font-size:0.85rem; color:rgba(26,60,35,0.45); font-family:'Inter',sans-serif; font-weight:300;">
        Pick two roles and see how they stack up — skills, salary, difficulty, overlap and your personal fit.
    </div>
</div>
<div style="height:1px; background:rgba(26,60,35,0.08); margin-bottom:2.5rem;"></div>
""", unsafe_allow_html=True)

roles = get_all_roles()

col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown('<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.4rem;">Role A</div>', unsafe_allow_html=True)
    role_a = st.selectbox("Role A", roles, index=0, label_visibility="collapsed", key="cmp_a")
with col2:
    st.markdown('<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.4rem;">Role B</div>', unsafe_allow_html=True)
    role_b = st.selectbox("Role B", roles, index=1, label_visibility="collapsed", key="cmp_b")

if role_a == role_b:
    st.markdown("""
    <div style="background:rgba(122,92,16,0.07); border:1px solid rgba(122,92,16,0.18);
                border-radius:3px; padding:1rem 1.5rem; margin-top:1rem;">
        <span style="font-size:0.85rem; color:#7A5C10; font-family:Inter,sans-serif;">
            Please select two different roles to compare.
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

info_a   = get_role_info(role_a)
info_b   = get_role_info(role_b)
skills_a = set(info_a["required_skills"])
skills_b = set(info_b["required_skills"])
only_a   = sorted(skills_a - skills_b)
only_b   = sorted(skills_b - skills_a)
common   = sorted(skills_a & skills_b)

# ── HELPERS ───────────────────────────────────────────
def salary_to_num(s):
    import re
    nums = re.findall(r"[\d.]+", str(s))
    return float(nums[0]) if nums else 0

def difficulty_weeks(d):
    return {"Beginner": 8, "Intermediate": 20, "Advanced": 36}.get(d, 20)

# ── PERSONALISATION ───────────────────────────────────
user_skills = set()
if "user_skills" in st.session_state:
    user_skills = set(s.strip().lower() for s in st.session_state.user_skills)

def match_score(role_skills):
    if not role_skills: return 0
    matched = sum(1 for s in role_skills if s.lower() in user_skills)
    return round(matched / len(role_skills) * 100)

def gap_skills(role_skills):
    return [s for s in role_skills if s.lower() not in user_skills]

def time_to_ready(role_skills, difficulty):
    missing = len(gap_skills(role_skills))
    base    = difficulty_weeks(difficulty)
    return max(2, round(base * (missing / max(len(role_skills), 1))))

score_a     = match_score(info_a["required_skills"]) if user_skills else None
score_b     = match_score(info_b["required_skills"]) if user_skills else None
missing_a   = gap_skills(info_a["required_skills"])
missing_b   = gap_skills(info_b["required_skills"])
weeks_a     = time_to_ready(info_a["required_skills"], info_a["difficulty"])
weeks_b     = time_to_ready(info_b["required_skills"], info_b["difficulty"])
overlap_pct = round(len(common) / max(len(skills_a | skills_b), 1) * 100)
sal_a       = salary_to_num(info_a["salary"])
sal_b       = salary_to_num(info_b["salary"])

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2rem 0;"></div>', unsafe_allow_html=True)

# ── OVERVIEW CARDS ────────────────────────────────────
col_a, col_vs, col_b = st.columns([1, 0.15, 1], gap="small")

def render_card(col, role, info, score, weeks, miss):
    diff        = info["difficulty"]
    diff_color  = "#2A6B3A" if diff == "Beginner" else "#7A5C10" if diff == "Intermediate" else "#7A2A2A"
    score_color = "#2A6B3A" if (score or 0) >= 70 else "#7A5C10" if (score or 0) >= 40 else "#7A2A2A"

    def row(label, value, color="#1A3C23", size="1rem", weight="600", border=True):
        border_style = "border-bottom:1px solid rgba(26,60,35,0.07); padding-bottom:0.8rem;" if border else ""
        return f"""
        <div style="display:flex; justify-content:space-between; align-items:center; {border_style}">
            <span style="font-size:0.7rem; color:rgba(26,60,35,0.4); font-family:Inter,sans-serif;
                         letter-spacing:1px; text-transform:uppercase;">{label}</span>
            <span style="font-family:'Fraunces',serif; font-weight:{weight};
                         color:{color}; font-size:{size};">{value}</span>
        </div>"""

    with col:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.45); border:1px solid rgba(26,60,35,0.1);
                    border-radius:3px; padding:2rem;">
            <div style="font-family:'Fraunces',serif; font-size:1.4rem; font-weight:600;
                        color:#1A3C23; margin-bottom:1.5rem; line-height:1.2;">{role}</div>
            <div style="display:flex; flex-direction:column; gap:0.8rem;">
                {row("Your Match", f"{score}%", score_color, "1.3rem", "700") if user_skills else ""}
                {row("Skills to Learn", len(miss), "#7A2A2A") if user_skills else ""}
                {row("Time to Ready", f"~{weeks} wks") if user_skills else ""}
                {row("Salary", info['salary'])}
                {row("Difficulty", diff, diff_color)}
                {row("Total Skills", len(info['required_skills']), border=False)}
            </div>
        </div>
        """, unsafe_allow_html=True)

for col, role, info, score, weeks, miss in [
    (col_a, role_a, info_a, score_a, weeks_a, missing_a),
    (col_b, role_b, info_b, score_b, weeks_b, missing_b),
]:
    render_card(col, role, info, score, weeks, miss)

with col_vs:
    st.markdown("""
    <div style="display:flex; align-items:center; justify-content:center; height:100%; padding-top:5rem;">
        <div style="font-family:'Fraunces',serif; font-size:1rem; color:rgba(26,60,35,0.2);
                    font-style:italic; writing-mode:vertical-rl;">vs</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2.5rem 0;"></div>', unsafe_allow_html=True)

# ── CAREER TRANSITION RECOMMENDATION ─────────────────
if user_skills:
    better_role  = role_a if (score_a or 0) >= (score_b or 0) else role_b
    other_role   = role_b if better_role == role_a else role_a
    better_score = max(score_a or 0, score_b or 0)
    other_weeks  = weeks_b if better_role == role_a else weeks_a
    other_miss   = len(missing_b) if better_role == role_a else len(missing_a)

    st.markdown(f"""
    <div style="background:rgba(42,107,58,0.06); border:1px solid rgba(42,107,58,0.15);
                border-left:3px solid #2A6B3A; border-radius:3px; padding:1.8rem 2rem; margin-bottom:2.5rem;">
        <div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase;
                    color:rgba(26,60,35,0.4); font-family:Inter,sans-serif; margin-bottom:0.8rem;">
            Career Transition Recommendation
        </div>
        <div style="font-family:'Fraunces',serif; font-size:1.3rem; font-weight:600;
                    color:#1A3C23; margin-bottom:0.6rem;">
            You're closer to <em>{better_role}</em> — {better_score}% match
        </div>
        <div style="font-size:0.85rem; color:rgba(26,60,35,0.55); font-family:Inter,sans-serif; line-height:1.7;">
            Based on your current skills, <strong>{better_role}</strong> requires less upskilling.
            <strong>{other_role}</strong> needs {other_miss} more skills (~{other_weeks} weeks of learning).
            Consider transitioning via <strong>{better_role}</strong> first to build experience,
            then pivot to <strong>{other_role}</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)

elif not user_skills:
    st.markdown("""
    <div style="background:rgba(26,60,35,0.04); border:1px solid rgba(26,60,35,0.1);
                border-radius:3px; padding:1rem 1.5rem; margin-bottom:2rem;">
        <span style="font-size:0.82rem; color:rgba(26,60,35,0.5); font-family:Inter,sans-serif;">
            💡 Run an analysis on the <strong>Analyze</strong> page first to unlock personalised match scores,
            time-to-ready estimates and transition recommendations.
        </span>
    </div>
    """, unsafe_allow_html=True)

# ── OVERLAP SCORE ─────────────────────────────────────
st.markdown('<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:1.2rem;">Skill Overlap</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="medium")
for col, val, lbl, sub in [
    (c1, f"{overlap_pct}%", "Overlap Score",       f"{len(common)} skills shared"),
    (c2, str(len(only_a)),  f"Unique to {role_a[:14]}", "not in other role"),
    (c3, str(len(only_b)),  f"Unique to {role_b[:14]}", "not in other role"),
]:
    with col:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.45); border:1px solid rgba(26,60,35,0.1);
                    border-radius:3px; padding:1.2rem 1.5rem; text-align:center; margin-bottom:1.5rem;">
            <div style="font-family:'Fraunces',serif; font-size:2.2rem; font-weight:700;
                        color:#1A3C23; line-height:1;">{val}</div>
            <div style="font-size:0.65rem; color:rgba(26,60,35,0.4); letter-spacing:1.5px;
                        text-transform:uppercase; font-family:Inter,sans-serif; margin-top:0.4rem;">{lbl}</div>
            <div style="font-size:0.75rem; color:rgba(26,60,35,0.3); font-family:Inter,sans-serif;
                        margin-top:0.2rem;">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:0.5rem 0 2.5rem;"></div>', unsafe_allow_html=True)

# ── CHARTS ROW ───────────────────────────────────────
chart_cols = st.columns(2, gap="large") if user_skills else st.columns(1)

# Salary chart
with chart_cols[0]:
    st.markdown('<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.8rem;">Salary Comparison</div>', unsafe_allow_html=True)
    fig_sal = go.Figure()
    fig_sal.add_trace(go.Bar(
        x=[role_a, role_b],
        y=[sal_a, sal_b],
        marker_color=["#1A3C23", "rgba(26,60,35,0.45)"],
        width=0.45,
        text=[info_a["salary"], info_b["salary"]],
        textposition="outside",
        textfont=dict(family="Fraunces", size=13, color="#1A3C23"),
    ))
    fig_sal.update_layout(
        height=240, showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=30, b=0, l=0, r=0),
        xaxis=dict(showgrid=False, tickfont=dict(family="Inter", size=11, color="rgba(26,60,35,0.6)")),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
    )
    st.plotly_chart(fig_sal, use_container_width=True, config={"displayModeBar": False})

# Time to ready chart (only if personalised)
if user_skills:
    with chart_cols[1]:
        st.markdown('<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.8rem;">Time to Ready — Your Skills</div>', unsafe_allow_html=True)
        fig_time = go.Figure()
        fig_time.add_trace(go.Bar(
            x=[role_a, role_b],
            y=[weeks_a, weeks_b],
            marker_color=["#1A3C23", "rgba(26,60,35,0.45)"],
            width=0.45,
            text=[f"~{weeks_a} wks", f"~{weeks_b} wks"],
            textposition="outside",
            textfont=dict(family="Fraunces", size=13, color="#1A3C23"),
        ))
        fig_time.update_layout(
            height=240, showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=30, b=0, l=0, r=0),
            xaxis=dict(showgrid=False, tickfont=dict(family="Inter", size=11, color="rgba(26,60,35,0.6)")),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        )
        st.plotly_chart(fig_time, use_container_width=True, config={"displayModeBar": False})

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2.5rem 0;"></div>', unsafe_allow_html=True)

# ── SKILL BREAKDOWN ───────────────────────────────────
st.markdown('<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:1.5rem;">Skill Breakdown</div>', unsafe_allow_html=True)

def chips_html(skills, bg, color, border):
    if not skills:
        return '<span style="font-size:0.82rem; color:rgba(26,60,35,0.3); font-family:Inter,sans-serif;">None</span>'
    parts = []
    for s in skills:
        has_it  = s.lower() in user_skills
        opacity = "0.35" if has_it else "1"
        tick    = " ✓" if has_it else ""
        parts.append(
            f'<span style="background:{bg}; color:{color}; border:1px solid {border}; '
            f'padding:0.3rem 0.8rem; border-radius:2px; font-size:0.75rem; '
            f'font-family:Inter,sans-serif; display:inline-block; margin:0.2rem; '
            f'opacity:{opacity};">{s}{tick}</span>'
        )
    return "".join(parts)

c1, c2, c3 = st.columns(3, gap="large")
with c1:
    st.markdown(f'<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.8rem;">Only in {role_a} ({len(only_a)})</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="line-height:2.4;">{chips_html(only_a, "rgba(26,60,35,0.07)", "#1A3C23", "rgba(26,60,35,0.18)")}</div>', unsafe_allow_html=True)

with c2:
    st.markdown(f'<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.8rem;">Shared ({len(common)})</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="line-height:2.4;">{chips_html(common, "rgba(42,107,58,0.08)", "#2A6B3A", "rgba(42,107,58,0.18)")}</div>', unsafe_allow_html=True)

with c3:
    st.markdown(f'<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.8rem;">Only in {role_b} ({len(only_b)})</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="line-height:2.4;">{chips_html(only_b, "rgba(26,60,35,0.04)", "rgba(26,60,35,0.55)", "rgba(26,60,35,0.12)")}</div>', unsafe_allow_html=True)

if user_skills:
    st.markdown("""
    <div style="margin-top:1rem;">
        <span style="font-size:0.72rem; color:rgba(26,60,35,0.3); font-family:Inter,sans-serif;">
            ✓ faded = you already have this skill
        </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2.5rem 0;"></div>', unsafe_allow_html=True)

# ── CTA ───────────────────────────────────────────────
c1, c2 = st.columns(2)
with c1:
    if st.button(f"Analyze for {role_a} →", type="primary", use_container_width=True):
        st.session_state.current_page = "Analyze"
        st.rerun()
with c2:
    if st.button(f"Analyze for {role_b}", use_container_width=True):
        st.session_state.current_page = "Analyze"
        st.rerun()