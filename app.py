import streamlit as st
import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Personalized Learning Recommendation System",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("🎓 Personalized Learning Recommendation System")

st.write(
    "AI-based system that recommends a personalized learning path "
    "based on a student's skills, career goals, assessment scores "
    "and learning preferences."
)

st.divider()


# =========================================================
# LOAD DATASET
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_excel("dataset.xlsx")

    return df


try:
    df = load_data()

except Exception:
    st.error(
        "Dataset not found. Please keep your Excel dataset "
        "in the same folder as app.py and name it dataset.xlsx."
    )
    st.stop()


# =========================================================
# FEATURES
# =========================================================

features = [
    "Current_Branch",
    "Year",
    "Current_Knowledge_Level",
    "Programming_Skill",
    "Learning_History",
    "Skill_Gap",
    "Career_Goal",
    "Career_Clarity",
    "Target_Domain",
    "Assessment_Score",
    "Aptitude_Score",
    "Coding_Score",
    "Time_Availability_Hours_Per_Week",
    "Preferred_Learning_Style",
    "Interests",
    "Student_Situation",
    "Learning_Readiness"
]

categorical_features = [
    "Current_Branch",
    "Current_Knowledge_Level",
    "Programming_Skill",
    "Learning_History",
    "Skill_Gap",
    "Career_Goal",
    "Career_Clarity",
    "Target_Domain",
    "Preferred_Learning_Style",
    "Interests",
    "Student_Situation",
    "Learning_Readiness"
]

numerical_features = [
    "Year",
    "Assessment_Score",
    "Aptitude_Score",
    "Coding_Score",
    "Time_Availability_Hours_Per_Week"
]


# =========================================================
# TRAIN MODEL
# =========================================================

X = df[features]
y = df["Recommended_Course"]


preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)


model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),

        (
            "classifier",
            RandomForestClassifier(
                n_estimators=300,
                random_state=42,
                class_weight="balanced"
            )
        )
    ]
)


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


model.fit(X_train, y_train)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("🎯 Student Information")

st.sidebar.write(
    "Enter the student's information below "
    "to generate a personalized recommendation."
)


# =========================================================
# INPUT SECTION
# =========================================================

col1, col2 = st.columns(2)


with col1:

    current_branch = st.selectbox(
        "Current Branch",
        sorted(df["Current_Branch"].dropna().unique())
    )

    year = st.selectbox(
        "Year",
        sorted(df["Year"].dropna().unique())
    )

    knowledge_level = st.selectbox(
        "Current Knowledge Level",
        sorted(df["Current_Knowledge_Level"].dropna().unique())
    )

    programming_skill = st.selectbox(
        "Programming Skill",
        sorted(df["Programming_Skill"].dropna().unique())
    )

    learning_history = st.selectbox(
        "Learning History",
        sorted(df["Learning_History"].dropna().unique())
    )

    skill_gap = st.selectbox(
        "Skill Gap",
        sorted(df["Skill_Gap"].dropna().unique())
    )

    career_goal = st.selectbox(
        "Career Goal",
        sorted(df["Career_Goal"].dropna().unique())
    )

    career_clarity = st.selectbox(
        "Career Clarity",
        sorted(df["Career_Clarity"].dropna().unique())
    )

    target_domain = st.selectbox(
        "Target Domain",
        sorted(df["Target_Domain"].dropna().unique())
    )


with col2:

    assessment_score = st.slider(
        "Assessment Score",
        min_value=0,
        max_value=100,
        value=70
    )

    aptitude_score = st.slider(
        "Aptitude Score",
        min_value=0,
        max_value=100,
        value=70
    )

    coding_score = st.slider(
        "Coding Score",
        min_value=0,
        max_value=100,
        value=50
    )

    time_available = st.slider(
        "Time Availability (Hours/Week)",
        min_value=1,
        max_value=40,
        value=10
    )

    learning_style = st.selectbox(
        "Preferred Learning Style",
        sorted(df["Preferred_Learning_Style"].dropna().unique())
    )

    interests = st.selectbox(
        "Interests",
        sorted(df["Interests"].dropna().unique())
    )

    student_situation = st.selectbox(
        "Student Situation",
        sorted(df["Student_Situation"].dropna().unique())
    )

    learning_readiness = st.selectbox(
        "Learning Readiness",
        sorted(df["Learning_Readiness"].dropna().unique())
    )


