import streamlit as st
import re
from modules.skill_analyzer import get_all_roles, get_role_info
from modules.demand_score import get_demand_emoji

ROLE_DEFINITIONS = {
    "AI Engineer": "AI Engineers sit at the crossroads of software engineering and machine learning. They take research-stage models and turn them into reliable, scalable systems that run in the real world — handling model serving, latency optimisation, and production monitoring. Unlike pure data scientists, they write production-grade code and care deeply about system design, APIs, and infrastructure.",
    "Backend Developer": "Backend Developers are the architects of what happens behind the scenes. They design the databases, APIs, and server logic that power every button click on a website or app. They think about data consistency, performance under load, security, and how services talk to each other. Most of the internet runs on their work, even if users never see it.",
    "Blockchain Developer": "Blockchain Developers build decentralised applications — software that runs on a network of computers rather than a single server. They write smart contracts on platforms like Ethereum, design token systems, and think carefully about cryptographic security. It's a niche with high demand and a steep learning curve.",
    "Business Analyst": "Business Analysts are translators — they convert messy business problems into clear requirements that engineers can build. They run stakeholder interviews, map processes, analyse data, and write specifications that guide product decisions. Good BAs are rare because they need both people skills and analytical rigour.",
    "Cloud Engineer": "Cloud Engineers design and manage the invisible infrastructure modern software runs on. They provision servers, configure security, and build the automation that keeps everything running at scale. AWS, Azure, and GCP are their primary playgrounds — and the cloud market continues to grow rapidly.",
    "Computer Vision Engineer": "Computer Vision Engineers teach machines to see. They build systems that detect objects in images, read text from photos, or assess medical scans using deep learning. Applications range from self-driving cars to manufacturing quality control — making it one of the most impactful areas of AI.",
    "Cybersecurity Analyst": "Cybersecurity Analysts are digital defenders. They monitor networks for threats, investigate breaches, run penetration tests, and harden systems against attack. With cyber threats growing more sophisticated every year, this role has become one of the fastest-growing in tech — and one of the hardest to fill.",
    "Data Analyst": "Data Analysts turn raw numbers into stories that drive decisions. They write SQL, build dashboards, run A/B tests, and present findings to stakeholders who need clear answers. It's often an entry point into the data field, but skilled analysts who communicate insights well are enormously valuable at any level.",
    "Data Architect": "Data Architects design the blueprint for how an organisation stores, moves, and accesses its data. They decide which databases to use, how data flows between systems, and how to ensure data quality and governance. It's a senior role that shapes every downstream data project in the company.",
    "Data Engineer": "Data Engineers build the plumbing of the data world. They design pipelines that ingest, clean, and transform raw data from dozens of sources into formats that analysts and data scientists can actually use. As data volumes explode, demand for engineers who can build reliable, scalable pipelines has never been higher.",
    "Data Scientist": "Data Scientists apply mathematics, statistics, and machine learning to extract insights from complex datasets. They build predictive models, run experiments, and help organisations make evidence-based decisions. The role blends technical depth with communication skills — the best data scientists can explain their models to non-technical executives.",
    "Database Administrator": "Database Administrators (DBAs) are the guardians of an organisation's most valuable asset: its data. They keep databases fast, available, and secure — tuning queries, managing backups, planning capacity, and responding when things go wrong. With data growing exponentially, experienced DBAs remain in high demand.",
    "DevOps Engineer": "DevOps Engineers dissolve the wall between development and operations. They build CI/CD pipelines that ship code safely and frequently, manage infrastructure as code, and create automation that lets small teams move fast. The role has fundamentally transformed how software gets built and deployed across the industry.",
    "Embedded Systems Engineer": "Embedded Systems Engineers write software for devices that aren't traditional computers — microcontrollers in medical devices, firmware in electronics, control systems in machinery. They work close to the metal, optimising for limited memory, real-time requirements, and environments with no operating system.",
    "Frontend Developer": "Frontend Developers build everything users interact with on the web — layouts, animations, forms, and flows that make up the user experience. They translate designer mockups into living interfaces using HTML, CSS, and JavaScript frameworks. The best frontends are fast, accessible, and feel completely effortless to use.",
    "Full Stack Developer": "Full Stack Developers are versatile generalists who can build an entire web application from database to user interface. They're particularly valuable at startups where someone needs to own features end-to-end. The tradeoff is breadth over depth — they know a lot, but specialists often go deeper in any single area.",
    "Game Developer": "Game Developers create interactive experiences — from indie puzzle games to AAA open worlds. They work with engines like Unity or Unreal, implement physics and AI systems, optimise for target hardware, and collaborate with artists and designers. It's one of the most creatively demanding roles in the entire tech industry.",
    "IoT Engineer": "IoT Engineers connect the physical and digital worlds. They build firmware on sensors, gateways that aggregate data, cloud pipelines that process it, and dashboards that visualise it. As industries from agriculture to healthcare embed more intelligence into physical objects, IoT expertise has become highly sought after.",
    "IT Support Specialist": "IT Support Specialists keep organisations running by solving the technical problems that inevitably arise. They troubleshoot hardware and software issues, manage user accounts, maintain network connectivity, and document solutions. It's often a first step into tech — and a fast way to build broad practical knowledge.",
    "Machine Learning Engineer": "Machine Learning Engineers productionise machine learning. Where data scientists experiment, ML Engineers build infrastructure to train models reliably, serve predictions at scale, and monitor behaviour over time. They write cleaner, more maintainable code than researchers and think deeply about system architecture and reliability.",
    "Mobile Developer": "Mobile Developers build the apps people use on their phones every day. They work with Swift for iOS, Kotlin for Android, or cross-platform frameworks like Flutter and React Native. Mobile development demands attention to performance, battery life, offline behaviour, and the constraints of small screens.",
    "Network Engineer": "Network Engineers design and maintain the infrastructure that connects computers — routers, switches, firewalls, and the protocols that govern data flow. They troubleshoot connectivity, plan capacity, and increasingly work with software-defined networking and cloud networking as infrastructure moves online.",
    "NLP Engineer": "NLP Engineers build systems that work with human language — search engines, chatbots, translation tools, and the large language models reshaping the tech industry. It's a rapidly evolving field where research moves fast and techniques that were cutting-edge six months ago can already be considered standard practice.",
    "Product Manager": "Product Managers own the 'why' and 'what' of a product. They synthesise user research, business strategy, and technical constraints into a roadmap — then work with engineering and design to execute it. Great PMs are rare: they need commercial instincts, empathy for users, and enough technical fluency to earn engineers' respect.",
    "QA Engineer": "QA Engineers are the last line of defence before software reaches users. They design test plans, write automated test suites, investigate bugs, and advocate for quality throughout development. As systems grow more complex, automated testing has become a core engineering discipline rather than an afterthought.",
    "Security Engineer": "Security Engineers build the defences that protect systems from attack. They design authentication systems, review code for vulnerabilities, implement encryption, and respond to incidents. They think like attackers — anticipating how systems can be exploited so they can be hardened before it actually happens.",
    "Site Reliability Engineer": "Site Reliability Engineers apply software engineering to the problem of running reliable systems. They manage SLOs, build runbooks, automate toil, conduct post-mortems, and design systems to fail gracefully. The role was pioneered at Google and is now standard at large tech companies managing operational complexity at scale.",
    "Software Engineer": "Software Engineers design, build, and maintain the systems that power modern life — spanning web apps, compilers, operating systems, APIs, and everything in between. It's one of the broadest roles in tech. Core skills are problem decomposition, clean code, and the ability to learn new technologies quickly as the landscape shifts.",
    "Systems Architect": "Systems Architects make the big decisions about how complex software is structured. They choose technology stacks, define component boundaries, design for scalability and resilience, and ensure different parts of a system can evolve independently. It's a senior role requiring both deep technical knowledge and strategic thinking.",
    "UX Designer": "UX Designers ensure software is intuitive, accessible, and genuinely useful to the people who use it. They conduct user research, create wireframes, run usability tests, and work closely with engineers to bring designs to life. In a world full of feature-rich but confusing software, good UX is a genuine competitive advantage.",
}
DEFAULT_DEFINITION = "A specialised technology role requiring a strong combination of technical skills, problem-solving ability, and domain expertise."

