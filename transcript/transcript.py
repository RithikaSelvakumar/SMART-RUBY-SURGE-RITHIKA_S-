import os
import time
import speech_recognition as sr
from moviepy import VideoFileClip
from pydub import AudioSegment
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from langchain_community.llms import Ollama  # Import Ollama for LLaMA model interaction

# Initialize LLaMA model
llm = Ollama(model="llama3.2")

# Ensure source_documents folder exists
source_documents_folder = "source_documents"
os.makedirs(source_documents_folder, exist_ok=True)

# Function to format transcript using LLaMA
def format_transcript_with_llama(raw_transcript):
    """Use LLaMA (via LangChain's Ollama) to clean and structure the transcript."""
    system_prompt = """
    You are an AI assistant that improves raw speech-to-text transcripts. Your job is to:
    - Fix punctuation and capitalization.
    - Remove filler words like "um", "uh", "you know".
    - Format the text into readable paragraphs (but don't add speaker labels).
    - Ensure clarity and proper sentence structure.
    Nothing extra about how u did and what you did should be responded.
    Only the formatted transcript should be given as response.
    Here is the transcript that needs to be formatted:
    """

    formatted_transcript = llm.invoke(system_prompt + raw_transcript)
    return formatted_transcript

# Function to save transcript as a PDF
def save_transcript_as_pdf(video_id, transcription):
    """Save the formatted transcribed text as a PDF file."""
    pdf_path = os.path.join(source_documents_folder, f"{video_id}_transcript.pdf")
    
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    
    y_position = 750  # Start position
    
    for line in transcription.split("\n"):
        c.drawString(50, y_position, line)
        y_position -= 20  # Move down for next line
        if y_position < 50:  # Start a new page if space runs out
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = 750
    
    c.save()
    print(f"✅ Formatted transcript saved as {pdf_path}")

# Function to extract audio from video
def video_to_audio(video_path, audio_output_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_output_path, codec="pcm_s16le")

# Function to split audio into smaller chunks
def split_audio(audio_path, chunk_length_ms=30000):
    audio = AudioSegment.from_wav(audio_path)
    total_length_ms = len(audio)
    chunks = []

    for i in range(0, total_length_ms, chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunk_path = f"{audio_path}_chunk{i//chunk_length_ms}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks

# Function to transcribe an audio chunk
def transcribe_audio_chunk(audio_chunk_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_chunk_path) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return "Audio could not be transcribed."
        except sr.RequestError as e:
            return f"API Error: {e}"

# Process a single video file and save the formatted transcript as a PDF
def process_video(video_path):
    video_id = os.path.splitext(os.path.basename(video_path))[0]
    timestamp = int(time.time())
    audio_path = f"audio_{video_id}_{timestamp}.wav"

    print(f"🔹 Processing: {video_path}")

    # Convert video to audio
    video_to_audio(video_path, audio_path)

    # Split the audio into chunks and transcribe
    audio_chunks = split_audio(audio_path)
    raw_transcript = ""
    for chunk in audio_chunks:
        raw_transcript += transcribe_audio_chunk(chunk) + "\n"
        os.remove(chunk)  # Cleanup

    # Format transcript using LLaMA
    formatted_transcript = format_transcript_with_llama(raw_transcript)

    # Save formatted transcript as PDF
    save_transcript_as_pdf(video_id, formatted_transcript.strip())

    # Cleanup audio file
    os.remove(audio_path)

# Process multiple videos in a folder
def process_multiple_videos(video_folder):
    video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.mkv', '.avi'))]

    if not video_files:
        print("❌ No video files found in the folder!")
        return

    print(f"🎥 Found {len(video_files)} videos. Processing...\n")
    
    for video_file in video_files:
        video_path = os.path.join(video_folder, video_file)
        process_video(video_path)

    print("\n✅ All videos processed! Check the 'source_documents' folder for formatted transcripts.")

# Example usage
if __name__ == '__main__':
    video_directory = "videos"  # Folder containing multiple videos
    process_multiple_videos(video_directory)
