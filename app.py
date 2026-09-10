import streamlit as st
import pandas as pd
import joblib
import os

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Personalized Learning Recommendation System",
    page_icon="🎓",
    layout="wide"
)

# ============================================================
# TITLE
# ============================================================

st.title("🎓 Personalized Learning Recommendation System")

st.write(
    "An ML-based system that recommends personalized learning "
    "content for engineering students based on their academic "
    "performance, branch, career goal, skill gaps and quiz level."
)

st.divider()

# ============================================================
# FILE NAMES
# ============================================================

MODEL_FILE = "model.joblib"
ENCODER_FILE = "encoders.joblib"
DATASET_FILE = "Personalized_Learning_Recommendation_Dataset_1000.xlsx"

# ============================================================
# SESSION STATE
# ============================================================

if "step" not in st.session_state:
    st.session_state.step = 1

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

if "quiz_percentage" not in st.session_state:
    st.session_state.quiz_percentage = 0

if "quiz_level" not in st.session_state:
    st.session_state.quiz_level = ""

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = ""

if "recommended_course" not in st.session_state:
    st.session_state.recommended_course = None

# ============================================================
# CHECK FILES
# ============================================================

if not os.path.exists(MODEL_FILE):

    st.error(
        "❌ model.joblib not found. "
        "Please keep model.joblib in the same folder as app.py."
    )

    st.stop()


if not os.path.exists(ENCODER_FILE):

    st.error(
        "❌ encoders.joblib not found. "
        "Please keep encoders.joblib in the same folder as app.py."
    )

    st.stop()


if not os.path.exists(DATASET_FILE):

    st.error(
        "❌ Dataset not found. Please keep "
        "Personalized_Learning_Recommendation_Dataset_1000.xlsx "
        "in the same folder as app.py."
    )

    st.stop()

# ============================================================
# LOAD MODEL AND ENCODERS
# ============================================================

try:

    model = joblib.load(MODEL_FILE)

    encoders = joblib.load(ENCODER_FILE)

    branch_encoder = encoders["branch_encoder"]

    career_encoder = encoders["career_encoder"]

    course_encoder = encoders["course_encoder"]

except Exception as e:

    st.error("❌ Error loading ML model or encoders.")

    st.code(str(e))

    st.stop()

# ============================================================
# LOAD DATASET
# ============================================================

try:

    courses = pd.read_excel(
        DATASET_FILE,
        sheet_name="Courses_Resources"
    )

except Exception as e:

    st.error("❌ Error reading Excel dataset.")

    st.code(str(e))

    st.stop()

# ============================================================
# QUIZ QUESTIONS
# ============================================================

