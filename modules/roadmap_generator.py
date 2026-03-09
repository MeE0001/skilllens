"""
roadmap_generator.py
====================
Generates a prioritized learning roadmap for missing skills.
Skill names updated to match O*NET 30.2 data (fetch_onet_data.py output).
"""

# ── RESOURCES per skill ───────────────────────────────
RESOURCES = {
    # Languages
    "Python":           [("Python.org Tutorial", "https://docs.python.org/3/tutorial/"), ("freeCodeCamp Python", "https://www.freecodecamp.org/learn/scientific-computing-with-python/")],
    "SQL":              [("SQLZoo", "https://sqlzoo.net/"), ("Mode SQL Tutorial", "https://mode.com/sql-tutorial/")],
    "JavaScript":       [("javascript.info", "https://javascript.info/"), ("freeCodeCamp JS", "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/")],
    "TypeScript":       [("TypeScript Handbook", "https://www.typescriptlang.org/docs/handbook/intro.html"), ("Total TypeScript", "https://www.totaltypescript.com/")],
    "Java":             [("Java Tutorial - Oracle", "https://docs.oracle.com/javase/tutorial/"), ("Codecademy Java", "https://www.codecademy.com/learn/learn-java")],
    "C++":              [("learncpp.com", "https://www.learncpp.com/"), ("cppreference.com", "https://en.cppreference.com/")],
    "C#":               [("Microsoft C# Docs", "https://learn.microsoft.com/en-us/dotnet/csharp/"), ("C# Station", "https://csharp-station.com/Tutorial/CSharp/")],
    "Go":               [("Tour of Go", "https://tour.golang.org/"), ("Go by Example", "https://gobyexample.com/")],
    "Rust":             [("The Rust Book", "https://doc.rust-lang.org/book/"), ("Rust by Example", "https://doc.rust-lang.org/rust-by-example/")],
    "R":                [("R for Data Science", "https://r4ds.had.co.nz/"), ("Swirl - Learn R", "https://swirlstats.com/")],
    "Swift":            [("Swift.org", "https://www.swift.org/getting-started/"), ("Hacking with Swift", "https://www.hackingwithswift.com/")],
    "Kotlin":           [("Kotlin Docs", "https://kotlinlang.org/docs/getting-started.html"), ("Kotlin Koans", "https://kotlinlang.org/docs/koans.html")],
    "Scala":            [("Scala Tour", "https://docs.scala-lang.org/tour/tour-of-scala.html"), ("Scala Exercises", "https://www.scala-exercises.org/")],
    "MATLAB":           [("MATLAB Onramp", "https://matlabacademy.mathworks.com/"), ("MATLAB Docs", "https://www.mathworks.com/help/matlab/")],
    "Shell":            [("The Linux Command Line", "https://linuxcommand.org/tlcl.php"), ("Bash Guide", "https://mywiki.wooledge.org/BashGuide")],
    "Bash":             [("Bash Scripting Tutorial", "https://linuxconfig.org/bash-scripting-tutorial"), ("ShellCheck", "https://www.shellcheck.net/")],

    # Cloud
    "AWS":              [("AWS Skill Builder", "https://skillbuilder.aws/"), ("AWS Free Tier", "https://aws.amazon.com/free/")],
    "Azure":            [("Microsoft Learn Azure", "https://learn.microsoft.com/en-us/training/azure/"), ("Azure Free Account", "https://azure.microsoft.com/en-us/free/")],
    "GCP":              [("Google Cloud Skills Boost", "https://cloudskillsboost.google/"), ("GCP Free Tier", "https://cloud.google.com/free")],
    "Terraform":        [("Terraform Tutorials", "https://developer.hashicorp.com/terraform/tutorials"), ("Terraform Docs", "https://developer.hashicorp.com/terraform/docs")],
    "Ansible":          [("Ansible Docs", "https://docs.ansible.com/"), ("Ansible for Beginners - YouTube", "https://www.youtube.com/watch?v=1id6ERvfozo")],

    # Containers / DevOps
    "Docker":           [("Docker Getting Started", "https://docs.docker.com/get-started/"), ("Play with Docker", "https://labs.play-with-docker.com/")],
    "Kubernetes":       [("Kubernetes.io Tutorials", "https://kubernetes.io/docs/tutorials/"), ("KillerCoda K8s", "https://killercoda.com/kubernetes")],
    "CI/CD":            [("GitHub Actions Docs", "https://docs.github.com/en/actions"), ("GitLab CI/CD Docs", "https://docs.gitlab.com/ee/ci/")],
    "Git":              [("Pro Git Book", "https://git-scm.com/book/en/v2"), ("Learn Git Branching", "https://learngitbranching.js.org/")],
    "GitHub":           [("GitHub Skills", "https://skills.github.com/"), ("GitHub Docs", "https://docs.github.com/")],
    "GitHub Actions":   [("GitHub Actions Docs", "https://docs.github.com/en/actions"), ("GitHub Actions Tutorial", "https://www.youtube.com/watch?v=R8_veQiYBjI")],
    "Linux":            [("The Linux Command Line", "https://linuxcommand.org/tlcl.php"), ("OverTheWire: Bandit", "https://overthewire.org/wargames/bandit/")],

    # AI / ML
    "Machine Learning": [("fast.ai", "https://www.fast.ai/"), ("Coursera ML Specialization", "https://www.coursera.org/specializations/machine-learning-introduction")],
    "Deep Learning":    [("fast.ai Deep Learning", "https://course.fast.ai/"), ("Deep Learning Book", "https://www.deeplearningbook.org/")],
    "TensorFlow":       [("TensorFlow Tutorials", "https://www.tensorflow.org/tutorials"), ("TF Playground", "https://playground.tensorflow.org/")],
    "PyTorch":          [("PyTorch Tutorials", "https://pytorch.org/tutorials/"), ("Deep Learning with PyTorch", "https://pytorch.org/assets/deep-learning/Deep-Learning-with-PyTorch.pdf")],
    "Scikit-learn":     [("Scikit-learn Docs", "https://scikit-learn.org/stable/user_guide.html"), ("Kaggle ML Course", "https://www.kaggle.com/learn/intro-to-machine-learning")],
    "NLP":              [("HuggingFace NLP Course", "https://huggingface.co/learn/nlp-course"), ("Stanford NLP", "https://web.stanford.edu/class/cs224n/")],
    "LangChain":        [("LangChain Docs", "https://python.langchain.com/docs/get_started/introduction"), ("LangChain Crash Course", "https://www.youtube.com/watch?v=lG7Uxts9SXs")],
    "Statistics":       [("StatQuest YouTube", "https://www.youtube.com/@statquest"), ("Khan Academy Stats", "https://www.khanacademy.org/math/statistics-probability")],
    "Algorithms":       [("LeetCode", "https://leetcode.com/"), ("NeetCode.io", "https://neetcode.io/")],
    "Spark":            [("Apache Spark Docs", "https://spark.apache.org/docs/latest/"), ("Databricks Free Training", "https://www.databricks.com/learn/training/catalog")],
    "Hadoop":           [("Hadoop Docs", "https://hadoop.apache.org/docs/stable/"), ("Udemy Hadoop Basics", "https://www.udemy.com/course/the-ultimate-hands-on-hadoop/")],

    # Data
    "Pandas":           [("Pandas Docs", "https://pandas.pydata.org/docs/user_guide/index.html"), ("Kaggle Pandas Course", "https://www.kaggle.com/learn/pandas")],
    "NumPy":            [("NumPy Quickstart", "https://numpy.org/doc/stable/user/quickstart.html"), ("NumPy Tutorial - freeCodeCamp", "https://www.freecodecamp.org/news/the-ultimate-guide-to-the-numpy-scientific-computing-library-for-python/")],
    "Tableau":          [("Tableau Free Training", "https://www.tableau.com/learn/training"), ("Tableau Public", "https://public.tableau.com/")],
    "Power BI":         [("Microsoft Power BI Learn", "https://learn.microsoft.com/en-us/training/powerplatform/power-bi"), ("Guy in a Cube - YouTube", "https://www.youtube.com/@GuyInACube")],
    "Excel":            [("Excel Jet", "https://exceljet.net/"), ("Microsoft Excel Training", "https://support.microsoft.com/en-us/office/excel-training")],
    "dbt":              [("dbt Docs", "https://docs.getdbt.com/docs/introduction"), ("dbt Learn", "https://courses.getdbt.com/collections")],
    "Snowflake":        [("Snowflake University", "https://learn.snowflake.com/"), ("Snowflake Quickstarts", "https://quickstarts.snowflake.com/")],
    "Airflow":          [("Airflow Docs", "https://airflow.apache.org/docs/"), ("Astronomer Learn", "https://docs.astronomer.io/learn")],
    "Kafka":            [("Confluent Kafka Tutorials", "https://developer.confluent.io/learn-kafka/"), ("Kafka Docs", "https://kafka.apache.org/documentation/")],
    "Databricks":       [("Databricks Academy", "https://www.databricks.com/learn/training/catalog"), ("Databricks Community Edition", "https://community.cloud.databricks.com/")],

    # Databases
    "PostgreSQL":       [("PostgreSQL Tutorial", "https://www.postgresqltutorial.com/"), ("PostgreSQL Docs", "https://www.postgresql.org/docs/")],
    "MySQL":            [("MySQL Tutorial", "https://www.mysqltutorial.org/"), ("MySQL Docs", "https://dev.mysql.com/doc/")],
    "MongoDB":          [("MongoDB University", "https://learn.mongodb.com/"), ("MongoDB Docs", "https://www.mongodb.com/docs/")],
    "Redis":            [("Redis University", "https://university.redis.com/"), ("Redis Docs", "https://redis.io/docs/")],

    # Web / Frontend
    "React":            [("React Docs", "https://react.dev/learn"), ("Scrimba React Course", "https://scrimba.com/learn/learnreact")],
    "Node.js":          [("Node.js Docs", "https://nodejs.org/en/docs/"), ("The Odin Project Node", "https://www.theodinproject.com/paths/full-stack-javascript")],
    "Next.js":          [("Next.js Learn", "https://nextjs.org/learn"), ("Next.js Docs", "https://nextjs.org/docs")],
    "HTML":             [("MDN HTML Guide", "https://developer.mozilla.org/en-US/docs/Learn/HTML"), ("freeCodeCamp HTML", "https://www.freecodecamp.org/learn/responsive-web-design/")],
    "CSS":              [("CSS Tricks", "https://css-tricks.com/"), ("Kevin Powell - YouTube", "https://www.youtube.com/@KevinPowell")],
    "FastAPI":          [("FastAPI Docs", "https://fastapi.tiangolo.com/"), ("Full Stack FastAPI Tutorial", "https://fastapi.tiangolo.com/tutorial/")],
    "Django":           [("Django Official Tutorial", "https://docs.djangoproject.com/en/stable/intro/tutorial01/"), ("Django Girls", "https://tutorial.djangogirls.org/")],
    "Flask":            [("Flask Docs", "https://flask.palletsprojects.com/en/latest/tutorial/"), ("Miguel Grinberg Flask Blog", "https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world")],

    # Cybersecurity
    "Cybersecurity":    [("TryHackMe", "https://tryhackme.com/"), ("Cybrary", "https://www.cybrary.it/")],
    "Network Security": [("CompTIA Security+ Study", "https://www.comptia.org/certifications/security"), ("Professor Messer - YouTube", "https://www.youtube.com/@professormesser")],
    "Penetration Testing": [("HackTheBox", "https://www.hackthebox.com/"), ("TryHackMe Pentest", "https://tryhackme.com/path/outline/jrpenetrationtester")],

    # Mobile
    "Flutter":          [("Flutter Docs", "https://docs.flutter.dev/get-started/codelab"), ("Flutter YouTube", "https://www.youtube.com/@flutterdev")],
    "React Native":     [("React Native Docs", "https://reactnative.dev/docs/getting-started"), ("Expo Go", "https://expo.dev/go")],
    "Swift":            [("Swift.org", "https://www.swift.org/getting-started/"), ("Hacking with Swift", "https://www.hackingwithswift.com/")],

    # Design
    "Figma":            [("Figma Learn", "https://www.figma.com/resources/learn-design/"), ("DesignCourse - YouTube", "https://www.youtube.com/@DesignCourse")],
    "UX Research":      [("Google UX Design Certificate", "https://www.coursera.org/professional-certificates/google-ux-design"), ("NN/g UX Research", "https://www.nngroup.com/articles/ux-research-cheat-sheet/")],

    # Project Management
    "Agile":            [("Atlassian Agile Guide", "https://www.atlassian.com/agile"), ("Scrum.org", "https://www.scrum.org/resources/what-is-scrum")],
    "Scrum":            [("Scrum Guide", "https://scrumguides.org/scrum-guide.html"), ("Scrum.org", "https://www.scrum.org/")],
    "Jira":             [("Atlassian Jira Training", "https://www.atlassian.com/software/jira/guides"), ("Jira Tutorial - YouTube", "https://www.youtube.com/watch?v=uM_m6EzMg3k")],

    # Blockchain
    "Solidity":         [("CryptoZombies", "https://cryptozombies.io/"), ("Solidity Docs", "https://docs.soliditylang.org/")],
    "Blockchain":       [("MIT Blockchain Course", "https://ocw.mit.edu/courses/mas-s62-cryptocurrency-engineering-and-design-spring-2018/"), ("Binance Academy", "https://academy.binance.com/")],

    # Gaming
    "Unity":            [("Unity Learn", "https://learn.unity.com/"), ("Unity YouTube", "https://www.youtube.com/@unity")],

    # IoT / Embedded
    "IoT":              [("Arduino Tutorials", "https://www.arduino.cc/en/Tutorial/HomePage"), ("Coursera IoT Specialization", "https://www.coursera.org/specializations/iot")],

    # Misc
    "Prompt Engineering": [("Anthropic Prompt Engineering", "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview"), ("OpenAI Prompt Guide", "https://platform.openai.com/docs/guides/prompt-engineering")],
    "Microservices":    [("Martin Fowler Microservices", "https://martinfowler.com/articles/microservices.html"), ("Microservices.io", "https://microservices.io/")],
    "REST APIs":        [("REST API Tutorial", "https://restfulapi.net/"), ("Postman Learning", "https://learning.postman.com/")],
    "APIs":             [("REST API Tutorial", "https://restfulapi.net/"), ("Postman Learning", "https://learning.postman.com/")],
    "Data Modeling":    [("dbt Data Modeling", "https://docs.getdbt.com/terms/data-modeling"), ("Vertabelo Academy", "https://vertabelo.com/blog/data-modeling-101/")],
    "ETL":              [("ETL Fundamentals", "https://www.talend.com/resources/what-is-etl/"), ("Apache Nifi Docs", "https://nifi.apache.org/docs.html")],
    "Elasticsearch":    [("Elastic Docs", "https://www.elastic.co/guide/index.html"), ("Elastic Free Training", "https://www.elastic.co/training/")],
}

