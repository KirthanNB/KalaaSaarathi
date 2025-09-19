# bot/main.py (enhanced version)
import os
import random
import uuid
from fastapi import FastAPI, Form, Response, Request, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import requests
from requests.auth import HTTPBasicAuth
import json
import traceback
import logging
import asyncio
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import our modules
try:
    from gemini_helper import describe_image, analyze_product_description
    GEMINI_AVAILABLE = True
    logger.info("Gemini helper loaded successfully")
except Exception as e:
    logger.error(f"Gemini helper not available: {e}")
    GEMINI_AVAILABLE = False
    def describe_image(image_path): return "Beautiful handmade craft with traditional artistry."
    def analyze_product_description(prompt): return '{"enhanced_description": "Handmade with care", "price_suggestions": [299,499,799]}'

try:
    from imagen_helper import remove_bg_and_upload
    IMAGEN_AVAILABLE = True
    logger.info("Imagen helper loaded successfully")
except Exception as e:
    logger.error(f"Imagen helper not available: {e}")
    IMAGEN_AVAILABLE = False
    def remove_bg_and_upload(path): return [f"https://storage.googleapis.com/craftlink-images/fallback{i}.jpg" for i in range(1,5)]

try:
    from deploy_shop import build_and_host, update_products_json
    DEPLOY_AVAILABLE = True
    logger.info("Deploy shop loaded successfully")
except Exception as e:
    logger.error(f"Deploy shop not available: {e}")
    DEPLOY_AVAILABLE = False
    def build_and_host(product_id, description, images): return f"https://neethi-saarathi-ids.web.app/product/{product_id}.html"
    def update_products_json(data): pass

# Set Google credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

# Initialize Twilio client
twilio_sid = os.getenv("TWILIO_ACCOUNT_SID", "your_twilio_sid")
twilio_token = os.getenv("TWILIO_AUTH_TOKEN", "your_twilio_token")
twilio_client = Client(twilio_sid, twilio_token)