quiz_questions = {

    "Python": [

        {
            "question":
            "Which keyword is used to define a function in Python?",

            "options":
            [
                "function",
                "def",
                "define",
                "fun"
            ],

            "answer":
            "def"
        },

        {
            "question":
            "Which data type is immutable in Python?",

            "options":
            [
                "List",
                "Dictionary",
                "Tuple",
                "Set"
            ],

            "answer":
            "Tuple"
        },

        {
            "question":
            "Which symbol is used for comments in Python?",

            "options":
            [
                "//",
                "#",
                "/*",
                "--"
            ],

            "answer":
            "#"
        },

        {
            "question":
            "Which function is used to display output in Python?",

            "options":
            [
                "display()",
                "show()",
                "print()",
                "output()"
            ],

            "answer":
            "print()"
        },

        {
            "question":
            "Which collection stores key-value pairs?",

            "options":
            [
                "List",
                "Tuple",
                "Dictionary",
                "Set"
            ],

            "answer":
            "Dictionary"
        }

    ],

    "Java": [

        {
            "question":
            "Which keyword is used for inheritance in Java?",

            "options":
            [
                "inherit",
                "extends",
                "implements",
                "inherits"
            ],

            "answer":
            "extends"
        },

        {
            "question":
            "Which method is the entry point of a Java program?",

            "options":
            [
                "start()",
                "run()",
                "main()",
                "execute()"
            ],

            "answer":
            "main()"
        },

        {
            "question":
            "Which keyword is used to create an object in Java?",

            "options":
            [
                "create",
                "object",
                "new",
                "make"
            ],

            "answer":
            "new"
        },

        {
            "question":
            "Java is primarily which type of programming language?",

            "options":
            [
                "Object-oriented",
                "Markup",
                "Query",
                "Assembly"
            ],

            "answer":
            "Object-oriented"
        },

        {
            "question":
            "Which symbol is used to end a statement in Java?",

            "options":
            [
                ".",
                ",",
                ";",
                ":"
            ],

            "answer":
            ";"
        }

    ],

    "C++": [

        {
            "question":
            "Which symbol is used to end a statement in C++?",

            "options":
            [
                ".",
                ",",
                ";",
                ":"
            ],

            "answer":
            ";"
        },

        {
            "question":
            "Which feature allows the same function name with different parameters?",

            "options":
            [
                "Inheritance",
                "Overloading",
                "Encapsulation",
                "Abstraction"
            ],

            "answer":
            "Overloading"
        },

        {
            "question":
            "Which operator is used to access a member through a pointer?",

            "options":
            [
                ".",
                "::",
                "->",
                "&"
            ],

            "answer":
            "->"
        },

        {
            "question":
            "Which header is commonly used for input and output in C++?",

            "options":
            [
                "stdio.h",
                "iostream",
                "string.h",
                "math.h"
            ],

            "answer":
            "iostream"
        },

        {
            "question":
            "C++ supports which programming paradigm?",

            "options":
            [
                "Object-oriented",
                "Only procedural",
                "Only functional",
                "Only declarative"
            ],

            "answer":
            "Object-oriented"
        }

    ],

    "SQL": [

        {
            "question":
            "Which SQL command is used to retrieve data?",

            "options":
            [
                "GET",
                "SELECT",
                "FETCH",
                "READ"
            ],

            "answer":
            "SELECT"
        },

        {
            "question":
            "Which command is used to remove a table?",

            "options":
            [
                "DELETE",
                "REMOVE",
                "DROP",
                "CLEAR"
            ],

            "answer":
            "DROP"
        },

        {
            "question":
            "Which clause is used to filter rows in SQL?",

            "options":
            [
                "WHERE",
                "FILTER",
                "CHECK",
                "SELECT"
            ],

            "answer":
            "WHERE"
        },

        {
            "question":
            "Which key uniquely identifies a row?",

            "options":
            [
                "Foreign Key",
                "Primary Key",
                "Candidate Key",
                "Secondary Key"
            ],

            "answer":
            "Primary Key"
        },

        {
            "question":
            "Which command adds a new row to a table?",

            "options":
            [
                "ADD",
                "INSERT",
                "UPDATE",
                "CREATE"
            ],

            "answer":
            "INSERT"
        }

    ],

    "HTML": [

        {
            "question":
            "HTML is mainly used to create what?",

            "options":
            [
                "Web page structure",
                "Database",
                "Operating system",
                "Network"
            ],

            "answer":
            "Web page structure"
        },

        {
            "question":
            "Which HTML tag creates a hyperlink?",

            "options":
            [
                "<link>",
                "<a>",
                "<href>",
                "<url>"
            ],

            "answer":
            "<a>"
        },

        {
            "question":
            "Which tag creates the largest heading?",

            "options":
            [
                "<h6>",
                "<head>",
                "<h1>",
                "<heading>"
            ],

            "answer":
            "<h1>"
        },

        {
            "question":
            "Which tag is used to insert an image?",

            "options":
            [
                "<image>",
                "<img>",
                "<picture>",
                "<src>"
            ],

            "answer":
            "<img>"
        },

        {
            "question":
            "Which attribute specifies the image path?",

            "options":
            [
                "href",
                "src",
                "link",
                "path"
            ],

            "answer":
            "src"
        }

    ],

    "Data Structures": [

        {
            "question":
            "Which data structure follows LIFO?",

            "options":
            [
                "Queue",
                "Stack",
                "Array",
                "Graph"
            ],

            "answer":
            "Stack"
        },

        {
            "question":
            "Which data structure follows FIFO?",

            "options":
            [
                "Stack",
                "Queue",
                "Tree",
                "Graph"
            ],

            "answer":
            "Queue"
        },

        {
            "question":
            "Which structure consists of nodes connected by edges?",

            "options":
            [
                "Array",
                "Graph",
                "Stack",
                "Queue"
            ],

            "answer":
            "Graph"
        },

        {
            "question":
            "Which data structure represents hierarchical relationships?",

            "options":
            [
                "Tree",
                "Queue",
                "Array",
                "Stack"
            ],

            "answer":
            "Tree"
        },

        {
            "question":
            "Binary search is normally applied to what kind of array?",

            "options":
            [
                "Unsorted array",
                "Sorted array",
                "Empty array only",
                "Random array"
            ],

            "answer":
            "Sorted array"
        }

    ]

}

