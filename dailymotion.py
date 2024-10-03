import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load API Key from environment variables
load_dotenv()
DAILY_MOTION_API_KEY = os.getenv("DAILY_MOTION_API_KEY")

# Base Dailymotion API URL
BASE_URL = "https://api.dailymotion.com"

def safe_api_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        st.error(f"Other error occurred: {err}")
    return None

def search_videos_by_keyword(keyword, max_results=10):
    url = f"{BASE_URL}/videos?search={keyword}&limit={max_results}"
    return safe_api_request(url)

def show_videos(videos):
    if videos and 'list' in videos:
        cols = st.columns(3)
        for index, video in enumerate(videos['list']):
            video_url = f"https://www.dailymotion.com/embed/video/{video['id']}"
            video_title = video['title']
            with cols[index % 3]:
                st.write(f"**{video_title}**")
                st.components.v1.iframe(src=video_url, width=None, height=200, scrolling=True)
                if st.button(f"Download {video_title}", key=f"dailymotion_download_{video['id']}"):
                    st.warning("Dailymotion download functionality will be added soon.")
    else:
        st.warning("No videos found.")

def show(keyword=None, max_results=10):
    if keyword:
        st.write(f"Searching for Dailymotion videos with keyword: **{keyword}**")
        video_data = search_videos_by_keyword(keyword, max_results)
        if video_data:
            st.markdown("""
                            <div class="custom-title">
                             <h2>Dailymotion Search Results:"</h2>
                            </div>
                            """, 
                            unsafe_allow_html=True)
            show_videos(video_data)
        else:
            st.warning("No results found for the keyword search on Dailymotion.")
    else:
        st.warning("Please enter a keyword to search for Dailymotion videos.")

# Uncomment the following lines if you want to test this script independently
# if __name__ == "__main__":
#     st.title("Dailymotion Video Search")
#     keyword = st.text_input("Enter a keyword to search for Dailymotion videos:")
#     max_results = st.slider("Max Results", min_value=1, max_value=50, value=10, step=1)
#     if keyword:
#         show(keyword, max_results)