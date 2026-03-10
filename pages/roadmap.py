import streamlit as st
import streamlit.components.v1 as components
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

def weeks_from_time(t):
    if not t: return 2
    t = t.lower()
    if "week" in t:
        try: return int(''.join(filter(str.isdigit, t.split("week")[0].strip().split()[-1])))
        except: return 2
    if "month" in t:
        try: return int(''.join(filter(str.isdigit, t.split("month")[0].strip().split()[-1]))) * 4
        except: return 4
    return 2

total_weeks  = sum(weeks_from_time(s.get("time_estimate", "")) for s in roadmap)
total_months = round(total_weeks / 4, 1)
role_short   = role.split()[0]

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
    <div style="font-size:0.88rem; color:rgba(26,60,35,0.45); font-family:'Inter',sans-serif; font-weight:300;">
        {len(roadmap)} skills to learn &middot; estimated {total_months} months to job-ready
    </div>
</div>
<div style="height:1px; background:rgba(26,60,35,0.08); margin-bottom:2.5rem;"></div>
""", unsafe_allow_html=True)

# ── SUMMARY STATS ─────────────────────────────────────
c1, c2, c3, c4 = st.columns(4, gap="medium")
for col, val, lbl, accent in [
    (c1, len(roadmap),  "Total Skills",    "#1A3C23"),
    (c2, len(high),     "High Priority",   "#7A2A2A"),
    (c3, len(medium),   "Medium Priority", "#7A5C10"),
    (c4, len(low),      "Low Priority",    "#2A6B3A"),
]:
    with col:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.5); border:1px solid rgba(26,60,35,0.1);
                    border-radius:3px; padding:1.3rem 1.5rem; border-top:3px solid {accent};">
            <div style="font-family:'Fraunces',serif; font-size:2.2rem; font-weight:700;
                        color:{accent}; line-height:1;">{val}</div>
            <div style="font-size:0.6rem; color:rgba(26,60,35,0.38); letter-spacing:1.5px;
                        text-transform:uppercase; font-family:Inter,sans-serif; margin-top:0.4rem;">{lbl}</div>
        </div>
        """, unsafe_allow_html=True)

# ── PHASE PROGRESS BAR ────────────────────────────────
st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2.5rem 0 2rem;"></div>', unsafe_allow_html=True)

total   = max(len(roadmap), 1)
high_w  = round(len(high)   / total * 100)
med_w   = round(len(medium) / total * 100)
low_w   = 100 - high_w - med_w

components.html("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<div style="font-family:Inter,sans-serif; padding:0 0 0.5rem;">
    <div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase;
                color:rgba(26,60,35,0.35); margin-bottom:0.9rem;">Your 3-Phase Journey</div>
    <div style="display:flex; border-radius:3px; overflow:hidden; height:12px; gap:3px;">
        <div style="width:""" + str(high_w) + """%; background:#7A2A2A; border-radius:2px 0 0 2px; transition:width 0.5s;"></div>
        <div style="width:""" + str(med_w)  + """%; background:#B8860B; transition:width 0.5s;"></div>
        <div style="width:""" + str(low_w)  + """%; background:#2A6B3A; border-radius:0 2px 2px 0; transition:width 0.5s;"></div>
    </div>
    <div style="display:flex; gap:2rem; margin-top:0.8rem; flex-wrap:wrap;">
        <div style="display:flex; align-items:center; gap:0.5rem;">
            <div style="width:10px; height:10px; background:#7A2A2A; border-radius:2px;"></div>
            <span style="font-size:0.72rem; color:rgba(26,60,35,0.5);">Phase 1 · Critical (""" + str(len(high)) + """ skills)</span>
        </div>
        <div style="display:flex; align-items:center; gap:0.5rem;">
            <div style="width:10px; height:10px; background:#B8860B; border-radius:2px;"></div>
            <span style="font-size:0.72rem; color:rgba(26,60,35,0.5);">Phase 2 · Core (""" + str(len(medium)) + """ skills)</span>
        </div>
        <div style="display:flex; align-items:center; gap:0.5rem;">
            <div style="width:10px; height:10px; background:#2A6B3A; border-radius:2px;"></div>
            <span style="font-size:0.72rem; color:rgba(26,60,35,0.5);">Phase 3 · Polish (""" + str(len(low)) + """ skills)</span>
        </div>
    </div>
</div>
""", height=85)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:1.5rem 0 2.5rem;"></div>', unsafe_allow_html=True)

# ── ROADMAP SECTIONS ──────────────────────────────────
PHASES = [
    ("High",   high,   "Phase 1 — Start Here",    "01", "#7A2A2A", "rgba(122,42,42,0.05)", "rgba(122,42,42,0.12)", "These skills have the highest market demand. Learn them first."),
    ("Medium", medium, "Phase 2 — Then Learn",     "02", "#7A5C10", "rgba(122,92,16,0.05)", "rgba(122,92,16,0.12)", "Core competencies that round out your profile."),
    ("Low",    low,    "Phase 3 — Nice to Have",   "03", "#2A6B3A", "rgba(42,107,58,0.05)", "rgba(42,107,58,0.12)", "Bonus skills that make you stand out from candidates."),
]

