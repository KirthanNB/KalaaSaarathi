import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import uuid
import requests
from io import BytesIO

def make_poster(shop_url: str, hero_img: str, price: int) -> str:
    """Generate a printable poster with QR code"""
    # Download the hero image
    response = requests.get(hero_img)
    product_image = Image.open(BytesIO(response.content))
    
    # Resize product image
    product_image = product_image.resize((400, 400))
    
    # Create QR code
    qr = qrcode.make(shop_url)
    qr = qr.resize((200, 200))
    
    # Create canvas
    canvas = Image.new("RGB", (600, 900), "white")
    draw = ImageDraw.Draw(canvas)
    
    # Try to load font, fallback to default
    try:
        font_large = ImageFont.truetype("arial.ttf", 36)
        font_medium = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 18)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Add title
    draw.text((300, 30), "CraftLink", fill="black", font=font_large, anchor="mt")
    draw.text((300, 70), "Handmade with Love", fill="gray", font=font_medium, anchor="mt")
    
    # Add product image
    canvas.paste(product_image, (100, 100))
    
    # Add price
    draw.text((300, 520), f"₹{price}", fill="green", font=font_large, anchor="mt")
    
    # Add QR code and instructions
    canvas.paste(qr, (200, 570))
    draw.text((300, 780), "Scan to Buy", fill="black", font=font_medium, anchor="mt")
    draw.text((300, 810), "WhatsApp +91-XXXXXX-XXXX", fill="gray", font=font_small, anchor="mt")
    
    # Save poster
    os.makedirs("posters", exist_ok=True)
    poster_path = f"posters/{uuid.uuid4().hex}.pdf"
    canvas.save(poster_path, "PDF", resolution=100)
    
    return poster_path