# ── PRIORITY: maps skill → "High" / "Medium" / "Low" ─
# Based on O*NET Hot Technology flags + 2025 job market demand
SKILL_PRIORITY = {
    # High — core, universally required, hot technology
    "Python": "High", "SQL": "High", "Machine Learning": "High",
    "AWS": "High", "Docker": "High", "Kubernetes": "High",
    "Git": "High", "CI/CD": "High", "Linux": "High",
    "JavaScript": "High", "Statistics": "High", "Deep Learning": "High",
    "PyTorch": "High", "TensorFlow": "High", "React": "High",
    "Cybersecurity": "High", "Azure": "High", "Cloud": "High",
    "Algorithms": "High", "Data Modeling": "High",
    "REST APIs": "High", "APIs": "High", "Node.js": "High",
    "GitHub": "High", "GitHub Actions": "High",

    # Medium — important, role-specific tools
    "TypeScript": "Medium", "Pandas": "Medium", "NumPy": "Medium",
    "Scikit-learn": "Medium", "Terraform": "Medium", "Airflow": "Medium",
    "Kafka": "Medium", "Spark": "Medium", "Snowflake": "Medium",
    "PostgreSQL": "Medium", "MongoDB": "Medium", "Redis": "Medium",
    "Power BI": "Medium", "Tableau": "Medium", "Excel": "Medium",
    "FastAPI": "Medium", "Django": "Medium", "Flask": "Medium",
    "NLP": "Medium", "LangChain": "Medium", "GCP": "Medium",
    "Databricks": "Medium", "dbt": "Medium", "Next.js": "Medium",
    "Network Security": "Medium", "Penetration Testing": "Medium",
    "Agile": "Medium", "Scrum": "Medium", "Figma": "Medium",
    "Microservices": "Medium", "Ansible": "Medium",
    "Flutter": "Medium", "React Native": "Medium",
    "ETL": "Medium", "Data Warehousing": "Medium",
    "Prompt Engineering": "Medium",

    # Low — useful but niche or supplementary
    "Java": "Low", "C++": "Low", "C#": "Low", "Go": "Low",
    "Rust": "Low", "Scala": "Low", "R": "Low", "MATLAB": "Low",
    "Shell": "Low", "Bash": "Low", "Hadoop": "Low",
    "MySQL": "Low", "SQL Server": "Low", "Elasticsearch": "Low",
    "HTML": "Low", "CSS": "Low", "Jira": "Low",
    "Solidity": "Low", "Blockchain": "Low", "Unity": "Low",
    "IoT": "Low", "Swift": "Low", "Kotlin": "Low",
    "UX Research": "Low",
}

