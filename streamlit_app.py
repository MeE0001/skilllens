import streamlit as st

st.set_page_config(
    page_title="SkillLens",
    page_icon="◎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: #EDEADE !important; }
#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding-top: 7rem !important;
    padding-left: 5rem !important;
    padding-right: 5rem !important;
    padding-bottom: 6rem !important;
    max-width: 1280px !important;
}

/* ── NAVBAR ── */
div[data-testid="stRadio"]:first-of-type {
    position: fixed !important;
    top: 0 !important; left: 0 !important; right: 0 !important;
    z-index: 99999 !important;
    background: rgba(237,234,222,0.96) !important;
    backdrop-filter: blur(16px) !important;
    border-bottom: 1px solid rgba(26,60,35,0.1) !important;
    padding: 0 16rem 0 18rem !important;
    margin: 0 !important;
    height: 56px !important;
    display: flex !important;
    align-items: center !important;
}
div[data-testid="stRadio"]:first-of-type > label { display: none !important; }
div[data-testid="stRadio"]:first-of-type > div[role="radiogroup"] {
    display: flex !important; flex-direction: row !important;
    gap: 0 !important; align-items: center !important;
    flex-wrap: nowrap !important; height: 56px !important;
}
div[data-testid="stRadio"]:first-of-type > div[role="radiogroup"] > label {
    display: flex !important; align-items: center !important;
    justify-content: center !important; padding: 0 1.2rem !important;
    height: 56px !important; border-radius: 0 !important;
    cursor: pointer !important; border: none !important;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.2s ease !important; margin-bottom: -1px !important;
}
div[data-testid="stRadio"]:first-of-type > div[role="radiogroup"] > label > div:last-child {
    color: rgba(26,60,35,0.4) !important; font-size: 0.72rem !important;
    font-weight: 500 !important; letter-spacing: 1.2px !important;
    text-transform: uppercase !important; white-space: nowrap !important;
    font-family: 'Inter', sans-serif !important;
}
div[data-testid="stRadio"]:first-of-type > div[role="radiogroup"] > label:hover > div:last-child {
    color: #1A3C23 !important;
}
div[data-testid="stRadio"]:first-of-type > div[role="radiogroup"] > label:has(input:checked) {
    border-bottom: 2px solid #1A3C23 !important;
}
div[data-testid="stRadio"]:first-of-type > div[role="radiogroup"] > label:has(input:checked) > div:last-child {
    color: #1A3C23 !important; font-weight: 600 !important;
}
div[data-testid="stRadio"]:first-of-type > div[role="radiogroup"] > label > div:first-child { display: none !important; }
div[data-testid="stRadio"]:first-of-type input[type="radio"] { display: none !important; }

/* ── BUTTONS ── */
.stButton > button {
    font-family: 'Inter', sans-serif !important; font-weight: 500 !important;
    font-size: 0.76rem !important; letter-spacing: 1px !important;
    text-transform: uppercase !important; border-radius: 4px !important;
    transition: all 0.2s ease !important; padding: 0.62rem 1.6rem !important;
}
.stButton > button[kind="primary"] {
    background: #1A3C23 !important; border: none !important; color: #EDEADE !important;
}
.stButton > button[kind="primary"]:hover {
    background: #2C5E38 !important; transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(26,60,35,0.22) !important;
}
.stButton > button:not([kind="primary"]) {
    background: transparent !important;
    border: 1px solid rgba(26,60,35,0.3) !important; color: #1A3C23 !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: rgba(26,60,35,0.05) !important; border-color: #1A3C23 !important;
}

/* ── INPUTS ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.6) !important;
    border: 1px solid rgba(26,60,35,0.2) !important;
    border-radius: 4px !important; color: #1A3C23 !important;
    font-family: 'Inter', sans-serif !important; font-size: 0.88rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #1A3C23 !important;
    box-shadow: 0 0 0 3px rgba(26,60,35,0.07) !important; background: white !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(26,60,35,0.28) !important; }
.stTextInput label, .stSelectbox label {
    color: rgba(26,60,35,0.6) !important; font-size: 0.72rem !important;
    font-weight: 500 !important; letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

/* ── CHECKBOXES ── */
[data-testid="stCheckbox"] label p {
    color: rgba(26,60,35,0.65) !important; font-size: 0.85rem !important;
    font-family: 'Inter', sans-serif !important; font-weight: 400 !important;
}
[data-testid="stCheckbox"] input:checked + div svg {
    fill: #1A3C23 !important; stroke: #1A3C23 !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(26,60,35,0.12) !important; gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important; font-size: 0.72rem !important;
    letter-spacing: 1px !important; text-transform: uppercase !important;
    color: rgba(26,60,35,0.38) !important; padding: 0.85rem 1.8rem !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #1A3C23 !important; border-bottom: 2px solid #1A3C23 !important;
    background: transparent !important; font-weight: 600 !important;
}