# =========================================================
# CREATE STUDENT DATA
# =========================================================

student_data = pd.DataFrame({

    "Current_Branch": [current_branch],

    "Year": [year],

    "Current_Knowledge_Level": [knowledge_level],

    "Programming_Skill": [programming_skill],

    "Learning_History": [learning_history],

    "Skill_Gap": [skill_gap],

    "Career_Goal": [career_goal],

    "Career_Clarity": [career_clarity],

    "Target_Domain": [target_domain],

    "Assessment_Score": [assessment_score],

    "Aptitude_Score": [aptitude_score],

    "Coding_Score": [coding_score],

    "Time_Availability_Hours_Per_Week": [time_available],

    "Preferred_Learning_Style": [learning_style],

    "Interests": [interests],

    "Student_Situation": [student_situation],

    "Learning_Readiness": [learning_readiness]
})


# =========================================================
# RECOMMENDATION BUTTON
# =========================================================

st.divider()

if st.button(
    "🚀 Generate Personalized Learning Path",
    use_container_width=True
):

    # -----------------------------------------------------
    # PREDICT COURSE
    # -----------------------------------------------------

    prediction = model.predict(student_data)

    recommended_course = prediction[0]


    # -----------------------------------------------------
    # TOP 3 RECOMMENDATIONS
    # -----------------------------------------------------

    probabilities = model.predict_proba(student_data)[0]

    course_names = model.classes_

    top_indices = np.argsort(probabilities)[::-1][:3]

    top_courses = pd.DataFrame({

        "Course": course_names[top_indices],

        "Probability (%)":
        (probabilities[top_indices] * 100).round(2)

    })


    # -----------------------------------------------------
    # FIND LEARNING PATH
    # -----------------------------------------------------

    matching = df[
        df["Recommended_Course"] == recommended_course
    ]


    # =====================================================
    # RESULT
    # =====================================================

    st.success("Personalized learning path generated successfully! 🎉")

    st.subheader("🎯 Recommended Course")

    st.info(
        f"### {recommended_course}"
    )


    # =====================================================
    # TOP 3 COURSE RECOMMENDATIONS
    # =====================================================

    st.subheader("📊 Top Course Recommendations")

    result_col1, result_col2 = st.columns([2, 1])


    with result_col1:

        st.dataframe(
            top_courses,
            use_container_width=True,
            hide_index=True
        )


    with result_col2:

        st.metric(
            "Best Match",
            recommended_course
        )


    # =====================================================
    # LEARNING PATH
    # =====================================================

    if len(matching) > 0:

        path = matching.iloc[0]

        st.divider()

        st.subheader("📚 Personalized Learning Path")


        path_col1, path_col2 = st.columns(2)


        with path_col1:

            st.markdown("### 📘 Recommended Course")

            st.write(
                path["Recommended_Course"]
            )


            st.markdown("### 💻 Recommended Project")

            st.write(
                path["Recommended_Project"]
            )


        with path_col2:

            st.markdown("### 🏆 Recommended Certification")

            st.write(
                path["Recommended_Certification"]
            )


            st.markdown("### 📝 Practice Plan")

            st.write(
                path["Practice_Plan"]
            )


    # =====================================================
    # STUDENT PROFILE
    # =====================================================

    st.divider()

    st.subheader("👤 Student Profile")

    profile_col1, profile_col2, profile_col3, profile_col4 = st.columns(4)


    with profile_col1:

        st.metric(
            "Assessment Score",
            assessment_score
        )


    with profile_col2:

        st.metric(
            "Aptitude Score",
            aptitude_score
        )


    with profile_col3:

        st.metric(
            "Coding Score",
            coding_score
        )


    with profile_col4:

        st.metric(
            "Weekly Learning Time",
            f"{time_available} hrs"
        )


    # =====================================================
    # MODEL CONFIDENCE
    # =====================================================

    st.divider()

    st.subheader("🤖 Model Recommendation Confidence")

    chart_data = top_courses.set_index("Course")

    st.bar_chart(
        chart_data["Probability (%)"]
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Personalized Learning Recommendation System | "
    "Random Forest Machine Learning Model"
)