# ── TIME ESTIMATES per skill ──────────────────────────
SKILL_TIME = {
    "Python": "3–6 months", "SQL": "2–4 weeks", "Machine Learning": "4–6 months",
    "Deep Learning": "3–5 months", "Statistics": "2–3 months",
    "PyTorch": "2–3 months", "TensorFlow": "2–3 months",
    "AWS": "2–3 months", "Azure": "2–3 months", "GCP": "2–3 months",
    "Docker": "3–4 weeks", "Kubernetes": "2–3 months",
    "Terraform": "4–6 weeks", "Git": "1–2 weeks", "Linux": "4–6 weeks",
    "CI/CD": "3–4 weeks", "GitHub Actions": "2–3 weeks",
    "JavaScript": "3–5 months", "TypeScript": "4–6 weeks",
    "React": "2–3 months", "Node.js": "2–3 months", "Next.js": "4–6 weeks",
    "FastAPI": "2–3 weeks", "Django": "4–6 weeks", "Flask": "2–3 weeks",
    "Pandas": "3–4 weeks", "NumPy": "2–3 weeks", "Scikit-learn": "4–6 weeks",
    "Spark": "6–8 weeks", "Kafka": "4–6 weeks", "Airflow": "3–4 weeks",
    "Snowflake": "3–4 weeks", "dbt": "2–3 weeks", "Databricks": "4–6 weeks",
    "PostgreSQL": "3–4 weeks", "MongoDB": "2–3 weeks", "Redis": "1–2 weeks",
    "Tableau": "3–4 weeks", "Power BI": "3–4 weeks", "Excel": "2–3 weeks",
    "NLP": "3–5 months", "LangChain": "3–4 weeks",
    "Prompt Engineering": "1–2 weeks", "Algorithms": "3–6 months",
    "Cybersecurity": "3–6 months", "Network Security": "2–3 months",
    "Penetration Testing": "3–6 months", "Agile": "1–2 weeks",
    "Scrum": "1–2 weeks", "Figma": "3–4 weeks",
    "Flutter": "2–3 months", "React Native": "2–3 months",
    "Blockchain": "2–3 months", "Solidity": "2–3 months",
    "Java": "3–5 months", "C++": "4–6 months", "Go": "2–3 months",
    "Rust": "3–5 months", "R": "2–3 months", "Scala": "2–3 months",
}

