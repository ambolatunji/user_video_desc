import streamlit as st

def show():
    st.title("Find Your Social Media Videos")
    
    # Use some HTML to create a nice heading
    st.markdown("""
        <div class="custom-title">
            <h2>Enter Your Social Media Username</h2>
        </div>
    """, unsafe_allow_html=True)

    # Input for social media username
    username = st.text_input("Username (same on all selected platforms):")
    
    if username:
        # Multi-select for social media platforms
        platforms = st.multiselect(
            "Select Social Media Platforms:",
            ["Instagram", "YouTube", "TikTok", "Twitter/X"],
            help="Select the platforms where this username exists"
        )

        # Show a message or results when platforms are selected
        if platforms:
            st.success(f"Fetching videos for username: **{username}** on platforms: {', '.join(platforms)}")
        else:
            st.warning("Please select at least one platform.")
    else:
        st.warning("Please enter a username.")
    
    # Optional: Add more HTML sections or CSS-styled UI components
    st.markdown("""
        <div class="footer">
            <p>Stay tuned for more social media integrations! 🚀</p>
        </div>
    """, unsafe_allow_html=True)
