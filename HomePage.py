import streamlit as st

def show():
    st.title("Welcome to the Social Media Video Finder App")
    
    st.write("""
        This app allows users to search and display public social media videos by entering their username.
        You can search across multiple platforms if the same username is used.
        
        ### Features:
        - Enter your social media username (e.g., YouTube, Instagram, TikTok)
        - Multi-select platforms for cross-platform search
        - View public videos directly in the app
    """)

    # Optional Image or Icon
    st.image("assets/images/social_media_banner.png", use_column_width=True)
