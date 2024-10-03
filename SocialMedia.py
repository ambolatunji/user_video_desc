import streamlit as st
import youtube
from vimeo import show as vimeo_show
from dailymotion import show as dailymotion_show
from youtube import get_videos_from_playlist
from youtube import show as youtube_show
from youtube import download_video, download_playlist
from datetime import datetime, timedelta

def show():
    st.title("Find Your Social Media Videos")

    st.markdown("""
        <div class="custom-title">
            <h2>Enter Your Social Media Username or Keyword</h2>
        </div>
    """, unsafe_allow_html=True)

    # Input for social media username
    username = st.text_input("Username (same on all platforms, if available):")
    
    # Input for keyword search
    keyword = st.text_input("Keyword Search:")

    # Multi-select for social media platforms
    platforms = st.multiselect(
        "Select Social Media Platforms:",
        ["Instagram", "YouTube", "TikTok", "Twitter/X", "Vimeo", "Dailymotion"],
        default=["YouTube", "Vimeo", "DailyMontio"] if username else [],
        help="Select the platforms where this username exists"
    )

    # Logic: If the username is the same across all platforms, automatically select all platforms
    if username or keyword:
        st.success(f"Searching for username **{username}** or keyword **{keyword}** across selected platforms: {', '.join(platforms)}")

        max_results = st.slider("Max Results per Platform", min_value=1, max_value=50, value=10, step=1)

        # Display YouTube results if YouTube is selected
        if "YouTube" in platforms:
            # A progress bar to simulate loading process
            st.write("## Fetching YouTube data, please wait...")
            progress = st.progress(0)
            for i in range(100):
                progress.progress(i + 1)
            youtube.show(username=username, keyword=keyword, max_results=max_results)

        if "Vimeo" in platforms:
            st.write("## Fetching Vimeo data, please wait...")
            vimeo_show(keyword=keyword, max_results=max_results)
        
        if "Dailymotion" in platforms:
            st.write("## Fetching DailyMotion data, please wait...")
            dailymotion_show(keyword=keyword, max_results=max_results)
    
        # Add placeholders for other platforms
        if "Instagram" in platforms:
            st.write("Instagram integration is coming soon!")
        if "TikTok" in platforms:
            st.write("TikTok integration is coming soon!")
        if "Twitter/X" in platforms:
            st.write("Twitter/X integration is coming soon!")
    else:
        st.warning("Please enter a username or a keyword.")

    st.balloons()

    # Add other widgets as needed
    st.markdown("""
        <div class="footer">
            <p>Stay tuned for more social media integrations! 🚀</p>
        </div>
    """, unsafe_allow_html=True)
