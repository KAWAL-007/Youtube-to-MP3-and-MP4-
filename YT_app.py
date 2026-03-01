import streamlit as st
import yt_dlp
import os
import re

st.set_page_config(page_title="YouTube Downloader", layout="centered")

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_mp3(url):
    output_folder = "downloads"
    os.makedirs(output_folder, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
        "quiet": True,
        "nocheckcertificate": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        mp3_file = filename.rsplit(".", 1)[0] + ".mp3"

    with open(mp3_file, "rb") as f:
        data = f.read()

    os.remove(mp3_file)

    return data, os.path.basename(mp3_file)

def download_mp4(url, resolution):
    output_folder = "downloads"
    os.makedirs(output_folder, exist_ok=True)

    ydl_opts = {
        "format": f"bestvideo[height<={resolution[:-1]}]+bestaudio/best",
        "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
        "quiet": True,
        "nocheckcertificate": True,
        "merge_output_format": "mp4"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

        if not filename.endswith(".mp4"):
            filename = filename.rsplit(".", 1)[0] + ".mp4"

    with open(filename, "rb") as f:
        data = f.read()

    os.remove(filename)

    return data, os.path.basename(filename)


# ================= UI =================

st.title("YouTube Downloader 🎥")

url = st.text_input("Enter YouTube URL:")
mode = st.selectbox("Download Format:", ["MP4", "MP3"])

if mode == "MP4":
    resolution = st.selectbox("Select Quality:", ["720p", "1080p"])

if st.button("Download"):
    if not url:
        st.warning("Please enter a URL")
    else:
        try:
            with st.spinner("Processing..."):
                if mode == "MP3":
                    data, filename = download_mp3(url)
                    st.success("Download Ready ✅")
                    st.download_button("Download MP3", data, file_name=filename, mime="audio/mp3")
                else:
                    data, filename = download_mp4(url, resolution)
                    st.success("Download Ready ✅")
                    st.download_button("Download MP4", data, file_name=filename, mime="video/mp4")

        except Exception as e:
            st.error("Something went wrong ❌")
            st.text(str(e))