diff_color_map = {"Beginner": "#2A6B3A", "Intermediate": "#7A5C10", "Advanced": "#7A2A2A"}
diff_bg_map    = {"Beginner": "rgba(42,107,58,0.09)", "Intermediate": "rgba(122,92,16,0.09)", "Advanced": "rgba(122,42,42,0.09)"}

# ── HEADER ────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:1.5rem;">
    <div style="font-size:0.68rem; font-weight:500; letter-spacing:3px; text-transform:uppercase;
                color:rgba(26,60,35,0.35); margin-bottom:0.5rem; font-family:'Inter',sans-serif;">Role Explorer</div>
    <div style="font-family:'Fraunces',serif; font-size:2.6rem; font-weight:300; color:#1A3C23;
                letter-spacing:-0.5px; line-height:1.1; margin-bottom:0.4rem;">
        Explore <em style="font-weight:600;">every role</em>
    </div>
    <div style="font-size:0.85rem; color:rgba(26,60,35,0.45); font-family:'Inter',sans-serif; font-weight:300;">
        Scroll the list on the left — click any role to see details on the right without losing your place.
    </div>
</div>
<div style="height:1px; background:rgba(26,60,35,0.08); margin-bottom:1.5rem;"></div>
""", unsafe_allow_html=True)

roles = get_all_roles()

# ── FILTERS ───────────────────────────────────────────
c1, c2, c3 = st.columns([3, 1.3, 1.3], gap="medium")
with c1:
    search = st.text_input("Search", placeholder="Search roles...", label_visibility="collapsed")
with c2:
    diff_filter = st.selectbox("Difficulty", ["All Levels", "Beginner", "Intermediate", "Advanced"], label_visibility="collapsed")
with c3:
    sort_by = st.selectbox("Sort", ["A → Z", "Salary ↑", "Salary ↓", "Skills Count"], label_visibility="collapsed")

def salary_num(s):
    nums = re.findall(r"[\d.]+", str(s))
    return float(nums[0]) if nums else 0

filtered = [r for r in roles if not search or search.lower() in r.lower()]
if diff_filter != "All Levels":
    filtered = [r for r in filtered if get_role_info(r)["difficulty"] == diff_filter]
if sort_by == "Salary ↑":
    filtered = sorted(filtered, key=lambda r: salary_num(get_role_info(r)["salary"]))
elif sort_by == "Salary ↓":
    filtered = sorted(filtered, key=lambda r: salary_num(get_role_info(r)["salary"]), reverse=True)
elif sort_by == "Skills Count":
    filtered = sorted(filtered, key=lambda r: len(get_role_info(r)["required_skills"]), reverse=True)
else:
    filtered = sorted(filtered)

if "explorer_selected" not in st.session_state:
    st.session_state.explorer_selected = filtered[0] if filtered else None

sel = st.session_state.explorer_selected

# ── LAYOUT ────────────────────────────────────────────
left, right = st.columns([1, 1.6], gap="large")

# ── LEFT: SCROLLABLE LIST via st.container(height=) ──
with left:
    st.markdown(f'<div style="font-size:0.68rem; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; letter-spacing:1px; margin-bottom:0.5rem;">{len(filtered)} ROLES</div>', unsafe_allow_html=True)

    scroll_box = st.container(height=560, border=True)
    with scroll_box:
        if not filtered:
            st.markdown('<div style="padding:2rem; color:rgba(26,60,35,0.3); font-family:Fraunces,serif; text-align:center;">No roles found.</div>', unsafe_allow_html=True)
        else:
            for i, role in enumerate(filtered):
                info      = get_role_info(role)
                diff      = info["difficulty"]
                dc        = diff_color_map.get(diff, "#1A3C23")
                db        = diff_bg_map.get(diff, "rgba(26,60,35,0.05)")
                is_active = sel == role
                sep       = "border-top:1px solid rgba(26,60,35,0.07);" if i > 0 else ""
                row_bg    = "background:rgba(26,60,35,0.04);" if is_active else ""
                lborder   = "border-left:2px solid #1A3C23;" if is_active else "border-left:2px solid transparent;"
                weight    = "600" if is_active else "400"

                col_info, col_btn = st.columns([5, 1], gap="small")
                with col_info:
                    st.markdown(f"""
                    <div style="padding:0.65rem 0.5rem; {sep} {row_bg} {lborder}">
                        <div style="display:flex; align-items:center; gap:0.5rem; flex-wrap:wrap; margin-bottom:0.15rem;">
                            <span style="font-family:'Fraunces',serif; font-weight:{weight};
                                         font-size:0.9rem; color:#1A3C23;">{role}</span>
                            <span style="background:{db}; color:{dc}; font-size:0.54rem;
                                         letter-spacing:1px; text-transform:uppercase;
                                         font-family:Inter,sans-serif; font-weight:600;
                                         padding:0.16rem 0.4rem; border-radius:2px;">{diff}</span>
                        </div>
                        <div style="font-size:0.72rem; color:rgba(26,60,35,0.42); font-family:Inter,sans-serif;">
                            {info['salary']} · {len(info['required_skills'])} skills
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_btn:
                    st.markdown('<div style="padding-top:0.55rem;">', unsafe_allow_html=True)
                    label = "✓" if is_active else "→"
                    btype = "primary" if is_active else "secondary"
                    if st.button(label, key=f"exp_{i}", use_container_width=True, type=btype):
                        st.session_state.explorer_selected = role
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