# ── DIFFICULTY per skill ──────────────────────────────
SKILL_DIFFICULTY = {
    "Python": "Beginner", "SQL": "Beginner", "Git": "Beginner",
    "HTML": "Beginner", "CSS": "Beginner", "Excel": "Beginner",
    "Agile": "Beginner", "Scrum": "Beginner", "Prompt Engineering": "Beginner",
    "Pandas": "Intermediate", "NumPy": "Intermediate", "Scikit-learn": "Intermediate",
    "Docker": "Intermediate", "Linux": "Intermediate", "PostgreSQL": "Intermediate",
    "MongoDB": "Intermediate", "Redis": "Intermediate", "MySQL": "Intermediate",
    "Tableau": "Intermediate", "Power BI": "Intermediate",
    "JavaScript": "Intermediate", "TypeScript": "Intermediate",
    "React": "Intermediate", "Node.js": "Intermediate",
    "FastAPI": "Intermediate", "Django": "Intermediate", "Flask": "Intermediate",
    "AWS": "Intermediate", "Azure": "Intermediate", "GCP": "Intermediate",
    "Terraform": "Intermediate", "CI/CD": "Intermediate",
    "GitHub Actions": "Intermediate", "Figma": "Intermediate",
    "Airflow": "Intermediate", "dbt": "Intermediate", "Snowflake": "Intermediate",
    "Machine Learning": "Advanced", "Deep Learning": "Advanced",
    "PyTorch": "Advanced", "TensorFlow": "Advanced", "Statistics": "Advanced",
    "NLP": "Advanced", "LangChain": "Intermediate", "Algorithms": "Advanced",
    "Kubernetes": "Advanced", "Spark": "Advanced", "Kafka": "Advanced",
    "Databricks": "Intermediate", "Cybersecurity": "Advanced",
    "Network Security": "Advanced", "Penetration Testing": "Advanced",
    "Microservices": "Advanced", "Go": "Intermediate", "Rust": "Advanced",
    "Scala": "Advanced", "Java": "Intermediate", "C++": "Advanced",
    "Blockchain": "Advanced", "Solidity": "Advanced",
}

