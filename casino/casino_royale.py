import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime


st.set_page_config(page_title="Casino Royale", layout="wide")


defaults = {
    "entered": False,
    "history": [],
    "scores": [],
    "rps_score": 0,
    "dice_score": 0,
    "card_score": 0,
    "coin_score": 0,
    "logs_cleared": False,
    "current_log": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


if not os.path.exists("logs"):
    os.mkdir("logs")

if not st.session_state.logs_cleared:
    for f in os.listdir("logs"):
        os.remove(os.path.join("logs", f))
    st.session_state.logs_cleared = True


if st.session_state.current_log is None:
    filename = f"logs/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    st.session_state.current_log = filename

def save_log():
    if not st.session_state.history:
        return

    formatted = ""
    for game, score in st.session_state.history:
        result = "Win" if score > 0 else "Loss" if score < 0 else "Draw"
        formatted += f"{game} - {result}\n"

    with open(st.session_state.current_log, "w", encoding="utf-8") as f:
        f.write(formatted)

# ---------------- SCORE PANEL ---------------- #
def score_panel(title, score):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"## {title}")
    with col2:
        st.metric("Score", score)
    st.divider()

# ---------------- ROCK PAPER SCISSORS ---------------- #
def play_rps():

    score_panel("Rock Paper Scissors", st.session_state.rps_score)

    col1, col2, col3 = st.columns(3)
    choice = None

    with col1:
        st.image("assets/rock.png", width=220)
        if st.button("Rock", key="rps1", use_container_width=True):
            choice = "Rock"

    with col2:
        st.image("assets/paper.png", width=168)
        if st.button("Paper", key="rps2", use_container_width=True):
            choice = "Paper"

    with col3:
        st.image("assets/scissor.png", width=150)
        if st.button("Scissors", key="rps3", use_container_width=True):
            choice = "Scissors"

    if choice:
        computer = random.choice(["Rock", "Paper", "Scissors"])

        st.divider()
        st.markdown(f"### Your Choice: {choice}")
        st.markdown(f"### Computer Choice: {computer}")
        st.divider()

        if choice == computer:
            score = 0
            st.info("Draw")
        elif (choice == "Rock" and computer == "Scissors") or \
             (choice == "Paper" and computer == "Rock") or \
             (choice == "Scissors" and computer == "Paper"):
            score = 1
            st.session_state.rps_score += 1
            st.success("You Win")
            st.balloons()
        else:
            score = -1
            st.error("You Lose")

        st.session_state.history.append(("RPS", score))
        st.session_state.scores.append(score)
        save_log()

# ---------------- DICE GAME ---------------- #
def play_dice():

    score_panel("Dice Game", st.session_state.dice_score)

    st.image("assets/dice.png", width=260)

    if st.button("Roll Dice", key="dice", use_container_width=True):
        user = random.randint(1, 6)
        computer = random.randint(1, 6)

        st.markdown(f"### You rolled: {user}")
        st.markdown(f"### Computer rolled: {computer}")
        st.divider()

        if user > computer:
            score = 1
            st.session_state.dice_score += 1
            st.success("You Win")
            st.balloons()
        elif user < computer:
            score = -1
            st.error("You Lose")
        else:
            score = 0
            st.info("Draw")

        st.session_state.history.append(("Dice", score))
        st.session_state.scores.append(score)
        save_log()

# ---------------- CARD GAME ---------------- #
def play_card():

    score_panel("Card Draw", st.session_state.card_score)

    st.image("assets/cards.jpg", width=280)

    if st.button("Draw Card", key="card", use_container_width=True):
        user = random.randint(1, 13)
        computer = random.randint(1, 13)

        st.markdown(f"### You drew: {user}")
        st.markdown(f"### Computer drew: {computer}")
        st.divider()

        if user > computer:
            score = 1
            st.session_state.card_score += 1
            st.success("You Win")
            st.balloons()
        elif user < computer:
            score = -1
            st.error("You Lose")
        else:
            score = 0
            st.info("Draw")

        st.session_state.history.append(("Card", score))
        st.session_state.scores.append(score)
        save_log()

# ---------------- COIN GAME ---------------- #
def play_coin():

    score_panel("Coin Flip", st.session_state.coin_score)

    st.image("assets/coin.png", width=240)
    guess = st.radio("Choose", ["Head", "Tail"], horizontal=True)

    if st.button("Flip Coin", key="coin", use_container_width=True):
        result = random.choice(["Head", "Tail"])

        st.markdown(f"### Result: {result}")
        st.divider()

        if guess == result:
            score = 1
            st.session_state.coin_score += 1
            st.success("Correct")
            st.balloons()
        else:
            score = -1
            st.error("Wrong")

        st.session_state.history.append(("Coin", score))
        st.session_state.scores.append(score)
        save_log()



# ---------------- ANALYTICS ---------------- #
def dashboard():

    st.markdown("## Game Analytics")

    if not st.session_state.scores:
        st.info("Play games first to see your statistics.")
        return

    scores = np.array(st.session_state.scores)

    wins = np.sum(scores > 0)
    losses = np.sum(scores < 0)
    draws = np.sum(scores == 0)

    fig, ax = plt.subplots()
    ax.pie([wins, losses, draws],
           labels=["Wins", "Losses", "Draws"],
           autopct="%1.1f%%",
           startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

# ---------------- LANDING PAGE ---------------- #
if not st.session_state.entered:

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("assets/arcade.jpg", width=520)
        st.markdown("# Casino Royale")
        st.markdown("### Interactive Game Collection")
        st.write("Play mini games and track your results.")
        st.divider()
        if st.button("Enter", use_container_width=True):
            st.session_state.entered = True
            st.rerun()



else:

    st.title("Casino Royale")

    left, right = st.columns([4, 1])

    with left:
        game = st.selectbox(
            "Select a Game",
            ["Select a game to begin",
             "Rock Paper Scissors",
             "Dice Game",
             "Card Draw",
             "Coin Flip"]
        )

        st.divider()

        if game == "Rock Paper Scissors":
            play_rps()
        elif game == "Dice Game":
            play_dice()
        elif game == "Card Draw":
            play_card()
        elif game == "Coin Flip":
            play_coin()
        else:
            st.info("Select a game to begin.")

    with right:

        st.subheader("Tools")

        if st.button("Analytics", use_container_width=True):
            dashboard()

        if st.button("View Current Log", use_container_width=True):
            if os.path.exists(st.session_state.current_log):
                with open(st.session_state.current_log, "r", encoding="utf-8") as f:
                    st.code(f.read())
            else:
                st.info("Play games first to generate log.")

        if st.button("Exit", use_container_width=True):
            st.session_state.entered = False
