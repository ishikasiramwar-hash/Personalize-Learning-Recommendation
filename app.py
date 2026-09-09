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
# FILE PATHS
# ============================================================

MODEL_FILE = "personalized_learning_system.pkl"

DATASET_FILE = "Personalized_Learning_Recommendation_Dataset_1000.xlsx"

# ============================================================
# CHECK MODEL FILE
# ============================================================

if not os.path.exists(MODEL_FILE):

    st.error(
        "❌ Model file not found.\n\n"
        "Please put 'personalized_learning_system.pkl' "
        "in the same folder as app.py."
    )

    st.stop()

# ============================================================
# CHECK DATASET
# ============================================================

if not os.path.exists(DATASET_FILE):

    st.error(
        "❌ Dataset file not found.\n\n"
        "Please put 'Personalized_Learning_Recommendation_Dataset_1000.xlsx' "
        "in the same folder as app.py."
    )

    st.stop()

# ============================================================
# LOAD MODEL
# ============================================================

try:

    system = joblib.load(MODEL_FILE)

    model = system["model"]

    branch_encoder = system["branch_encoder"]

    career_encoder = system["career_encoder"]

    course_encoder = system["course_encoder"]

except Exception as e:

    st.error("❌ Error loading the model.")

    st.exception(e)

    st.stop()

# ============================================================
# LOAD DATASET
# ============================================================

try:

    resources = pd.read_excel(
        DATASET_FILE,
        sheet_name="Courses_Resources"
    )

except Exception as e:

    st.error("❌ Error loading Excel dataset.")

    st.exception(e)

    st.stop()

# ============================================================
# FEATURES
# ============================================================

features = [
    "Branch",
    "Semester",
    "Career_Goal",
    "Average_Assessment_Score",
    "Lowest_Assessment_Score",
    "Skill_Gap_Count",
    "Time_Available_Hours"
]

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f5f7fb;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666666;
        margin-bottom: 25px;
    }

    .recommendation-box {
        padding: 25px;
        border-radius: 15px;
        background-color: #eef6ff;
        border-left: 6px solid #4a90e2;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .section-box {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">🎓 Personalized Learning Recommendation System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI/ML-Based Personalized Learning Path for Engineering Students'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("👨‍🎓 Student Details")

st.sidebar.write(
    "Enter the student's information below."
)

# ============================================================
# BRANCHES
# ============================================================

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

# ============================================================
# CAREER GOALS
# ============================================================

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

# ============================================================
# USER INPUT
# ============================================================

branch = st.sidebar.selectbox(
    "🏫 Engineering Branch",
    branches
)

semester = st.sidebar.selectbox(
    "📚 Semester",
    [1, 2, 3, 4, 5, 6, 7, 8],
    index=5
)

career_goal = st.sidebar.selectbox(
    "🎯 Career Goal",
    career_goals
)

average_score = st.sidebar.slider(
    "📊 Average Assessment Score",
    min_value=0,
    max_value=100,
    value=65
)

lowest_score = st.sidebar.slider(
    "📉 Lowest Assessment Score",
    min_value=0,
    max_value=100,
    value=45
)

skill_gap_count = st.sidebar.number_input(
    "🧠 Number of Skill Gaps",
    min_value=0,
    max_value=20,
    value=2
)

time_available = st.sidebar.slider(
    "⏱️ Learning Hours Per Week",
    min_value=1,
    max_value=40,
    value=8
)

# ============================================================
# STUDENT PROFILE
# ============================================================

st.subheader("👤 Student Profile")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Branch",
        branch
    )

with col2:

    st.metric(
        "Semester",
        semester
    )

with col3:

    st.metric(
        "Average Score",
        f"{average_score}%"
    )

with col4:

    st.metric(
        "Weekly Hours",
        f"{time_available} hrs"
    )

# ============================================================
# SKILL STATUS
# ============================================================

st.divider()

st.subheader("🧠 Current Skill Status")

if lowest_score < 40:

    st.error(
        "🔴 HIGH SKILL GAP — Student needs strong improvement."
    )

elif lowest_score < 60:

    st.warning(
        "🟡 MEDIUM SKILL GAP — Additional practice is recommended."
    )

else:

    st.success(
        "🟢 LOW SKILL GAP — Student is performing well."
    )

# ============================================================
# GENERATE BUTTON
# ============================================================

st.divider()

generate = st.button(
    "🚀 Generate My Personalized Learning Path",
    use_container_width=True
)

# ============================================================
# GENERATE RECOMMENDATION
# ============================================================

