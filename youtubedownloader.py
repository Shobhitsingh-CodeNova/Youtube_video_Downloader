import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")
st.title("🎬 YouTube Video / Audio Downloader")

# ---------- INPUT ----------
url = st.text_input("🔗 Enter YouTube URL")

download_type = st.radio(
    "📥 Download type:",
    ["🎥 Video (MP4)", "🎧 Audio (MP3)"]
)

quality = st.selectbox(
    "🎞️ Select Video Quality:",
    ["Best", "720p", "480p", "360p"],
    disabled=(download_type == "🎧 Audio (MP3)")
)

# ---------- PROGRESS ----------
progress_bar = st.progress(0)
status_text = st.empty()

def progress_hook(d):
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "0%").replace("%", "")
        try:
            progress_bar.progress(int(float(percent)))
            status_text.text(f"⏳ Downloading... {percent}%")
        except:
            pass
    elif d["status"] == "finished":
        progress_bar.progress(100)
        status_text.text("✅ Download finished")

# ---------- BUTTON ----------
if st.button("⬇️ Download", type="primary"):

    if not url.startswith("http"):
        st.error("❌ Please enter a valid YouTube URL")
        st.stop()

    try:
        # ---------- FOLDERS ----------
        video_dir = "My_Youtube_Videos"
        audio_dir = "My_Youtube_Audios"
        os.makedirs(video_dir, exist_ok=True)
        os.makedirs(audio_dir, exist_ok=True)

        # ---------- QUALITY MAP ----------
        quality_map = {
            "Best": "bestvideo+bestaudio/best",
            "720p": "bestvideo[height<=720]+bestaudio/best",
            "480p": "bestvideo[height<=480]+bestaudio/best",
            "360p": "bestvideo[height<=360]+bestaudio/best"
        }

        # ---------- OPTIONS ----------
        if download_type == "🎥 Video (MP4)":
            ydl_opts = {
                "format": quality_map[quality],
                "merge_output_format": "mp4",
                "outtmpl": f"{video_dir}/%(title)s.%(ext)s",
                "progress_hooks": [progress_hook],
                "quiet": True,
                "no_warnings": True
            }
        else:
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": f"{audio_dir}/%(title)s.%(ext)s",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                "progress_hooks": [progress_hook],
                "quiet": True,
                "no_warnings": True
            }

        # ---------- DOWNLOAD ----------
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        # ---------- OUTPUT ----------
        st.success("🎉 Download Complete!")
        st.balloons()

        if download_type == "🎥 Video (MP4)":
            st.video(file_path)
        else:
            st.audio(file_path)

        if "thumbnail" in info:
            st.image(info["thumbnail"], caption="Video Thumbnail")

    except Exception as e:
        st.error("❌ Something went wrong")
        st.code(str(e))
