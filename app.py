import streamlit as st
import HomePage
import SocialMedia

# Configure the page
st.set_page_config(page_title="Social Media Video Finder", layout="wide")

# Load the CSS styles
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load CSS
load_css('style.css')

# Navigation options
pages = {
    "Home": HomePage,
    "Social Media": SocialMedia,
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Load the selected page
page = pages[selection]
page.show()

