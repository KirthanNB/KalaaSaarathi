import os, requests, uuid
from google.cloud import vision, storage
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

client = vision.ImageAnnotatorClient()
storage_client = storage.Client()

BUCKET = "craftlink-images"   # we’ll create this bucket in browser

def remove_bg_and_upload(local_path: str) -> str:
    # 1. remove background via Vision AI (trim bbox)
    with open(local_path, "rb") as f:
        content = f.read()
    image = vision.Image(content=content)
    response = client.object_localization(image=image)
    objects = response.localized_object_annotations
    # simple: keep biggest bounding box
    if not objects:
        bbox = (0, 0, 1, 1)
    else:
        bbox = (obj.bounding_poly.normalized_vertices for obj in objects)
    # 2. fake crop & save 4 festival backgrounds (demo)
    # (tomorrow real Imagen2 call; today we copy 4 demo files)
    urls = []
    for bg in ["diwali", "holi", "sunset", "plain"]:
        file_name = f"{uuid.uuid4().hex[:8]}.jpg"
        blob = storage_client.bucket(BUCKET).blob(file_name)
        blob.upload_from_filename(local_path)  # demo: same file
        blob.make_public()
        urls.append(blob.public_url)
    return urls