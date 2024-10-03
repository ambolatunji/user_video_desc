from pytube import YouTube, Playlist
import youtube
import os

# Directory where videos will be downloaded
DOWNLOAD_DIRECTORY = "downloads/"

# Ensure the download directory exists
if not os.path.exists(DOWNLOAD_DIRECTORY):
    os.makedirs(DOWNLOAD_DIRECTORY)

def download_video(video_url):
    try:
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        stream.download(DOWNLOAD_DIRECTORY)
        output_path = stream.download(DOWNLOAD_DIRECTORY)
        return f"{yt.title} has been downloaded successfully! Saved at {output_path}"
    except Exception as e:
        return f"An error occurred while downloading the video: {str(e)}"

def download_playlist(playlist_url):
    try:
        playlist = Playlist(playlist_url)
        for video in playlist.videos:
            video.streams.get_highest_resolution().download(DOWNLOAD_DIRECTORY)
        return f"Playlist '{playlist.title}' has been downloaded successfully!"
    except Exception as e:
        return f"An error occurred while downloading the playlist: {str(e)}"
    
# Placeholder for Vimeo and Dailymotion download functions
def download_vimeo_video(video_url):
    return "Vimeo download functionality will be implemented soon."

def download_dailymotion_video(video_url):
    return "Dailymotion download functionality will be implemented soon."
