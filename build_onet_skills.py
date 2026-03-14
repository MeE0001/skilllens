"""
Run from your project root:
    python build_onet_skills.py

Place Occupation_Data.xlsx and Skills.xlsx in the project root first.
Outputs: data/job_skills.csv
"""

import pandas as pd, os

ONET_ROLE_MAP = {
    "Data Scientists":                                          "Data Scientist",
    "Business Intelligence Analysts":                          "Data Analyst",
    "Computer Systems Analysts":                               "Business Analyst",
    "Data Warehousing Specialists":                            "Data Warehouse Engineer",
    "Computer and Information Research Scientists":            "AI Engineer",
    "Software Developers":                                     "Software Engineer",
    "Computer Programmers":                                    "Backend Developer",
    "Web Developers":                                          "Frontend Developer",
    "Web and Digital Interface Designers":                     "UX Designer",
    "Information Security Analysts":                           "Cybersecurity Analyst",
    "Information Security Engineers":                         "Security Engineer",
    "Digital Forensics Analysts":                             "Digital Forensics Analyst",
    "Blockchain Engineers":                                    "Blockchain Developer",
    "Computer Systems Engineers/Architects":                   "Solutions Architect",
    "Computer Network Architects":                             "Network Architect",
    "Network and Computer Systems Administrators":             "Network Engineer",
    "Database Administrators":                                 "Database Administrator",
    "Database Architects":                                     "Data Architect",
    "Software Quality Assurance Analysts and Testers":         "QA Engineer",
    "Computer Hardware Engineers":                             "Hardware Engineer",
    "Computer Network Support Specialists":                    "IT Support Specialist",
    "Web Administrators":                                      "Web Administrator",
    "Video Game Designers":                                    "Game Developer",
    "Computer and Information Systems Managers":               "Engineering Manager",
    "Information Technology Project Managers":                 "IT Project Manager",
    "Health Informatics Specialists":                          "Health Informatics Specialist",
    "Clinical Data Managers":                                  "Clinical Data Manager",
    "Bioinformatics Scientists":                               "Bioinformatics Scientist",
    "Bioinformatics Technicians":                              "Bioinformatics Technician",
    "Geographic Information Systems Technologists and Technicians": "GIS Specialist",
    "Remote Sensing Scientists and Technologists":             "Remote Sensing Specialist",
    "Telecommunications Engineering Specialists":              "Telecom Engineer",
    "Robotics Engineers":                                      "Robotics Engineer",
    "Robotics Technicians":                                    "Robotics Technician",
    "Mechatronics Engineers":                                  "Mechatronics Engineer",
    "Microsystems Engineers":                                  "Microsystems Engineer",
    "Photonics Engineers":                                     "Photonics Engineer",
    "Nanosystems Engineers":                                   "Nanosystems Engineer",
    "Electrical Engineers":                                    "Electrical Engineer",
    "Electronics Engineers, Except Computer":                  "Electronics Engineer",
    "Financial Quantitative Analysts":                         "Quantitative Analyst",
    "Intelligence Analysts":                                   "Intelligence Analyst",
    "Technical Writers":                                       "Technical Writer",
    "Computer Science Teachers, Postsecondary":                "CS Educator",
    "Media Technical Directors/Managers":                      "Media Technology Manager",
    "Sound Engineering Technicians":                           "Audio Engineer",
}

