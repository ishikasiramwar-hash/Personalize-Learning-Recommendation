import streamlit as st
import pandas as pd
import joblib
import os


# ============================================================
# PAGE CONFIG
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
    "An ML-based system that recommends learning content "
    "according to a student's branch, career goal, performance, "
    "skill gaps, and quiz performance."
)

st.divider()


# ============================================================
# FILE NAMES
# ============================================================

MODEL_FILE = "model.joblib"
ENCODER_FILE = "encoders.joblib"
DATASET_FILE = "Personalized_Learning_Recommendation_Dataset_1000.xlsx"


# ============================================================
# CHECK FILES
# ============================================================

if not os.path.exists(MODEL_FILE):

    st.error(
        "❌ model.joblib not found. "
        "Upload model.joblib in the same folder as app.py."
    )

    st.stop()


if not os.path.exists(ENCODER_FILE):

    st.error(
        "❌ encoders.joblib not found. "
        "Upload encoders.joblib in the same folder as app.py."
    )

    st.stop()


if not os.path.exists(DATASET_FILE):

    st.error(
        "❌ Dataset not found. "
        "Upload Personalized_Learning_Recommendation_Dataset_1000.xlsx "
        "in the same folder as app.py."
    )

    st.stop()


# ============================================================
# LOAD MODEL
# ============================================================

try:

    model = joblib.load(MODEL_FILE)

    encoders = joblib.load(ENCODER_FILE)

    branch_encoder = encoders["branch_encoder"]
    career_encoder = encoders["career_encoder"]
    course_encoder = encoders["course_encoder"]

except Exception as e:

    st.error("❌ Error loading ML model.")

    st.code(str(e))

    st.stop()


# ============================================================
# LOAD EXCEL DATA
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
# SESSION STATE
# ============================================================

if "quiz_submitted" not in st.session_state:

    st.session_state.quiz_submitted = False


if "quiz_score" not in st.session_state:

    st.session_state.quiz_score = 0


if "quiz_level" not in st.session_state:

    st.session_state.quiz_level = ""


# ============================================================
# SIDEBAR - STUDENT INFORMATION
# ============================================================

st.sidebar.header("👤 Student Information")


branches = list(branch_encoder.classes_)

selected_branch = st.sidebar.selectbox(
    "Engineering Branch",
    branches
)


career_goals = list(career_encoder.classes_)

selected_career = st.sidebar.selectbox(
    "Career Goal",
    career_goals
)


semester = st.sidebar.slider(
    "Semester",
    1,
    8,
    4
)


time_available = st.sidebar.slider(
    "Available Learning Hours / Week",
    1,
    40,
    10
)


average_score = st.sidebar.slider(
    "Average Assessment Score",
    0,
    100,
    65
)


lowest_score = st.sidebar.slider(
    "Lowest Assessment Score",
    0,
    100,
    50
)


skill_gap_count = st.sidebar.slider(
    "Number of Skill Gaps",
    0,
    10,
    2
)


# ============================================================
# ML RECOMMENDATION FUNCTION
# ============================================================