# ── RIGHT: DETAIL PANEL ───────────────────────────────
with right:
    if not sel:
        st.markdown("""
        <div style="padding:5rem 2rem; border:1px dashed rgba(26,60,35,0.15);
                    border-radius:3px; text-align:center; margin-top:2rem;">
            <div style="font-family:'Fraunces',serif; font-size:1.3rem; font-weight:300;
                        color:rgba(26,60,35,0.3);">Select a role to view details</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        info       = get_role_info(sel)
        diff       = info["difficulty"]
        dc         = diff_color_map.get(diff, "#1A3C23")
        db         = diff_bg_map.get(diff, "rgba(26,60,35,0.05)")
        definition = ROLE_DEFINITIONS.get(sel, DEFAULT_DEFINITION)

        st.markdown(f"""
        <div style="font-size:0.6rem; letter-spacing:2px; text-transform:uppercase;
                    color:rgba(26,60,35,0.35); font-family:Inter,sans-serif;
                    margin-bottom:0.4rem;">Role Detail</div>
        <div style="font-family:'Fraunces',serif; font-size:2rem; font-weight:600;
                    color:#1A3C23; line-height:1.15; margin-bottom:0.9rem;">{sel}</div>
        <div style="font-size:0.875rem; color:rgba(26,60,35,0.65); font-family:Inter,sans-serif;
                    line-height:1.75; padding:1rem 1.2rem;
                    background:rgba(255,255,255,0.5);
                    border-left:2px solid rgba(26,60,35,0.25);
                    border-radius:0 3px 3px 0;
                    margin-bottom:1.3rem;">{definition}</div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display:flex; gap:0.8rem; margin-bottom:1.3rem;">
            <div style="flex:1; background:rgba(255,255,255,0.5); border:1px solid rgba(26,60,35,0.1);
                        border-radius:3px; padding:0.85rem 1rem;">
                <div style="font-size:0.57rem; letter-spacing:1.5px; text-transform:uppercase;
                            color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.3rem;">Salary</div>
                <div style="font-family:'Fraunces',serif; font-weight:600; color:#1A3C23; font-size:1rem;">{info['salary']}</div>
            </div>
            <div style="flex:1; background:{db}; border:1px solid rgba(26,60,35,0.08);
                        border-radius:3px; padding:0.85rem 1rem;">
                <div style="font-size:0.57rem; letter-spacing:1.5px; text-transform:uppercase;
                            color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.3rem;">Difficulty</div>
                <div style="font-family:'Fraunces',serif; font-weight:600; color:{dc}; font-size:1rem;">{diff}</div>
            </div>
            <div style="flex:1; background:rgba(255,255,255,0.5); border:1px solid rgba(26,60,35,0.1);
                        border-radius:3px; padding:0.85rem 1rem;">
                <div style="font-size:0.57rem; letter-spacing:1.5px; text-transform:uppercase;
                            color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.3rem;">Skills Required</div>
                <div style="font-family:'Fraunces',serif; font-weight:600; color:#1A3C23; font-size:1rem;">{len(info['required_skills'])}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="font-size:0.62rem; letter-spacing:2px; text-transform:uppercase;
                    color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.7rem;">Required Skills</div>
        """, unsafe_allow_html=True)

        chips = "".join([
            f'<span style="background:transparent; color:#1A3C23; border:1px solid rgba(26,60,35,0.18); '
            f'padding:0.28rem 0.75rem; border-radius:2px; font-size:0.74rem; font-family:Inter,sans-serif; '
            f'display:inline-block; margin:0.18rem;">{s}</span>'
            for s in info["required_skills"]
        ])
        st.markdown(f'<div style="line-height:2.6; margin-bottom:1.5rem;">{chips}</div>', unsafe_allow_html=True)

        ca, cb = st.columns(2)
        with ca:
            if st.button("Analyze This Role →", type="primary", use_container_width=True, key="exp_analyze"):
                st.session_state.prefill_role = sel
                st.session_state.current_page = "Analyze"
                st.rerun()
        with cb:
            if st.button("Compare Roles", use_container_width=True, key="exp_compare"):
                st.session_state.current_page = "Compare"
                st.rerun()