CUSTOM_ROLES = {
    "Machine Learning Engineer": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning", "MLOps", "Docker", "AWS", "Feature Engineering", "Model Deployment"],
    "DevOps Engineer":           ["Docker", "Kubernetes", "AWS", "Terraform", "Linux", "Git", "CI/CD", "Monitoring", "Ansible", "Jenkins"],
    "Cloud Engineer":            ["AWS", "Azure", "GCP", "Terraform", "Docker", "Kubernetes", "Linux", "Networking", "IAM", "Cloud Security"],
    "Mobile Developer":          ["Swift", "Kotlin", "React Native", "Flutter", "APIs", "Git", "UI Design", "App Store Deployment", "Firebase"],
    "Full Stack Developer":      ["JavaScript", "React", "Node.js", "Python", "SQL", "Docker", "APIs", "Git", "PostgreSQL", "TypeScript"],
    "NLP Engineer":              ["Python", "NLP", "PyTorch", "TensorFlow", "LLMs", "Hugging Face", "Deep Learning", "Text Processing", "BERT", "SpaCy"],
    "Computer Vision Engineer":  ["Python", "OpenCV", "PyTorch", "Deep Learning", "CNNs", "TensorFlow", "Image Processing", "Object Detection", "YOLO"],
    "Embedded Systems Engineer": ["C", "C++", "RTOS", "Microcontrollers", "Linux", "Assembly", "Hardware Interfacing", "FPGA", "IoT"],
    "Site Reliability Engineer": ["Linux", "Docker", "Kubernetes", "Python", "Monitoring", "AWS", "CI/CD", "Incident Management", "SLOs", "Chaos Engineering"],
    "Prompt Engineer":           ["LLMs", "Python", "Prompt Design", "APIs", "NLP", "Fine-tuning", "ChatGPT", "LangChain", "RAG", "Vector Databases"],
    "Scrum Master":              ["Scrum", "Agile", "Jira", "Facilitation", "Stakeholder Management", "Kanban", "Coaching", "Sprint Planning", "Retrospectives"],
    "Product Manager":           ["Agile", "Scrum", "Roadmapping", "Stakeholder Management", "Data Analysis", "User Research", "Jira", "A/B Testing", "PRDs"],
    "Data Engineer":             ["Python", "SQL", "Spark", "Airflow", "AWS", "Docker", "PostgreSQL", "Kafka", "dbt", "ETL"],
}

