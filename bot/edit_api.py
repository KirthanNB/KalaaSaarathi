from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import uuid
import aiofiles

app = FastAPI()

# Enable CORS for web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://neethi-saarathi-ids.web.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import image helper with fallback
try:
    from imagen_helper import remove_bg_and_upload
    IMAGEN_AVAILABLE = True
except:
    IMAGEN_AVAILABLE = False
    def remove_bg_and_upload(local_path: str) -> list:
        return [f"https://storage.googleapis.com/craftlink-images/fallback{i}.jpg?t={uuid.uuid4().hex[:8]}" for i in range(1, 5)]

@app.post("/api/edit-product")
async def edit_product(
    product_id: str = Form(...),
    price: str = Form(None),
    description: str = Form(None),
    image: UploadFile = File(None)
):
    try:
        # Load products
        products_file = "../shop/out/products.json"
        
        # Read existing products or create empty array
        if os.path.exists(products_file):
            try:
                async with aiofiles.open(products_file, "r") as f:
                    content = await f.read()
                    data = json.loads(content)
            except json.JSONDecodeError:
                data = {"products": []}
        else:
            data = {"products": []}
        
        # Find product
        product = None
        for p in data["products"]:
            if p["id"] == product_id:
                product = p
                break
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Update fields
        updated = False
        if price and price.isdigit():
            product["price"] = int(price)
            updated = True
        
        if description:
            product["description"] = description
            updated = True
        
        if image:
            # Save and process new image
            image_content = await image.read()
            temp_path = f"temp_{uuid.uuid4().hex}.jpg"
            
            async with aiofiles.open(temp_path, "wb") as f:
                await f.write(image_content)
            
            new_images = remove_bg_and_upload(temp_path)
            product["images"] = new_images
            os.remove(temp_path)
            updated = True
        
        if updated:
            # Save updated products
            async with aiofiles.open(products_file, "w") as f:
                await f.write(json.dumps(data, indent=2))
            
            return {
                "success": True,
                "message": "Product updated successfully",
                "product": {
                    "id": product_id,
                    "title": product.get("title", "Handmade Craft"),
                    "price": product.get("price", 350),
                    "description": product.get("description", ""),
                    "shop_url": f"https://neethi-saarathi-ids.web.app/product/{product_id}.html"
                }
            }
        else:
            return {
                "success": False,
                "message": "No changes were made"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")

@app.get("/api/products/{product_id}")
async def get_product_api(product_id: str):
    try:
        products_file = "../shop/out/products.json"
        if not os.path.exists(products_file):
            raise HTTPException(status_code=404, detail="Product not found")
        
        async with aiofiles.open(products_file, "r") as f:
            content = await f.read()
            data = json.loads(content)
        
        for product in data.get("products", []):
            if product.get("id") == product_id:
                return {
                    "success": True,
                    "product": product
                }
        
        raise HTTPException(status_code=404, detail="Product not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching product: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")