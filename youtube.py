import os
import streamlit as st
import requests
from dotenv import load_dotenv
from download import download_video, download_playlist
from datetime import datetime, timedelta

# Load API Key from environment variables
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Base YouTube API URLs
BASE_URL = "https://www.googleapis.com/youtube/v3"

# Function to fetch user channel details
def get_channel_id_from_username(username):
    url = f"{BASE_URL}/channels?forUsername={username}&part=id&key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Check if a valid channel is found
    if "items" in data and len(data["items"]) > 0:
        return data["items"][0]["id"]  # Return the first channel ID found
    else:
        return None  # Return None if no channel was found'''

def get_channel_details_by_id(channel_id):
    url = f"{BASE_URL}/channels?part=snippet,contentDetails,statistics&id={channel_id}&key={API_KEY}"
    response = requests.get(url)
    return response.json()

# Enhanced function to handle both username and channel ID
def get_channel_details(username_or_channel):
    # First, check if it's a channel ID (assuming it's a valid channel ID)
    channel_data = get_channel_details_by_id(username_or_channel)

    # If no results with ID, treat it as a username and convert to channel ID
    if not channel_data or "items" not in channel_data or len(channel_data["items"]) == 0:
        channel_id = get_channel_id_from_username(username_or_channel)
        if channel_id:
            channel_data = get_channel_details_by_id(channel_id)
        else:
            st.error("No channel found for this username.")
            return None
    return channel_data

# Function to fetch user's videos from their uploads playlist with embeddable filter
def get_videos_from_playlist(playlist_id, max_results=10):
    url = f"{BASE_URL}/playlistItems?playlistId={playlist_id}&part=snippet,contentDetails&maxResults=10&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        videos = response.json()

        # Filter out non-embeddable videos
        filtered_videos = []
        for video in videos["items"]:
            video_id = video["snippet"]["resourceId"]["videoId"]
            # Fetch video details to check embeddability
            video_details_url = f"{BASE_URL}/videos?part=contentDetails&id={video_id}&key={API_KEY}"
            video_details_response = requests.get(video_details_url)
            video_details = video_details_response.json()

            if video_details and "items" in video_details and video_details["items"]:
                if video_details["items"][0]["contentDetails"].get("embeddable", True):
                    filtered_videos.append(video)

        return filtered_videos
    else:
        st.error(f"Failed to retrieve videos from playlist. Status code: {response.status_code}")
        return None

# Function to search for videos based on a keyword with embeddable filter
def search_videos_by_keyword(keyword, video_type=None, order=None, published_after=None, published_before=None, max_results=10):
    if max_results > 100:
        max_results = 100  # Limit the results to 100 as per API max limits
    url = f"{BASE_URL}/search?part=snippet&contentDetails&q={keyword}&type=video&maxResults={max_results}&key={API_KEY}"
    # Add filters to the API call
    if video_type:
        url += f"&videoType={video_type}"
    if order:
        url += f"&order={order}"
    if published_after:
        url += f"&publishedAfter={published_after}"
    if published_before:
        url += f"&publishedBefore={published_before}"

    #Make the Request
    response = requests.get(url)
    if response.status_code == 200:
        search_results = response.json()

        # Filter out non-embeddable videos
        filtered_videos = []
        for video in search_results["items"]:
            if "id" in video and "videoId" in video["id"]:
                video_id = video["id"]["videoId"]
                video_details_url = f"{BASE_URL}/videos?part=contentDetails&id={video_id}&key={API_KEY}"
                video_details_response = requests.get(video_details_url)
                video_details = video_details_response.json()

            if video_details and "items" in video_details and video_details["items"]:
                if video_details["items"][0]["contentDetails"].get("embeddable", True):
                    filtered_videos.append(video)

        return filtered_videos
    else:
        st.error(f"Failed to retrieve videos by keyword. Status code: {response.status_code}")
        return None

# Display YouTube videos and playlists (Modular version)

def show_videos(videos):
    if videos and len(videos) > 0:
        cols = st.columns(3)
        for index, video in enumerate(videos):
            if "id" in video and "videoId" in video["id"]:
                video_id = video["id"]["videoId"]
            elif "snippet" in video and "resourceId" in video["snippet"]:
                video_id = video["snippet"]["resourceId"]["videoId"]
            else:
                continue

            video_title = video["snippet"]["title"]
            with cols[index % 3]:
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                st.video(video_url)
                if st.button(f"Download {video_title}", key=f"download_{video_id}"):
                    download_message = download_video(video_url)
                    st.success(download_message)
    else:
        st.warning("No videos found.")

def show(username=None, keyword=None, max_results=10):
    if username:
        channel_data = get_channel_details(username)
        if channel_data and "items" in channel_data and len(channel_data["items"]) > 0:
            channel_info = channel_data["items"][0]
            st.write(f"Channel Title: {channel_info['snippet']['title']}")
            st.write(f"Subscribers: {channel_info['statistics']['subscriberCount']}")
            st.write(f"Total Views: {channel_info['statistics']['viewCount']}")

            uploads_playlist_id = channel_info['contentDetails']['relatedPlaylists']['uploads']
            video_data = get_videos_from_playlist(uploads_playlist_id, max_results)

            if video_data:
                st.markdown("""
                            <div class="custom-title">
                             <h2>Youtube Latest Videos:</h2>
                            </div>
                            """, 
                            unsafe_allow_html=True)
                show_videos(video_data)

            else:
                st.warning("No videos found for this channel.")

    # Video type filter
    video_type = st.selectbox(
        "Filter by Video Type", 
        options=["Any", "Video", "Playlist", "Live Broadcast", "Movie", "Episode"],
        index=0  # Default to "Any"
    )

    # Sort order filter
    sort_order = st.selectbox(
        "Sort By", 
        options=["Relevance", "Date", "View Count", "Rating"],
        index=0  # Default to "Relevance"
    )

    # Date range filter
    date_filter = st.radio(
        "Filter by Date",
        options=["Any time", "Today", "This week", "This month"]
    )

    # Set the date range based on user selection
    published_after = None
    published_before = None
    if date_filter == "Today":
        published_after = (datetime.utcnow() - timedelta(days=1)).isoformat("T") + "Z"
    elif date_filter == "This week":
        published_after = (datetime.utcnow() - timedelta(weeks=1)).isoformat("T") + "Z"
    elif date_filter == "This month":
        published_after = (datetime.utcnow() - timedelta(days=30)).isoformat("T") + "Z"

    # Map sort order and video type options to YouTube API parameters
    order_map = {
        "Relevance": "relevance",
        "Date": "date",
        "View Count": "viewCount",
        "Rating":"rating"
    }

    video_type_map = {
        "Any": None,
        "Video": "video",
        "Playlist": "playlist",
        "Live Broadcast": "live",
        "Movie": "movie",
        "Episode": "episode"
    }
    
    if keyword:
        st.write(f"Searching for videos with keyword: **{keyword}**")
        #video_data = search_videos_by_keyword(keyword, max_results)

        keyword_video_data = search_videos_by_keyword(
            keyword=keyword,
            video_type=video_type_map[video_type],
            order=order_map[sort_order],
            published_after=published_after,
            max_results=max_results
        )

        if keyword_video_data:
            st.markdown("""
                            <div class="custom-title">
                             <h2>Youtube Keyword Search Results:</h2>
                            </div>
                            """, 
                            unsafe_allow_html=True)
            show_videos(keyword_video_data)

    else:
        st.warning("No results found for the keyword search.")


# Enhanced error handling for API requests
def safe_api_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for 4XX/5XX responses
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        st.error(f"Other error occurred: {err}")
    return None

