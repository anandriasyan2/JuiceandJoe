import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# ---------- Quiz Data ----------
quiz_data = [
    {
        "question": "What was our total sales yesterday?",
        "options": ["$1,500", "$2,350", "$3,250", "$2,800"],
        "answer": 2,
        "image": "images/sales_dashboard.png"
    },
    {
        "question": "Which drink was our top seller yesterday?",
        "options": ["Green Mile", "Iron Man", "Power Shake", "Pick Me Up"],
        "answer": 2,
        "image": "images/top_seller.png"
    },
    {
        "question": "What is our current waste percentage?",
        "options": ["2%", "4%", "6%", "3.7%"],
        "answer": 3,
        "image": "images/waste_dashboard.png"
    },
    {
        "question": "Which hour of the day had the lowest number of customers yesterday?",
        "options": ["8–9 AM", "12–1 PM", "3–4 PM", "6–7 PM"],
        "answer": 2,
        "image": "images/customer_flow.png"
    },
    {
        "question": "What’s our current average ticket size?",
        "options": ["$10.25", "$11.10", "$12.70", "$13.20"],
        "answer": 2,
        "image": "images/avg_ticket.png"
    },
    {
        "question": "Which item had the highest waste yesterday?",
        "options": ["Bananas", "Spinach", "Almond Milk", "Chicken"],
        "answer": 0,
        "image": "images/item_waste.png"
    },
    {
        "question": "Which store region had the highest sales last week?",
        "options": ["UK", "Denmark", "France", "Portugal"],
        "answer": 1,
        "image": "images/region_sales.png"
    },
    {
        "question": "What’s our current upsell success rate?",
        "options": ["12%", "18%", "22%", "28%"],
        "answer": 2,
        "image": "images/upsell_rate.png"
    },
    {
        "question": "Which smoothie had the **least** sales yesterday?",
        "options": ["Pick Me Up", "Iron Man", "Green Mile", "Go Away Doc"],
        "answer": 3,
        "image": "images/low_sellers.png"
    },
    {
        "question": "Which day this week had the highest sales so far?",
        "options": ["Monday", "Wednesday", "Thursday", "Friday"],
        "answer": 3,
        "image": "images/daily_sales.png"
    }
]

# ---------- Session State ----------
if "team_name" not in st.session_state:
    st.session_state.team_name = ""
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "quiz_complete" not in st.session_state:
    st.session_state.quiz_complete = False
if "show_intro" not in st.session_state:
    st.session_state.show_intro = True
if "quiz_start_time" not in st.session_state:
    st.session_state.quiz_start_time = None
if "just_answered" not in st.session_state:
    st.session_state.just_answered = False

# ---------- Leaderboard Setup ----------
LEADERBOARD_FILE = "leaderboard.csv"
if not os.path.exists(LEADERBOARD_FILE):
    pd.DataFrame(columns=["Team", "Score"]).to_csv(LEADERBOARD_FILE, index=False)

# ---------- Custom CSS ----------
st.markdown("""
    <style>
        h1, h2, h3 {
            color: #ffb6c1;
            font-weight: 700;
            font-family: "Helvetica Neue", sans-serif;
        }
        .stRadio > div {
            background-color: #fff0f5;
            border-radius: 10px;
            padding: 10px;
        }
        button {
            background-color: #ffb6c1 !important;
            color: black !important;
            border-radius: 12px;
            font-weight: bold;
        }
        .stAlert {
            background-color: #fff0f5;
            border: 2px solid #ffb6c1;
        }
        .stDataFrame {
            border: 2px solid #ffb6c1;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Intro Page ----------
if st.session_state.show_intro:
    if os.path.exists("images/joe_header.png"):
        st.image("images/joe_header.png", use_container_width=True)

    st.title("🧃 Weekly Trivia: Dash & Discover!")
    st.markdown("""
    ### Welcome, Joe & The Juice Team!  
    Every week, we test your **store knowledge, data intuition**, and your ability to **use BI dashboards**!

    🧠 This isn’t just a quiz — it’s part of our **knowledge management mission**.  
    📊 You’ll need to **check dashboards**, **discuss with your team**, and **make smart decisions**.

    ---
    ⏱ **You’ll have 5 minutes to complete the quiz. Work as a team, act fast, and have fun!**
    """, unsafe_allow_html=True)

    st.subheader("Enter your team name to begin:")
    team_input = st.text_input("Team Name")

    if st.button("🍹 Start Quiz"):
        if team_input.strip():
            st.session_state.team_name = team_input.strip()
            st.session_state.show_intro = False
            st.session_state.quiz_start_time = datetime.now()
            st.rerun()
        else:
            st.warning("Please enter your team name to begin.")

# ---------- Timer + Quiz ----------
if (
    not st.session_state.show_intro and
    not st.session_state.quiz_complete and
    st.session_state.team_name
):
    if st.session_state.quiz_start_time:
        elapsed = datetime.now() - st.session_state.quiz_start_time
        remaining = timedelta(minutes=5) - elapsed
        minutes, seconds = divmod(remaining.seconds, 60)

        if remaining.total_seconds() > 0:
            st.info(f"⏳ Time Remaining: {minutes:02d}:{seconds:02d}")
        else:
            st.warning("⏱ Time's up! Submitting your quiz automatically...")
            st.session_state.quiz_complete = True
            st.rerun()

    # Quiz Question
    if not st.session_state.quiz_complete:
        q = quiz_data[st.session_state.current_q]
        st.subheader(f"Q{st.session_state.current_q + 1}: {q['question']}")

        if os.path.exists(q["image"]):
            st.image(q["image"], use_container_width=True)

        selected = st.radio("Choose your answer:", q["options"], key=f"q{st.session_state.current_q}")

        if not st.session_state.just_answered:
            if st.button("Submit Answer"):
                correct_index = q["answer"]
                is_correct = q["options"].index(selected) == correct_index

                if is_correct:
                    st.success("✅ Correct!")
                    st.session_state.score += 1
                else:
                    st.error("❌ Incorrect!")

                st.session_state.just_answered = True
                st.rerun()
        else:
            st.session_state.current_q += 1
            st.session_state.just_answered = False

            if st.session_state.current_q >= len(quiz_data):
                st.session_state.quiz_complete = True

            st.rerun()

# ---------- Results ----------
elif st.session_state.quiz_complete:
    st.balloons()
    st.success("🎉 Quiz Complete!")
    st.write(f"**Team `{st.session_state.team_name}` scored {st.session_state.score} out of {len(quiz_data)}**")

    df = pd.read_csv(LEADERBOARD_FILE)
    new_row = pd.DataFrame([{
        "Team": st.session_state.team_name,
        "Score": st.session_state.score
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(LEADERBOARD_FILE, index=False)

    st.markdown("---")
    st.subheader("🏆 Leaderboard")
    leaderboard_df = pd.read_csv(LEADERBOARD_FILE).sort_values(by="Score", ascending=False).head(10)
    st.dataframe(leaderboard_df.reset_index(drop=True))

    if st.button("🔁 Play Again"):
        for key in ["team_name", "score", "current_q", "quiz_complete", "show_intro", "quiz_start_time", "just_answered"]:
            st.session_state[key] = "" if key == "team_name" else False if "show" in key or "complete" in key or "just" in key else 0
        st.session_state["show_intro"] = True
        st.rerun()
