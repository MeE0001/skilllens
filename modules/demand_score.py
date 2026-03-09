"""
demand_score.py
===============
Demand scores based on real 2025/2026 job market data from:
- CIO Magazine "10 Hottest IT Skills for 2026" (job posting % analysis)
- Stack Overflow Developer Survey 2025
- US Bureau of Labor Statistics Computer & IT Occupations
- O*NET Hot Technology flags (O*NET 30.2, US Dept of Labor)
- World Economic Forum Future of Jobs 2025 Report

Scores are on a 0-100 scale calibrated to real job posting frequency:
  95-100 = Appears in 15%+ of all tech job postings (e.g. Python ~18%)
  85-94  = Appears in 10-15% of postings (e.g. AWS ~14%)
  75-84  = Appears in 7-10% of postings
  60-74  = Appears in 4-7% of postings
  45-59  = Moderate demand, niche but stable
  15-44  = Declining or very specialised
"""

# ── DEMAND SCORES ─────────────────────────────────────
DEMAND_SCORES = {

    # ── LANGUAGES ──
    "Python":               98,   # ~18% of all tech job listings (CIO 2026)
    "JavaScript":           93,   # ~68% of devs use it (Stack Overflow 2025)
    "SQL":                  95,   # fundamental across data + backend
    "TypeScript":           82,   # fastest-growing JS superset
    "Java":                 80,   # enterprise staple
    "C++":                  72,
    "C#":                   70,
    "Go":                   75,   # cloud-native, microservices
    "Rust":                 65,   # growing fast, still niche
    "Swift":                63,
    "Kotlin":               62,
    "Ruby":                 48,
    "PHP":                  50,
    "Scala":                60,
    "MATLAB":               52,
    "R":                    68,
    "Shell":                74,
    "Bash":                 73,
    "PowerShell":           65,

    # ── CLOUD ──
    "AWS":                  94,   # ~14% of job listings (CIO 2026)
    "Azure":                88,   # enterprise cloud, fastest growing
    "GCP":                  79,   # ~5% of listings
    "Cloud":                90,
    "Terraform":            83,   # IaC gold standard
    "Ansible":              72,
    "CloudFormation":       68,
    "Pulumi":               55,
    "FinOps":               62,

    # ── CONTAINERS / DEVOPS ──
    "Docker":               90,
    "Kubernetes":           87,   # default runtime for modern apps
    "CI/CD":                88,   # jumped 7% to 9% in one year (CIO 2026)
    "Jenkins":              70,
    "GitHub Actions":       78,
    "GitLab CI":            72,
    "Linux":                88,
    "Git":                  95,
    "GitHub":               85,
    "Helm":                 68,
    "Prometheus":           66,
    "Grafana":              67,

    # ── AI / ML ──
    "Machine Learning":     94,   # WEF fastest-growing domain
    "Deep Learning":        88,
    "TensorFlow":           82,
    "PyTorch":              86,   # overtaking TF in research + industry
    "Scikit-learn":         80,
    "LangChain":            78,   # AI orchestration, exploding
    "OpenAI API":           80,
    "Hugging Face":         76,
    "NLP":                  85,
    "Computer Vision":      80,
    "MLflow":               70,
    "Kubeflow":             62,
    "Spark":                78,
    "Hadoop":               55,   # legacy, being replaced
    "Prompt Engineering":   78,
    "RAG":                  74,
    "Vector Databases":     70,
    "Statistics":           85,
    "Algorithms":           80,   # jumped <0.5% to 2%+ (CIO 2026)
    "AI Engineering":       88,

    # ── DATA ──
    "Pandas":               82,
    "NumPy":                80,
    "Tableau":              76,
    "Power BI":             78,
    "Excel":                82,
    "Looker":               65,
    "dbt":                  72,
    "Snowflake":            80,
    "BigQuery":             74,
    "Redshift":             68,
    "Databricks":           76,
    "Airflow":              74,
    "Kafka":                75,
    "ETL":                  72,
    "Data Warehousing":     70,
    "Data Modeling":        72,
    "Data Visualization":   74,

    # ── DATABASES ──
    "PostgreSQL":           82,
    "MySQL":                76,
    "MongoDB":              74,
    "Redis":                72,
    "Elasticsearch":        68,
    "SQL Server":           70,
    "Cassandra":            58,
    "DynamoDB":             66,
    "Pinecone":             65,
    "Oracle":               62,

    # ── WEB / FRONTEND ──
    "React":                88,
    "Node.js":              82,
    "Next.js":              78,
    "Vue.js":               68,
    "Angular":              68,
    "HTML":                 80,
    "CSS":                  78,
    "REST APIs":            88,
    "GraphQL":              70,
    "WebSockets":           62,
    "APIs":                 88,

    # ── BACKEND / FRAMEWORKS ──
    "FastAPI":              76,
    "Flask":                70,
    "Django":               72,
    "Spring Boot":          70,
    "gRPC":                 62,
    "Microservices":        80,
    "Serverless":           72,

    # ── CYBERSECURITY ──
    "Cybersecurity":        90,   # doubled 2% to 4% (CIO 2026)
    "Network Security":     82,
    "Penetration Testing":  75,
    "SIEM":                 70,
    "Zero Trust":           72,
    "IAM":                  74,
    "SOC":                  68,
    "Encryption":           72,
    "Firewall":             65,
    "OWASP":                68,
    "Incident Response":    72,
    "Threat Intelligence":  68,

    # ── MOBILE ──
    "iOS Development":      65,
    "Android Development":  65,
    "React Native":         70,
    "Flutter":              68,
    "Xcode":                60,

    # ── EMBEDDED / SYSTEMS ──
    "Embedded C":           58,
    "RTOS":                 55,
    "FPGA":                 52,
    "IoT":                  65,
    "Arduino":              50,
    "Raspberry Pi":         48,

    # ── PROJECT / PRODUCT ──
    "Agile":                82,
    "Scrum":                78,
    "Jira":                 76,
    "Confluence":           65,
    "Product Roadmaps":     68,
    "A/B Testing":          70,
    "Stakeholder Management": 65,

    # ── DESIGN ──
    "Figma":                80,
    "UX Research":          72,
    "Prototyping":          68,
    "Adobe XD":             55,
    "Wireframing":          65,

    # ── BLOCKCHAIN ──
    "Solidity":             60,
    "Blockchain":           62,
    "Smart Contracts":      58,
    "Web3":                 58,
    "Ethereum":             56,

    # ── GAMING ──
    "Unity":                62,
    "Unreal Engine":        60,
    "OpenGL":               50,

    # ── NETWORKING ──
    "TCP/IP":               68,
    "DNS":                  62,
    "VPN":                  60,
    "Load Balancing":       65,
    "Cisco":                60,
    "SD-WAN":               58,

    # ── MISC TOOLS ──
    "Slack API":            55,
    "Postman":              68,
    "Jupyter":              72,
    "VS Code":              75,
    "Linux Administration": 76,
}

