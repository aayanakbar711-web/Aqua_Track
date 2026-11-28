import html
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st


# =========================================================
# AQUATRACK SETTINGS
# =========================================================
APP_TITLE = "AquaTrack"
DAILY_GOAL_ML = 2500
WATER_SIZES = [150, 250, 350, 500]
HISTORY_FILE = Path("water_history.csv")
REMINDER_MINUTES = 60

COLUMNS = [
    "date",
    "time",
    "day",
    "month",
    "year",
    "amount_ml",
    "action",
]


# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# COLORS AND STYLING
# =========================================================
BG = "#102A43"
CARD = "#163B5C"
BLUE = "#1D4ED8"
DARK_BLUE = "#0B1F33"
GREEN = "#2DD4BF"
ORANGE = "#FBBF24"
RED = "#FB7185"
TEXT = "#F8FAFC"
MUTED = "#B8D3E8"
LIGHT_BLUE = "#38BDF8"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: radial-gradient(
            circle at top right,
            #17466A 0%,
            {BG} 42%,
            #0B1F33 100%
        );
        color: {TEXT};
    }}

    [data-testid="stHeader"] {{
        background: rgba(16, 42, 67, 0.85);
    }}

    [data-testid="stToolbar"] {{
        right: 1rem;
    }}

    .block-container {{
        max-width: 1200px;
        padding-top: 1.25rem;
        padding-bottom: 3rem;
    }}

    h1, h2, h3, h4, p, label, span {{
        color: {TEXT};
    }}

    .brand-header {{
        display: flex;
        align-items: center;
        gap: 14px;
        margin: 0 0 1.4rem 0;
        padding: 14px 18px;
        border: 1px solid rgba(125, 211, 252, 0.22);
        border-radius: 20px;
        background: rgba(22, 59, 92, 0.82);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
    }}

    .brand-logo {{
        width: 58px;
        height: 58px;
        flex: 0 0 58px;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF;
        font-size: 20px;
        font-weight: 900;
        letter-spacing: 1px;
        background: linear-gradient(145deg, #38BDF8, #1D4ED8);
        border: 1px solid rgba(255, 255, 255, 0.28);
        box-shadow: 0 5px 18px rgba(29, 78, 216, 0.35);
    }}

    .brand-name {{
        font-size: 2rem;
        line-height: 1.1;
        font-weight: 900;
        color: #FFFFFF;
    }}

    .brand-name span {{
        color: #38BDF8;
    }}

    .brand-tagline {{
        color: #B8D3E8;
        font-size: 0.78rem;
        letter-spacing: 2px;
        font-weight: 700;
        margin-top: 5px;
    }}

    .hero {{
        text-align: center;
        padding: 0.25rem 0 1rem 0;
    }}

    .hero p {{
        color: {MUTED};
        letter-spacing: 2px;
        font-size: 0.82rem;
        font-weight: 700;
        margin-top: 0.2rem;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        border-color: rgba(125, 211, 252, 0.20);
        border-radius: 20px;
        background: linear-gradient(
            145deg,
            rgba(22, 59, 92, 0.98),
            rgba(18, 48, 74, 0.98)
        );
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16);
    }}

    .metric-label {{
        color: {MUTED};
        font-size: 0.9rem;
    }}

    .metric-value {{
        color: #FFFFFF;
        font-size: 1.65rem;
        font-weight: 850;
    }}

    .badge {{
        background: #123653;
        border: 1px solid rgba(125, 211, 252, 0.18);
        border-radius: 14px;
        padding: 0.85rem 1rem;
        margin: 0.45rem 0;
    }}

    .badge-title {{
        font-weight: 800;
        color: #FFFFFF;
    }}

    .badge-desc {{
        color: {MUTED};
        font-size: 0.88rem;
    }}

    .badge-status {{
        font-size: 0.76rem;
        font-weight: 800;
    }}

    div.stButton > button {{
        border-radius: 13px;
        min-height: 2.8rem;
        font-weight: 750;
        border: 1px solid rgba(125, 211, 252, 0.35);
        color: #EAF6FF;
        background: #17466A;
        transition: all 0.2s ease;
    }}

    div.stButton > button:hover {{
        border-color: #38BDF8;
        color: #FFFFFF;
        transform: translateY(-1px);
        box-shadow: 0 5px 16px rgba(56, 189, 248, 0.18);
    }}

    div.stButton > button[kind="primary"] {{
        background: linear-gradient(100deg, #1D4ED8, #0284C7);
        border-color: #38BDF8;
        color: white;
    }}

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {{
        background: #0F304B;
        border-color: #3B6B8D;
        color: #FFFFFF;
        border-radius: 12px;
    }}

    div[data-baseweb="select"] * {{
        color: #FFFFFF !important;
    }}

    div[data-testid="stCheckbox"] label,
    div[data-testid="stToggle"] label {{
        color: #EAF6FF;
    }}

    .glass-wrap {{
        display: flex;
        justify-content: center;
        padding: 1rem 0 0.3rem;
    }}

    .glass {{
        width: 132px;
        height: 190px;
        position: relative;
        border: 4px solid #38BDF8;
        border-top: 0;
        border-radius: 8px 8px 28px 28px;
        background: rgba(56, 189, 248, 0.10);
        overflow: hidden;
        clip-path: polygon(0 0, 100% 0, 87% 100%, 13% 100%);
    }}

    .glass:before {{
        content: "";
        position: absolute;
        left: -3px;
        right: -3px;
        top: -5px;
        height: 15px;
        border: 4px solid #38BDF8;
        border-radius: 50%;
        background: #DFF6FF;
        z-index: 2;
    }}

    .water {{
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        background: linear-gradient(
            180deg,
            #7DD3FC,
            #38BDF8,
            #1D4ED8
        );
        transition: height 0.7s ease;
    }}

    .glass-shine {{
        position: absolute;
        z-index: 3;
        left: 25px;
        top: 25px;
        height: 125px;
        width: 5px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.75);
    }}

    .progress-ring {{
        width: 180px;
        height: 180px;
        border-radius: 50%;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
        background: conic-gradient(
            #38BDF8 var(--progress),
            #244B69 0
        );
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.12);
    }}

    .progress-inner {{
        width: 146px;
        height: 146px;
        border-radius: 50%;
        background: #102A43;
        border: 1px solid rgba(125, 211, 252, 0.2);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }}

    .progress-percent {{
        font-size: 2rem;
        font-weight: 900;
        color: #7DD3FC;
    }}

    .progress-amount {{
        font-size: 0.78rem;
        color: {MUTED};
    }}

    .custom-progress-track {{
        width: 100%;
        height: 15px;
        border-radius: 999px;
        overflow: hidden;
        background: #244B69;
        border: 1px solid rgba(125, 211, 252, 0.18);
        box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.2);
        margin: 0.75rem 0 0.4rem;
    }}

    .custom-progress-fill {{
        height: 100%;
        border-radius: 999px;
        transition: width 0.7s ease, background 0.5s ease;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.35);
    }}

    [data-testid="stTabs"] button {{
        color: #B8D3E8 !important;
        font-weight: 750;
    }}

    [data-testid="stTabs"] button[aria-selected="true"] {{
        color: #7DD3FC !important;
        border-bottom-color: #38BDF8 !important;
    }}

    [data-testid="stDataFrame"],
    [data-testid="stTable"] {{
        background: #163B5C;
        border-radius: 12px;
    }}

    [data-testid="stAlert"] {{
        border-radius: 12px;
    }}

    @media (max-width: 640px) {{
        .brand-name {{
            font-size: 1.55rem;
        }}

        .brand-logo {{
            width: 50px;
            height: 50px;
            flex-basis: 50px;
        }}

        .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# CSV DATA FUNCTIONS
# =========================================================
def load_history():
    """Load saved water records while preserving the existing CSV file."""
    if not HISTORY_FILE.exists():
        empty_df = pd.DataFrame(columns=COLUMNS)
        empty_df.to_csv(HISTORY_FILE, index=False)
        return empty_df

    try:
        df = pd.read_csv(HISTORY_FILE)

        # Add any columns missing from an older version of the file.
        for column in COLUMNS:
            if column not in df.columns:
                df[column] = ""

        df = df[COLUMNS].copy()
        df["amount_ml"] = (
            pd.to_numeric(df["amount_ml"], errors="coerce")
            .fillna(0)
            .astype(int)
        )
        df["date"] = df["date"].fillna("").astype(str)
        df["time"] = df["time"].fillna("").astype(str)
        df["action"] = df["action"].fillna("Add").astype(str)

        return df

    except (pd.errors.EmptyDataError, OSError, ValueError):
        return pd.DataFrame(columns=COLUMNS)


def save_history(df):
    """Save records to the same CSV file."""
    df.to_csv(HISTORY_FILE, index=False)


def record_event(amount, action):
    """Add a signed water event to the session history and CSV."""
    now = datetime.now()

    new_row = {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%I:%M %p"),
        "day": now.strftime("%A"),
        "month": now.strftime("%B"),
        "year": now.strftime("%Y"),
        "amount_ml": int(amount),
        "action": action,
    }

    updated_history = pd.concat(
        [
            st.session_state.history,
            pd.DataFrame([new_row]),
        ],
        ignore_index=True,
    )

    st.session_state.history = updated_history
    save_history(updated_history)


def today_total_for(df, day_string):
    """Return net water intake for a particular date."""
    if df.empty:
        return 0

    day_rows = df.loc[df["date"] == day_string, "amount_ml"]
    return int(day_rows.sum())


def get_week_data():
    """Return intake for today and the previous six days."""
    today = date.today()
    rows = []

    for offset in range(6, -1, -1):
        current_day = today - timedelta(days=offset)
        rows.append(
            {
                "Day": current_day.strftime("%a"),
                "Date": current_day.isoformat(),
                "Water (ml)": max(
                    0,
                    today_total_for(
                        st.session_state.history,
                        current_day.isoformat(),
                    ),
                ),
            }
        )

    return pd.DataFrame(rows)


def calculate_streak():
    """Count consecutive days reaching the daily goal."""
    today = date.today()

    today_total = today_total_for(
        st.session_state.history,
        today.isoformat(),
    )

    # If today's goal is not complete, begin checking from yesterday.
    cursor = (
        today
        if today_total >= DAILY_GOAL_ML
        else today - timedelta(days=1)
    )

    streak = 0

    while (
        today_total_for(
            st.session_state.history,
            cursor.isoformat(),
        )
        >= DAILY_GOAL_ML
    ):
        streak += 1
        cursor -= timedelta(days=1)

    return streak


def calculate_lifetime_net_intake(df):
    """Calculate net recorded intake, including water removals."""
    if df.empty:
        return 0

    return max(0, int(df["amount_ml"].sum()))


# =========================================================
# INITIALIZE SESSION STATE
# =========================================================
if "history" not in st.session_state:
    st.session_state.history = load_history()


# =========================================================
# HEADER
# =========================================================
st.markdown(
    f"""
    <div class="brand-header">
        <div class="brand-logo">AT</div>
        <div>
            <div class="brand-name">AquaTrack <span>💧</span></div>
            <div class="brand-tagline">
                YOUR DAILY HYDRATION COMPANION
            </div>
        </div>
    </div>

    <div class="hero">
        <p>{datetime.now().strftime("%A, %d %B %Y")}</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# CURRENT TOTALS
# =========================================================
today_string = date.today().isoformat()

today_total = max(
    0,
    today_total_for(st.session_state.history, today_string),
)
remaining = max(0, DAILY_GOAL_ML - today_total)
percent = min(100, int(today_total / DAILY_GOAL_ML * 100))
streak = calculate_streak()

if percent >= 100:
    encouragement = "Amazing! Daily goal completed! 🏆"
    encouragement_color = GREEN
elif percent >= 50:
    encouragement = "Great progress! Keep it up! 💧"
    encouragement_color = LIGHT_BLUE
else:
    encouragement = "Every sip counts. Keep going! 💙"
    encouragement_color = MUTED


# =========================================================
# NAVIGATION TABS
# =========================================================
dashboard_tab, weekly_tab, badges_tab, history_tab = st.tabs(
    [
        "🏠 Dashboard",
        "📊 Weekly Progress",
        "🏆 Achievements",
        "🧾 History",
    ]
)


# =========================================================
# DASHBOARD
# =========================================================
with dashboard_tab:
    top_left, top_right = st.columns([1.2, 1], gap="large")

    # -------------------- LEFT COLUMN --------------------
    with top_left:
        with st.container(border=True):
            st.markdown(
                f"""
                <div class="metric-label">Total Water Today</div>
                <div class="metric-value">{today_total:,} ml</div>
                <div class="metric-label">Remaining to daily goal</div>
                <div class="metric-value">{remaining:,} ml</div>
                <p style="color:{encouragement_color};
                          font-weight:800; margin:0.6rem 0 0">
                    {encouragement}
                </p>
                <p style="color:{ORANGE};
                          font-weight:800; margin:0.4rem 0 0">
                    🔥 Current Streak: {streak}
                    day{"s" if streak != 1 else ""}
                </p>
                """,
                unsafe_allow_html=True,
            )

        # WATER CONTROLS
        with st.container(border=True):
            st.subheader("Water Controls")

            selected_size = st.selectbox(
                "Select water size",
                WATER_SIZES,
                index=1,
                format_func=lambda value: f"{value} ml",
                key="water_size",
            )

            add_col, remove_col = st.columns(2)

            with add_col:
                if st.button(
                    "➕ Add Water",
                    type="primary",
                    use_container_width=True,
                ):
                    record_event(selected_size, "Add")
                    st.rerun()

            with remove_col:
                if st.button(
                    "➖ Remove Water",
                    use_container_width=True,
                ):
                    if today_total <= 0:
                        st.warning(
                            "There is no water recorded to remove."
                        )
                    else:
                        actual_amount = min(selected_size, today_total)
                        record_event(-actual_amount, "Remove")
                        st.rerun()

            confirm_reset = st.checkbox(
                "I understand this will clear today's water entries.",
                key="confirm_reset",
            )

            if st.button(
                "↻ Reset Today",
                use_container_width=True,
            ):
                if confirm_reset:
                    history_df = st.session_state.history
                    st.session_state.history = history_df[
                        history_df["date"] != today_string
                    ].copy()

                    save_history(st.session_state.history)
                    st.rerun()
                else:
                    st.warning(
                        "Please tick the confirmation box before resetting."
                    )

        # WATER REMINDER
        with st.container(border=True):
            st.subheader("💡 Water Reminder")

            reminder_on = st.toggle(
                "Enable reminder preference",
                key="reminder_on",
            )

            if reminder_on:
                st.info(
                    f"Reminder preference is ON. "
                    f"Take a water break every {REMINDER_MINUTES} minutes."
                )
                st.caption(
                    "Streamlit does not send timed browser notifications "
                    "from this app. Use a device alarm for an actual reminder."
                )
            else:
                st.caption(
                    "Turn this on to display your reminder preference."
                )

    # -------------------- RIGHT COLUMN --------------------
    with top_right:
        with st.container(border=True):
            st.subheader("Daily Goal Progress")

            st.markdown(
                f"""
                <div class="progress-ring"
                     style="--progress:{percent * 3.6}deg">
                    <div class="progress-inner">
                        <div class="progress-percent">{percent}%</div>
                        <div class="progress-amount">
                            {today_total:,} / {DAILY_GOAL_ML:,} ml
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if percent < 30:
                progress_color = (
                    "linear-gradient(90deg,#38BDF8,#7DD3FC)"
                )
            elif percent < 70:
                progress_color = (
                    "linear-gradient(90deg,#1D4ED8,#38BDF8)"
                )
            else:
                progress_color = (
                    "linear-gradient(90deg,#1D4ED8,#38BDF8,#2DD4BF)"
                )

            st.markdown(
                f"""
                <div class="custom-progress-track">
                    <div class="custom-progress-fill"
                         style="width:{percent}%;
                                background:{progress_color};">
                    </div>
                </div>
                <div style="display:flex;
                            justify-content:space-between;
                            font-size:0.78rem;
                            color:#B8D3E8">
                    <span>{percent}% completed</span>
                    <span>100%</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.caption(f"Daily target: {DAILY_GOAL_ML:,} ml")

        # LIVE WATER GLASS
        water_height = min(
            100,
            int(today_total / DAILY_GOAL_ML * 100),
        )

        with st.container(border=True):
            st.subheader("Live Water Glass")

            st.markdown(
                f"""
                <div class="glass-wrap">
                    <div class="glass">
                        <div class="water"
                             style="height:{water_height}%">
                        </div>
                        <div class="glass-shine"></div>
                    </div>
                </div>
                <div style="font-weight:800;
                            color:{LIGHT_BLUE};
                            text-align:center">
                    {water_height}% full
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.caption(
                "The glass fills as your daily progress increases."
            )


# =========================================================
# WEEKLY PROGRESS
# =========================================================
with weekly_tab:
    st.subheader("Your Last 7 Days")
    st.caption("Daily water intake in millilitres.")

    week_df = get_week_data()
    chart_df = week_df.set_index("Day")[["Water (ml)"]]

    st.bar_chart(
        chart_df,
        y="Water (ml)",
        use_container_width=True,
    )

    st.dataframe(
        week_df[["Date", "Day", "Water (ml)"]],
        use_container_width=True,
        hide_index=True,
    )

    weekly_average = int(week_df["Water (ml)"].mean())

    metric_col1, metric_col2 = st.columns(2)
    with metric_col1:
        st.metric("7-day average", f"{weekly_average:,} ml")
    with metric_col2:
        completed_days = int(
            (week_df["Water (ml)"] >= DAILY_GOAL_ML).sum()
        )
        st.metric("Goals completed", f"{completed_days} / 7")

    st.success(f"Daily target: {DAILY_GOAL_ML:,} ml")


# =========================================================
# ACHIEVEMENTS
# =========================================================
with badges_tab:
    st.subheader("Your Achievements")

    history_df = st.session_state.history
    lifetime_total = calculate_lifetime_net_intake(history_df)

    badge_definitions = [
        (
            "💧 First Sip",
            "Log your first net water intake",
            lifetime_total > 0,
        ),
        (
            "🎯 Goal Getter",
            "Complete your daily water goal",
            today_total >= DAILY_GOAL_ML,
        ),
        (
            "🔥 3-Day Streak",
            "Complete your goal 3 days in a row",
            streak >= 3,
        ),
        (
            "🏆 7-Day Champion",
            "Complete your goal 7 days in a row",
            streak >= 7,
        ),
        (
            "🌊 Hydration Star",
            "Reach 10,000 ml of net recorded intake",
            lifetime_total >= 10000,
        ),
    ]

    earned = sum(
        1
        for _, _, unlocked in badge_definitions
        if unlocked
    )

    st.markdown(
        f"**{earned}/{len(badge_definitions)} badges unlocked**"
    )

    for title, description, unlocked in badge_definitions:
        status = "UNLOCKED ✓" if unlocked else "LOCKED"
        status_color = GREEN if unlocked else MUTED

        st.markdown(
            f"""
            <div class="badge">
                <div class="badge-title">
                    {html.escape(title)}
                </div>
                <div class="badge-desc">
                    {html.escape(description)}
                </div>
                <div class="badge-status"
                     style="color:{status_color};text-align:right">
                    {status}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# WATER HISTORY
# =========================================================
with history_tab:
    st.subheader("Water Intake History")

    history_df = st.session_state.history.copy()

    if history_df.empty:
        st.info(
            "No water history yet. Add your first glass from the Dashboard."
        )
    else:
        today_history = history_df[
            history_df["date"] == today_string
        ].copy()

        today_history = today_history.iloc[::-1]

        st.markdown("### Today's Entries")

        if today_history.empty:
            st.info("No water entries recorded today.")
        else:
            display_df = today_history[
                ["date", "time", "action", "amount_ml"]
            ].copy()

            display_df["amount_ml"] = display_df["amount_ml"].map(
                lambda amount: (
                    f"{amount:+,} ml"
                    if amount < 0
                    else f"+{amount:,} ml"
                )
            )

            display_df.columns = [
                "Date",
                "Time",
                "Action",
                "Amount",
            ]

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
            )

        st.markdown("---")
        st.caption("Most recent 200 records")

        all_display = history_df.iloc[::-1].head(200)[
            ["date", "time", "day", "amount_ml", "action"]
        ].copy()

        all_display["amount_ml"] = all_display["amount_ml"].map(
            lambda amount: f"{amount:+,} ml"
        )

        all_display.columns = [
            "Date",
            "Time",
            "Day",
            "Amount",
            "Action",
        ]

        st.dataframe(
            all_display,
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# FOOTER
# =========================================================
st.markdown(
    f"""
    <div style="
        text-align:center;
        color:{MUTED};
        font-size:0.8rem;
        padding-top:1rem">
        AquaTrack • Small sips, big progress 💧
    </div>
    """,
    unsafe_allow_html=True,
)
