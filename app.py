import streamlit as st
import pandas as pd

# =========================================================
# REBOOT
# Your Personal Rhythm
# =========================================================

APP_NAME = "REBOOT"
TAGLINE = "Your Personal Rhythm"
VERSION = "1.0.0"

st.set_page_config(
    page_title=f"{APP_NAME} | {TAGLINE}",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #f7f9fa;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stHeader"] {
    background: transparent;
}

/* Header */

.app-header {
    text-align: center;
    padding: 10px 0 25px 0;
}

.app-name {
    font-size: 52px;
    font-weight: 800;
    letter-spacing: 5px;
    color: #111827;
}

.app-tagline {
    font-size: 20px;
    color: #4b5563;
}

.app-motto {
    margin-top: 8px;
    color: #18aaa3;
    font-size: 15px;
}

/* Section */

.section-title {
    font-size: 25px;
    font-weight: 750;
    color: #111827;
    margin: 25px 0 15px 0;
}

/* Cards */

.card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 15px;
}

.metric-title {
    color: #6b7280;
    font-size: 14px;
    font-weight: 700;
}

.metric-value {
    color: #111827;
    font-size: 25px;
    font-weight: 800;
    margin-top: 7px;
}

/* Score */

.score-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    padding: 25px;
    text-align: center;
}

.score {
    font-size: 50px;
    font-weight: 800;
    color: #111827;
}

.score-small {
    color: #6b7280;
}

/* Attention */

.attention {
    background: #effaf9;
    border-left: 5px solid #18aaa3;
    border-radius: 10px;
    padding: 14px;
    margin-bottom: 10px;
}

/* Footer */