EXTRA_SKILLS = {
    "Data Scientist":            ["Python", "SQL", "Machine Learning", "Statistics", "TensorFlow", "PyTorch", "Pandas", "Data Visualization", "Scikit-learn"],
    "Data Analyst":              ["SQL", "Excel", "Python", "Tableau", "Power BI", "Statistics", "Data Visualization", "Google Analytics"],
    "Business Analyst":          ["SQL", "Excel", "Requirements Gathering", "Process Modeling", "Agile", "Tableau", "JIRA", "Stakeholder Management"],
    "Data Warehouse Engineer":   ["SQL", "Snowflake", "Redshift", "dbt", "ETL", "Python", "Data Modeling", "AWS", "Spark"],
    "AI Engineer":               ["Python", "Deep Learning", "NLP", "PyTorch", "TensorFlow", "LLMs", "APIs", "Cloud", "Transformers"],
    "Software Engineer":         ["Python", "Java", "Data Structures", "Algorithms", "Git", "SQL", "APIs", "System Design", "Code Review"],
    "Backend Developer":         ["Python", "Node.js", "SQL", "APIs", "Docker", "PostgreSQL", "Redis", "System Design", "Microservices"],
    "Frontend Developer":        ["JavaScript", "React", "TypeScript", "HTML", "CSS", "APIs", "Figma", "Webpack", "Testing"],
    "UX Designer":               ["Figma", "User Research", "Prototyping", "Wireframing", "Usability Testing", "Adobe XD", "Design Systems", "Accessibility"],
    "Cybersecurity Analyst":     ["Network Security", "Linux", "Python", "Penetration Testing", "SIEM", "Firewalls", "Risk Assessment", "OWASP"],
    "Security Engineer":         ["Network Security", "Linux", "Python", "SIEM", "Firewalls", "Cloud Security", "Zero Trust", "Vulnerability Management"],
    "Digital Forensics Analyst": ["Digital Forensics", "Python", "Linux", "Malware Analysis", "Incident Response", "Wireshark", "Chain of Custody"],
    "Blockchain Developer":      ["Solidity", "Web3.js", "Smart Contracts", "Ethereum", "Python", "Cryptography", "APIs", "DeFi", "Hardhat"],
    "Solutions Architect":       ["AWS", "System Design", "Microservices", "APIs", "Docker", "Cloud", "Security", "Networking", "Cost Optimization"],
    "Network Architect":         ["Networking", "Cisco", "TCP/IP", "Cloud Networking", "Security", "SD-WAN", "Firewalls", "BGP"],
    "Network Engineer":          ["Networking", "Linux", "Cisco", "Firewalls", "TCP/IP", "VPN", "Network Security", "Monitoring"],
    "Database Administrator":    ["SQL", "PostgreSQL", "MongoDB", "Redis", "Performance Tuning", "Backup & Recovery", "Linux", "Query Optimization"],
    "Data Architect":            ["SQL", "Data Modeling", "ETL", "AWS", "Spark", "Data Warehousing", "PostgreSQL", "Kafka", "dbt"],
    "QA Engineer":               ["Test Automation", "Selenium", "Python", "API Testing", "Jest", "CI/CD", "Bug Tracking", "Performance Testing"],
    "Hardware Engineer":         ["C", "C++", "VHDL", "FPGA", "PCB Design", "Embedded Systems", "Signal Processing", "CAD"],
    "IT Support Specialist":     ["Windows", "Linux", "Networking", "Troubleshooting", "Active Directory", "Help Desk", "Hardware", "ITIL"],
    "Web Administrator":         ["Linux", "Apache", "Nginx", "DNS", "SSL", "Cloud", "Security", "Monitoring", "Scripting"],
    "Game Developer":            ["C++", "Unity", "Unreal Engine", "C#", "3D Math", "Physics Simulation", "OpenGL", "Shaders"],
    "Engineering Manager":       ["Leadership", "Agile", "System Design", "Roadmapping", "Hiring", "Code Review", "Stakeholder Management"],
    "IT Project Manager":        ["Project Management", "Agile", "Scrum", "JIRA", "Stakeholder Management", "Risk Management", "Budgeting"],
    "Health Informatics Specialist": ["HL7", "FHIR", "SQL", "EHR Systems", "Python", "Healthcare Data", "Interoperability"],
    "Clinical Data Manager":     ["SQL", "Clinical Trials", "SAS", "Data Validation", "Regulatory Compliance", "CDISC", "Python"],
    "Bioinformatics Scientist":  ["Python", "R", "Genomics", "Bioinformatics Tools", "Statistics", "Machine Learning", "SQL", "BLAST"],
    "Bioinformatics Technician": ["Python", "R", "Genomics", "Linux", "Bioinformatics Tools", "Data Processing"],
    "GIS Specialist":            ["ArcGIS", "QGIS", "Python", "SQL", "Remote Sensing", "Cartography", "Spatial Analysis"],
    "Remote Sensing Specialist": ["Remote Sensing", "GIS", "Python", "Image Processing", "Satellite Data", "R", "Machine Learning"],
    "Telecom Engineer":          ["Networking", "5G", "LTE", "TCP/IP", "Linux", "RF Engineering", "VoIP", "SDN"],
    "Robotics Engineer":         ["Python", "C++", "ROS", "Control Systems", "Computer Vision", "Machine Learning", "Embedded Systems"],
    "Robotics Technician":       ["C++", "ROS", "Electrical Systems", "Pneumatics", "PLC", "Troubleshooting", "CAD"],
    "Mechatronics Engineer":     ["C", "C++", "Control Systems", "Electronics", "CAD", "MATLAB", "Embedded Systems", "PLC"],
    "Microsystems Engineer":     ["MEMS", "Semiconductor", "MATLAB", "Python", "Nanotechnology", "Signal Processing", "CAD"],
    "Photonics Engineer":        ["Optics", "Laser Systems", "Python", "MATLAB", "Signal Processing", "Fiber Optics"],
    "Nanosystems Engineer":      ["Nanofabrication", "Materials Science", "Python", "MATLAB", "Characterization", "Simulation"],
    "Electrical Engineer":       ["Circuit Design", "MATLAB", "C", "PCB Design", "Signal Processing", "Power Systems", "Embedded Systems"],
    "Electronics Engineer":      ["Circuit Design", "MATLAB", "C", "PCB Design", "Embedded Systems", "VHDL", "Signal Processing"],
    "Quantitative Analyst":      ["Python", "R", "Statistics", "Machine Learning", "Financial Modeling", "SQL", "Monte Carlo", "Risk Modeling"],
    "Intelligence Analyst":      ["Data Analysis", "Python", "OSINT", "SQL", "Critical Thinking", "Geopolitics", "Visualization"],
    "Technical Writer":          ["Technical Writing", "Documentation", "Markdown", "APIs", "Git", "XML", "Content Management"],
    "CS Educator":               ["Python", "Algorithms", "Data Structures", "Curriculum Design", "Teaching", "Research", "Communication"],
    "Media Technology Manager":  ["Media Systems", "Leadership", "Broadcasting", "Video Production", "Project Management"],
    "Audio Engineer":            ["Pro Tools", "Signal Processing", "Audio Mixing", "Acoustics", "DAW", "Sound Design"],
}

