🎥 YouTube to MP3 & MP4 Downloader (Streamlit App)
⚠️ IMPORTANT NOTICE

🚨 This project is currently NOT working on Streamlit Cloud.

The app stopped functioning due to HTTP 403 Forbidden errors from YouTube servers.
This happens because YouTube blocks download requests coming from shared cloud hosting IP addresses (such as Streamlit Cloud).

✅ The application still works when run locally on your own machine.
❌ It does NOT work when deployed on Streamlit Cloud or similar shared hosting platforms.

📌 About The Project

This is a simple YouTube Downloader Web App built using:

Streamlit (Frontend)

yt-dlp (YouTube extraction)

FFmpeg (Audio/Video processing)

The app allows users to:

🎵 Download YouTube videos as MP3 (audio)

🎥 Download YouTube videos as MP4 (video)

Select video quality (720p / 1080p)

Download directly from the browser

🛠 Tech Stack

Python 3.x

Streamlit

yt-dlp

FFmpeg

🚀 Features

Clean and simple UI

MP3 audio extraction (192kbps)

MP4 video download with selected resolution

Automatic audio-video merging

Error handling support

🧠 Why It Stopped Working on Streamlit Cloud

YouTube actively blocks download requests from:

Streamlit Cloud

Heroku

Replit

Many shared VPS providers

When the app tries to download content from YouTube servers, it receives:

HTTP Error 403: Forbidden

This is not a coding error — it is a server-side restriction from YouTube.

✅ How To Run Locally (Works)
1️⃣ Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
2️⃣ Install dependencies

Create a virtual environment (recommended):

pip install -r requirements.txt
3️⃣ Install FFmpeg

Make sure FFmpeg is installed on your system:

Windows → Install and add to PATH

Linux → sudo apt install ffmpeg

Mac → brew install ffmpeg

4️⃣ Run the app
streamlit run YT_app.py

Open the local URL shown in terminal.

📂 Project Structure
├── YT_app.py
├── requirements.txt
├── packages.txt (for cloud deployment)
└── README.md
📦 requirements.txt
streamlit
yt-dlp
⚖️ Disclaimer

This project is built strictly for:

Educational purposes

Learning Streamlit deployment

Understanding media processing workflows

Downloading copyrighted content may violate YouTube's Terms of Service.
Use responsibly.

💡 Future Improvements

Thumbnail preview before download

Video title auto-fetch

Progress bar support

Better UI design

Desktop version instead of cloud deployment

👨‍💻 Author

Kawaljot Singh
