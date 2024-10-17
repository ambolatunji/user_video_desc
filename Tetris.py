import streamlit.components.v1 as components

def run():
    tetris_game_html = """
    <iframe src="https://tetris.com/play-tetris" width="100%" height="400" frameborder="0"></iframe>
    """
    components.html(tetris_game_html, height=400)