SALARY_MAP = {
    "Data Scientist":            "Rs.80L-Rs.134L",
    "Data Analyst":              "Rs.50L-Rs.92L",
    "Data Engineer":             "Rs.84L-Rs.134L",
    "Data Warehouse Engineer":   "Rs.80L-Rs.130L",
    "Machine Learning Engineer": "Rs.101L-Rs.151L",
    "AI Engineer":               "Rs.101L-Rs.160L",
    "Backend Developer":         "Rs.80L-Rs.130L",
    "Frontend Developer":        "Rs.71L-Rs.122L",
    "Full Stack Developer":      "Rs.76L-Rs.130L",
    "DevOps Engineer":           "Rs.84L-Rs.139L",
    "Cloud Engineer":            "Rs.88L-Rs.139L",
    "Cybersecurity Analyst":     "Rs.76L-Rs.126L",
    "Security Engineer":         "Rs.84L-Rs.143L",
    "Software Engineer":         "Rs.84L-Rs.139L",
    "Mobile Developer":          "Rs.80L-Rs.130L",
    "Database Administrator":    "Rs.67L-Rs.109L",
    "Data Architect":            "Rs.92L-Rs.147L",
    "Network Engineer":          "Rs.63L-Rs.109L",
    "Network Architect":         "Rs.84L-Rs.134L",
    "Site Reliability Engineer": "Rs.97L-Rs.147L",
    "Product Manager":           "Rs.80L-Rs.139L",
    "Business Analyst":          "Rs.55L-Rs.92L",
    "UX Designer":               "Rs.63L-Rs.113L",
    "NLP Engineer":              "Rs.97L-Rs.147L",
    "Computer Vision Engineer":  "Rs.97L-Rs.147L",
    "Embedded Systems Engineer": "Rs.71L-Rs.118L",
    "Blockchain Developer":      "Rs.84L-Rs.143L",
    "Game Developer":            "Rs.63L-Rs.113L",
    "IT Support Specialist":     "Rs.34L-Rs.63L",
    "Technical Writer":          "Rs.46L-Rs.80L",
    "Scrum Master":              "Rs.71L-Rs.118L",
    "Quantitative Analyst":      "Rs.92L-Rs.168L",
    "Prompt Engineer":           "Rs.76L-Rs.134L",
    "QA Engineer":               "Rs.50L-Rs.92L",
    "Solutions Architect":       "Rs.101L-Rs.168L",
    "Hardware Engineer":         "Rs.63L-Rs.109L",
    "Robotics Engineer":         "Rs.76L-Rs.130L",
    "Digital Forensics Analyst": "Rs.67L-Rs.113L",
    "Web Administrator":         "Rs.46L-Rs.84L",
    "Engineering Manager":       "Rs.126L-Rs.210L",
    "IT Project Manager":        "Rs.76L-Rs.130L",
    "Bioinformatics Scientist":  "Rs.71L-Rs.122L",
    "Bioinformatics Technician": "Rs.46L-Rs.84L",
    "GIS Specialist":            "Rs.50L-Rs.92L",
    "Remote Sensing Specialist": "Rs.55L-Rs.97L",
    "Telecom Engineer":          "Rs.63L-Rs.109L",
    "Electrical Engineer":       "Rs.63L-Rs.109L",
    "Electronics Engineer":      "Rs.63L-Rs.109L",
    "Intelligence Analyst":      "Rs.67L-Rs.113L",
    "Audio Engineer":            "Rs.42L-Rs.80L",
    "CS Educator":               "Rs.46L-Rs.84L",
    "Mechatronics Engineer":     "Rs.63L-Rs.109L",
    "Robotics Technician":       "Rs.42L-Rs.76L",
    "Clinical Data Manager":     "Rs.63L-Rs.113L",
    "Health Informatics Specialist": "Rs.67L-Rs.118L",
    "Media Technology Manager":  "Rs.63L-Rs.109L",
    "Microsystems Engineer":     "Rs.76L-Rs.130L",
    "Photonics Engineer":        "Rs.76L-Rs.130L",
    "Nanosystems Engineer":      "Rs.76L-Rs.130L",
}

