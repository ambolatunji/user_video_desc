import streamlit as st
import Snake
import Tetris
from TicTacToe import TicTacToe
from tictactoe_agent import play_TicTacToe
import time
import random

def show():
    st.title("Welcome to the Game Section")

    st.markdown("""
        Choose a game from the dropdown below and enjoy playing!
    """)

    # Game options
    game_choice = st.selectbox("Select a game to play", ["Snake", "Tetris", "Tic-Tac-Toe"])

    if game_choice == "Snake":
        Snake.main()
    elif game_choice == "Tetris":
        Tetris.run()
    elif game_choice == "Tic-Tac-Toe":
        play_TicTacToe()

    st.markdown("""
        Have fun and stay tuned for more games! 🎮
    """)


if __name__ == "__main__":
    show()