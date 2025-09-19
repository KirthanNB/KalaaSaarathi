from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import uuid
import os
from datetime import datetime
from .imagen_helper import remove_bg_and_upload
from .deploy_shop import build_and_host
from .gemini_helper import analyze_product_description

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://neethi-saarathi-ids.web.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def analyze_product_with_ai(title: str, description: str, category: str):
    """Use AI to enhance product description and suggest improvements"""
    prompt = f"""Analyze this handmade product and enhance the description:

Title: {title}
Category: {category}
Initial Description: {description}

Please provide:
1. An emotional, grandmother-style description in English with Hindi words
2. 3 appropriate price suggestions (budget, standard, premium)
3. Key features and specifications
4. SEO-friendly tags

Format as JSON with: enhanced_description, price_suggestions, features, tags"""
    
    try:
        # This would call your Gemini AI
        response = analyze_product_description(prompt)
        return json.loads(response)
    except:
        # Fallback if AI is unavailable
        return {
            "enhanced_description": f"✨ {description} Beautiful handmade {category} crafted with care and tradition.",
            "price_suggestions": [299, 499, 799],
            "features": ["Handmade", "Eco-friendly", "Traditional craftsmanship"],
            "tags": ["handmade", category, "artisan"]
        }

def suggest_pricing(category: str, material: str):
    """Suggest pricing based on category and material"""
    base_prices = {
        'pottery': {'clay': 399, 'terracotta': 499, 'ceramic': 699},
        'textiles': {'cotton': 599, 'silk': 1299, 'wool': 899},
        'jewelry': {'silver': 799, 'gold': 2999, 'beads': 399},
        'paintings': {'canvas': 999, 'paper': 499, 'wall': 1499},
        'wooden': {'teak': 899, 'rosewood': 1299, 'bamboo': 499},
        'default': 499
    }
    
    material = material.lower() if material else ''
    category_data = base_prices.get(category, base_prices['default'])
    
    for mat, price in category_data.items():
        if mat in material:
            return price
    
    return category_data.get('default', 499)

@app.post("/api/create-product")
async def create_product(
    images: list[UploadFile] = File(...),
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    price: str = Form(...),
    original_price: str = Form(None),
    material: str = Form(None),
    dimensions: str = Form(None),
    artisan_name: str = Form(...),
    artisan_region: str = Form(...),
    whatsapp_number: str = Form(...)
):
    try:
        # Analyze product with AI
        ai_analysis = analyze_product_with_ai(title, description, category)
        
        # Process images
        image_urls = []
        for image in images:
            temp_path = f"temp_{uuid.uuid4().hex}.jpg"
            content = await image.read()
            with open(temp_path, "wb") as f:
                f.write(content)
            urls = remove_bg_and_upload(temp_path)
            image_urls.extend(urls)
            os.remove(temp_path)
        
        # Create product data
        product_id = str(uuid.uuid4())
        product_data = {
            "id": product_id,
            "title": title,
            "description": ai_analysis["enhanced_description"],
            "price": int(price),
            "original_price": int(original_price) if original_price else None,
            "images": image_urls[:4],  # Limit to 4 images
            "category": category,
            "artisan_id": f"artisan_{whatsapp_number.replace('+', '').replace(' ', '_')}",
            "artisan_name": artisan_name,
            "artisan_region": artisan_region,
            "material": material,
            "dimensions": dimensions,
            "rating": round(4.5 + (uuid.uuid4().int % 5) / 10, 1),  # Random 4.5-5.0
            "reviews_count": uuid.uuid4().int % 25,
            "orders_completed": uuid.uuid4().int % 50,
            "in_stock": True,
            "tags": ai_analysis["tags"],
            "features": ai_analysis["features"],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "whatsapp_number": whatsapp_number
        }
        
        # Update products.json
        products_file = "../shop/out/products.json"
        if os.path.exists(products_file):
            with open(products_file, "r") as f:
                data = json.load(f)
        else:
            data = {"products": []}
        
        data["products"].append(product_data)
        data["products"] = data["products"][-50:]  # Keep last 50 products
        
        with open(products_file, "w") as f:
            json.dump(data, f, indent=2)
        
        # Create product page
        shop_url = build_and_host(product_id, product_data['description'], product_data['images'])
        
        return {
            "success": True,
            "message": "Product created successfully!",
            "product_url": shop_url,
            "product_id": product_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002, log_level="info")