DIFFICULTY_MAP = {
    "Data Scientist":            "Advanced",
    "Data Analyst":              "Intermediate",
    "Data Engineer":             "Advanced",
    "Data Warehouse Engineer":   "Intermediate",
    "Machine Learning Engineer": "Advanced",
    "AI Engineer":               "Advanced",
    "Backend Developer":         "Intermediate",
    "Frontend Developer":        "Intermediate",
    "Full Stack Developer":      "Advanced",
    "DevOps Engineer":           "Advanced",
    "Cloud Engineer":            "Advanced",
    "Cybersecurity Analyst":     "Advanced",
    "Security Engineer":         "Advanced",
    "Software Engineer":         "Intermediate",
    "Mobile Developer":          "Intermediate",
    "Database Administrator":    "Intermediate",
    "Data Architect":            "Advanced",
    "Network Engineer":          "Intermediate",
    "Network Architect":         "Advanced",
    "Site Reliability Engineer": "Advanced",
    "Product Manager":           "Intermediate",
    "Business Analyst":          "Beginner",
    "UX Designer":               "Intermediate",
    "NLP Engineer":              "Advanced",
    "Computer Vision Engineer":  "Advanced",
    "Embedded Systems Engineer": "Advanced",
    "Blockchain Developer":      "Advanced",
    "Game Developer":            "Intermediate",
    "IT Support Specialist":     "Beginner",
    "Technical Writer":          "Beginner",
    "Scrum Master":              "Intermediate",
    "Quantitative Analyst":      "Advanced",
    "Prompt Engineer":           "Intermediate",
    "QA Engineer":               "Intermediate",
    "Solutions Architect":       "Advanced",
    "Hardware Engineer":         "Advanced",
    "Robotics Engineer":         "Advanced",
    "Digital Forensics Analyst": "Advanced",
    "Web Administrator":         "Beginner",
    "Engineering Manager":       "Advanced",
    "IT Project Manager":        "Intermediate",
    "Bioinformatics Scientist":  "Advanced",
    "Bioinformatics Technician": "Intermediate",
    "GIS Specialist":            "Intermediate",
    "Remote Sensing Specialist": "Intermediate",
    "Telecom Engineer":          "Intermediate",
    "Electrical Engineer":       "Intermediate",
    "Electronics Engineer":      "Intermediate",
    "Intelligence Analyst":      "Intermediate",
    "Audio Engineer":            "Intermediate",
    "CS Educator":               "Intermediate",
    "Mechatronics Engineer":     "Advanced",
    "Robotics Technician":       "Intermediate",
    "Clinical Data Manager":     "Intermediate",
    "Health Informatics Specialist": "Intermediate",
    "Media Technology Manager":  "Intermediate",
    "Microsystems Engineer":     "Advanced",
    "Photonics Engineer":        "Advanced",
    "Nanosystems Engineer":      "Advanced",
    "Electronics Engineer":      "Intermediate",
}

