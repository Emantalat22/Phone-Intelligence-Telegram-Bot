import whisper

model = None


def extract_voice_text(audio_path):

    global model

    if model is None:
        print("Loading Whisper model...")
        model = whisper.load_model("tiny")
        print("Whisper model loaded!")

    result = model.transcribe(audio_path)

    return result["text"]