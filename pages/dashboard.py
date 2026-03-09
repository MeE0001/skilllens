import streamlit as st
import plotly.graph_objects as go
from modules.demand_score import get_demand_score, get_demand_emoji

# ── GUARD ─────────────────────────────────────────────
if "result" not in st.session_state or not st.session_state.result:
    st.markdown("""
    <div style="text-align:center; padding:5rem 2rem;">
        <div style="font-family:'Fraunces',serif; font-size:2rem; font-weight:300;
                    color:rgba(26,60,35,0.4); margin-bottom:1rem;">No analysis yet</div>
        <div style="font-size:0.85rem; color:rgba(26,60,35,0.35); font-family:'Inter',sans-serif;
                    margin-bottom:2rem;">Run an analysis first to see your dashboard.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Analyze →", type="primary"):
        st.session_state.current_page = "Analyze"
        st.rerun()
    st.stop()

result     = st.session_state.result
role       = st.session_state.get("role", "Unknown Role")
score      = result["score"]
matched    = result["matched"]
missing    = result["missing"]
readiness  = result["readiness"]
salary     = result.get("salary", "N/A")
difficulty = result.get("difficulty", "N/A")

score_color = "#2A6B3A" if score >= 70 else "#7A5C10" if score >= 40 else "#7A2A2A"
diff_color  = "#2A6B3A" if difficulty == "Beginner" else "#7A5C10" if difficulty == "Intermediate" else "#7A2A2A"

# ── HEADER ────────────────────────────────────────────
st.markdown(f"""
<div style="margin-bottom:2rem;">
    <div style="font-size:0.68rem; font-weight:500; letter-spacing:3px; text-transform:uppercase;
                color:rgba(26,60,35,0.35); margin-bottom:0.6rem; font-family:'Inter',sans-serif;">
        Dashboard
    </div>
    <div style="font-family:'Fraunces',serif; font-size:2.8rem; font-weight:300; color:#1A3C23;
                letter-spacing:-0.5px; line-height:1.1; margin-bottom:0.5rem;">
        Your results for <em style="font-weight:600;">{role}</em>
    </div>
</div>
<div style="height:1px; background:rgba(26,60,35,0.08); margin-bottom:2.5rem;"></div>
""", unsafe_allow_html=True)

# ── SCORE HERO ROW ────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns([1.8, 1, 1, 1, 1], gap="medium")

with c1:
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.45); border:1px solid rgba(26,60,35,0.1);
                border-radius:3px; padding:1.8rem 2rem;">
        <div style="font-size:0.6rem; letter-spacing:2px; text-transform:uppercase;
                    color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.5rem;">Match Score</div>
        <div style="font-family:'Fraunces',serif; font-size:4rem; font-weight:700;
                    color:{score_color}; line-height:1; letter-spacing:-2px;">{score}%</div>
        <div style="background:rgba(26,60,35,0.08); border-radius:2px; height:4px;
                    margin-top:1rem; width:100%;">
            <div style="background:{score_color}; width:{score}%; height:4px; border-radius:2px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

for val, lbl in [
    (len(matched), "Matched"),
    (len(missing), "Missing"),
    (salary,       "Avg Salary"),
    (readiness,    "Readiness"),
]:
    with [c2, c3, c4, c5][[len(matched), len(missing), salary, readiness].index(val)]:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.45); border:1px solid rgba(26,60,35,0.1);
                    border-radius:3px; padding:1.8rem 1.2rem; height:100%;">
            <div style="font-size:0.6rem; letter-spacing:2px; text-transform:uppercase;
                        color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.5rem;">{lbl}</div>
            <div style="font-family:'Fraunces',serif; font-size:1.8rem; font-weight:600;
                        color:#1A3C23; line-height:1;">{val}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2.5rem 0;"></div>', unsafe_allow_html=True)

# ── CHARTS ROW ────────────────────────────────────────
col_chart1, col_chart2 = st.columns([1, 1.4], gap="large")

with col_chart1:
    st.markdown('<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:1rem;">Coverage</div>', unsafe_allow_html=True)
    fig_donut = go.Figure(go.Pie(
        values=[len(matched), len(missing)],
        labels=["Matched", "Missing"],
        hole=0.72,
        marker=dict(colors=["#1A3C23", "rgba(26,60,35,0.1)"],
                    line=dict(color="#EDEADE", width=3)),
        textinfo="none",
        hovertemplate="%{label}: %{value}<extra></extra>"
    ))
    fig_donut.add_annotation(
        text=f"<b>{score}%</b>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=28, color="#1A3C23", family="Fraunces"),
        xanchor="center"
    )
    fig_donut.update_layout(
        showlegend=False, margin=dict(t=0, b=0, l=0, r=0),
        height=220, paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

with col_chart2:
    st.markdown('<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:1rem;">Skill Breakdown</div>', unsafe_allow_html=True)

    top_missing  = missing[:8]
    demand_scores = [get_demand_score(s) for s in top_missing]

    fig_bar = go.Figure(go.Bar(
        x=demand_scores,
        y=top_missing,
        orientation="h",
        marker=dict(
            color=["#1A3C23" if d >= 80 else "rgba(26,60,35,0.4)" if d >= 60 else "rgba(26,60,35,0.2)"
                   for d in demand_scores],
            line=dict(width=0)
        ),
        hovertemplate="%{y}: demand %{x}<extra></extra>"
    ))
    fig_bar.update_layout(
        xaxis=dict(showgrid=False, showticklabels=False, range=[0, 110],
                   zeroline=False),
        yaxis=dict(showgrid=False, tickfont=dict(family="Inter", size=11,
                   color="rgba(26,60,35,0.7)")),
        margin=dict(t=0, b=0, l=0, r=40),
        height=220,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2.5rem 0;"></div>', unsafe_allow_html=True)

# ── SKILLS DETAIL ─────────────────────────────────────
col_have, col_need = st.columns(2, gap="large")

with col_have:
    st.markdown('<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:1rem;">Skills You Have</div>', unsafe_allow_html=True)
    chips = "".join([
        f'<span style="background:rgba(42,107,58,0.09); color:#2A6B3A; '
        f'border:1px solid rgba(42,107,58,0.18); padding:0.35rem 0.9rem; border-radius:2px; '
        f'font-size:0.78rem; font-family:Inter,sans-serif; display:inline-block; margin:0.2rem;">{s}</span>'
        for s in matched
    ]) or '<span style="color:rgba(26,60,35,0.3); font-size:0.85rem; font-family:Inter,sans-serif;">None matched</span>'
    st.markdown(f'<div style="line-height:2.4;">{chips}</div>', unsafe_allow_html=True)

with col_need:
    st.markdown('<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:1rem;">Skills to Acquire</div>', unsafe_allow_html=True)
    chips = "".join([
        f'<span style="background:rgba(122,42,42,0.06); color:#7A2A2A; '
        f'border:1px solid rgba(122,42,42,0.14); padding:0.35rem 0.9rem; border-radius:2px; '
        f'font-size:0.78rem; font-family:Inter,sans-serif; display:inline-block; margin:0.2rem;">{s}</span>'
        for s in missing
    ]) or '<span style="color:rgba(26,60,35,0.3); font-size:0.85rem; font-family:Inter,sans-serif;">Nothing missing — perfect score!</span>'
    st.markdown(f'<div style="line-height:2.4;">{chips}</div>', unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2.5rem 0;"></div>', unsafe_allow_html=True)

# ── DEMAND CARDS ──────────────────────────────────────
if missing:
    st.markdown('<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:1.5rem;">Market Demand for Missing Skills</div>', unsafe_allow_html=True)

    cols = st.columns(4, gap="medium")
    for i, skill in enumerate(missing[:8]):
        d     = get_demand_score(skill)
        emoji = get_demand_emoji(skill)
        bar_c = "#1A3C23" if d >= 80 else "rgba(26,60,35,0.4)" if d >= 60 else "rgba(26,60,35,0.2)"
        with cols[i % 4]:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.4); border:1px solid rgba(26,60,35,0.09);
                        border-radius:3px; padding:1.2rem; margin-bottom:0.7rem;">
                <div style="font-size:1.2rem; margin-bottom:0.5rem;">{emoji}</div>
                <div style="font-family:'Fraunces',serif; font-weight:600; font-size:0.9rem;
                            color:#1A3C23; margin-bottom:0.5rem;">{skill}</div>
                <div style="background:rgba(26,60,35,0.08); border-radius:2px; height:3px; margin-bottom:0.4rem;">
                    <div style="background:{bar_c}; width:{d}%; height:3px; border-radius:2px;"></div>
                </div>
                <div style="font-size:0.7rem; color:rgba(26,60,35,0.4); font-family:Inter,sans-serif;">
                    {d}/100 demand
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2.5rem 0;"></div>', unsafe_allow_html=True)

# ── CTA ───────────────────────────────────────────────
c1, c2, c3 = st.columns(3, gap="medium")
with c1:
    if st.button("View Roadmap →", type="primary", use_container_width=True):
        st.session_state.current_page = "Roadmap"
        st.rerun()
with c2:
    if st.button("Save Report", use_container_width=True):
        st.session_state.current_page = "Reports"
        st.rerun()
with c3:
    if st.button("New Analysis", use_container_width=True):
        st.session_state.current_page = "Analyze"
        st.rerun()