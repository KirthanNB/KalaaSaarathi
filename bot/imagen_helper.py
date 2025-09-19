# bot/imagen_helper.py (with video support)
import os
import uuid
from google.cloud import storage
import random
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"


def get_fallback_video_url():
    """Return a fallback video URL"""
    fallbacks = [
        "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4", 
        "https://storage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"
    ]
    return random.choice(fallbacks)

def remove_bg_and_upload(local_path: str) -> list:
    """Upload image to uniformly accessed bucket"""
    try:
        storage_client = storage.Client()
        bucket_name = "craftlink-images"
        bucket = storage_client.bucket(bucket_name)
        
        # Upload the image
        with open(local_path, "rb") as f:
            image_content = f.read()
        
        file_name = f"{uuid.uuid4().hex}.jpg"
        blob = bucket.blob(file_name)
        
        # REMOVE predefined_acl for uniform bucket-level access
        blob.upload_from_string(image_content, content_type='image/jpeg')
        
        # For uniform access, construct the URL directly
        image_url = f"https://storage.googleapis.com/{bucket_name}/{file_name}"
        
        print(f"✅ Image uploaded: {image_url}")
        return [image_url] * 4
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        # Use timestamped fallbacks to avoid cache issues
        timestamp = uuid.uuid4().hex[:8]
        return [
            f"https://storage.googleapis.com/craftlink-images/fallback1.jpg?t={timestamp}",
            f"https://storage.googleapis.com/craftlink-images/fallback2.jpg?t={timestamp}",
            f"https://storage.googleapis.com/craftlink-images/fallback3.jpg?t={timestamp}",
            f"https://storage.googleapis.com/craftlink-images/fallback4.jpg?t={timestamp}"
        ]

def upload_video(local_path: str) -> str:
    """Upload video to storage bucket with fallback"""
    try:
        # First check if bucket exists
        storage_client = storage.Client()
        bucket_name = "craftlink-videos"
        
        if not storage_client.bucket(bucket_name).exists():
            print("❌ Video bucket doesn't exist. Using fallback.")
            return get_fallback_video_url()
        
        bucket = storage_client.bucket(bucket_name)
        
        # Upload the video
        with open(local_path, "rb") as f:
            video_content = f.read()
        
        file_name = f"{uuid.uuid4().hex}.mp4"
        blob = bucket.blob(file_name)
        
        blob.upload_from_string(video_content, content_type='video/mp4')
        blob.make_public()
        
        video_url = blob.public_url
        print(f"✅ Video uploaded: {video_url}")
        return video_url
        
    except Exception as e:
        print(f"❌ Video upload failed: {e}")
        return get_fallback_video_url()

def get_fallback_video_url():
    """Return a fallback video URL"""
    fallbacks = [
        "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        "https://storage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"
    ]
    return random.choice(fallbacks)