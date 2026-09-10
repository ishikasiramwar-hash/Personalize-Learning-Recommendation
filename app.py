# ============================================================
# STEP 1 — STUDENT PROFILE
# ============================================================

if st.session_state.step == 1:

    # --------------------------------------------------------
    # CUSTOM CSS — MODERN / EYE-CATCHING UI
    # --------------------------------------------------------

    st.markdown("""
    <style>

    .profile-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .profile-subtitle {
        text-align: center;
        font-size: 17px;
        color: #666;
        margin-bottom: 30px;
    }

    .profile-card {
        padding: 25px;
        border-radius: 18px;
        background: linear-gradient(
            135deg,
            #f8f9ff,
            #eef3ff
        );
        border: 1px solid #dfe5ff;
        margin-bottom: 25px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.06);
    }

    .section-title {
        font-size: 23px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .step-box {
        text-align: center;
        padding: 15px;
        border-radius: 15px;
        background: #f5f7ff;
        margin-bottom: 25px;
    }

    .continue-text {
        text-align: center;
        font-size: 14px;
        color: #777;
        margin-top: 10px;
    }

    </style>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="profile-title">🎓 Student Profile</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="profile-subtitle">'
        'Tell us about yourself so we can create your personalized learning path.'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    st.progress(
        1 / 3,
        text="Step 1 of 3 — Student Profile"
    )

    # --------------------------------------------------------
    # STEP INDICATOR
    # --------------------------------------------------------

    st.markdown("""
    <div class="step-box">

    <b>👤 Profile</b>
    &nbsp;&nbsp;→&nbsp;&nbsp;
    📝 Quiz
    &nbsp;&nbsp;→&nbsp;&nbsp;
    🎯 Recommendation

    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # PROFILE CARD
    # --------------------------------------------------------

    st.markdown(
        '<div class="profile-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">'
        '👨‍🎓 Academic & Career Information'
        '</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # DROPDOWN VALUES
    # ========================================================

    branches = list(
        branch_encoder.classes_
    )

    career_goals = list(
        career_encoder.classes_
    )

    # Add placeholder
    branch_options = [
        "-- Select Branch --"
    ] + branches

    career_options = [
        "-- Select Career Goal --"
    ] + career_goals

    # --------------------------------------------------------
    # BRANCH & CAREER
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # SEMESTER & LEARNING TIME
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        semester_options = [
            "-- Select Semester --",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8"
        ]

        selected_semester = st.selectbox(
            "📚 Current Semester",
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

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # ACADEMIC PERFORMANCE
    # ========================================================

    st.markdown(
        '<div class="profile-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">'
        '📊 Academic Performance & Skill Gaps'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # AVERAGE SCORE
    # --------------------------------------------------------

    average_score_options = [
        "-- Select Average Score --",
        "Below 40%",
        "40% – 59%",
        "60% – 69%",
        "70% – 79%",
        "80% – 89%",
        "90% – 100%"
    ]

    lowest_score_options = [
        "-- Select Lowest Score --",
        "Below 40%",
        "40% – 59%",
        "60% – 69%",
        "70% – 79%",
        "80% – 89%",
        "90% – 100%"
    ]

    col1, col2 = st.columns(2)

    with col1:

        average_score_range = st.selectbox(
            "📈 Average Assessment Score",
            average_score_options,
            index=0,
            key="profile_average"
        )

    with col2:

        lowest_score_range = st.selectbox(
            "📉 Lowest Assessment Score",
            lowest_score_options,
            index=0,
            key="profile_lowest"
        )

    # --------------------------------------------------------
    # SKILL GAPS
    # --------------------------------------------------------

    skill_gap_options = [
        "-- Select Skill Gap Level --",
        "No Skill Gap",
        "1–2 Skill Gaps",
        "3–4 Skill Gaps",
        "5–6 Skill Gaps",
        "7+ Skill Gaps"
    ]

    selected_skill_gap = st.selectbox(
        "⚠️ Current Skill Gap Level",
        skill_gap_options,
        index=0,
        key="profile_skill_gap"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # CONVERT DROPDOWN VALUES TO ML VALUES
    # ========================================================

    def convert_score(score_range):

        if score_range == "Below 40%":
            return 30

        elif score_range == "40% – 59%":
            return 50

        elif score_range == "60% – 69%":
            return 65

        elif score_range == "70% – 79%":
            return 75

        elif score_range == "80% – 89%":
            return 85

        elif score_range == "90% – 100%":
            return 95

        return None


    def convert_skill_gap(skill_gap):

        if skill_gap == "No Skill Gap":
            return 0

        elif skill_gap == "1–2 Skill Gaps":
            return 2

        elif skill_gap == "3–4 Skill Gaps":
            return 4

        elif skill_gap == "5–6 Skill Gaps":
            return 6

        elif skill_gap == "7+ Skill Gaps":
            return 7

        return None


    def convert_time(time_value):

        if time_value == "1–5 hours/week":
            return 5

        elif time_value == "6–10 hours/week":
            return 10

        elif time_value == "11–15 hours/week":
            return 15

        elif time_value == "16–20 hours/week":
            return 20

        elif time_value == "21–30 hours/week":
            return 30

        elif time_value == "30+ hours/week":
            return 35

        return None


    # ========================================================
    # CONTINUE BUTTON
    # ========================================================

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "🚀 Continue to Skill Quiz",
        use_container_width=True,
        type="primary"
    ):

        # ----------------------------------------------------
        # VALIDATE ALL DROPDOWNS
        # ----------------------------------------------------

        if selected_branch == "-- Select Branch --":

            st.error(
                "⚠️ Please select your Engineering Branch."
            )

            st.stop()


        if selected_career == "-- Select Career Goal --":

            st.error(
                "⚠️ Please select your Career Goal."
            )

            st.stop()


        if selected_semester == "-- Select Semester --":

            st.error(
                "⚠️ Please select your Semester."
            )

            st.stop()


        if selected_time == "-- Select Learning Time --":

            st.error(
                "⚠️ Please select your available learning time."
            )

            st.stop()


        if average_score_range == "-- Select Average Score --":

            st.error(
                "⚠️ Please select your Average Assessment Score."
            )

            st.stop()


        if lowest_score_range == "-- Select Lowest Score --":

            st.error(
                "⚠️ Please select your Lowest Assessment Score."
            )

            st.stop()


        if selected_skill_gap == "-- Select Skill Gap Level --":

            st.error(
                "⚠️ Please select your Skill Gap Level."
            )

            st.stop()


        # ----------------------------------------------------
        # CONVERT VALUES
        # ----------------------------------------------------

        average_score = convert_score(
            average_score_range
        )

        lowest_score = convert_score(
            lowest_score_range
        )

        skill_gap_count = convert_skill_gap(
            selected_skill_gap
        )

        time_available = convert_time(
            selected_time
        )

        semester = int(
            selected_semester
        )


        # ----------------------------------------------------
        # SAVE PROFILE
        # ----------------------------------------------------

        st.session_state.selected_branch = (
            selected_branch
        )

        st.session_state.selected_career = (
            selected_career
        )

        st.session_state.semester = (
            semester
        )

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


        # ----------------------------------------------------
        # GO TO QUIZ
        # ----------------------------------------------------

        st.session_state.step = 2

        st.rerun()


    st.markdown(
        '<div class="continue-text">'
        '🔒 Your profile information is used only to generate '
        'your personalized learning recommendation.'
        '</div>',
        unsafe_allow_html=True
    )