app = FastAPI(title="KalaaSaarathi API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def download_twilio_media(media_url: str) -> bytes:
    """Download media from Twilio"""
    response = requests.get(media_url, auth=HTTPBasicAuth(twilio_sid, twilio_token))
    response.raise_for_status()
    return response.content

def save_image(content: bytes, filename: str) -> str:
    """Save image to temporary file"""
    os.makedirs("temp_images", exist_ok=True)
    filepath = f"temp_images/{filename}"
    with open(filepath, "wb") as f:
        f.write(content)
    return filepath

def get_product(product_id: str):
    """Get product data from products.json"""
    try:
        products_file = "../shop/out/products.json"
        if os.path.exists(products_file):
            with open(products_file, "r") as f:
                data = json.load(f)
                for product in data.get("products", []):
                    if product.get("id") == product_id:
                        return product
        return None
    except:
        return None

def update_product(product_id: str, field: str, value: any) -> bool:
    """Update product in products.json"""
    try:
        products_file = "../shop/out/products.json"
        
        # Read existing products or create empty array
        if os.path.exists(products_file):
            try:
                with open(products_file, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {"products": []}
        else:
            data = {"products": []}
        
        # Find and update product
        updated = False
        for product in data.get("products", []):
            if product.get("id") == product_id:
                product[field] = value
                updated = True
                break
        
        if updated:
            with open(products_file, "w") as f:
                json.dump(data, f, indent=2)
            return True
        return False
        
    except Exception as e:
        logger.error(f"Update product error: {e}")
        return False

def handle_edit_command(phone_number: str, message: str, media_url: str = None) -> str:
    """Handle edit commands from WhatsApp"""
    try:
        parts = message.strip().split()
        if len(parts) < 4 and not media_url:
            return "Usage: edit PRODUCT_ID FIELD VALUE\nExample: edit abc123 price 500\n\nFields: price, description, image"
        
        product_id = parts[1]
        field = parts[2].lower() if len(parts) > 2 else "image"
        value = " ".join(parts[3:]) if len(parts) > 3 else ""
        
        # Handle different field types
        if field == "price":
            if not value.isdigit():
                return "❌ Price must be a number. Example: edit abc123 price 500"
            success = update_product(product_id, "price", int(value))
            
        elif field == "description":
            success = update_product(product_id, "description", value)
            
        elif field == "image" and media_url:
            # Download and process new image
            image_content = download_twilio_media(media_url)
            image_filename = f"{uuid.uuid4().hex}.jpg"
            image_path = save_image(image_content, image_filename)
            
            if IMAGEN_AVAILABLE:
                image_urls = remove_bg_and_upload(image_path)
            else:
                image_urls = [f"https://storage.googleapis.com/craftlink-images/fallback{i}.jpg" for i in range(1,5)]
                
            success = update_product(product_id, "images", image_urls)
            
        elif field == "image":
            return "❌ Please send an image with the edit command: edit PRODUCT_ID image"
            
        else:
            return "❌ Invalid field. Use: price, description, or image"
        
        if success:
            # Redeploy the shop with updated product
            product_data = get_product(product_id)
            if product_data:
                if DEPLOY_AVAILABLE:
                    build_and_host(product_id, product_data.get('description', ''), product_data.get('images', []))
                else:
                    build_and_host(product_id, product_data.get('description', ''), product_data.get('images', []))
            return f"✅ Updated {field} for product {product_id[:8]}"
        else:
            return "❌ Product not found. Check the product ID."
            
    except Exception as e:
        logger.error(f"Edit command error: {e}")
        return f"❌ Error: {str(e)}"

def handle_myproducts_command(phone_number: str) -> str:
    """Send user their product list"""
    try:
        products_file = "../shop/out/products.json"
        if not os.path.exists(products_file):
            return "You don't have any products yet. Send a photo to create your first shop!"
        
        with open(products_file, "r") as f:
            data = json.load(f)
        
        user_products = []
        user_phone = phone_number.replace("whatsapp:", "")
        
        for product in data.get("products", []):
            # Simple user matching by phone number pattern
            if user_phone in product.get("id", "") or user_phone in product.get("user_phone", ""):
                user_products.append(product)
        
        if not user_products:
            return "You don't have any products yet. Send a photo to create your first shop!"
        
        response = "📋 Your Products:\n\n"
        for product in user_products[-5:]:  # Show last 5 products
            response += f"🆔 {product['id'][:8]}...\n"
            response += f"📦 {product.get('title', 'Handmade Craft')}\n"
            response += f"💰 ₹{product.get('price', 350)}\n"
            response += f"🔗 https://neethi-saarathi-ids.web.app/product/{product['id']}.html\n"
            response += "━━━━━━━━━━━━━━━━━━━━\n"
        
        response += "\nTo edit: 'edit PRODUCT_ID field value'\nExample: 'edit abc123 price 500'"
        return response
        
    except Exception as e:
        logger.error(f"MyProducts error: {e}")
        return "❌ Error fetching your products. Please try again later."

async def process_image_async(media_url: str, phone_number: str):
    """Process image in background and send follow-up messages"""
    try:
        logger.info(f"Async processing started for {phone_number}")
        
        # Download the image
        image_content = download_twilio_media(media_url)
        image_filename = f"{uuid.uuid4().hex}.jpg"
        image_path = save_image(image_content, image_filename)
        logger.info(f"Image saved to: {image_path}")
        
        # Step 1: Analyze with Gemini
        try:
            if GEMINI_AVAILABLE:
                analysis = describe_image(image_path)
            else:
                analysis = "Beautiful handmade craft with traditional artistry. Price band: ₹250-400 #handmade #craft #artisan"
            logger.info(f"Analysis complete: {analysis[:100]}...")
            
            # Send analysis first
            twilio_client.messages.create(
                body=analysis,
                from_="whatsapp:+14155238886",
                to=phone_number
            )
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            analysis = "Beautiful handmade craft with traditional artistry. Price band: ₹250-400 #handmade #craft #artisan"
            twilio_client.messages.create(
                body=analysis,
                from_="whatsapp:+14155238886",
                to=phone_number
            )
        
        # Step 2: Process image
        try:
            if IMAGEN_AVAILABLE:
                image_urls = remove_bg_and_upload(image_path)
            else:
                image_urls = [f"https://storage.googleapis.com/craftlink-images/fallback{i}.jpg" for i in range(1,5)]
            logger.info(f"Image processing complete: {len(image_urls)} URLs")
        except Exception as e:
            logger.error(f"Image processing failed: {e}")
            image_urls = [f"https://storage.googleapis.com/craftlink-images/fallback{i}.jpg" for i in range(1,5)]
        
        # Step 3: Generate shop URL
        product_id = str(uuid.uuid4())
        try:
            if DEPLOY_AVAILABLE:
                shop_url = build_and_host(product_id, analysis, image_urls)
            else:
                shop_url = f"https://neethi-saarathi-ids.web.app/product/{product_id}.html"
            logger.info(f"Shop URL generated: {shop_url}")
        except Exception as e:
            logger.error(f"Deployment failed: {e}")
            shop_url = f"https://neethi-saarathi-ids.web.app/product/{product_id}.html"
        
        # Update products.json with user reference
        product_data = {
            "id": product_id,
            "title": f"Handmade Craft #{product_id[:6]}",
            "description": analysis,
            "price": 350,
            "images": image_urls,
            "category": "handmade",
            "artisan_region": "India",
            "created_at": datetime.now().isoformat(),
            "user_phone": phone_number.replace("whatsapp:", "")
        }
        update_products_json(product_data)
        
        # Send shop link
        twilio_client.messages.create(
            body=f"🛍️ Your shop is ready: {shop_url}",
            from_="whatsapp:+14155238886",
            to=phone_number
        )
        
        # Send final message with edit instructions
        twilio_client.messages.create(
            body=f"📦 We'll help you with shipping and payments!\n\nTo edit this product later:\n• edit {product_id[:8]} price NEW_PRICE\n• edit {product_id[:8]} description \"NEW_DESCRIPTION\"\n• edit {product_id[:8]} image + send new photo\n• Type 'myproducts' to see all your items",
            from_="whatsapp:+14155238886",
            to=phone_number
        )
        
        logger.info(f"Async processing completed for {phone_number}")
        
    except Exception as e:
        logger.error(f"Async processing error: {e}")
        logger.error(traceback.format_exc())
        # Send error message
        try:
            twilio_client.messages.create(
                body="⚠️ Sorry, I encountered an error processing your image. Please try again.",
                from_="whatsapp:+14155238886",
                to=phone_number
            )
        except Exception as send_error:
            logger.error(f"Failed to send error message: {send_error}")

@app.post("/whatsapp")
async def whatsapp_reply(
    request: Request,
    Body: str = Form(""),
    NumMedia: str = Form("0"),
    MediaUrl0: str = Form(None),
    From: str = Form("")
):
    # Log the raw form data
    form_data = await request.form()
    logger.info(f"Received form data: {dict(form_data)}")
    
    resp = MessagingResponse()
    phone_number = From
    logger.info(f"Message from {phone_number}: Body='{Body}', MediaCount={NumMedia}")

    try:
        # Check for edit commands FIRST
        if Body.strip().lower().startswith("edit"):
            logger.info(f"Processing edit command: {Body}")
            if NumMedia != "0" and MediaUrl0:
                response_text = handle_edit_command(phone_number, Body, MediaUrl0)
            else:
                response_text = handle_edit_command(phone_number, Body)
            resp.message(response_text)
            
        elif Body.strip().lower() in ["myproducts", "mylist", "my items", "myproducts"]:
            logger.info(f"Processing myproducts command: {Body}")
            response_text = handle_myproducts_command(From)
            resp.message(response_text)
            
        elif NumMedia != "0" and MediaUrl0:
            logger.info(f"Processing media: {MediaUrl0}")
            
            # Send immediate response to prevent timeout
            resp.message("📸 Got your image! Processing it now with AI... I'll send the analysis and shop link in a moment.")
            
            # Process image in background (async)
            asyncio.create_task(process_image_async(MediaUrl0, From))
            
        else:
            if Body.strip().lower() in ["hi", "hello", "hey", "start", "नमस्ते"]:
                welcome_msg = """👋 नमस्ते! Welcome to KalaaSaarathi!

Send me a photo of your handmade craft and I'll:
1. 📸 Analyze it with AI
2. 🛍️ Create an online shop
3. 📊 Suggest a fair price
4. 📦 Help with shipping

Commands:
• myproducts - List your items
• edit PRODUCT_ID price 500 - Change price
• edit PRODUCT_ID description "New text" - Update description
• edit PRODUCT_ID image + send photo - Change image

Just send a photo to get started!"""
                resp.message(welcome_msg)
            else:
                resp.message("📸 Please send a photo of your craft to get started! I'll analyze it and create a shop for you.\n\nType 'help' for commands.")

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        logger.error(traceback.format_exc())
        resp.message("⚠️ Sorry, I encountered an error. Please try sending the photo again.")

    # Log the response
    response_content = str(resp)
    logger.info(f"Sending response: {response_content}")
    return Response(content=response_content, media_type="application/xml")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "services": {
            "gemini": GEMINI_AVAILABLE,
            "image_processing": IMAGEN_AVAILABLE,
            "deployment": DEPLOY_AVAILABLE
        }
    }

@app.post("/api/create-product")
async def api_create_product(
    images: list[UploadFile] = File(...),
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    price: str = Form(...),
    artisan_name: str = Form(...),
    artisan_region: str = Form(...),
    whatsapp_number: str = Form(...)
):
    try:
        logger.info("Web product creation started")
        
        # Process images
        image_urls = []
        for image in images:
            content = await image.read()
            temp_path = f"temp_web_{uuid.uuid4().hex}.jpg"
            with open(temp_path, "wb") as f:
                f.write(content)
            
            if IMAGEN_AVAILABLE:
                urls = remove_bg_and_upload(temp_path)
            else:
                urls = [f"https://storage.googleapis.com/craftlink-images/fallback{i}.jpg" for i in range(1,5)]
            
            image_urls.extend(urls)
            os.remove(temp_path)
        
        # Create product
        product_id = str(uuid.uuid4())
        product_data = {
            "id": product_id,
            "title": title,
            "description": description,
            "price": int(price),
            "images": image_urls,
            "category": category,
            "artisan_name": artisan_name,
            "artisan_region": artisan_region,
            "created_at": datetime.now().isoformat(),
            "whatsapp_number": whatsapp_number
        }
        
        # Update products.json
        update_products_json(product_data)
        
        # Build product page
        if DEPLOY_AVAILABLE:
            shop_url = build_and_host(product_id, description, image_urls)
        else:
            shop_url = f"https://neethi-saarathi-ids.web.app/product/{product_id}.html"
        
        logger.info(f"Web product created: {product_id}")
        
        return {
            "success": True,
            "message": "Product created successfully!",
            "product_url": shop_url,
            "product_id": product_id
        }
        
    except Exception as e:
        logger.error(f"Error in web product creation: {e}")
        raise HTTPException(status_code=500, detail="Error creating product")

@app.get("/api/products")
async def get_products():
    try:
        products_file = "../shop/out/products.json"
        if os.path.exists(products_file):
            with open(products_file, "r") as f:
                data = json.load(f)
            return data
        return {"products": []}
    except Exception as e:
        logger.error(f"Error loading products: {e}")
        return {"products": []}

@app.get("/api/test")
async def test_endpoint():
    return {"message": "API is working!", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")