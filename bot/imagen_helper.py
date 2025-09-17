import os
import uuid
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

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