if generate:

    try:

        # ----------------------------------------------------
        # ENCODE BRANCH
        # ----------------------------------------------------

        if branch not in branch_encoder.classes_:

            st.error(
                f"Branch '{branch}' is not available in the trained model."
            )

            st.stop()

        branch_encoded = branch_encoder.transform(
            [branch]
        )[0]

        # ----------------------------------------------------
        # ENCODE CAREER
        # ----------------------------------------------------

        if career_goal not in career_encoder.classes_:

            st.error(
                f"Career goal '{career_goal}' is not available "
                "in the trained model."
            )

            st.stop()

        career_encoded = career_encoder.transform(
            [career_goal]
        )[0]

        # ----------------------------------------------------
        # CREATE INPUT
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # ML PREDICTION
        # ----------------------------------------------------

        prediction = model.predict(
            input_data
        )

        recommended_course = course_encoder.inverse_transform(
            prediction
        )[0]

        # ====================================================
        # SUCCESS MESSAGE
        # ====================================================

        st.success(
            "✅ Personalized learning path generated successfully!"
        )

        # ====================================================
        # MAIN RECOMMENDATION
        # ====================================================

        st.markdown(
            f"""
            <div class="recommendation-box">

            <h2>🎯 Your Recommended Next Course</h2>

            <h1>{recommended_course}</h1>

            <p>
            This recommendation is generated using machine
            learning based on your branch, semester, career goal,
            assessment performance, skill gaps and available
            learning time.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        # ====================================================
        # COURSE DETAILS
        # ====================================================

        course_info = resources[
            resources["Course"].astype(str).str.strip()
            == str(recommended_course).strip()
        ]

        if not course_info.empty:

            row = course_info.iloc[0]

            st.divider()

            st.subheader("📚 Recommended Learning Resources")

            col1, col2 = st.columns(2)

            # ------------------------------------------------
            # LEFT COLUMN
            # ------------------------------------------------

            with col1:

                st.markdown("### 📝 Practice Plan")

                practice = row.get(
                    "Practice_Plan",
                    "Practice the recommended concepts regularly."
                )

                st.info(
                    str(practice)
                )

                st.markdown("### 💻 Recommended Project")

                project = row.get(
                    "Project",
                    "Build a practical project related to this course."
                )

                st.info(
                    str(project)
                )

            # ------------------------------------------------
            # RIGHT COLUMN
            # ------------------------------------------------

            with col2:

                st.markdown("### 🏆 Recommended Certification")

                certification = row.get(
                    "Certification",
                    "Complete a relevant certification."
                )

                st.info(
                    str(certification)
                )

                st.markdown("### 📈 Difficulty Level")

                difficulty = row.get(
                    "Difficulty",
                    "Intermediate"
                )

                st.info(
                    str(difficulty)
                )

        else:

            st.warning(
                "Course was predicted, but detailed resource "
                "information was not found in the dataset."
            )

        # ====================================================
        # WEEKLY LEARNING PLAN
        # ====================================================

        st.divider()

        st.subheader("📅 Personalized Weekly Learning Plan")

        theory_hours = round(
            time_available * 0.30,
            1
        )

        practice_hours = round(
            time_available * 0.30,
            1
        )

        project_hours = round(
            time_available * 0.25,
            1
        )

        revision_hours = round(
            time_available * 0.15,
            1
        )

        weekly_plan = pd.DataFrame(
            {
                "Learning Activity": [
                    "📖 Theory / Concepts",
                    "✍️ Practice",
                    "💻 Project Work",
                    "🔄 Revision"
                ],

                "Hours": [
                    theory_hours,
                    practice_hours,
                    project_hours,
                    revision_hours
                ]
            }
        )

        st.dataframe(
            weekly_plan,
            use_container_width=True,
            hide_index=True
        )

        # ====================================================
        # PERFORMANCE
        # ====================================================

        st.divider()

        st.subheader("📊 Current Performance")

        st.write(
            f"Average Assessment Score: **{average_score}%**"
        )

        st.progress(
            average_score / 100
        )

        st.write(
            f"Lowest Assessment Score: **{lowest_score}%**"
        )

        st.write(
            f"Identified Skill Gaps: **{skill_gap_count}**"
        )

        # ====================================================
        # PERSONALIZED SUMMARY
        # ====================================================

        st.divider()

        st.subheader("🎓 Personalized Learning Summary")

        st.write(
            f"""
            **Branch:** {branch}

            **Semester:** {semester}

            **Career Goal:** {career_goal}

            **Average Performance:** {average_score}%

            **Lowest Performance:** {lowest_score}%

            **Skill Gaps:** {skill_gap_count}

            **Available Time:** {time_available} hours/week

            **Next Course:** {recommended_course}
            """
        )

        # ====================================================
        # FINAL MESSAGE
        # ====================================================

        st.success(
            f"🚀 Start learning **{recommended_course}** "
            "and follow your personalized weekly plan."
        )

    except Exception as e:

        st.error(
            "❌ Something went wrong while generating "
            "the recommendation."
        )

        st.exception(e)

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Personalized Learning Recommendation System | "
    "Machine Learning Project | MCA"
)
