import os, vertexai, json
from vertexai.preview.vision_models import ImageTextModel
from vertexai.preview.generative_models import GenerativeModel, Part
from google.cloud import texttospeech
def speak_hindi(text: str, output_file: str):
    client = texttospeech.TextToSpeechClient()
    synthesis = client.synthesize_speech(
        input=texttospeech.SynthesisInput(text=text),
        voice=texttospeech.VoiceSelectionParams(language_code="hi-IN", name="hi-IN-Neural2-A"),
        audio_config=texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    )
    with open(output_file, "wb") as f:
        f.write(synthesis.audio_content)
# point to your key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
vertexai.init(project="craftlink-2025", location="asia-south1")

model = GenerativeModel("gemini-1.5-flash")

def describe_image(image_path: str):
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    prompt = """You are a nostalgic Indian grandparent.
    In 60 words describe this craft. Add 3 Hindi words, 5 SEO hashtags, and a fair ₹ price band like 200-400."""
    response = model.generate_content([Part.from_data(image_bytes, "image/jpeg"), prompt])
    return response.text