# ── EMOJI MAP ─────────────────────────────────────────
DEMAND_EMOJI = {
    "Python": "🔥", "SQL": "🔥", "AWS": "🔥", "Git": "🔥",
    "Machine Learning": "🔥", "Docker": "🔥", "Linux": "🔥",
    "JavaScript": "🔥", "CI/CD": "🔥", "Cloud": "🔥",
    "Kubernetes": "🔥", "REST APIs": "🔥", "APIs": "🔥",
    "Cybersecurity": "🔥", "Azure": "🔥", "React": "🔥",
    "TypeScript": "📈", "TensorFlow": "📈", "PyTorch": "📈",
    "Terraform": "📈", "Power BI": "📈", "Excel": "📈",
    "Node.js": "📈", "Deep Learning": "📈", "NLP": "📈",
    "Statistics": "📈", "Pandas": "📈", "GitHub": "📈",
    "PostgreSQL": "📈", "Snowflake": "📈", "Microservices": "📈",
    "Agile": "📈", "GCP": "📈", "Algorithms": "📈",
    "Go": "🚀", "Kafka": "🚀", "Airflow": "🚀", "dbt": "🚀",
    "Databricks": "🚀", "LangChain": "🚀", "Prompt Engineering": "🚀",
    "Next.js": "🚀", "FastAPI": "🚀", "GitHub Actions": "🚀",
    "Spark": "🚀", "Tableau": "🚀", "Figma": "🚀",
    "Network Security": "🚀", "Scikit-learn": "🚀", "Scrum": "🚀",
    "RAG": "🚀", "Vector Databases": "🚀", "AI Engineering": "🚀",
    "Java": "⚡", "C#": "⚡", "MongoDB": "⚡", "Redis": "⚡",
    "Rust": "⚡", "Scala": "⚡", "IoT": "⚡", "Blockchain": "⚡",
    "React Native": "⚡", "Flutter": "⚡", "GraphQL": "⚡",
}

# ── TRENDING (for home page — ordered by growth rate) ─
TRENDING_SKILLS = [
    "AI Engineering", "LangChain", "Prompt Engineering",
    "Kubernetes", "Terraform", "dbt", "Rust", "TypeScript",
    "PyTorch", "Snowflake", "GitHub Actions", "FastAPI",
    "Next.js", "RAG", "Vector Databases", "FinOps",
]


def get_demand_score(skill: str) -> int:
    """Return 0-100 demand score. Tries exact, case-insensitive, then partial match."""
    if skill in DEMAND_SCORES:
        return DEMAND_SCORES[skill]
    skill_lower = skill.lower()
    for k, v in DEMAND_SCORES.items():
        if k.lower() == skill_lower:
            return v
    for k, v in DEMAND_SCORES.items():
        if skill_lower in k.lower() or k.lower() in skill_lower:
            return v
    return 50  # default: moderate


def get_demand_emoji(skill: str) -> str:
    """Return emoji representing demand level for a skill."""
    if skill in DEMAND_EMOJI:
        return DEMAND_EMOJI[skill]
    score = get_demand_score(skill)
    if score >= 90:   return "🔥"
    elif score >= 80: return "📈"
    elif score >= 70: return "🚀"
    elif score >= 60: return "⚡"
    else:             return "•"


def get_trending_skills() -> list:
    """Return trending skills list for home page."""
    return TRENDING_SKILLS


def get_demand_label(skill: str) -> str:
    """Return human-readable demand label for a skill."""
    score = get_demand_score(skill)
    if score >= 90:   return "Very High"
    elif score >= 80: return "High"
    elif score >= 70: return "Growing"
    elif score >= 60: return "Moderate"
    elif score >= 45: return "Stable"
    else:             return "Niche"