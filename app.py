# ============================================================
# STEP 1 — STUDENT PROFILE
# ============================================================

if st.session_state.step == 1:

    # ---------- CUSTOM CSS ----------
    st.markdown("""
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #6b7280;
        margin-bottom: 30px;
    }

    .profile-card {
        padding: 25px;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #f8fafc,
            #eef2ff
        );
        border: 1px solid #e5e7eb;
        box-shadow: 0 8px 25px rgba(0,0,0,0.06);
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .step-box {
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        background: #eef2ff;
        font-weight: 600;
    }

    .highlight-box {
        padding: 18px;
        border-radius: 16px;
        background: linear-gradient(
            135deg,
            #eef2ff,
            #f5f3ff
        );
        border-left: 5px solid #6366f1;
        margin-top: 20px;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------- HEADER ----------

    st.markdown(
        '<div class="main-title">🎓 Personalized Learning</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Build your profile to receive an AI-powered learning path'
        '</div>',
        unsafe_allow_html=True
    )

    # ---------- PROGRESS ----------

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            '<div class="step-box">🟣 1. Student Profile</div>',
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            '<div class="step-box">⚪ 2. Skill Quiz</div>',
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            '<div class="step-box">⚪ 3. Recommendation</div>',
            unsafe_allow_html=True
        )

    st.progress(0.33)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- PROFILE CARD ----------

    st.markdown(
        '<div class="profile-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">👤 Student Information</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Please select your details. "
        "No option is selected automatically."
    )

    # ========================================================
    # DROPDOWN FILTERS
    # ========================================================

    branches = list(branch_encoder.classes_)

    career_goals = list(career_encoder.classes_)

    branch_options = [
        "-- Select Engineering Branch --"
    ] + branches

    career_options = [
        "-- Select Career Goal --"
    ] + career_goals

    col1, col2 = st.columns(2)

    with col1:

        selected_branch = st.selectbox(
            "🎓 Engineering Branch",
            branch_options,
            index=0,
            key="profile_branch"
        )

    with col2:

        selected_career = st.selectbox(
            "💼 Career Goal",
            career_options,
            index=0,
            key="profile_career"
        )

    # ========================================================
    # ACADEMIC DETAILS
    # ========================================================

    st.markdown(
        '<div class="section-title">📚 Academic Details</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        semester_options = [
            "-- Select Semester --"
        ] + [
            f"Semester {i}"
            for i in range(1, 9)
        ]

        selected_semester = st.selectbox(
            "📖 Current Semester",
            semester_options,
            index=0,
            key="profile_semester"
        )

    with col2:

        time_options = [
            "-- Select Learning Time --",
            "1–5 hours/week",
            "6–10 hours/week",
            "11–15 hours/week",
            "16–20 hours/week",
            "21–30 hours/week",
            "30+ hours/week"
        ]

        selected_time = st.selectbox(
            "⏰ Available Learning Time",
            time_options,
            index=0,
            key="profile_time"
        )

    # ========================================================
    # ASSESSMENT DETAILS
    # ========================================================

    st.markdown(
        '<div class="section-title">📊 Assessment & Skills</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        average_options = [
            "-- Select Average Score --",
            "0–39%",
            "40–49%",
            "50–59%",
            "60–69%",
            "70–79%",
            "80–89%",
            "90–100%"
        ]

        selected_average = st.selectbox(
            "📊 Average Assessment Score",
            average_options,
            index=0,
            key="profile_average"
        )

    with col2:

        lowest_options = [
            "-- Select Lowest Score --",
            "0–39%",
            "40–49%",
            "50–59%",
            "60–69%",
            "70–79%",
            "80–89%",
            "90–100%"
        ]

        selected_lowest = st.selectbox(
            "📉 Lowest Assessment Score",
            lowest_options,
            index=0,
            key="profile_lowest"
        )

    with col3:

        skill_gap_options = [
            "-- Select Skill Gaps --",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6+"
        ]

        selected_skill_gap = st.selectbox(
            "⚠️ Skill Gap Count",
            skill_gap_options,
            index=0,
            key="profile_skill_gap"
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # INFORMATION BOX
    # ========================================================

    st.markdown(
        """
        <div class="highlight-box">
        <b>💡 How it works</b><br><br>
        Your branch, career goal, academic performance, available
        learning time and skill gaps will be analyzed by the
        recommendation system. You will then complete a short
        skill quiz before receiving your personalized learning path.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ========================================================
    # CONTINUE BUTTON
    # ========================================================

    if st.button(
        "🚀 Continue to Skill Quiz",
        use_container_width=True,
        type="primary"
    ):

        # ----------------------------------------------------
        # VALIDATE DROPDOWNS
        # ----------------------------------------------------

        if selected_branch == "-- Select Engineering Branch --":

            st.error(
                "❌ Please select your Engineering Branch."
            )

            st.stop()

        if selected_career == "-- Select Career Goal --":

            st.error(
                "❌ Please select your Career Goal."
            )

            st.stop()

        if selected_semester == "-- Select Semester --":

            st.error(
                "❌ Please select your Semester."
            )

            st.stop()

        if selected_time == "-- Select Learning Time --":

            st.error(
                "❌ Please select your available learning time."
            )

            st.stop()

        if selected_average == "-- Select Average Score --":

            st.error(
                "❌ Please select your Average Assessment Score."
            )

            st.stop()

        if selected_lowest == "-- Select Lowest Score --":

            st.error(
                "❌ Please select your Lowest Assessment Score."
            )

            st.stop()

        if selected_skill_gap == "-- Select Skill Gaps --":

            st.error(
                "❌ Please select your Skill Gap Count."
            )

            st.stop()

        # ====================================================
        # CONVERT DROPDOWN VALUES TO NUMBERS
        # ====================================================

        semester = int(
            selected_semester.split()[-1]
        )

        # ----------------------------------------------------
        # LEARNING TIME
        # ----------------------------------------------------

        if selected_time == "1–5 hours/week":
            time_available = 5

        elif selected_time == "6–10 hours/week":
            time_available = 10

        elif selected_time == "11–15 hours/week":
            time_available = 15

        elif selected_time == "16–20 hours/week":
            time_available = 20

        elif selected_time == "21–30 hours/week":
            time_available = 30

        else:
            time_available = 35

        # ----------------------------------------------------
        # AVERAGE SCORE
        # ----------------------------------------------------

        def convert_score(score_range):

            if score_range == "0–39%":
                return 30

            elif score_range == "40–49%":
                return 45

            elif score_range == "50–59%":
                return 55

            elif score_range == "60–69%":
                return 65

            elif score_range == "70–79%":
                return 75

            elif score_range == "80–89%":
                return 85

            elif score_range == "90–100%":
                return 95

            return 0

        average_score = convert_score(
            selected_average
        )

        lowest_score = convert_score(
            selected_lowest
        )

        # ----------------------------------------------------
        # SKILL GAP
        # ----------------------------------------------------

        if selected_skill_gap == "6+":

            skill_gap_count = 6

        else:

            skill_gap_count = int(
                selected_skill_gap
            )

        # ====================================================
        # SAVE PROFILE
        # ====================================================

        st.session_state.selected_branch = (
            selected_branch
        )

        st.session_state.selected_career = (
            selected_career
        )

        st.session_state.semester = semester

        st.session_state.time_available = (
            time_available
        )

        st.session_state.average_score = (
            average_score
        )

        st.session_state.lowest_score = (
            lowest_score
        )

        st.session_state.skill_gap_count = (
            skill_gap_count
        )

        # ====================================================
        # MOVE TO QUIZ
        # ====================================================

        st.session_state.step = 2

        st.rerun()