# ============================================================
# STEP 1
# STUDENT PROFILE
# ============================================================

if st.session_state.step == 1:

    st.header("1️⃣ Student Profile")

    st.write(
        "Enter your academic and learning information."
    )

    st.info(
        "💡 Complete your profile first. "
        "After this, you will take a short skill quiz."
    )

    branches = list(
        branch_encoder.classes_
    )

    career_goals = list(
        career_encoder.classes_
    )

    selected_branch = st.selectbox(
        "🎓 Engineering Branch",
        branches
    )

    selected_career = st.selectbox(
        "💼 Career Goal",
        career_goals
    )

    col1, col2 = st.columns(2)

    with col1:

        semester = st.slider(
            "📚 Semester",
            min_value=1,
            max_value=8,
            value=4
        )

    with col2:

        time_available = st.slider(
            "⏰ Available Learning Hours / Week",
            min_value=1,
            max_value=40,
            value=10
        )

    col1, col2 = st.columns(2)

    with col1:

        average_score = st.slider(
            "📊 Average Assessment Score",
            min_value=0,
            max_value=100,
            value=65
        )

    with col2:

        lowest_score = st.slider(
            "📉 Lowest Assessment Score",
            min_value=0,
            max_value=100,
            value=50
        )

    skill_gap_count = st.slider(
        "⚠️ Number of Skill Gaps",
        min_value=0,
        max_value=10,
        value=2
    )

    st.divider()

    if st.button(
        "➡️ Continue to Quiz",
        use_container_width=True
    ):

        # Save profile information

        st.session_state.selected_branch = selected_branch

        st.session_state.selected_career = selected_career

        st.session_state.semester = semester

        st.session_state.time_available = time_available

        st.session_state.average_score = average_score

        st.session_state.lowest_score = lowest_score

        st.session_state.skill_gap_count = skill_gap_count

        # Go to quiz

        st.session_state.step = 2

        st.rerun()


# ============================================================
# STEP 2
# QUIZ
# ============================================================

elif st.session_state.step == 2:

    st.header("2️⃣ Quick Skill Quiz")

    st.write(
        "Test your current knowledge before receiving your "
        "personalized learning recommendation."
    )

    st.info(
        "⚠️ You must answer every question before submitting."
    )

    # --------------------------------------------------------
    # PROFILE SUMMARY
    # --------------------------------------------------------

    st.subheader("👤 Your Profile")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Branch",
            st.session_state.selected_branch
        )

    with col2:

        st.metric(
            "Career Goal",
            st.session_state.selected_career
        )

    with col3:

        st.metric(
            "Semester",
            st.session_state.semester
        )

    with col4:

        st.metric(
            "Learning Hours",
            f"{st.session_state.time_available} hrs"
        )

    st.divider()

    # --------------------------------------------------------
    # TOPIC
    # --------------------------------------------------------

    available_topics = list(
        quiz_questions.keys()
    )

    selected_topic = st.selectbox(
        "📚 Select Quiz Topic",
        available_topics,
        key="quiz_topic"
    )

    st.session_state.selected_topic = selected_topic

    questions = quiz_questions[selected_topic]

    st.divider()

    st.subheader(
        f"📝 {selected_topic} Quiz"
    )

    # --------------------------------------------------------
    # QUESTIONS
    # --------------------------------------------------------

    for i, question in enumerate(questions):

        st.write(
            f"### Question {i + 1}"
        )

        st.write(
            question["question"]
        )

        # IMPORTANT:
        # No answer is selected by default.

        answer_options = [
            "-- Select an answer --"
        ] + question["options"]

        st.radio(
            "Choose your answer:",
            answer_options,
            index=0,
            key=f"quiz_{selected_topic}_{i}"
        )

        st.divider()

    # --------------------------------------------------------
    # SUBMIT QUIZ
    # --------------------------------------------------------

    if st.button(
        "✅ Submit Quiz",
        use_container_width=True
    ):

        unanswered = []

        for i in range(len(questions)):

            selected_answer = st.session_state.get(
                f"quiz_{selected_topic}_{i}"
            )

            if (
                selected_answer is None
                or
                selected_answer == "-- Select an answer --"
            ):

                unanswered.append(i + 1)

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if len(unanswered) > 0:

            st.error(
                "❌ Please answer all questions before submitting."
            )

            st.warning(
                "Unanswered question(s): "
                +
                ", ".join(
                    map(str, unanswered)
                )
            )

        else:

            score = 0

            # ------------------------------------------------
            # CALCULATE SCORE
            # ------------------------------------------------

            for i, question in enumerate(questions):

                selected_answer = st.session_state.get(
                    f"quiz_{selected_topic}_{i}"
                )

                if selected_answer == question["answer"]:

                    score += 1

            percentage = (
                score / len(questions)
            ) * 100

            # ------------------------------------------------
            # DETERMINE LEVEL
            # ------------------------------------------------

            if percentage < 40:

                level = "Beginner"

            elif percentage < 70:

                level = "Intermediate"

            else:

                level = "Advanced"

            # Save quiz result

            st.session_state.quiz_submitted = True

            st.session_state.quiz_score = score

            st.session_state.quiz_percentage = percentage

            st.session_state.quiz_level = level

            # Move to recommendation

            st.session_state.step = 3

            st.rerun()