.footer {
    text-align: center;
    color: #9ca3af;
    font-size: 13px;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATA
# =========================================================

if "sleep" not in st.session_state:
    st.session_state.sleep = 7.0

if "steps" not in st.session_state:
    st.session_state.steps = 6000

if "study" not in st.session_state:
    st.session_state.study = 2.0

if "exercise" not in st.session_state:
    st.session_state.exercise = 45

if "screen" not in st.session_state:
    st.session_state.screen = 4.0

if "mood" not in st.session_state:
    st.session_state.mood = 7

if "energy" not in st.session_state:
    st.session_state.energy = 7

if "weekly_scores" not in st.session_state:
    st.session_state.weekly_scores = [
        72, 76, 70, 81, 78, 84, 0
    ]


# =========================================================
# SCORE
# =========================================================

def calculate_score():

    sleep_score = min(st.session_state.sleep / 8, 1) * 20

    steps_score = min(st.session_state.steps / 10000, 1) * 15

    study_score = min(st.session_state.study / 4, 1) * 15

    exercise_score = min(st.session_state.exercise / 60, 1) * 15

    screen_score = max(
        0,
        15 - max(0, st.session_state.screen - 2) * 3
    )

    mood_score = st.session_state.mood

    energy_score = st.session_state.energy

    total = (
        sleep_score
        + steps_score
        + study_score
        + exercise_score
        + screen_score
        + mood_score
        + energy_score
    )

    return round(max(0, min(100, total)))


def get_status(score):

    if score >= 85:
        return "Excellent"

    if score >= 70:
        return "Good"

    if score >= 50:
        return "Fair"

    return "Needs Attention"


def get_attention():

    messages = []

    if st.session_state.sleep < 7:
        messages.append(
            "Your sleep was a little low today. "
            "Try giving yourself some extra time to rest tonight."
        )

    if st.session_state.steps < 5000:
        messages.append(
            "Your activity was lower today. "
            "A short walk could help you stay active."
        )

    if st.session_state.study < 1.5:
        messages.append(
            "Try adding one short distraction-free study session."
        )

    if st.session_state.exercise < 30:
        messages.append(
            "Your exercise was a little low today. "
            "Some movement could help."
        )

    if st.session_state.screen > 6:
        messages.append(
            "Your screen time was a little high today. "
            "Try taking some screen-free breaks."
        )

    if st.session_state.mood < 5:
        messages.append(
            "Take some time to relax and reset today."
        )

    if st.session_state.energy < 5:
        messages.append(
            "Your energy is a little low. "
            "Rest and recovery may help."
        )

    if not messages:
        messages.append(
            "You're doing well today. Keep your rhythm going."
        )

    return messages


score = calculate_score()
status = get_status(score)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="app-header">

    <div class="app-name">REBOOT</div>

    <div class="app-tagline">
        Your Personal Rhythm
    </div>

    <div class="app-motto">
        Small steps. Better days. Reboot yourself.
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# NAVIGATION
# =========================================================

page = st.radio(
    "Pages",
    ["HOME", "TODAY", "HEALTH", "PROGRESS"],
    horizontal=True,
    label_visibility="collapsed"
)


# =========================================================
# HOME
# =========================================================

if page == "HOME":

    st.markdown(
        '<div class="section-title">Reboot Score</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1, 2])

    with left:

        st.markdown(f"""
        <div class="score-card">

            <div class="score">{score}</div>

            <div class="score-small">
                / 100
            </div>

            <br>

            <b>{status}</b>

            <br>

            <span class="score-small">
                Today's Status
            </span>

        </div>
        """, unsafe_allow_html=True)

    with right:

        st.markdown(
            '<div class="section-title">What Needs Attention?</div>',
            unsafe_allow_html=True
        )

        for message in get_attention():

            st.markdown(
                f'<div class="attention">{message}</div>',
                unsafe_allow_html=True
            )


    # -----------------------------------------------------
    # OVERVIEW
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">Today\'s Overview</div>',
        unsafe_allow_html=True
    )

    metrics = [
        ("SLEEP", f"{st.session_state.sleep:.1f} h"),
        ("STEPS", f"{st.session_state.steps:,}"),
        ("STUDY / FOCUS", f"{st.session_state.study:.1f} h"),
        ("EXERCISE / ACTIVITY", f"{st.session_state.exercise} min"),
        ("SCREEN TIME", f"{st.session_state.screen:.1f} h"),
        ("MOOD", f"{st.session_state.mood}/10"),
        ("ENERGY", f"{st.session_state.energy}/10"),
    ]

    columns = st.columns(4)

    for i, (name, value) in enumerate(metrics):

        with columns[i % 4]:

            st.markdown(f"""
            <div class="card">

                <div class="metric-title">
                    {name}
                </div>

                <div class="metric-value">
                    {value}
                </div>

            </div>
            """, unsafe_allow_html=True)


# =========================================================
# TODAY
# =========================================================

elif page == "TODAY":

    st.markdown(
        '<div class="section-title">Quick Daily Check-In</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Enter your information for today."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.session_state.sleep = st.slider(
            "Sleep",
            0.0,
            12.0,
            float(st.session_state.sleep),
            0.5
        )

        st.session_state.steps = st.number_input(
            "Steps",
            min_value=0,
            max_value=50000,
            value=int(st.session_state.steps),
            step=500
        )

        st.session_state.study = st.slider(
            "Study / Focus",
            0.0,
            12.0,
            float(st.session_state.study),
            0.5
        )

        st.session_state.exercise = st.slider(
            "Exercise / Activity",
            0,
            240,
            int(st.session_state.exercise),
            5
        )

    with col2:

        st.session_state.screen = st.slider(
            "Screen Time",
            0.0,
            16.0,
            float(st.session_state.screen),
            0.5
        )

        st.session_state.mood = st.slider(
            "Mood",
            1,
            10,
            int(st.session_state.mood)
        )

        st.session_state.energy = st.slider(
            "Energy",
            1,
            10,
            int(st.session_state.energy)
        )

    if st.button(
        "Save Today's Check-In",
        type="primary"
    ):

        new_score = calculate_score()

        st.session_state.weekly_scores[-1] = new_score

        st.success(
            f"Saved! Your Reboot Score is {new_score}/100."
        )


# =========================================================
# HEALTH
# =========================================================

elif page == "HEALTH":

    st.markdown(
        '<div class="section-title">Health & Activity</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="card">

        <h3>Sync Health Data</h3>

        <p>
        REBOOT can be connected to health data in a future
        Android version using Health Connect.
        </p>

        <p>
        The current web version does not pretend to have
        access to your phone's private health data.
        </p>

    </div>
    """, unsafe_allow_html=True)

    if st.button("Sync Health Data"):

        st.info(
            "Automatic Health Connect syncing is not available "
            "in this web version yet."
        )

    st.markdown(
        '<div class="section-title">Available Metrics</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="card">

    <b>REBOOT currently tracks:</b>

    <br><br>

    • Sleep<br>
    • Steps<br>
    • Study / Focus<br>
    • Exercise / Activity<br>
    • Screen Time<br>
    • Mood<br>
    • Energy

    </div>
    """, unsafe_allow_html=True)

    st.info(
        "For now, enter your health information manually "
        "from the TODAY page."
    )


# =========================================================
# PROGRESS
# =========================================================

elif page == "PROGRESS":

    st.markdown(
        '<div class="section-title">Weekly Progress</div>',
        unsafe_allow_html=True
    )

    scores = st.session_state.weekly_scores

    chart = pd.DataFrame({
        "Day": [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Today"
        ],
        "Score": scores
    })

    st.line_chart(
        chart.set_index("Day"),
        height=320
    )

    completed = [
        x for x in scores
        if x > 0
    ]

    if completed:

        average = round(
            sum(completed) / len(completed)
        )

        best = max(completed)

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Weekly Average",
                f"{average}/100"
            )

        with c2:
            st.metric(
                "Best This Week",
                f"{best}/100"
            )

    else:

        st.info(
            "Complete your daily check-ins "
            "to build your progress."
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

    REBOOT · Your Personal Rhythm · Version 1.0.0

</div>
""", unsafe_allow_html=True)