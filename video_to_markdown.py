import os
import time
import re
from moviepy.editor import VideoFileClip
from markitdown import _markitdown
from googletrans import Translator
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks

translator = Translator()

def extract_audio(video_path):
    """
    Extract audio from the video file.
    """
    video = VideoFileClip(video_path)
    audio_path = video_path.replace(".webm", ".wav")
    video.audio.write_audiofile(audio_path)
    video.close()
    return audio_path

def split_audio_into_chunks(audio_path, chunk_length=10):
    """
    Split the audio into smaller chunks of specified length (in seconds).
    """
    audio = AudioSegment.from_file(audio_path)
    chunks = make_chunks(audio, chunk_length * 1000)  # Chunk length in milliseconds
    chunk_files = []

    for i, chunk in enumerate(chunks):
        chunk_name = f"{audio_path}_chunk{i}.wav"
        chunk.export(chunk_name, format="wav")
        chunk_files.append(chunk_name)

    return chunk_files

def transcribe_audio_chunks(chunk_files):
    """
    Transcribe each audio chunk using Google Speech Recognition and combine the results.
    """
    transcription = ""
    recognizer = sr.Recognizer()

    for chunk_file in chunk_files:
        with sr.AudioFile(chunk_file) as source:
            print(f"Processing chunk: {chunk_file}")
            audio_data = recognizer.record(source)

        try:
            # Transcribe the audio using Google Web Speech API
            chunk_transcription = recognizer.recognize_google(audio_data)
            transcription += f"{chunk_transcription} "
        except sr.UnknownValueError:
            transcription += "[Unintelligible] "
        except sr.RequestError as e:
            print(f"Google Speech Recognition error: {e}")
            transcription += "[Error in transcription] "

    return transcription

def translate_text_to_markdown(text):
    """
    Translate text to English and convert it to Markdown.
    """
    translated_text = translator.translate(text, src="auto", dest="en").text
    markdown_content = f"# Video Transcription\n\n{translated_text}\n\n## Key Points\n\n- Automatically transcribed\n- Translated to English\n"
    return markdown_content

def cleanup_chunks(chunk_files):
    """
    Delete all audio chunk files used during processing.
    """
    for chunk_file in chunk_files:
        if os.path.exists(chunk_file):
            os.remove(chunk_file)
            print(f"Deleted chunk file: {chunk_file}")

def process_latest_video(download_folder):
    """
    Find the latest .webm file in the download folder, process it, and save as markdown.
    """
    # Find the latest .webm file
    webm_files = [
        os.path.join(download_folder, f)
        for f in os.listdir(download_folder)
        if f.endswith(".webm")
    ]
    if not webm_files:
        print("No .webm files found in the download folder.")
        return

    latest_file = max(webm_files, key=os.path.getmtime)
    print(f"Processing video: {latest_file}")

    # Extract audio from the video
    audio_path = extract_audio(latest_file)
    print(f"Extracted audio: {audio_path}")

    # Split audio into chunks
    chunk_files = split_audio_into_chunks(audio_path)
    print(f"Audio split into {len(chunk_files)} chunks.")

    # Transcribe audio chunks to text
    transcription = transcribe_audio_chunks(chunk_files)
    print("Transcription completed.")

    # Save transcription to a .txt file
    txt_file = latest_file.replace(".webm", ".txt")
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(transcription)
    print(f"Transcription saved to: {txt_file}")

    # Convert transcription to Markdown
    markdown_content = translate_text_to_markdown(transcription)

    # Save Markdown content to a file
    markdown_file = latest_file.replace(".webm", ".md")
    with open(markdown_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(f"Markdown file saved: {markdown_file}")

    # Cleanup chunk files
    cleanup_chunks(chunk_files)

if __name__ == "__main__":
    time.sleep(3)  # Wait for 3 seconds before starting
    download_folder = "/Users/homesachin/Desktop/zoneone/flask_youtube_downloader/downloads"
    if not os.path.exists(download_folder):
        print(f"Download folder not found: {download_folder}")
    else:
        process_latest_video(download_folder)
