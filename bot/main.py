from fastapi import FastAPI, Form
import shutil, os, uuid
from gemini_helper import describe_image
from twilio.rest import Client
import os
sid   = os.getenv("TWILIO_SID")      # Cloud Build injects
token = os.getenv("TWILIO_TOKEN")
twilio_client = Client(sid, token)

app = FastAPI()

# --- helper stubs (replace later with real implementations) ---
def remove_bg_and_upload(local_file: str):
    """Fake background removal + upload, return list of image URLs."""
    # TODO: replace with actual background-removal + cloud upload
    return [f"https://example.com/{os.path.basename(local_file)}_clean.png"]

def deploy_shop(product_id: str):
    """Fake mini-shop deployment, return shop URL."""
    # TODO: replace with actual shop deployment logic
    return f"https://craftshop.example.com/{product_id}"

# --- routes ---
@app.get("/")
def hello():
    return {"message": "CraftLink Day-3 brain alive"}

@app.post("/whatsapp")
def whatsapp_photo(
    From: str = Form(...),
    NumMedia: str = Form(...),
    MediaUrl0: str = Form(None)
):
    # 1. Check if user sent a photo
    if NumMedia == "0":
        return {"reply": "कृपया अपने शिल्प की फोटो भेजें."}

    # 2. Save the photo (currently fake with demo_pot.jpg)
    photo_id = str(uuid.uuid4())[:8]
    local_file = f"inbox/{photo_id}.jpg"
    os.makedirs("inbox", exist_ok=True)
    shutil.copy("demo_pot.jpg", local_file)   # replace later with real download

    # 3. Ask Gemini to describe image
    story = describe_image(local_file)

    # 4. Generate clean product images
    image_urls = remove_bg_and_upload(local_file)

    # 5. Deploy mini-shop
    shop_url = deploy_shop(photo_id)

    # 6. Reply back to artisan
    return {
        "reply": f"{story}\n\nYour shop: {shop_url}",
        "images": image_urls
    }