DEFAULT_RESOURCES = [("Google", "https://www.google.com/search?q=learn+{skill}")]


def generate_roadmap(missing_skills: list) -> list:
    """
    Given a list of missing skill names, return a sorted list of step dicts.
    Priority order: High → Medium → Low → Unknown.
    Within same priority, harder skills come first (learn early).
    """
    PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2, "Unknown": 3}
    DIFFICULTY_ORDER = {"Advanced": 0, "Intermediate": 1, "Beginner": 2}

    steps = []
    for i, skill in enumerate(missing_skills, 1):
        # Fuzzy match priority — try exact, then case-insensitive, then partial
        priority = SKILL_PRIORITY.get(skill)
        if not priority:
            skill_lower = skill.lower()
            for k, v in SKILL_PRIORITY.items():
                if k.lower() == skill_lower:
                    priority = v
                    break
        if not priority:
            for k, v in SKILL_PRIORITY.items():
                if skill_lower in k.lower() or k.lower() in skill_lower:
                    priority = v
                    break
        if not priority:
            priority = "Medium"  # default — don't drop skills

        difficulty = SKILL_DIFFICULTY.get(skill, "Intermediate")
        time_est   = SKILL_TIME.get(skill, "4–6 weeks")

        # Get resources — try exact, then fuzzy
        resources = RESOURCES.get(skill)
        if not resources:
            for k, v in RESOURCES.items():
                if k.lower() == skill.lower():
                    resources = v
                    break
        if not resources:
            resources = [("Search: Learn " + skill, "https://www.google.com/search?q=learn+" + skill.replace(" ", "+"))]

        steps.append({
            "skill":        skill,
            "priority":     priority,
            "difficulty":   difficulty,
            "time":         time_est,
            "resources":    resources,
            "sort_key":     (PRIORITY_ORDER.get(priority, 3), DIFFICULTY_ORDER.get(difficulty, 1)),
        })

    # Sort: High first, then by difficulty within each priority
    steps.sort(key=lambda x: x["sort_key"])

    # Add step numbers after sorting
    for i, step in enumerate(steps, 1):
        step["step"] = i

    return steps