def generate_ml_recommendation():

    try:

        branch_encoded = branch_encoder.transform(
            [selected_branch]
        )[0]

        career_encoded = career_encoder.transform(
            [selected_career]
        )[0]

        input_data = pd.DataFrame(
            [[
                branch_encoded,
                semester,
                career_encoded,
                average_score,
                lowest_score,
                skill_gap_count,
                time_available
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

        prediction = model.predict(input_data)[0]

        recommended_course = course_encoder.inverse_transform(
            [prediction]
        )[0]

        return recommended_course

    except Exception as e:

        st.error("Recommendation error.")

        st.code(str(e))

        return None


# ============================================================
# SIDEBAR BUTTON
# ============================================================

if st.sidebar.button(
    "🚀 Generate Recommendation",
    use_container_width=True
):

    st.session_state.recommended_course = (
        generate_ml_recommendation()
    )


# ============================================================
# MAIN TABS
# ============================================================

tab1, tab2, tab3 = st.tabs(
    [
        "🎯 Recommendation",
        "📝 Skill Quiz",
        "📊 Learning Analysis"
    ]
)


# ============================================================
# TAB 1 - RECOMMENDATION
# ============================================================

with tab1:

    st.header("🎯 Personalized Learning Recommendation")


    if (
        "recommended_course"
        not in st.session_state
        or st.session_state.recommended_course is None
    ):

        st.info(
            "👈 Enter your details in the sidebar "
            "and click 'Generate Recommendation'."
        )

    else:

        recommended_course = (
            st.session_state.recommended_course
        )


        # ----------------------------------------------------
        # STUDENT PROFILE
        # ----------------------------------------------------

        st.subheader("👤 Student Profile")


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Branch",
                selected_branch
            )


        with col2:

            st.metric(
                "Semester",
                semester
            )


        with col3:

            st.metric(
                "Career Goal",
                selected_career
            )


        with col4:

            st.metric(
                "Weekly Hours",
                f"{time_available} hrs"
            )


        st.divider()


        # ----------------------------------------------------
        # PERFORMANCE
        # ----------------------------------------------------

        st.subheader("📈 Academic Performance")


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Average Score",
                f"{average_score}%"
            )


        with col2:

            st.metric(
                "Lowest Score",
                f"{lowest_score}%"
            )


        with col3:

            st.metric(
                "Skill Gaps",
                skill_gap_count
            )


        st.divider()


        # ----------------------------------------------------
        # COURSE
        # ----------------------------------------------------

        st.subheader("📚 Recommended Course")


        st.success(
            f"### {recommended_course}"
        )


        # ----------------------------------------------------
        # COURSE DETAILS
        # ----------------------------------------------------

        course_info = courses[
            courses["Course"].astype(str).str.strip()
            ==
            str(recommended_course).strip()
        ]


        if not course_info.empty:

            row = course_info.iloc[0]


            col1, col2 = st.columns(2)


            with col1:

                st.subheader("💻 Practice Plan")

                if "Practice_Plan" in courses.columns:

                    st.write(
                        row["Practice_Plan"]
                    )


                st.subheader("🛠️ Project")

                if "Project" in courses.columns:

                    st.write(
                        row["Project"]
                    )


            with col2:

                st.subheader("🏆 Certification")

                if "Certification" in courses.columns:

                    st.write(
                        row["Certification"]
                    )


                st.subheader("📊 Difficulty")

                if "Difficulty" in courses.columns:

                    st.write(
                        row["Difficulty"]
                    )


        else:

            st.warning(
                "Course details were not found "
                "in Courses_Resources."
            )


# ============================================================
# QUIZ QUESTIONS
# ============================================================

quiz_questions = {

    "Python": [

        {
            "question":
            "Which keyword is used to define a function in Python?",

            "options":
            ["function", "def", "define", "fun"],

            "answer":
            "def"
        },

        {
            "question":
            "Which data type is immutable in Python?",

            "options":
            ["List", "Dictionary", "Tuple", "Set"],

            "answer":
            "Tuple"
        },

        {
            "question":
            "Which symbol is used for comments in Python?",

            "options":
            ["//", "#", "/*", "--"],

            "answer":
            "#"
        },

        {
            "question":
            "Which function is used to display output in Python?",

            "options":
            ["display()", "show()", "print()", "output()"],

            "answer":
            "print()"
        },

        {
            "question":
            "Which collection stores key-value pairs?",

            "options":
            ["List", "Tuple", "Dictionary", "Set"],

            "answer":
            "Dictionary"
        }

    ],


    "Java": [

        {
            "question":
            "Which keyword is used for inheritance in Java?",

            "options":
            ["inherit", "extends", "implements", "inherits"],

            "answer":
            "extends"
        },

        {
            "question":
            "Which method is the entry point of a Java program?",

            "options":
            ["start()", "run()", "main()", "execute()"],

            "answer":
            "main()"
        },

        {
            "question":
            "Which keyword creates an object in Java?",

            "options":
            ["create", "object", "new", "make"],

            "answer":
            "new"
        },

        {
            "question":
            "Java is primarily a ______ language.",

            "options":
            ["Object-oriented", "Markup", "Query", "Assembly"],

            "answer":
            "Object-oriented"
        },

        {
            "question":
            "Which symbol is used to end a statement in Java?",

            "options":
            [".", ",", ";", ":"],

            "answer":
            ";"
        }

    ],


    "C++": [

        {
            "question":
            "Which symbol is used to end a statement in C++?",

            "options":
            [".", ",", ";", ":"],

            "answer":
            ";"
        },

        {
            "question":
            "Which feature allows the same function name with different parameters?",

            "options":
            ["Inheritance", "Overloading", "Encapsulation", "Abstraction"],

            "answer":
            "Overloading"
        },

        {
            "question":
            "Which operator is used to access a member through a pointer?",

            "options":
            [".", "::", "->", "&"],

            "answer":
            "->"
        },

        {
            "question":
            "Which header is commonly used for input and output in C++?",

            "options":
            ["stdio.h", "iostream", "string.h", "math.h"],

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
            ["GET", "SELECT", "FETCH", "READ"],

            "answer":
            "SELECT"
        },

        {
            "question":
            "Which command is used to remove a table?",

            "options":
            ["DELETE", "REMOVE", "DROP", "CLEAR"],

            "answer":
            "DROP"
        },

        {
            "question":
            "Which clause filters rows in SQL?",

            "options":
            ["WHERE", "FILTER", "CHECK", "SELECT"],

            "answer":
            "WHERE"
        },

        {
            "question":
            "Which key uniquely identifies a row?",

            "options":
            ["Foreign Key", "Primary Key", "Candidate Key", "Secondary Key"],

            "answer":
            "Primary Key"
        },

        {
            "question":
            "Which command adds a new row to a table?",

            "options":
            ["ADD", "INSERT", "UPDATE", "CREATE"],

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
            "Which tag creates a hyperlink?",

            "options":
            ["<link>", "<a>", "<href>", "<url>"],

            "answer":
            "<a>"
        },

        {
            "question":
            "Which tag creates the largest heading?",

            "options":
            ["<h6>", "<head>", "<h1>", "<heading>"],

            "answer":
            "<h1>"
        },

        {
            "question":
            "Which tag is used to insert an image?",

            "options":
            ["<image>", "<img>", "<picture>", "<src>"],

            "answer":
            "<img>"
        },

        {
            "question":
            "Which attribute specifies an image path?",

            "options":
            ["href", "src", "link", "path"],

            "answer":
            "src"
        }

    ],


    "Data Structures": [

        {
            "question":
            "Which data structure follows LIFO?",

            "options":
            ["Queue", "Stack", "Array", "Graph"],

            "answer":
            "Stack"
        },

        {
            "question":
            "Which data structure follows FIFO?",

            "options":
            ["Stack", "Queue", "Tree", "Graph"],

            "answer":
            "Queue"
        },

        {
            "question":
            "Which structure consists of nodes connected by edges?",

            "options":
            ["Array", "Graph", "Stack", "Queue"],

            "answer":
            "Graph"
        },

        {
            "question":
            "Which data structure represents hierarchical relationships?",

            "options":
            ["Tree", "Queue", "Array", "Stack"],

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
# TAB 2 - QUIZ
# ============================================================

with tab2:

    st.header("📝 Skill Assessment Quiz")

    st.write(
        "Take a short quiz to understand your current "
        "knowledge level."
    )


    # --------------------------------------------------------
    # TOPIC
    # --------------------------------------------------------

    available_topics = list(quiz_questions.keys())


    selected_topic = st.selectbox(
        "Select Quiz Topic",
        available_topics
    )


    st.info(
        f"📚 You selected: **{selected_topic}**"
    )


    questions = quiz_questions[selected_topic]


    st.divider()


    # --------------------------------------------------------
    # QUESTIONS
    # --------------------------------------------------------

    for i, question in enumerate(questions):

        st.subheader(
            f"Question {i + 1}"
        )

        st.write(
            question["question"]
        )


        st.radio(
            "Choose your answer:",
            question["options"],
            key=f"quiz_{selected_topic}_{i}"
        )


    st.divider()


    # --------------------------------------------------------
    # SUBMIT
    # --------------------------------------------------------

    if st.button(
        "✅ Submit Quiz",
        use_container_width=True
    ):

        score = 0


        for i, question in enumerate(questions):

            selected_answer = st.session_state[
                f"quiz_{selected_topic}_{i}"
            ]


            if selected_answer == question["answer"]:

                score += 1


        percentage = (
            score / len(questions)
        ) * 100


        # ----------------------------------------------------
        # LEVEL
        # ----------------------------------------------------

        if percentage < 40:

            level = "Beginner"

        elif percentage < 70:

            level = "Intermediate"

        else:

            level = "Advanced"


        st.session_state.quiz_submitted = True

        st.session_state.quiz_score = score

        st.session_state.quiz_level = level


        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        st.success(
            "🎉 Quiz submitted successfully!"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Score",
                f"{score}/{len(questions)}"
            )


        with col2:

            st.metric(
                "Percentage",
                f"{percentage:.0f}%"
            )


        with col3:

            st.metric(
                "Learning Level",
                level
            )


        # ----------------------------------------------------
        # FEEDBACK
        # ----------------------------------------------------

        if level == "Beginner":

            st.warning(
                "📖 You should strengthen your basic concepts "
                "before moving to advanced topics."
            )


        elif level == "Intermediate":

            st.info(
                "💻 Your fundamentals are developing well. "
                "Focus on practice and projects."
            )


        else:

            st.success(
                "🚀 Excellent! You can move toward advanced "
                "topics and real-world projects."
            )


        st.divider()


        # ----------------------------------------------------
        # ANSWER REVIEW
        # ----------------------------------------------------

        st.subheader("📋 Answer Review")


        for i, question in enumerate(questions):

            selected_answer = st.session_state[
                f"quiz_{selected_topic}_{i}"
            ]


            if selected_answer == question["answer"]:

                st.success(
                    f"Q{i+1}: Correct ✅"
                )

            else:

                st.error(
                    f"Q{i+1}: Incorrect ❌"
                )

                st.write(
                    f"Correct answer: "
                    f"**{question['answer']}**"
                )


# ============================================================
# TAB 3 - LEARNING ANALYSIS
# ============================================================

with tab3:

    st.header("📊 Learning Analysis")


    if not st.session_state.quiz_submitted:

        st.info(
            "Complete the quiz first to see your learning analysis."
        )

    else:

        score = st.session_state.quiz_score

        level = st.session_state.quiz_level


        st.subheader("🎯 Your Learning Profile")


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Quiz Score",
                f"{score}/5"
            )


        with col2:

            st.metric(
                "Learning Level",
                level
            )


        with col3:

            st.metric(
                "Quiz Topic",
                selected_topic
            )


        st.divider()


        st.subheader("📚 Recommended Action")


        if level == "Beginner":

            st.write(
                "### Start with Fundamentals"
            )

            st.markdown(
                """
                - 📖 Learn basic concepts
                - 📝 Practice simple questions
                - 🎥 Use beginner-friendly learning resources
                - 💻 Complete small exercises
                - 🛠️ Build a basic mini-project
                """
            )


        elif level == "Intermediate":

            st.write(
                "### Improve Through Practice"
            )

            st.markdown(
                """
                - 📚 Study intermediate concepts
                - 💻 Solve coding/practical problems
                - 🛠️ Build a practical project
                - 📊 Practice assessment questions
                - 🏆 Start preparing for certification
                """
            )


        else:

            st.write(
                "### Move to Advanced Learning"
            )

            st.markdown(
                """
                - 🚀 Learn advanced concepts
                - 🛠️ Build an industry-level project
                - 💻 Solve challenging problems
                - 🏆 Prepare for certification
                - 💼 Build your portfolio
                """
            )


        st.divider()


        # ----------------------------------------------------
        # COMBINED RECOMMENDATION
        # ----------------------------------------------------

        st.subheader("🤖 Personalized Recommendation")


        if (
            "recommended_course"
            in st.session_state
            and st.session_state.recommended_course
        ):

            st.success(
                f"Based on your ML recommendation, "
                f"you should study:\n\n"
                f"**{st.session_state.recommended_course}**"
            )


        st.write(
            f"Your quiz level for **{selected_topic}** is "
            f"**{level}**."
        )


        if level == "Beginner":

            st.write(
                "👉 Focus on fundamentals before moving to "
                "advanced learning."
            )

        elif level == "Intermediate":

            st.write(
                "👉 Combine learning with regular practice "
                "and project development."
            )

        else:

            st.write(
                "👉 Focus on advanced projects, "
                "certifications, and industry skills."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Personalized Learning Recommendation System | "
    "Machine Learning + Skill Assessment Quiz"
)
