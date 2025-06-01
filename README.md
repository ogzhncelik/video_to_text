video_to_text is a Python-based script designed to automatically transcribe audio and video files into text using OpenAI’s Whisper speech recognition model. It supports multiple file formats, leverages GPU acceleration (if available), and is tailored for Turkish language transcription. The tool is ideal for researchers, journalists, content creators, or anyone who needs fast and accurate transcription from media files.

---

KEY FEATURES

Audio & Video File Support
• Accepts common audio formats: .wav, .mp3, .aac  
• Accepts video formats: .mp4, .mkv, .avi, .mov  
• Automatically extracts audio from video using ffmpeg  

Transcription Engine
• Uses Whisper Large model for accurate speech recognition  
• Processes content in Turkish (`language='tr'` by default)  
• Utilizes GPU (CUDA) if available for faster processing  

Output Management
• Automatically creates a `/text` folder  
• Saves each transcription as a .txt file named after the media filename  
• Deletes temporary audio files after processing  

Error Handling
• Skips files that cannot be processed or transcribed  
• Provides clear warnings in case of ffmpeg or model errors  

---

HOW IT WORKS

1. Folder Scanning  
The script looks through a specified folder for all supported audio and video files.

2. Audio Extraction  
If a video file is detected, ffmpeg is used to extract a mono 16kHz audio stream and save it as `temp_audio.wav`.

3. Whisper Transcription  
The audio file is passed to Whisper’s transcription engine, which outputs the spoken content as text in Turkish.

4. Output Saving  
Each transcription is saved as a .txt file inside a newly created `/text` subfolder within the original directory.

---

USAGE

• Edit the `file_path` value inside the script:
```python
if __name__ == "__main__":
    file_path = "/your/folder/path"
    transcribe_videos_in_folder(file_path)
REQUIREMENTS

• Python 3.8+
• ffmpeg installed and added to PATH
• Python packages: whisper, torch

Install with:
pip install torch openai-whisper
