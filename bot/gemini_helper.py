# bot/gemini_helper.py (enhanced version)
import os
import vertexai
import json
import re
from vertexai.preview.generative_models import GenerativeModel, Part

# Configure Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
vertexai.init(project="craftlink-2025", location="asia-south1")

model = GenerativeModel("gemini-1.5-flash")

def describe_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    
    prompt = """You are a nostalgic Indian grandparent who appreciates handmade crafts.
    In 60 words describe this craft with love and emotion. 
    Suggest 5 SEO hashtags.
    Price: ₹price_low-price_high. Tags: #tag1 #tag2 #tag3 #tag4 #tag5"""
    
    response = model.generate_content([Part.from_data(image_bytes, "image/jpeg"), prompt])
    return response.text

def extract_price_from_description(description: str) -> int:
    """Extract price from AI-generated description"""
    try:
        # Look for price patterns like ₹200-400 or 200-400
        price_match = re.search(r'₹?\s*(\d+)\s*-\s*₹?\s*(\d+)', description)
        if price_match:
            low, high = int(price_match.group(1)), int(price_match.group(2))
            return (low + high) // 2  # Return average price
        
        # Look for single price like ₹350
        single_price_match = re.search(r'₹?\s*(\d+)', description)
        if single_price_match:
            return int(single_price_match.group(1))
    except:
        pass
    
    # Default price if none found
    return 350

def extract_title_from_description(description: str) -> str:
    """Extract a title from the AI-generated description"""
    try:
        # Get the first sentence as title
        first_sentence = description.split('.')[0]
        if len(first_sentence) > 10:  # Ensure it's meaningful
            # Remove Hindi and price parts
            title = re.sub(r'Hindi:.*|Price:.*|Tags:.*', '', first_sentence)
            title = title.strip()
            if title and len(title) > 5:
                return title[:50]  # Limit length
    except:
        pass
    
    return "Beautiful Handmade Craft"

def extract_category_from_description(description: str) -> str:
    """Extract category from AI-generated description"""
    try:
        categories = [
            "pottery", "textiles", "jewelry", "paintings", "wooden",
            "metalwork", "leather", "papercraft", "home-decor", "accessories"
        ]
        
        description_lower = description.lower()
        for category in categories:
            if category in description_lower:
                return category
    except:
        pass
    
    return "handmade"

def analyze_product_description(prompt: str) -> str:
    """Analyze product description and suggest improvements"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Fallback response
        return json.dumps({
            "enhanced_description": "Beautiful handmade craft with traditional artistry.",
            "price_suggestions": [299, 499, 799],
            "features": ["Handmade", "Eco-friendly", "Traditional craftsmanship"],
            "tags": ["handmade", "craft", "artisan"]
        })