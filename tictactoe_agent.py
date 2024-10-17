import streamlit as st
import numpy as np
from TicTacToe import TicTacToe
import random

def play_TicTacToe():
    if 'game' not in st.session_state:
        st.session_state.game = TicTacToe()
        st.session_state.mode = "Human vs Human"
        st.session_state.difficulty = "medium"
        st.session_state.moves = 0
        st.session_state.winning_line = None
        st.session_state.game_history = []
        st.session_state.fun_facts = [
            "Did you know? The game Tic-Tac-Toe is also known as Noughts and Crosses in the UK!",
            "Fun fact: There are 255,168 possible ways to play a game of Tic-Tac-Toe!",
            "Trivia: The first known reference to Tic-Tac-Toe was in 1300 BC Egypt!",
            "Interesting: A perfect Tic-Tac-Toe player will never lose!",
            "Wow: Tic-Tac-Toe was one of the first games played by early computer programs!"
        ]

    # Game mode selection
    new_mode = st.radio("Choose game mode:", ("Human vs Human", "Human vs AI"))
    if new_mode != st.session_state.mode:
        st.session_state.mode = new_mode
        st.session_state.game.reset_game()
        st.session_state.moves = 0
        st.session_state.winning_line = None

    if st.session_state.mode == "Human vs AI":
        new_difficulty = st.selectbox("Choose AI difficulty:", ("normal", "superhard"))
        if new_difficulty != st.session_state.difficulty:
            st.session_state.difficulty = new_difficulty
            st.session_state.game.set_difficulty(new_difficulty)

    # Reset and Restart buttons
    col1, col2 = st.columns(2)
    if col1.button("Reset Game"):
        st.session_state.game.reset_game()
        st.session_state.moves = 0
        st.session_state.winning_line = None
        st.session_state.game_history = []
    if col2.button("Restart Game"):
        st.session_state.game.reset_game()
        st.session_state.moves = 0
        st.session_state.winning_line = None

    # Display current player's turn with color
    player_color = "blue" if st.session_state.game.current_player == 'X' else "red"
    st.markdown(f"<h3 style='color: {player_color};'>Current turn: Player {st.session_state.game.current_player}</h3>", unsafe_allow_html=True)

    # Game board display and interaction
    move_made = False
    cols = st.columns(3)  # Create 3 columns for each row of the grid
    for i in range(3):
        for j in range(3):
            index = i * 3 + j
            cell_value = st.session_state.game.board[index]
            with cols[j]:
                if st.button(f"{cell_value if cell_value != ' ' else '-'}", key=f"cell_{index}", 
                             help=f"Click to place your mark in cell {index + 1}",
                             disabled=st.session_state.winning_line is not None):
                    if st.session_state.game.make_move(index):
                        st.session_state.moves += 1
                        move_made = True

    if move_made:
        winner, line = st.session_state.game.check_winner()
        if winner:
            st.session_state.winning_line = line
            st.write(f"Player {winner} wins! 🎉")
            st.session_state.game_history.append(f"Player {winner} won")
        elif st.session_state.moves == 9:
            st.write("It's a tie! 🤝")
            st.session_state.game_history.append("Tie game")
        else:
            st.session_state.game.switch_player()


     #AI move (if applicable)
    if st.session_state.mode == "Human vs AI" and st.session_state.game.current_player == st.session_state.game.ai_player and not winner:
        ai_move = st.session_state.game.ai_move()
        if ai_move is not None and st.session_state.game.make_move(ai_move):
            st.session_state.moves += 1
            winner, line = st.session_state.game.check_winner()
            if winner:
                st.session_state.winning_line = line
                st.write(f"Player {winner} wins! 🎉")
                st.session_state.game_history.append(f"Player {winner} won")
            elif st.session_state.moves == 9:
                st.write("It's a tie! 🤝")
                st.session_state.game_history.append("Tie game")
            else:
                st.session_state.game.switch_player()
        else:
            st.write("AI couldn't make a move. Game over!")

    # Rerun to update the board
    #if move_made or st.session_state.game.current_player == st.session_state.game.ai_player:
     #   st.experimental_rerun()

    # Display game history
    st.sidebar.markdown("### Game History")
    for i, result in enumerate(st.session_state.game_history, 1):
        st.sidebar.write(f"Game {i}: {result}")

    # Display fun facts and move counter
    st.sidebar.markdown(f"**Moves played**: {st.session_state.moves}")
    if st.session_state.moves % 3 == 0 and st.session_state.moves > 0:
        st.sidebar.info(random.choice(st.session_state.fun_facts))

    # Add a fun message based on the number of moves
    if st.session_state.moves == 3:
        st.sidebar.success("Halfway there! Who will win? 🤔")
    elif st.session_state.moves == 6:
        st.sidebar.warning("One move left! The suspense is killing me! 😱")