for priority, group, phase_label, phase_num, color, bg, border_c, desc in PHASES:
    if not group:
        continue

    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:1.2rem; margin-bottom:0.6rem;">
        <div style="background:{bg}; border:1px solid {border_c}; border-radius:3px;
                    padding:0.45rem 1rem; display:flex; align-items:center; gap:0.7rem;">
            <span style="font-family:'Fraunces',serif; font-size:0.72rem; font-weight:700;
                         color:{color}; opacity:0.45;">{phase_num}</span>
            <span style="font-size:0.68rem; font-weight:600; letter-spacing:1px; text-transform:uppercase;
                         font-family:Inter,sans-serif; color:{color};">{phase_label}</span>
        </div>
        <div style="flex:1; height:1px; background:rgba(26,60,35,0.07);"></div>
        <span style="font-size:0.68rem; color:rgba(26,60,35,0.3); font-family:Inter,sans-serif;">
            {len(group)} skill{"s" if len(group) != 1 else ""}
        </span>
    </div>
    <div style="font-size:0.8rem; color:rgba(26,60,35,0.4); font-family:Inter,sans-serif;
                margin-bottom:1.5rem;">{desc}</div>
    """, unsafe_allow_html=True)

    # Build all skill rows as a single components.html block
    rows_html = """
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,600;0,700&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
    <div style="font-family:Inter,sans-serif;">
    """

    for i, step in enumerate(group):
        skill     = step["skill"]
        time_val  = step.get("time_estimate", "2–4 weeks")
        diff      = step.get("difficulty", "Intermediate")
        resources = step.get("resources", [])[:3]

        diff_color = "#7A2A2A" if diff == "Advanced" else "#7A5C10" if diff == "Intermediate" else "#2A6B3A"
        diff_bg    = "rgba(122,42,42,0.08)" if diff == "Advanced" else "rgba(122,92,16,0.08)" if diff == "Intermediate" else "rgba(42,107,58,0.08)"
        border_top = "border-top:1px solid rgba(26,60,35,0.07);" if i > 0 else ""

        res_html = ""
        for name, url in resources:
            res_html += (
                '<a href="' + url + '" target="_blank" style="color:#1A3C23; font-size:0.74rem; '
                'text-decoration:none; border-bottom:1px solid rgba(26,60,35,0.2); '
                'padding-bottom:1px; margin-right:1rem; display:inline-block; margin-bottom:0.3rem;">'
                '&#8599; ' + name + '</a>'
            )

        rows_html += (
            '<div style="display:grid; grid-template-columns:2.2rem 1fr 90px; '
            'gap:1rem; align-items:start; padding:1.3rem 0.2rem; ' + border_top + '">'

            # Step number
            '<div style="padding-top:0.1rem; text-align:center;">'
            '<span style="font-family:Fraunces,serif; font-size:0.85rem; font-weight:700; '
            'color:' + color + '; opacity:0.4;">' + f"{i+1:02d}" + '</span>'
            '</div>'

            # Skill info
            '<div>'
            '<div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.45rem; flex-wrap:wrap;">'
            '<span style="font-family:Fraunces,serif; font-weight:600; font-size:1rem; color:#1A3C23;">' + skill + '</span>'
            '<span style="background:' + diff_bg + '; color:' + diff_color + '; font-size:0.57rem; '
            'letter-spacing:1px; text-transform:uppercase; font-weight:600; '
            'padding:0.18rem 0.55rem; border-radius:2px;">' + diff + '</span>'
            '</div>'
            '<div style="font-size:0.78rem; color:rgba(26,60,35,0.42); margin-bottom:0.65rem; line-height:1.5;">'
            'Essential skill for ' + role_short + ' roles — prioritised by hiring demand.'
            '</div>'
            '<div>' + res_html + '</div>'
            '</div>'

            # Time estimate
            '<div style="text-align:right; padding-top:0.05rem;">'
            '<div style="font-family:Fraunces,serif; font-size:1.1rem; font-weight:700; '
            'color:#1A3C23; line-height:1.2;">' + time_val + '</div>'
            '<div style="font-size:0.57rem; color:rgba(26,60,35,0.3); letter-spacing:1px; '
            'text-transform:uppercase; margin-top:0.2rem;">est. time</div>'
            '</div>'

            '</div>'
        )

    rows_html += "</div>"

    card_height = len(group) * 115 + 30
    components.html(rows_html, height=card_height, scrolling=False)

    st.markdown('<div style="margin-bottom:2.5rem;"></div>', unsafe_allow_html=True)

# ── TOTAL TIME BANNER ─────────────────────────────────
st.markdown(f"""
<div style="background:#1A3C23; border-radius:3px; padding:1.8rem 2.5rem;
            display:flex; justify-content:space-between; align-items:center;
            flex-wrap:wrap; gap:1rem; margin-bottom:2.5rem;">
    <div>
        <div style="font-size:0.62rem; letter-spacing:2px; text-transform:uppercase;
                    color:rgba(237,234,222,0.4); font-family:Inter,sans-serif; margin-bottom:0.4rem;">
            Total Estimated Time
        </div>
        <div style="font-family:'Fraunces',serif; font-size:1.45rem; font-weight:600;
                    color:#EDEADE; line-height:1.3;">
            ~{total_months} months to become job-ready as<br>
            <em style="font-weight:300;">{role}</em>
        </div>
    </div>
    <div style="text-align:right;">
        <div style="font-family:'Fraunces',serif; font-size:3rem; font-weight:700;
                    color:#EDEADE; line-height:1;">{total_weeks}</div>
        <div style="font-size:0.6rem; color:rgba(237,234,222,0.4); letter-spacing:1.5px;
                    text-transform:uppercase; font-family:Inter,sans-serif;">total weeks</div>
    </div>
</div>
""", unsafe_allow_html=True)

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