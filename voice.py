import whisper

print("Loading Whisper model...")

model = whisper.load_model("tiny")

print("Whisper model loaded!")


def extract_voice_text(audio_path):

    result = model.transcribe(audio_path)

    return result["text"]