SKILL_NAME_MAP = {
    "Programming":                       "Programming",
    "Technology Design":                 "System Design",
    "Complex Problem Solving":           "Problem Solving",
    "Critical Thinking":                 "Critical Thinking",
    "Active Learning":                   "Self-Learning",
    "Mathematics":                       "Mathematics",
    "Systems Analysis":                  "Systems Analysis",
    "Operations Analysis":               "Data Analysis",
    "Judgment and Decision Making":      "Decision Making",
    "Monitoring":                        "Monitoring",
    "Science":                           "Research",
    "Writing":                           "Technical Writing",
    "Speaking":                          "Communication",
    "Reading Comprehension":             "Documentation",
    "Coordination":                      "Coordination",
    "Instructing":                       "Mentoring",
    "Social Perceptiveness":             "Stakeholder Management",
    "Management of Personnel Resources": "Team Leadership",
    "Troubleshooting":                   "Debugging",
    "Quality Control Analysis":          "QA Testing",
    "Installation":                      "Deployment",
    "Operations Monitoring":             "System Monitoring",
    "Operation and Control":             "System Administration",
    "Equipment Selection":               "Tool Selection",
    "Systems Evaluation":                "System Evaluation",
    "Active Listening":                  "Communication",
    "Learning Strategies":               "Self-Learning",
}

# ── Load & process ────────────────────────────────────────────────────────
print("Loading O*NET Skills data...")
skills_df = pd.read_excel("Skills.xlsx")

imp = skills_df[
    (skills_df["Scale Name"] == "Importance") &
    (skills_df["Data Value"] >= 3.0)
][["Title", "Element Name", "Data Value"]].copy()

rows = []
seen = set()

for onet_title, sl_role in ONET_ROLE_MAP.items():
    if sl_role in seen:
        continue
    seen.add(sl_role)

    onet_skills = imp[imp["Title"] == onet_title].sort_values(
        "Data Value", ascending=False
    )["Element Name"].tolist()

    mapped = list(dict.fromkeys([
        SKILL_NAME_MAP[s] for s in onet_skills if s in SKILL_NAME_MAP
    ]))

    extra = EXTRA_SKILLS.get(sl_role, [])
    combined = extra + [s for s in mapped if s not in extra]
    combined = list(dict.fromkeys(combined))[:15]

    rows.append({
        "role":       sl_role,
        "skills":     ", ".join(combined),
        "salary":     SALARY_MAP.get(sl_role, "Rs.50L-Rs.100L"),
        "difficulty": DIFFICULTY_MAP.get(sl_role, "Intermediate"),
    })

for sl_role, skills in CUSTOM_ROLES.items():
    if sl_role in seen:
        continue
    seen.add(sl_role)
    rows.append({
        "role":       sl_role,
        "skills":     ", ".join(skills),
        "salary":     SALARY_MAP.get(sl_role, "Rs.50L-Rs.100L"),
        "difficulty": DIFFICULTY_MAP.get(sl_role, "Intermediate"),
    })

df = pd.DataFrame(rows).sort_values("role").reset_index(drop=True)
os.makedirs("data", exist_ok=True)
df.to_csv("data/job_skills.csv", index=False)

print(f"\nDone! {len(df)} roles written to data/job_skills.csv\n")
print(df[["role", "difficulty", "salary"]].to_string(index=False))
