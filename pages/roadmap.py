import streamlit as st
from modules.roadmap_generator import generate_roadmap

# ── GUARD ─────────────────────────────────────────────
if "result" not in st.session_state or not st.session_state.result:
    st.markdown("""
    <div style="text-align:center; padding:5rem 2rem;">
        <div style="font-family:'Fraunces',serif; font-size:2rem; font-weight:300;
                    color:rgba(26,60,35,0.4); margin-bottom:1rem;">No roadmap yet</div>
        <div style="font-size:0.85rem; color:rgba(26,60,35,0.35); font-family:'Inter',sans-serif;
                    margin-bottom:2rem;">Complete an analysis to generate your learning roadmap.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Analyze →", type="primary"):
        st.session_state.current_page = "Analyze"
        st.rerun()
    st.stop()

result  = st.session_state.result
role    = st.session_state.get("role", "Unknown Role")
missing = result["missing"]
roadmap = generate_roadmap(missing)

high   = [s for s in roadmap if s["priority"] == "High"]
medium = [s for s in roadmap if s["priority"] == "Medium"]
low    = [s for s in roadmap if s["priority"] == "Low"]

# ── HEADER ────────────────────────────────────────────
st.markdown(f"""
<div style="margin-bottom:2rem;">
    <div style="font-size:0.68rem; font-weight:500; letter-spacing:3px; text-transform:uppercase;
                color:rgba(26,60,35,0.35); margin-bottom:0.6rem; font-family:'Inter',sans-serif;">
        Learning Roadmap
    </div>
    <div style="font-family:'Fraunces',serif; font-size:2.8rem; font-weight:300; color:#1A3C23;
                letter-spacing:-0.5px; line-height:1.1; margin-bottom:0.5rem;">
        Your path to <em style="font-weight:600;">{role}</em>
    </div>
    <div style="font-size:0.85rem; color:rgba(26,60,35,0.45); font-family:'Inter',sans-serif;
                font-weight:300; line-height:1.7;">
        {len(roadmap)} skills to learn · prioritized by market demand and difficulty.
    </div>
</div>
<div style="height:1px; background:rgba(26,60,35,0.08); margin-bottom:2.5rem;"></div>
""", unsafe_allow_html=True)

# ── SUMMARY STATS ─────────────────────────────────────
c1, c2, c3, c4 = st.columns(4, gap="medium")
for col, val, lbl in [
    (c1, len(roadmap), "Total Skills"),
    (c2, len(high),    "High Priority"),
    (c3, len(medium),  "Medium Priority"),
    (c4, len(low),     "Low Priority"),
]:
    with col:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.45); border:1px solid rgba(26,60,35,0.1);
                    border-radius:3px; padding:1.2rem 1.5rem;">
            <div style="font-family:'Fraunces',serif; font-size:2rem; font-weight:600;
                        color:#1A3C23; line-height:1;">{val}</div>
            <div style="font-size:0.62rem; color:rgba(26,60,35,0.38); letter-spacing:1.5px;
                        text-transform:uppercase; font-family:Inter,sans-serif; margin-top:0.4rem;">{lbl}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2.5rem 0;"></div>', unsafe_allow_html=True)

# ── ROADMAP STEPS ─────────────────────────────────────
priority_config = {
    "High":   {"color": "#7A2A2A", "bg": "rgba(122,42,42,0.06)",  "border": "rgba(122,42,42,0.15)",  "label": "Start Here"},
    "Medium": {"color": "#7A5C10", "bg": "rgba(122,92,16,0.06)",  "border": "rgba(122,92,16,0.15)",  "label": "Then Learn"},
    "Low":    {"color": "#2A6B3A", "bg": "rgba(42,107,58,0.06)",  "border": "rgba(42,107,58,0.15)",  "label": "Nice to Have"},
}

for group_label, group in [("High Priority", high), ("Medium Priority", medium), ("Low Priority", low)]:
    if not group:
        continue

    priority = group[0]["priority"]
    cfg      = priority_config[priority]

    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:1rem; margin-bottom:1.5rem;">
        <span style="background:{cfg['bg']}; color:{cfg['color']}; border:1px solid {cfg['border']};
                     padding:0.3rem 0.9rem; border-radius:2px; font-size:0.68rem; font-weight:500;
                     letter-spacing:1px; text-transform:uppercase; font-family:Inter,sans-serif;">
            {cfg['label']}
        </span>
        <div style="flex:1; height:1px; background:rgba(26,60,35,0.07);"></div>
        <span style="font-size:0.68rem; color:rgba(26,60,35,0.3); font-family:Inter,sans-serif;">
            {len(group)} skills
        </span>
    </div>
    """, unsafe_allow_html=True)

    for i, step in enumerate(group):
        border_top = "border-top:1px solid rgba(26,60,35,0.07);" if i > 0 else ""
        resources_html = "".join([
            f'<a href="{url}" target="_blank" style="color:#1A3C23; font-size:0.78rem; '
            f'font-family:Inter,sans-serif; text-decoration:none; border-bottom:1px solid rgba(26,60,35,0.2); '
            f'padding-bottom:1px; margin-right:1.2rem; display:inline-block; margin-bottom:0.3rem;">'
            f'↗ {name}</a>'
            for name, url in step.get("resources", [])[:3]
        ])

        col1, col2, col3 = st.columns([0.25, 2.5, 1.5], gap="medium")
        with col1:
            st.markdown(f'<div style="padding:1.3rem 0; {border_top} text-align:center;"><span style="font-family:Fraunces,serif; font-size:0.9rem; color:rgba(26,60,35,0.25);">{i+1:02d}</span></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="padding:1.3rem 0; {border_top}">
                <div style="font-family:'Fraunces',serif; font-weight:600; font-size:1rem;
                            color:#1A3C23; margin-bottom:0.6rem;">{step['skill']}</div>
                <div style="font-size:0.82rem; color:rgba(26,60,35,0.45); font-family:Inter,sans-serif;
                            line-height:1.6; margin-bottom:0.8rem;">
                    {step.get('time_estimate', '')} to learn · {step.get('difficulty', '')} difficulty
                </div>
                <div>{resources_html}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            time_val = step.get("time_estimate", "")
            st.markdown(f"""
            <div style="padding:1.3rem 0; {border_top} text-align:right;">
                <div style="font-family:'Fraunces',serif; font-size:1.2rem; font-weight:600;
                            color:#1A3C23;">{time_val}</div>
                <div style="font-size:0.62rem; color:rgba(26,60,35,0.3); letter-spacing:1px;
                            text-transform:uppercase; font-family:Inter,sans-serif;">est. time</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="margin-bottom:2rem;"></div>', unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:1rem 0 2.5rem;"></div>', unsafe_allow_html=True)

# ── CTA ───────────────────────────────────────────────
c1, c2 = st.columns(2)
with c1:
    if st.button("Save This Report →", type="primary", use_container_width=True):
        st.session_state.current_page = "Reports"
        st.rerun()
with c2:
    if st.button("Back to Dashboard", use_container_width=True):
        st.session_state.current_page = "Dashboard"
        st.rerun()