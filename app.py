import streamlit as st
import pandas as pd
import joblib

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Personalized Learning Recommendation System",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.title {
    font-size: 40px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: gray;
    margin-bottom: 30px;
}

.card {
    padding: 20px;
    border-radius: 12px;
    background-color: white;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.result {
    padding: 25px;
    border-radius: 15px;
    background-color: #eef5ff;
    text-align: center;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD ML MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():
    return joblib.load("recommendation_model.pkl")


try:
    model = load_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    st.error("❌ recommendation_model.pkl was not found.")
    st.info(
        "Please keep app.py and recommendation_model.pkl "
        "in the same folder."
    )

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(
    '<div class="title">🎓 Personalized Learning Recommendation System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered learning recommendations based on student performance, '
    'skills, interests and learning preferences'
    '</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🎯 Student Profile")

st.sidebar.write(
    "Enter the student's information to generate a personalized learning recommendation."
)

# --------------------------------------------------
# STUDENT INPUTS
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("📚 Academic Information")

    learning_level = st.selectbox(
        "Learning Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    assessment_score = st.number_input(
        "Assessment Score",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=1.0
    )

    assignment_score = st.number_input(
        "Assignment Score",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=1.0
    )

    course_completion = st.number_input(
        "Course Completion",
        min_value=0,
        max_value=20,
        value=3,
        step=1
    )

    previous_performance = st.number_input(
        "Previous Performance",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=1.0
    )

with col2:

    st.subheader("🧠 Learning Profile")

    preferred_style = st.selectbox(
        "Preferred Learning Style",
        [
            "Video",
            "Reading",
            "Hands-on",
            "Hybrid"
        ]
    )

    interests = st.text_input(
        "Interests",
        value="Python"
    )

    programming_skill = st.selectbox(
        "Programming Skill",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    time_available = st.number_input(
        "Time Availability (Hours/Week)",
        min_value=0.0,
        max_value=50.0,
        value=10.0,
        step=1.0
    )

# --------------------------------------------------
# FEATURE ENGINEERING
# --------------------------------------------------

average_performance = (
    assessment_score + assignment_score
) / 2


def get_availability_group(hours):

    if hours < 2:
        return "Low"

    elif hours <= 4:
        return "Medium"

    else:
        return "High"


study_availability_group = get_availability_group(
    time_available
)

# --------------------------------------------------
# DISPLAY STUDENT SUMMARY
# --------------------------------------------------

st.markdown("---")

st.subheader("📊 Student Performance Summary")

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Assessment",
    f"{assessment_score:.0f}%"
)

m2.metric(
    "Assignment",
    f"{assignment_score:.0f}%"
)

m3.metric(
    "Average Performance",
    f"{average_performance:.1f}%"
)

m4.metric(
    "Course Completion",
    course_completion
)

# --------------------------------------------------
# GENERATE RECOMMENDATION
# --------------------------------------------------

st.markdown("---")

if st.button(
    "🚀 Generate Personalized Recommendation",
    use_container_width=True
):

    # --------------------------------------------------
    # MODEL INPUT
    # --------------------------------------------------

    input_data = pd.DataFrame({

        "Learning_Level": [
            learning_level
        ],

        "Assessment_Score": [
            assessment_score
        ],

        "Assignment_Score": [
            assignment_score
        ],

        "Course_Completion": [
            course_completion
        ],

        "Preferred_Learning_Style": [
            preferred_style
        ],

        "Interests": [
            interests
        ],

        "Time_Availability_Hours": [
            time_available
        ],

        "Previous_Performance": [
            previous_performance
        ],

        "Programming_Skill": [
            programming_skill
        ],

        "Average_Performance": [
            average_performance
        ],

        "Study_Availability_Group": [
            study_availability_group
        ]
    })

    # --------------------------------------------------
    # ML PREDICTION
    # --------------------------------------------------

    if model_loaded:

        try:

            prediction = model.predict(input_data)[0]

            # --------------------------------------------------
            # RESULT
            # --------------------------------------------------

            st.markdown(
                '<div class="result">'
                '<h2>🎯 Recommended Learning Path</h2>'
                f'<h1>{prediction}</h1>'
                '</div>',
                unsafe_allow_html=True
            )

        except Exception as e:

            st.error(
                "❌ Model prediction failed."
            )

            st.code(str(e))

    # --------------------------------------------------
    # PERSONALIZED LEARNING PLAN
    # --------------------------------------------------

    st.markdown("---")

    st.subheader("📖 Personalized Learning Plan")

    # --------------------------------------------------
    # PERFORMANCE LEVEL
    # --------------------------------------------------

    if average_performance < 50:

        performance_level = "Low"

        focus = "Build your fundamental concepts"

        course = f"{interests} Fundamentals"

        practice = f"Basic {interests} Practice"

        project = f"Beginner {interests} Mini Project"

    elif average_performance < 75:

        performance_level = "Medium"

        focus = "Strengthen concepts through practice"

        course = f"Intermediate {interests} Course"

        practice = f"{interests} Coding Exercises"

        project = f"Intermediate {interests} Project"

    else:

        performance_level = "High"

        focus = "Move towards advanced concepts"

        course = f"Advanced {interests} Course"

        practice = f"Advanced {interests} Challenges"

        project = f"Advanced {interests} Project"

    # --------------------------------------------------
    # LEARNING METHOD
    # --------------------------------------------------

    if preferred_style == "Video":

        learning_method = (
            "Watch video lectures, demonstrations and visual tutorials."
        )

    elif preferred_style == "Reading":

        learning_method = (
            "Use textbooks, documentation, notes and reading materials."
        )

    elif preferred_style == "Hands-on":

        learning_method = (
            "Focus on coding exercises, practical tasks and projects."
        )

    else:

        learning_method = (
            "Use a combination of videos, reading and hands-on practice."
        )

    # --------------------------------------------------
    # TIME PLAN
    # --------------------------------------------------

    if time_available < 5:

        time_plan = (
            "Study 30–45 minutes per day and focus on one topic at a time."
        )

    elif time_available < 10:

        time_plan = (
            "Study around 1 hour per day with regular practice."
        )

    else:

        time_plan = (
            "Follow a structured daily plan with learning, practice and projects."
        )

    # --------------------------------------------------
    # DISPLAY PLAN
    # --------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown("### 📘 Course")

        st.write(course)

    with c2:

        st.markdown("### 💻 Practice")

        st.write(practice)

    with c3:

        st.markdown("### 🚀 Project")

        st.write(project)

    st.markdown("---")

    st.subheader("🎯 Focus Area")

    st.info(focus)

    st.subheader("🧑‍💻 Recommended Learning Method")

    st.write(learning_method)

    st.subheader("⏰ Study Plan")

    st.write(time_plan)

    # --------------------------------------------------
    # NEXT STEPS
    # --------------------------------------------------

    st.subheader("➡️ Recommended Next Steps")

    steps = [
        f"1. Complete the {course}.",
        f"2. Practice using {practice}.",
        f"3. Build the {project}.",
        "4. Take a quiz to check your understanding.",
        "5. Review weak topics.",
        "6. Continue to the next learning level."
    ]

    for step in steps:
        st.write(step)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "🎓 Personalized Learning Recommendation System | "
    "Machine Learning + Streamlit"
)
