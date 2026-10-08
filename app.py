import streamlit as st
import pandas as pd
from pathlib import Path

# ============================================================
# REBOOT — Your Personal Rhythm
# ============================================================

APP_NAME = "REBOOT"
TAGLINE = "Your Personal Rhythm"
MOTIVATION = "Small steps. Better days. Reboot yourself."
VERSION = "1.0.0"
ICON_PATH = Path("reboot_icon.png")


# ============================================================
# PAGE SETUP
# ============================================================

page_icon = "🔄"

if ICON_PATH.exists():
    page_icon = str(ICON_PATH)

st.set_page_config(
    page_title=f"{APP_NAME} — {TAGLINE}",
    page_icon=page_icon,
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main page */
    .stApp {
        background: #f7f9fa;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Hide Streamlit decoration/header area */
    [data-testid="stHeader"] {
        background: transparent;
    }

    /* Main REBOOT header */
    .reboot-header {
        text-align: center;
        padding: 10px 10px 25px 10px;
    }

    .reboot-title {
        font-size: 3.2rem;
        font-weight: 800;
        letter-spacing: 4px;
        margin: 0;
        color: #111827;
    }

    .reboot-tagline {
        font-size: 1.15rem;
        color: #4b5563;
        margin-top: 2px;
    }

    .reboot-motivation {
        font-size: 0.95rem;
        color: #18a9a2;
        margin-top: 8px;
    }

    /* Section headings */
    .section-title {
        font-size: 1.35rem;
        font-weight: 750;
        color: #111827;
        margin-top: 20px;
        margin-bottom: 12px;
    }

    /* Cards */
    .card {
        background: white;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }

    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 18px;
        min-height: 125px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 3px 10px rgba(0,0,0,0.035);
    }

    .metric-name {
        color: #6b7280;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    .metric-value {
        color: #111827;
        font-size: 1.55rem;
        font-weight: 800;
        margin-top: 8px;
    }

    .metric-description {
        color: #6b7280;
        font-size: 0.8rem;
        margin-top: 3px;
    }

    /* Score */
    .score-box {
        text-align: center;
        background: white;
        border-radius: 20px;
        padding: 25px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }

    .score-number {
        font-size: 2.7rem;
        font-weight: 800;
        color: #111827;
    }

    .score-label {
        color: #6b7280;
        font-size: 0.9rem;
    }

    /* Attention */
    .attention {
        background: #f0fbfa;
        border-left: 5px solid #18b8b0;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 10px;
        color: #374151;
    }

    /* Sync */
    .sync-card {
        background: #ffffff;
        border: 1px solid #dce8e8;
        border-radius: 18px;
        padding: 22px;
        margin-top: 10px;
    }

    .sync-title {
        font-size: 1.2rem;
        font-weight: 750;
        color: #111827;
    }

    .sync-text {
        color: #6b7280;
        margin-top: 6px;
        line-height: 1.5;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 0.8rem;
        padding: 30px 0 10px 0;
    }

    /* Mobile */
    @media (max-width: 700px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .reboot-title {
            font-size: 2.4rem;
        }

        .reboot-tagline {
            font-size: 1rem;
        }

        .metric-card {
            min-height: 110px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION DATA
# ============================================================

defaults = {
    "sleep": 7.0,
    "steps": 6000,
    "study": 2.0,
    "exercise": 45,
    "screen": 4.0,
    "mood": 7,
    "energy": 7,
    "saved": False,
    "weekly_scores": [72, 76, 70, 81, 78, 84, 0],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# SCORE CALCULATION
# ============================================================

def calculate_score():
    sleep_score = min(st.session_state.sleep / 8, 1) * 20

    steps_score = min(st.session_state.steps / 10000, 1) * 15

    study_score = min(st.session_state.study / 4, 1) * 15

    exercise_score = min(st.session_state.exercise / 60, 1) * 15

    screen_score = max(
        0,
        15 - max(0, st.session_state.screen - 2) * 3
    )

    mood_score = (st.session_state.mood / 10) * 10

    energy_score = (st.session_state.energy / 10) * 10

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
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Fair"
    else:
        return "Needs Attention"


def get_attention():
    messages = []

    if st.session_state.sleep < 7:
        messages.append(
            "Your sleep was a little low today. Try giving yourself some extra time to rest tonight."
        )

    if st.session_state.steps < 5000:
        messages.append(
            "Your activity was lower today. A short walk or some movement could help."
        )

    if st.session_state.study < 1.5:
        messages.append(
            "You could use a little more focused study time. Try one short distraction-free session."
        )

    if st.session_state.exercise < 30:
        messages.append(
            "Your exercise was a little low today. Even a short activity session can help."
        )

    if st.session_state.screen > 6:
        messages.append(
            "Your screen time was a little high today. Try taking a few short screen-free breaks."
        )

    if st.session_state.mood < 5:
        messages.append(
            "Your mood seems a little lower today. Give yourself some time to relax and reset."
        )

    if st.session_state.energy < 5:
        messages.append(
            "Your energy seems a little low today. Rest, hydration and a good routine may help."
        )

    if not messages:
        messages.append(
            "You're doing well today. Keep your rhythm going."
        )

    return messages


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="reboot-header">
        <div class="reboot-title">REBOOT</div>
        <div class="reboot-tagline">Your Personal Rhythm</div>
        <div class="reboot-motivation">
            Small steps. Better days. Reboot yourself.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# NAVIGATION
# ============================================================

page = st.radio(
    "Navigation",
    ["HOME", "TODAY", "HEALTH", "PROGRESS"],
    horizontal=True,
    label_visibility="collapsed",
)


score = calculate_score()
status = get_status(score)


# ============================================================
# HOME
# ============================================================

if page == "HOME":

    st.markdown(
        '<div class="section-title">Reboot Score</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 2])

    with col1:

        st.markdown(
            f"""
            <div class="score-box">

                <svg width="190" height="190" viewBox="0 0 190 190">

                    <circle
                        cx="95"
                        cy="95"
                        r="75"
                        fill="none"
                        stroke="#dfe5e7"
                        stroke-width="14"
                    />

                    <circle
                        cx="95"
                        cy="95"
                        r="75"
                        fill="none"
                        stroke="#18b8b0"
                        stroke-width="14"
                        stroke-linecap="round"
                        stroke-dasharray="{score * 4.71} 471"
                        transform="rotate(-90 95 95)"
                    />

                    <text
                        x="95"
                        y="102"
                        text-anchor="middle"
                        font-size="38"
                        font-weight="800"
                        fill="#111827"
                    >
                        {score}
                    </text>

                    <text
                        x="95"
                        y="125"
                        text-anchor="middle"
                        font-size="12"
                        fill="#6b7280"
                    >
                        / 100
                    </text>

                </svg>

                <div class="score-number">{status}</div>
                <div class="score-label">Today's Status</div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            '<div class="section-title">What Needs Attention?</div>',
            unsafe_allow_html=True,
        )

        for message in get_attention():
            st.markdown(
                f'<div class="attention">{message}</div>',
                unsafe_allow_html=True,
            )

    # --------------------------------------------------------
    # Today's Overview
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Today\'s Overview</div>',
        unsafe_allow_html=True,
    )

    metrics = [
        ("SLEEP", f"{st.session_state.sleep:.1f} h", "Rest"),
        ("STEPS", f"{st.session_state.steps:,}", "Activity"),
        ("STUDY / FOCUS", f"{st.session_state.study:.1f} h", "Focus time"),
        ("EXERCISE", f"{st.session_state.exercise} min", "Movement"),
        ("SCREEN TIME", f"{st.session_state.screen:.1f} h", "Device time"),
        ("MOOD", f"{st.session_state.mood}/10", "How you feel"),
        ("ENERGY", f"{st.session_state.energy}/10", "Energy level"),
    ]

    cols = st.columns(4)

    for i, (name, value, description) in enumerate(metrics):

        with cols[i % 4]:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-name">{name}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-description">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# TODAY
# ============================================================

elif page == "TODAY":

    st.markdown(
        '<div class="section-title">Quick Daily Check-In</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Enter today's information to update your Reboot Score."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.session_state.sleep = st.slider(
            "Sleep",
            min_value=0.0,
            max_value=12.0,
            value=float(st.session_state.sleep),
            step=0.5,
        )

        st.session_state.steps = st.number_input(
            "Steps",
            min_value=0,
            max_value=50000,
            value=int(st.session_state.steps),
            step=500,
        )

        st.session_state.study = st.slider(
            "Study / Focus",
            min_value=0.0,
            max_value=12.0,
            value=float(st.session_state.study),
            step=0.5,
        )

        st.session_state.exercise = st.slider(
            "Exercise / Activity",
            min_value=0,
            max_value=240,
            value=int(st.session_state.exercise),
            step=5,
        )

    with col2:

        st.session_state.screen = st.slider(
            "Screen Time",
            min_value=0.0,
            max_value=16.0,
            value=float(st.session_state.screen),
            step=0.5,
        )

        st.session_state.mood = st.slider(
            "Mood",
            min_value=1,
            max_value=10,
            value=int(st.session_state.mood),
        )

        st.session_state.energy = st.slider(
            "Energy",
            min_value=1,
            max_value=10,
            value=int(st.session_state.energy),
        )

    if st.button("Save Today's Check-In", type="primary"):

        new_score = calculate_score()

        st.session_state.weekly_scores[-1] = new_score
        st.session_state.saved = True

        st.success(
            f"Today's check-in saved. Your Reboot Score is {new_score}/100."
        )


# ============================================================
# HEALTH
# ============================================================

elif page == "HEALTH":

    st.markdown(
        '<div class="section-title">Health & Activity</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sync-card">

            <div class="sync-title">
                Sync Health Data
            </div>

            <div class="sync-text">
                REBOOT is ready for future health-data integration.
                The current web version uses manual data entry and does
                not pretend to have access to your phone's private
                health data.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button("Sync Health Data"):

        st.info(
            "Automatic Health Connect syncing requires a native Android "
            "integration. This Streamlit version cannot directly read "
            "Health Connect data."
        )

    st.markdown(
        '<div class="section-title">Enter Data Manually</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Use the TODAY page to enter your sleep, steps, study, exercise, "
        "screen time, mood and energy."
    )

    st.markdown(
        """
        <div class="card">

        <b>Current tracked metrics</b>

        <br><br>

        • Sleep<br>
        • Steps<br>
        • Study / Focus<br>
        • Exercise / Activity<br>
        • Screen Time<br>
        • Mood<br>
        • Energy

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PROGRESS
# ============================================================

elif page == "PROGRESS":

    st.markdown(
        '<div class="section-title">Weekly Progress</div>',
        unsafe_allow_html=True,
    )

    scores = st.session_state.weekly_scores

    chart_data = pd.DataFrame(
        {
            "Day": [
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Today",
            ],
            "Reboot Score": scores,
        }
    )

    st.line_chart(
        chart_data.set_index("Day"),
        y="Reboot Score",
        height=320,
    )

    completed_scores = [x for x in scores if x > 0]

    if completed_scores:

        average = round(sum(completed_scores) / len(completed_scores))
        best = max(completed_scores)
        lowest = min(completed_scores)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Weekly Average", f"{average}/100")

        with c2:
            st.metric("Best This Week", f"{best}/100")

        with c3:
            st.metric("Lowest", f"{lowest}/100")

    else:

        st.info("Complete your daily check-ins to build your progress.")


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        REBOOT · Your Personal Rhythm · Version 1.0.0
    </div>
    """,
    unsafe_allow_html=True,
)