# ============================================================
# STEP 3
# RECOMMENDATION
# ============================================================

elif st.session_state.step == 3:

    st.header("3️⃣ Personalized Recommendation")

    st.write(
        "Your profile and skill assessment have been analyzed."
    )

    # ========================================================
    # QUIZ RESULT
    # ========================================================

    st.subheader("📝 Quiz Result")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Quiz Topic",
            st.session_state.selected_topic
        )

    with col2:

        st.metric(
            "Score",
            f"{st.session_state.quiz_score}/5"
        )

    with col3:

        st.metric(
            "Learning Level",
            st.session_state.quiz_level
        )

    st.divider()

    # ========================================================
    # STUDENT PROFILE
    # ========================================================

    st.subheader("👤 Student Profile")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Branch",
            st.session_state.selected_branch
        )

    with col2:

        st.metric(
            "Career Goal",
            st.session_state.selected_career
        )

    with col3:

        st.metric(
            "Semester",
            st.session_state.semester
        )

    with col4:

        st.metric(
            "Learning Hours",
            f"{st.session_state.time_available}/week"
        )

    # ========================================================
    # ACADEMIC PERFORMANCE
    # ========================================================

    st.subheader("📊 Academic Performance")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Average Score",
            f"{st.session_state.average_score}%"
        )

    with col2:

        st.metric(
            "Lowest Score",
            f"{st.session_state.lowest_score}%"
        )

    with col3:

        st.metric(
            "Skill Gaps",
            st.session_state.skill_gap_count
        )

    st.divider()

    # ========================================================
    # ML PREDICTION
    # ========================================================

    st.subheader("🤖 ML Recommendation")

    try:

        # Encode branch

        branch_encoded = (
            branch_encoder.transform(
                [st.session_state.selected_branch]
            )[0]
        )

        # Encode career

        career_encoded = (
            career_encoder.transform(
                [st.session_state.selected_career]
            )[0]
        )

        # ----------------------------------------------------
        # CREATE INPUT DATA
        # ----------------------------------------------------

        input_data = pd.DataFrame(
            [[
                branch_encoded,
                st.session_state.semester,
                career_encoded,
                st.session_state.average_score,
                st.session_state.lowest_score,
                st.session_state.skill_gap_count,
                st.session_state.time_available
            ]],

            columns=[
                "Branch",
                "Semester",
                "Career_Goal",
                "Average_Assessment_Score",
                "Lowest_Assessment_Score",
                "Skill_Gap_Count",
                "Time_Available_Hours"
            ]
        )

        # ----------------------------------------------------
        # PREDICTION
        # ----------------------------------------------------

        prediction = model.predict(
            input_data
        )[0]

        # ----------------------------------------------------
        # CONVERT PREDICTION BACK TO COURSE NAME
        # ----------------------------------------------------

        recommended_course = (
            course_encoder.inverse_transform(
                [prediction]
            )[0]
        )

        st.session_state.recommended_course = (
            recommended_course
        )

        # ====================================================
        # DISPLAY COURSE
        # ====================================================

        st.success(
            f"🎯 Recommended Course: **{recommended_course}**"
        )

        # ====================================================
        # FIND COURSE DETAILS
        # ====================================================

        course_info = courses[
            courses["Course"]
            .astype(str)
            .str.strip()
            ==
            str(recommended_course)
            .strip()
        ]

        if not course_info.empty:

            row = course_info.iloc[0]

            st.divider()

            col1, col2 = st.columns(2)

            # ------------------------------------------------
            # PRACTICE PLAN
            # ------------------------------------------------

            with col1:

                st.subheader("📚 Practice Plan")

                if "Practice_Plan" in courses.columns:

                    practice_plan = row[
                        "Practice_Plan"
                    ]

                    if pd.notna(practice_plan):

                        st.write(
                            practice_plan
                        )

                    else:

                        st.write(
                            "Practice plan not available."
                        )

                # --------------------------------------------
                # PROJECT
                # --------------------------------------------

                st.subheader("🛠️ Recommended Project")

                if "Project" in courses.columns:

                    project = row[
                        "Project"
                    ]

                    if pd.notna(project):

                        st.write(
                            project
                        )

                    else:

                        st.write(
                            "Project information not available."
                        )

            # ------------------------------------------------
            # CERTIFICATION
            # ------------------------------------------------

            with col2:

                st.subheader("🏆 Recommended Certification")

                if "Certification" in courses.columns:

                    certification = row[
                        "Certification"
                    ]

                    if pd.notna(certification):

                        st.write(
                            certification
                        )

                    else:

                        st.write(
                            "Certification information not available."
                        )

                # --------------------------------------------
                # DIFFICULTY
                # --------------------------------------------

                st.subheader("📈 Course Difficulty")

                if "Difficulty" in courses.columns:

                    difficulty = row[
                        "Difficulty"
                    ]

                    if pd.notna(difficulty):

                        st.write(
                            difficulty
                        )

                    else:

                        st.write(
                            "Difficulty information not available."
                        )

        else:

            st.warning(
                "⚠️ Course was predicted, but detailed "
                "course information was not found in "
                "Courses_Resources."
            )

    except Exception as e:

        st.error(
            "❌ Error generating recommendation."
        )

        st.code(
            str(e)
        )

    st.divider()

    # ========================================================
    # ADAPTIVE LEARNING PATH
    # ========================================================

    st.subheader(
        "🧠 Your Personalized Learning Path"
    )

    level = st.session_state.quiz_level

    if level == "Beginner":

        st.warning(
            "🌱 Beginner Learning Path"
        )

        st.markdown(
            """
            **Your focus should be:**

            1. 📖 Learn fundamental concepts
            2. 📝 Practice basic questions
            3. 💻 Solve simple coding problems
            4. 🛠️ Build a small project
            5. 🎯 Complete the recommended course
            6. 🏆 Prepare for certification
            """
        )

    elif level == "Intermediate":

        st.info(
            "🚀 Intermediate Learning Path"
        )

        st.markdown(
            """
            **Your focus should be:**

            1. 📚 Strengthen intermediate concepts
            2. 💻 Solve practical problems
            3. 📝 Practice coding/technical questions
            4. 🛠️ Build a practical project
            5. 🎯 Complete the recommended course
            6. 🏆 Prepare for certification
            """
        )

    else:

        st.success(
            "🔥 Advanced Learning Path"
        )

        st.markdown(
            """
            **Your focus should be:**

            1. 🚀 Learn advanced concepts
            2. 💻 Solve challenging problems
            3. 🧠 Work on advanced algorithms/concepts
            4. 🛠️ Build an industry-level project
            5. 🎯 Complete the recommended course
            6. 🏆 Prepare for certification
            7. 💼 Add the project to your portfolio
            """
        )

    st.divider()

    # ========================================================
    # RECOMMENDATION SUMMARY
    # ========================================================

    st.subheader(
        "📋 Recommendation Summary"
    )

    st.markdown(
        f"""
        **Engineering Branch:** {st.session_state.selected_branch}

        **Career Goal:** {st.session_state.selected_career}

        **Semester:** {st.session_state.semester}

        **Quiz Topic:** {st.session_state.selected_topic}

        **Quiz Score:** {st.session_state.quiz_score}/5

        **Learning Level:** {st.session_state.quiz_level}

        **Average Assessment Score:** {st.session_state.average_score}%

        **Lowest Assessment Score:** {st.session_state.lowest_score}%

        **Skill Gaps:** {st.session_state.skill_gap_count}

        **Available Learning Time:** {st.session_state.time_available} hours/week

        **Recommended Course:** {st.session_state.recommended_course}
        """
    )

    st.divider()

    # ========================================================
    # START AGAIN
    # ========================================================

    if st.button(
        "🔄 Start New Student",
        use_container_width=True
    ):

        # Clear quiz-related session data

        for key in list(
            st.session_state.keys()
        ):

            del st.session_state[key]

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🎓 Personalized Learning Recommendation System | "
    "Machine Learning + Skill Assessment"
)
