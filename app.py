import streamlit as st
import pandas as pd
import joblib
import os

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Personalized Learning Recommendation System",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

MODEL_PATH = "personalized_learning_system.pkl"

if not os.path.exists(MODEL_PATH):
    st.error(
        "Model file not found. Please place "
        "'personalized_learning_system.pkl' in the same folder as app.py."
    )
    st.stop()

system = joblib.load(MODEL_PATH)

model = system["model"]
branch_encoder = system["branch_encoder"]
career_encoder = system["career_encoder"]
course_encoder = system["course_encoder"]
features = system["features"]

# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

DATASET_PATH = "Personalized_Learning_Recommendation_Dataset_1000.xlsx"

if not os.path.exists(DATASET_PATH):
    st.error(
        "Dataset not found. Please place "
        "'Personalized_Learning_Recommendation_Dataset_1000.xlsx' "
        "in the same folder as app.py."
    )
    st.stop()

resources = pd.read_excel(
    DATASET_PATH,
    sheet_name="Courses_Resources"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎓 Personalized Learning Recommendation System")

st.write(
    "An AI/ML-based system that creates a personalized learning "
    "path for engineering students."
)

st.divider()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("📚 Student Information")

branches = [
    "CSE",
    "IT",
    "ECE",
    "EEE",
    "Mechanical",
    "Civil",
    "Chemical",
    "Aerospace",
    "AI & DS",
    "Robotics"
]

career_goals = [
    "Software Developer",
    "AI/ML Engineer",
    "Data Scientist",
    "Data Analyst",
    "Web Developer",
    "Cybersecurity Engineer",
    "Cloud Engineer",
    "Embedded Engineer",
    "VLSI Engineer",
    "Robotics Engineer",
    "Mechanical Design Engineer",
    "Civil Engineer",
    "Structural Engineer",
    "Chemical Engineer",
    "Aerospace Engineer"
]

branch = st.sidebar.selectbox(
    "Select Engineering Branch",
    branches
)

semester = st.sidebar.slider(
    "Semester",
    min_value=1,
    max_value=8,
    value=6
)

career_goal = st.sidebar.selectbox(
    "Career Goal",
    career_goals
)

average_score = st.sidebar.slider(
    "Average Assessment Score",
    min_value=0,
    max_value=100,
    value=65
)

lowest_score = st.sidebar.slider(
    "Lowest Assessment Score",
    min_value=0,
    max_value=100,
    value=45
)

skill_gap_count = st.sidebar.number_input(
    "Number of Skill Gaps",
    min_value=0,
    max_value=20,
    value=2
)

time_available = st.sidebar.slider(
    "Available Learning Hours / Week",
    min_value=1,
    max_value=40,
    value=8
)

# --------------------------------------------------
# STUDENT PROFILE
# --------------------------------------------------

st.subheader("👨‍🎓 Student Profile")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Branch", branch)

with col2:
    st.metric("Semester", semester)

with col3:
    st.metric("Average Score", f"{average_score}%")

with col4:
    st.metric("Weekly Hours", f"{time_available} hrs")

# --------------------------------------------------
# GENERATE RECOMMENDATION
# --------------------------------------------------

if st.button(
    "🚀 Generate My Learning Path",
    use_container_width=True
):

    try:

        # Encode categorical values

        branch_encoded = branch_encoder.transform([branch])[0]

        career_encoded = career_encoder.transform([career_goal])[0]

        # Create input dataframe

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
            columns=features
        )

        # --------------------------------------------------
        # ML PREDICTION
        # --------------------------------------------------

        prediction = model.predict(input_data)[0]

        predicted_course = course_encoder.inverse_transform(
            [prediction]
        )[0]

        # --------------------------------------------------
        # FIND COURSE DETAILS
        # --------------------------------------------------

        course_info = resources[
            resources["Course"] == predicted_course
        ]

        # --------------------------------------------------
        # DISPLAY RECOMMENDATION
        # --------------------------------------------------

        st.success(
            "🎯 Personalized learning path generated successfully!"
        )

        st.divider()

        st.subheader("📖 Recommended Learning Path")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 📚 Recommended Course")

            st.info(predicted_course)

            st.markdown("### 🎯 Career Goal")

            st.write(career_goal)

            st.markdown("### 🧠 Skill Gap Level")

            if lowest_score < 40:
                st.error("High Skill Gap")
            elif lowest_score < 60:
                st.warning("Medium Skill Gap")
            else:
                st.success("Low Skill Gap")

        with col2:

            st.markdown("### ⏱️ Weekly Learning Time")

            st.info(f"{time_available} hours/week")

            st.markdown("### 📊 Average Performance")

            st.write(f"{average_score}%")

            st.markdown("### 📉 Lowest Score")

            st.write(f"{lowest_score}%")

        # --------------------------------------------------
        # RESOURCE DETAILS
        # --------------------------------------------------

        if not course_info.empty:

            row = course_info.iloc[0]

            st.divider()

            st.subheader("🛠️ Personalized Resources")

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("### 📝 Practice Plan")

                st.write(
                    row.get(
                        "Practice_Plan",
                        "Practice recommended topics regularly."
                    )
                )

                st.markdown("### 💻 Recommended Project")

                st.write(
                    row.get(
                        "Project",
                        "Build a practical project related to this course."
                    )
                )

            with col2:

                st.markdown("### 🏆 Certification")

                st.write(
                    row.get(
                        "Certification",
                        "Complete a relevant certification."
                    )
                )

                st.markdown("### 📈 Difficulty")

                st.write(
                    row.get(
                        "Difficulty",
                        "Intermediate"
                    )
                )

        # --------------------------------------------------
        # WEEKLY PLAN
        # --------------------------------------------------

        st.divider()

        st.subheader("📅 Suggested Weekly Learning Plan")

        theory_hours = round(time_available * 0.30, 1)
        practice_hours = round(time_available * 0.30, 1)
        project_hours = round(time_available * 0.25, 1)
        revision_hours = round(time_available * 0.15, 1)

        weekly_plan = pd.DataFrame({
            "Activity": [
                "Theory / Learning",
                "Practice",
                "Project",
                "Revision"
            ],
            "Hours": [
                theory_hours,
                practice_hours,
                project_hours,
                revision_hours
            ]
        })

        st.dataframe(
            weekly_plan,
            use_container_width=True,
            hide_index=True
        )

        # --------------------------------------------------
        # FINAL MESSAGE
        # --------------------------------------------------

        st.divider()

        st.success(
            f"Your next recommended learning step is: "
            f"{predicted_course}"
        )

        st.write(
            "Keep following the recommended course, practice plan "
            "and project to improve your skills progressively."
        )

    except Exception as e:

        st.error(
            "Unable to generate recommendation."
        )

        st.exception(e)
