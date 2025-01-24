import re
import subprocess
import threading

from yt_dlp import YoutubeDL

active_downloads = []


def get_video_info(video_url):
    """Get detailed information about a Youtube video using YT-DLP.

: PARA VIDEO_URL: URL OF THE VIDEO TO BE ANALYED.
: Return: A dictionary containing information such as title, duration, views,
Upload, uploader and thumbnail date."""
    options = {
        "quiet": True,
        "no_warnings": True,
        "format": "best",
    }
    with YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        return {
            "url": video_url,
            "title": info_dict.get("title"),
            "duration": info_dict.get("duration"),
            "view_count": info_dict.get("view_count"),
            "upload_date": info_dict.get("upload_date"),
            "uploader": info_dict.get("uploader"),
            "thumbnail_url": info_dict.get("thumbnail"),
        }


def handle_download(url):
    """Manages the download process of a video on a separate thread.

After downloading, removes active thread from the `Active_Downloads` list.

: Stop URL: URL of the video to be downloaded."""
    result = subprocess_download_video(url=url, output="./downloads")
    active_downloads.remove(threading.current_thread().name)
    print(f"Download completed: {result}")


def subprocess_download_video(url, options=None, output="./downloads"):
    """Run YT-DLP as a subprocess to download videos.

: Stop URL: URL of the video to be downloaded.
: PARAM OPTIONS: List of additional options for YT-DLP.
: Stop output: Directory where the downloaded files will be saved.
: Return: A dictionary containing status, standard output and errors, if any."""
    try:
        cmd = ["yt-dlp", url, "-o", f"{output}/%(title)s.%(ext)s"]
        if options:
            cmd.extend(options)

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return {
            "status": "completed" if result.returncode == 0 else "error",
            "output": result.stdout.decode(),
            "error": result.stderr.decode(),
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}