/* ── SELECTBOX ── */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.6) !important;
    border: 1px solid rgba(26,60,35,0.2) !important;
    border-radius: 4px !important; color: #1A3C23 !important;
}

/* ── ALERTS ── */
.stAlert { border-radius: 4px !important; font-size: 0.85rem !important; }
.stSpinner > div { border-top-color: #1A3C23 !important; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #E5E2D8; }
::-webkit-scrollbar-thumb { background: rgba(26,60,35,0.15); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ── SESSION DEFAULTS ──────────────────────────────────
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ── HANDLE SIGN OUT via query param ──────────────────
params = st.query_params
if params.get("signout") == "1":
    from database.supabase_client import sign_out
    sign_out()
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.query_params.clear()
    st.rerun()

# ── AUTH GATE ─────────────────────────────────────────
if not st.session_state.logged_in:
    from pages.auth import show_auth
    show_auth()
    st.stop()

# ── LOGO + USER BADGE + SIGN OUT (pure HTML, fixed) ──
user_name = st.session_state.get("user_name", "")
first     = user_name.split()[0] if user_name else "U"
initial   = first[0].upper()

st.markdown(f"""
<div style="position:fixed; top:0; left:0; z-index:999999;
            height:56px; display:flex; align-items:center; padding:0 3rem;
            background:rgba(237,234,222,0.96); backdrop-filter:blur(16px);
            border-bottom:1px solid rgba(26,60,35,0.1); pointer-events:none;">
    <span style="font-family:'Fraunces',serif; font-weight:600; font-size:1.15rem;
                 color:#1A3C23; letter-spacing:-0.5px;">
        <em>Skill</em>Lens
    </span>
</div>

<div style="position:fixed; top:0; right:0; z-index:999999;
            height:56px; display:flex; align-items:center; padding:0 2.5rem; gap:0.75rem;
            background:rgba(237,234,222,0.96); backdrop-filter:blur(16px);
            border-bottom:1px solid rgba(26,60,35,0.1);">
    <div style="width:26px; height:26px; border-radius:50%; background:#1A3C23;
                display:flex; align-items:center; justify-content:center;
                font-size:0.65rem; color:#EDEADE; font-weight:600;
                font-family:'Inter',sans-serif;">{initial}</div>
    <span style="font-size:0.72rem; color:rgba(26,60,35,0.65); font-weight:500;
                 letter-spacing:0.5px; font-family:'Inter',sans-serif;">{first}</span>
    <div style="width:1px; height:16px; background:rgba(26,60,35,0.15); margin:0 0.2rem;"></div>
    <a href="?signout=1" style="font-size:0.68rem; font-weight:500; letter-spacing:1px;
                text-transform:uppercase; color:rgba(26,60,35,0.45);
                text-decoration:none; font-family:'Inter',sans-serif;
                padding:0.3rem 0.7rem; border:1px solid rgba(26,60,35,0.2);
                border-radius:4px; transition:all 0.2s;"
       onmouseover="this.style.color='#1A3C23'; this.style.borderColor='#1A3C23';"
       onmouseout="this.style.color='rgba(26,60,35,0.45)'; this.style.borderColor='rgba(26,60,35,0.2)';">
        Sign out
    </a>
</div>
""", unsafe_allow_html=True)

# ── NAVBAR ────────────────────────────────────────────
pages = ["Home", "Analyze", "Dashboard", "Roadmap", "Reports", "Explorer", "Compare"]
page_files = {
    "Home":      "pages/home.py",
    "Analyze":   "pages/analyze.py",
    "Dashboard": "pages/dashboard.py",
    "Roadmap":   "pages/roadmap.py",
    "Reports":   "pages/reports.py",
    "Explorer":  "pages/explorer.py",
    "Compare":   "pages/compare.py",
}

current_index = pages.index(st.session_state.current_page) if st.session_state.current_page in pages else 0

selected = st.radio(
    label="Navigation",
    options=pages,
    index=current_index,
    horizontal=True,
    label_visibility="hidden",
)

if selected != st.session_state.current_page:
    st.session_state.current_page = selected
    st.rerun()

# ── RENDER PAGE ───────────────────────────────────────
with open(page_files[st.session_state.current_page]) as f:
    exec(f.read())