import streamlit as st
import streamlit.components.v1 as components
from database.supabase_client import save_report, get_reports, delete_report, sign_out

user_id   = st.session_state.get("user_id")
user_name = st.session_state.get("user_name", "")
result    = st.session_state.get("result")
role      = st.session_state.get("role")

# ── HEADER ────────────────────────────────────────────
col_h, col_logout = st.columns([3, 1])
with col_h:
    st.markdown(f"""
    <div style="margin-bottom:2rem;">
        <div style="font-size:0.68rem; font-weight:500; letter-spacing:3px; text-transform:uppercase;
                    color:rgba(26,60,35,0.35); margin-bottom:0.6rem; font-family:'Inter',sans-serif;">
            Reports
        </div>
        <div style="font-family:'Fraunces',serif; font-size:2.8rem; font-weight:300; color:#1A3C23;
                    letter-spacing:-0.5px; line-height:1.1;">
            Your saved <em style="font-weight:600;">analyses</em>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col_logout:
    st.markdown('<div style="padding-top:1.5rem;">', unsafe_allow_html=True)
    if st.button("Sign Out", use_container_width=True):
        sign_out()
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin-bottom:2.5rem;"></div>', unsafe_allow_html=True)

# ── SAVE CURRENT REPORT ───────────────────────────────
if result and role:
    st.markdown('<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:1rem;">Save Current Analysis</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.45); border:1px solid rgba(26,60,35,0.1);
                border-radius:3px; padding:1.5rem 2rem; margin-bottom:1rem;">
        <div style="display:flex; gap:2rem; align-items:center; flex-wrap:wrap;">
            <div>
                <div style="font-family:'Fraunces',serif; font-weight:600; font-size:1.1rem;
                            color:#1A3C23; margin-bottom:0.3rem;">{role}</div>
                <div style="font-size:0.82rem; color:rgba(26,60,35,0.45); font-family:Inter,sans-serif;">
                    Score: {result['score']}% · {len(result['matched'])} matched · {len(result['missing'])} missing
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_name, col_save = st.columns([3, 1])
    with col_name:
        report_name = st.text_input(
            "Report name",
            value=f"{role} Analysis",
            label_visibility="collapsed",
            placeholder="Give this report a name..."
        )
    with col_save:
        if st.button("Save →", type="primary", use_container_width=True):
            if not report_name.strip():
                st.error("Please enter a report name.")
            else:
                success, err = save_report(user_id, {
                    "name":       report_name,
                    "role":       role,
                    "score":      result["score"],
                    "matched":    result["matched"],
                    "missing":    result["missing"],
                    "readiness":  result["readiness"],
                    "salary":     result.get("salary", ""),
                    "difficulty": result.get("difficulty", ""),
                })
                if success:
                    st.success("Report saved!")
                    st.rerun()
                else:
                    st.error(f"Error: {err}")

    st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2rem 0;"></div>', unsafe_allow_html=True)

# ── SAVED REPORTS ─────────────────────────────────────
st.markdown('<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:1.5rem;">Saved Reports</div>', unsafe_allow_html=True)

reports = get_reports(user_id) if user_id else []

if not reports:
    st.markdown("""
    <div style="text-align:center; padding:3rem 2rem; background:rgba(255,255,255,0.3);
                border:1px solid rgba(26,60,35,0.08); border-radius:3px;">
        <div style="font-family:'Fraunces',serif; font-size:1.5rem; font-weight:300;
                    color:rgba(26,60,35,0.35); margin-bottom:0.5rem;">No reports yet</div>
        <div style="font-size:0.82rem; color:rgba(26,60,35,0.3); font-family:Inter,sans-serif;">
            Run an analysis and save it to see it here.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Summary stats
    scores = [r["score"] for r in reports]
    c1, c2, c3 = st.columns(3, gap="medium")
    for col, val, lbl in [
        (c1, len(reports),                        "Total Reports"),
        (c2, f"{int(sum(scores)/len(scores))}%",  "Avg Score"),
        (c3, f"{max(scores)}%",                   "Best Score"),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.45); border:1px solid rgba(26,60,35,0.1);
                        border-radius:3px; padding:1.2rem 1.5rem; margin-bottom:1.5rem;">
                <div style="font-family:'Fraunces',serif; font-size:2rem; font-weight:600;
                            color:#1A3C23; line-height:1;">{val}</div>
                <div style="font-size:0.62rem; color:rgba(26,60,35,0.38); letter-spacing:1.5px;
                            text-transform:uppercase; font-family:Inter,sans-serif; margin-top:0.4rem;">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    # Report rows
    for i, report in enumerate(reports):
        score       = report["score"]
        score_color = "#2A6B3A" if score >= 70 else "#7A5C10" if score >= 40 else "#7A2A2A"
        border_top  = "border-top:1px solid rgba(26,60,35,0.07);" if i > 0 else ""
        created     = str(report.get("created_at", ""))[:10]
        matched_str = ", ".join(report.get("matched_skills", [])[:4])
        missing_str = ", ".join(report.get("missing_skills", [])[:4])

        c1, c2, c3, c4 = st.columns([2.5, 1, 1, 0.8], gap="medium")
        with c1:
            st.markdown(f"""
            <div style="padding:1.2rem 0; {border_top}">
                <div style="font-family:'Fraunces',serif; font-weight:600; font-size:1rem;
                            color:#1A3C23; margin-bottom:0.3rem;">{report['report_name']}</div>
                <div style="font-size:0.75rem; color:rgba(26,60,35,0.4); font-family:Inter,sans-serif;">
                    {report['role']} · {created}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style="padding:1.2rem 0; {border_top}">
                <div style="font-family:'Fraunces',serif; font-size:1.6rem; font-weight:700;
                            color:{score_color}; line-height:1;">{score}%</div>
                <div style="font-size:0.6rem; color:rgba(26,60,35,0.3); font-family:Inter,sans-serif;
                            letter-spacing:1px; text-transform:uppercase;">match</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div style="padding:1.2rem 0; {border_top}">
                <div style="font-size:0.75rem; color:rgba(26,60,35,0.5); font-family:Inter,sans-serif;
                            line-height:1.6;">
                    <span style="color:#2A6B3A;">✓</span> {matched_str or 'None'}<br>
                    <span style="color:#7A2A2A;">✗</span> {missing_str or 'None'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div style="padding:0.5rem 0; {border_top}">', unsafe_allow_html=True)
            if st.button("Delete", key=f"del_{report['id']}", use_container_width=True):
                delete_report(report["id"])
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2rem 0;"></div>', unsafe_allow_html=True)
    if st.button("Clear All Reports", use_container_width=False):
        for r in reports:
            delete_report(r["id"])
        st.rerun()