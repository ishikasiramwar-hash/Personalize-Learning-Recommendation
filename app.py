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
    "Get a personalized learning path based on your engineering "
    "branch, career goal, assessment performance, and available time."
)

st.divider()


# ============================================================
# CHECK MODEL FILES
# ============================================================

MODEL_FILE = "model.joblib"
ENCODER_FILE = "encoders.joblib"

if not os.path.exists(MODEL_FILE):
    st.error(
        "❌ model.joblib is missing. "
        "Please upload model.joblib to the same folder as app.py."
    )
    st.stop()

if not os.path.exists(ENCODER_FILE):
    st.error(
        "❌ encoders.joblib is missing. "
        "Please upload encoders.joblib to the same folder as app.py."
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

    st.error("❌ Error loading ML model files.")
    st.code(str(e))
    st.stop()


# ============================================================
# LOAD DATASET
# ============================================================

DATASET_FILE = "Personalized_Learning_Recommendation_Dataset_1000.xlsx"

if not os.path.exists(DATASET_FILE):

    st.warning(
        "⚠️ Dataset file is missing. "
        "Please upload Personalized_Learning_Recommendation_Dataset_1000.xlsx "
        "to the same folder as app.py."
    )

    st.stop()


try:

    courses = pd.read_excel(
        DATASET_FILE,
        sheet_name="Courses_Resources"
    )

except Exception as e:

    st.error("❌ Could not read Courses_Resources sheet.")
    st.code(str(e))
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("👤 Student Information")

# Branches from encoder
branches = list(branch_encoder.classes_)

selected_branch = st.sidebar.selectbox(
    "Engineering Branch",
    branches
)


# Career goals from encoder
career_goals = list(career_encoder.classes_)

selected_career = st.sidebar.selectbox(
    "Career Goal",
    career_goals
)


semester = st.sidebar.slider(
    "Semester",
    min_value=1,
    max_value=8,
    value=4
)


time_available = st.sidebar.slider(
    "Available Learning Hours / Week",
    min_value=1,
    max_value=40,
    value=10
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
    value=50
)


skill_gap_count = st.sidebar.slider(
    "Number of Skill Gaps",
    min_value=0,
    max_value=10,
    value=2
)


# ============================================================
# RECOMMEND BUTTON
# ============================================================

recommend_button = st.sidebar.button(
    "🚀 Generate Recommendation",
    use_container_width=True
)


# ============================================================
# RECOMMENDATION FUNCTION
# ============================================================

def get_recommendation():

    try:

        # Encode branch
        branch_encoded = branch_encoder.transform(
            [selected_branch]
        )[0]

        # Encode career goal
        career_encoded = career_encoder.transform(
            [selected_career]
        )[0]

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

        # Predict course
        prediction = model.predict(input_data)[0]

        # Convert prediction back to course name
        recommended_course = course_encoder.inverse_transform(
            [prediction]
        )[0]

        return recommended_course

    except Exception as e:

        st.error("❌ Recommendation error.")
        st.code(str(e))

        return None


# ============================================================
# MAIN RESULT
# ============================================================

if recommend_button:

    recommended_course = get_recommendation()

    if recommended_course:

        st.success("✅ Personalized recommendation generated!")

        st.divider()

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

        st.subheader("📊 Learning Performance")

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
        # RECOMMENDED COURSE
        # ----------------------------------------------------

        st.subheader("🎯 Recommended Learning Path")

        st.info(
            f"### 📚 Recommended Course\n"
            f"**{recommended_course}**"
        )


        # ----------------------------------------------------
        # FIND COURSE INFORMATION
        # ----------------------------------------------------

        course_info = courses[
            courses["Course"].astype(str).str.strip()
            ==
            str(recommended_course).strip()
        ]


        if not course_info.empty:

            course_row = course_info.iloc[0]

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("### 📖 Course Details")

                if "Difficulty" in course_row:

                    st.write(
                        f"**Difficulty:** "
                        f"{course_row['Difficulty']}"
                    )

                if "Practice_Plan" in course_row:

                    st.write(
                        f"**Practice Plan:** "
                        f"{course_row['Practice_Plan']}"
                    )


            with col2:

                st.markdown("### 💡 Project & Certification")

                if "Project" in course_row:

                    st.write(
                        f"**Project:** "
                        f"{course_row['Project']}"
                    )

                if "Certification" in course_row:

                    st.write(
                        f"**Certification:** "
                        f"{course_row['Certification']}"
                    )


        else:

            st.warning(
                "Course information was not found in "
                "Courses_Resources sheet."
            )


        st.divider()


        # ----------------------------------------------------
        # WEEKLY PLAN
        # ----------------------------------------------------

        st.subheader("📅 Personalized Weekly Study Plan")

        weekly_plan = {
            "Activity": [
                "📚 Theory / Course Learning",
                "💻 Practice",
                "🛠️ Project Work",
                "🔄 Revision"
            ],
            "Percentage": [
                "30%",
                "30%",
                "25%",
                "15%"
            ],
            "Recommended Hours": [
                round(time_available * 0.30, 1),
                round(time_available * 0.30, 1),
                round(time_available * 0.25, 1),
                round(time_available * 0.15, 1)
            ]
        }

        plan_df = pd.DataFrame(weekly_plan)

        st.table(plan_df)


        st.divider()


        # ----------------------------------------------------
        # SKILL GAP ANALYSIS
        # ----------------------------------------------------

        st.subheader("🔍 Skill Gap Analysis")

        if lowest_score < 40:

            level = "Beginner"
            message = (
                "You have a significant skill gap. "
                "Start with basic concepts and guided practice."
            )

        elif lowest_score < 60:

            level = "Basic / Developing"
            message = (
                "You have some knowledge but need more practice "
                "and concept strengthening."
            )

        elif lowest_score < 75:

            level = "Intermediate"
            message = (
                "Your fundamentals are developing well. "
                "Focus on projects and advanced practice."
            )

        else:

            level = "Advanced"
            message = (
                "Your performance is strong. "
                "Focus on advanced projects and certifications."
            )


        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Current Learning Level",
                level
            )

        with col2:

            st.metric(
                "Priority",
                "High" if lowest_score < 60 else "Medium"
            )

        st.write(message)


        st.divider()


        # ----------------------------------------------------
        # CAREER PATH
        # ----------------------------------------------------

        st.subheader("🚀 Suggested Career Development")

        st.write(
            f"Based on your **{selected_branch}** branch and "
            f"career goal **{selected_career}**, focus on:"
        )

        st.markdown(
            f"""
            - 📚 Complete **{recommended_course}**
            - 💻 Practice regularly
            - 🛠️ Build at least one project
            - 🏆 Work toward a relevant certification
            - 📊 Improve your weak assessment areas
            - ⏰ Follow your {time_available}-hour weekly schedule
            """
        )


else:

    # ========================================================
    # WELCOME SCREEN
    # ========================================================

    st.subheader("👋 Welcome!")

    st.write(
        "Enter your learning information using the sidebar "
        "and click **Generate Recommendation**."
    )

    st.markdown(
        """
        ### The system considers:

        🏫 **Engineering Branch**  
        🎯 **Career Goal**  
        📚 **Semester**  
        📊 **Assessment Performance**  
        🔍 **Skill Gaps**  
        ⏰ **Available Learning Time**

        ### The system provides:

        ✅ Recommended Course  
        ✅ Practice Plan  
        ✅ Project Recommendation  
        ✅ Certification Recommendation  
        ✅ Weekly Learning Plan  
        ✅ Skill Gap Analysis
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Personalized Learning Recommendation System | "
    "Machine Learning Based Academic Project"
)
