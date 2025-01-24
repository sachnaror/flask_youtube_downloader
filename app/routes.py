import threading
from flask import Blueprint, render_template, request, jsonify
from .utils import active_downloads, get_video_info, handle_download
import subprocess

# Define Blueprint for routes
bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    """
    Main application route that renders the homepage.
    :return: The HTML template for the homepage.
    """
    return render_template("index.html")

@bp.route("/videos/download", methods=["POST"])
def download():
    """
    Route to start downloading a video from a URL.
    The video will be processed on a separate thread to avoid blocking the server.
    Video information will be obtained before downloading.
    :return: A JSON containing information about the state of the operation and the video.
    """
    data = request.json
    url = data.get("video_url")

    if not url:
        return jsonify({"error": "The URL is mandatory"}), 400

    video_info = get_video_info(url)
    thread_name = f"download-{len(active_downloads) + 1}"
    active_downloads.append(thread_name)

    thread = threading.Thread(target=handle_download, args=(url,), name=thread_name)
    thread.start()

    return jsonify({"success": True, "thread": thread_name, "video_info": video_info}), 202

@bp.route("/run-video-converter", methods=["GET"])
def run_video_converter():
    """
    Trigger the video_to_markdown.py script in the background.
    """
    script_path = "../video_to_markdown.py"  # Relative path to the script
    try:
        subprocess.Popen(['python', script_path])
        return "Script is running in the background!", 200
    except Exception as e:
        return f"Error starting the script: {str(e)}", 500
