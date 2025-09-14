import os
import vertexai
import json
from vertexai.preview.vision_models import ImageTextModel
from vertexai.preview.generative_models import GenerativeModel, Part
from google.cloud import texttospeech
import re

# Configure Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
vertexai.init(project="craftlink-2025", location="asia-south1")

model = GenerativeModel("gemini-1.5-flash")

def describe_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    
    prompt = """You are a nostalgic Indian grandparent who appreciates handmade crafts.
    In 60 words describe this craft with love and emotion. 
    Include 3 Hindi words (with English translation in parentheses),
    Suggest 5 SEO hashtags, and recommend a fair ₹ price range like 200-400.
    Format: Description. Hindi: word1 (meaning1), word2 (meaning2), word3 (meaning3). 
    Price: ₹price_low-price_high. Tags: #tag1 #tag2 #tag3 #tag4 #tag5"""
    
    response = model.generate_content([Part.from_data(image_bytes, "image/jpeg"), prompt])
    return response.text

def speak_hindi(text: str, output_file: str):
    """Convert Hindi text to speech with error handling"""
    try:
        # Extract Hindi words from the text
        hindi_words = re.findall(r'[\u0900-\u097F]+', text)
        if hindi_words:
            hindi_text = " ".join(hindi_words[:3])  # Speak first 3 Hindi words
        else:
            hindi_text = "सुंदर हस्तशिल्प"  # Default Hindi phrase
        
        client = texttospeech.TextToSpeechClient()
        synthesis = client.synthesize_speech(
            input=texttospeech.SynthesisInput(text=hindi_text),
            voice=texttospeech.VoiceSelectionParams(
                language_code="hi-IN", 
                name="hi-IN-Neural2-A"
            ),
            audio_config=texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
        )
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "wb") as f:
            f.write(synthesis.audio_content)
        return True
    except Exception as e:
        print(f"TTS Error: {e}")
        # Don't raise the exception, just log it
        return False