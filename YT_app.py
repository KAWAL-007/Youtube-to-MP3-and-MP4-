import streamlit as st
import pytubefix as pytube
import subprocess
import os
import re
from io import BytesIO
import requests
import tarfile
import stat
import platform

FFMPEG_URL = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"

def download_ffmpeg():
    if not os.path.exists("ffmpeg_bin"):
        os.makedirs("ffmpeg_bin", exist_ok=True)
        r = requests.get(FFMPEG_URL, stream=True)
        with open("ffmpeg.tar.xz", "wb") as f:
            f.write(r.content)
        with tarfile.open("ffmpeg.tar.xz") as tar:
            tar.extractall("ffmpeg_bin")
        for root, dirs, files in os.walk("ffmpeg_bin"):
            if "ffmpeg" in files:
                path = os.path.join(root, "ffmpeg")
                os.chmod(path, stat.S_IRWXU)
                return path
    for root, dirs, files in os.walk("ffmpeg_bin"):
        if "ffmpeg" in files:
            return os.path.join(root, "ffmpeg")

def get_ffmpeg_path():
    if platform.system() == "Windows":
        return "ffmpeg"  # Use installed ffmpeg
    return download_ffmpeg()  # Cloud environment

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_merge_video_audio(url, res):
    yt = pytube.YouTube(url)
    title = sanitize_filename(yt.title)
    video = yt.streams.filter(adaptive=True, mime_type="video/mp4", res=res).first()
    audio = yt.streams.filter(only_audio=True).first()

    video_path = video.download(filename="temp_video.mp4")
    audio_path = audio.download(filename="temp_audio.mp4")
    ffmpeg = get_ffmpeg_path()
    output_name = title + ".mp4"

    subprocess.run([ffmpeg, "-y", "-i", video_path, "-i", audio_path, "-c", "copy", output_name])

    with open(output_name, "rb") as f:
        data = f.read()

    os.remove(video_path)
    os.remove(audio_path)
    os.remove(output_name)

    return data, output_name

def download_audio_mp3(url):
    yt = pytube.YouTube(url)
    title = sanitize_filename(yt.title)
    audio = yt.streams.filter(only_audio=True).first()
    audio_path = audio.download(filename="temp_audio")
    ffmpeg = get_ffmpeg_path()
    output_name = title + ".mp3"

    subprocess.run([ffmpeg, "-y", "-i", audio_path, "-vn", "-b:a", "192k", output_name])

    with open(output_name, "rb") as f:
        data = f.read()

    os.remove(audio_path)
    os.remove(output_name)

    return data, output_name

st.title("YouTube Downloader 🎥")

url = st.text_input("Enter YouTube URL:")
mode = st.selectbox("Download Format:", ["MP4", "MP3"])

if mode == "MP4":
    res = st.selectbox("Select Quality:", ["720p", "1080p"])

if st.button("Download"):
    if not url:
        st.warning("Please enter a URL")
    else:
        with st.spinner("Processing..."):
            if mode == "MP4":
                data, filename = download_merge_video_audio(url, res)
                st.download_button("Download MP4", data, file_name=filename, mime="video/mp4")
            else:
                data, filename = download_audio_mp3(url)
                st.download_button("Download MP3", data, file_name=filename, mime="audio/mp3")