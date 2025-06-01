import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import os
import shutil
import subprocess
import whisper
import torch


def extract_audio(file_path, audio_path):
    try:
        if file_path.lower().endswith(('.aac', '.wav', '.mp3')):
            if os.path.abspath(file_path) != os.path.abspath(audio_path):
                shutil.copy(file_path, audio_path)
            else:
                print("⚠️ Audio file is already temp_audio.wav, copying skipped")
        else:
            command = [
                "ffmpeg",
                "-y",
                "-threads", "4",
                "-i", file_path,
                "-vn",
                "-acodec", "pcm_s16le",
                "-ar", "16000",
                "-ac", "1",
                audio_path
            ]
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Error: '{file_path}' could not be processed → ffmpeg could not run.")
    except Exception as e:
        print(f"⚠️ Error: '{file_path}' could not be processed → {e}")


def transcribe_videos_in_folder(folder_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("large").to(device)

    if device == "cuda":
        print(f"🚀 CUDA is active — Using GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("⚠️ CUDA disabled— CPU is using.")

    text_folder = os.path.join(folder_path, "text")
    os.makedirs(text_folder, exist_ok=True)

    video_files = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith(('.mp4', '.mkv', '.mov', '.avi', '.aac', '.wav', '.mp3'))
    ]

    for filename in video_files:
        video_path = os.path.join(folder_path, filename)
        temp_audio_path = os.path.join(folder_path, "temp_audio.wav")

        print(f"\n🔍 Processing: {filename}")
        extract_audio(video_path, temp_audio_path)

        if not os.path.exists(temp_audio_path):
            print(f"❌ Audio file could not create, skipping: {filename}")
            continue

        try:
            result = model.transcribe(temp_audio_path, language='tr', verbose=True)
            text_output_path = os.path.join(text_folder, f"{os.path.splitext(filename)[0]}.txt")

            with open(text_output_path, "w", encoding="utf-8") as f:
                f.write(result["text"])

            print(f"✅ Finish: {filename}")
        except Exception as e:
            print(f"⚠️ Transcription error: {filename} → {e}")

        os.remove(temp_audio_path)

    print("\n🎉 ALL PROCESS IS COMPLETED")


if __name__ == "__main__":
    file_path = "/file_path/"
    transcribe_videos_in_folder(file_path)
