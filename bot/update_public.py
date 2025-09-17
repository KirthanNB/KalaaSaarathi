import json
import os

def update_public_products():
    """Force update public/products.json from static products"""
    try:
        # Read from static products
        with open('src/app/product/static_products.json', 'r') as f:
            static_products = [json.loads(line) for line in f if line.strip()]
        
        # Update public file
        public_data = {"products": static_products[-20:]}  # Last 20 products
        with open('public/products.json', 'w') as f:
            json.dump(public_data, f, indent=2)
        
        print(f"Updated public/products.json with {len(static_products)} products")
        return True
        
    except Exception as e:
        print(f"Error updating public file: {e}")
        return False

if __name__ == "__main__":
    update_public_products()