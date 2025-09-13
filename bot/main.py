# ~~~~~~~~~~~~~~  C:\CraftLink\bot\main.py  ~~~~~~~~~~~~~
from fastapi import FastAPI, Form, Response
import os, uuid, requests
from twilio.twiml.messaging_response import MessagingResponse
from google.cloud import vision
import requests
from requests.auth import HTTPBasicAuth

app = FastAPI()

# Set Google credentials (make sure the JSON exists at this path)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\CraftLink\\bot\\craftlink-vision.json"

# Initialize Vision client
vision_client = vision.ImageAnnotatorClient()

def describe_image_twilio(media_url: str) -> str:
    try:
        sid = os.getenv("TWILIO_SID")
        token = os.getenv("TWILIO_TOKEN")

        # Download the image from Twilio
        response = requests.get(media_url, auth=HTTPBasicAuth(sid, token))
        if response.status_code != 200:
            return f"⚠️ Failed to fetch media: {response.status_code}"

        image = vision.Image(content=response.content)
        vision_resp = vision_client.label_detection(image=image)

        if vision_resp.error.message:
            return f"⚠️ Vision API error: {vision_resp.error.message}"

        labels = vision_resp.label_annotations
        if not labels:
            return "✨ No labels detected. Price band: ₹250-400  #handmade"

        description = ', '.join([label.description for label in labels])
        return f"✨ {description}. Price band: ₹250-400 #handmade"

    except Exception as e:
        return f"⚠️ An error occurred: {e}"

def deploy_shop(product_id: str) -> str:
    """
    Generate a product page URL hosted on Firebase.
    Replace the base URL with your actual Firebase Hosting domain.
    """
    return f"https://neethi-saarathi-ids.web.app/product/{product_id}"

@app.post("/whatsapp")
async def whatsapp_reply(
    Body: str = Form(""),
    NumMedia: str = Form("0"),
    MediaUrl0: str = Form(None)
):
    resp = MessagingResponse()

    try:
        if NumMedia != "0" and MediaUrl0:
            # Step 1: analyze the image
            analysis = describe_image_twilio(MediaUrl0)
            resp.message(analysis)

            # Step 2: generate a shop URL for this product
            product_id = str(uuid.uuid4())
            shop_url = deploy_shop(product_id)
            resp.message(f"🛒 View this item in our shop: {shop_url}")

        else:
            if Body.strip().lower() == "hi":
                resp.message("👋 Hey! Send me a photo and I'll describe it for you using AI.")
            else:
                resp.message(f"You said: {Body}")

    except Exception as e:
        resp = MessagingResponse()
        resp.message(f"⚠️ Error while processing: {e}")

    return Response(content=str(resp), media_type="application/xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
