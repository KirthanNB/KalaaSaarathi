import subprocess
import os
import json
import uuid
from datetime import datetime

def build_and_host(product_id: str, description: str, image_urls: list) -> str:
    """Create HTML product page"""
    try:
        shop_dir = "../shop"
        product_dir = f"{shop_dir}/out/product"
        
        # Ensure product directory exists
        os.makedirs(product_dir, exist_ok=True)
        
        # Create HTML product page
        # In build_and_host function, update the HTML template:
        html_content = f'''<!DOCTYPE html>
        <html lang="hi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{product_data['title']} - KalaaSaarathi</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Hind:wght@400;500;600&display=swap');
                
                body {{
                    font-family: 'Poppins', sans-serif;
                    background: linear-gradient(135deg, #fff5e6 0%, #ffecc7 100%);
                }}
                
                .hindi-font {{
                    font-family: 'Hind', 'Noto Sans Devanagari', sans-serif;
                }}
                
                .artisan-pattern {{
                    background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M50 50L100 0H0L50 50Z' fill='%23d97706' fill-opacity='0.05'/%3E%3C/svg%3E");
                }}
            </style>
        </head>
        <body class="min-h-screen artisan-pattern">
            <div class="container mx-auto px-4 py-8 max-w-6xl">
                <!-- Header -->
                <div class="flex items-center justify-between mb-8">
                    <a href="/" class="text-amber-600 hover:text-amber-700 font-semibold flex items-center">
                        <i class="fas fa-arrow-left mr-2"></i> Back to KalaaSaarathi
                    </a>
                    <div class="flex items-center space-x-2">
                        <div class="w-8 h-8 bg-amber-500 rounded-full flex items-center justify-center">
                            <i class="fas fa-hands text-white text-sm"></i>
                        </div>
                        <span class="text-amber-800 font-semibold">KalaaSaarathi</span>
                    </div>
                </div>

                <!-- Product Content -->
                <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
                    <div class="grid grid-cols-1 lg:grid-cols-2">
                        <!-- Images -->
                        <div class="p-6">
                            <div class="grid grid-cols-2 gap-4">
                                <img src="{image_urls[0]}" class="w-full h-48 object-cover rounded-lg shadow-md" alt="Product image">
                                <img src="{image_urls[1] if len(image_urls) > 1 else image_urls[0]}" class="w-full h-48 object-cover rounded-lg shadow-md" alt="Product image">
                            </div>
                        </div>

                        <!-- Details -->
                        <div class="p-8 bg-amber-50">
                            <h1 class="text-3xl font-bold text-amber-800 mb-4">{product_data['title']}</h1>
                            
                            <div class="bg-white p-6 rounded-lg mb-6">
                                <p class="text-gray-700 text-lg leading-relaxed">{description.replace('*', '')}</p>
                                <div class="flex items-center mt-6">
                                    <span class="text-3xl font-bold text-amber-600">₹{product_data['price']}</span>
                                    <span class="ml-4 px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-sm">Handmade</span>
                                </div>
                            </div>

                            <!-- Action Box -->
                            <div class="bg-amber-100 p-6 rounded-lg">
                                <h3 class="text-lg font-semibold text-amber-800 mb-3">How to Purchase</h3>
                                <p class="text-amber-700 mb-4">Contact us directly on WhatsApp to own this beautiful handmade piece</p>
                                <a href="https://wa.me/14155238886?text=I%20want%20to%20buy%20{product_data['id']}" 
                                class="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-semibold inline-flex items-center space-x-2 transition-colors">
                                    <i class="fab fa-whatsapp"></i>
                                    <span>Buy on WhatsApp</span>
                                </a>
                            </div>

                            <!-- Artisan Support -->
                            <div class="mt-6 bg-white p-4 rounded-lg">
                                <div class="flex items-center space-x-3">
                                    <div class="w-10 h-10 bg-amber-100 rounded-full flex items-center justify-center">
                                        <i class="fas fa-hands-helping text-amber-600"></i>
                                    </div>
                                    <div>
                                        <p class="text-sm text-amber-700">90% of proceeds go directly to the artisan</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Product ID -->
                <div class="text-center mt-8">
                    <p class="text-sm text-amber-600">Product ID: {product_id}</p>
                </div>
            </div>
        </body>
        </html>'''
        
        # Save HTML file
        html_file = f"{product_dir}/{product_id}.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"✅ Created HTML: {html_file}")
        
        # Deploy to Firebase
        deploy_result = subprocess.run(
            f"cd {shop_dir} && firebase deploy --only hosting --non-interactive",
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if deploy_result.returncode == 0:
            print("✅ Deployment successful!")
        else:
            print(f"⚠️ Deployment issues: {deploy_result.stderr}")
        
        return f"https://neethi-saarathi-ids.web.app/product/{product_id}.html"
        
    except Exception as e:
        print(f"Error: {e}")
        return f"https://neethi-saarathi-ids.web.app/product/{product_id}.html"


def create_html_product_page(product_data):
    """Create HTML product page with edit instructions"""
    os.makedirs("out/product", exist_ok=True)
    desc = product_data['description'].replace('<br>', '\n')

    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>{product_data['title']}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 min-h-screen">
    <div class="container mx-auto px-4 py-8 max-w-4xl">
        <a href="/" class="text-blue-600 hover:text-blue-800 mb-4 inline-block">← Back to Home</a>
        
        <h1 class="text-3xl font-bold text-gray-800 mb-6">{product_data['title']}</h1>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <img src="{product_data['images'][0]}" class="rounded-lg shadow-md w-full h-48 object-cover">
            <img src="{product_data['images'][1] if len(product_data['images']) > 1 else product_data['images'][0]}" class="rounded-lg shadow-md w-full h-48 object-cover">
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow-md mb-6">
            <p class="text-gray-700 whitespace-pre-line">{desc}</p>
            <p class="text-2xl font-semibold text-green-600 mt-4">₹{product_data['price']}</p>
        </div>
        
        <div class="bg-blue-50 p-4 rounded-lg">
            <h2 class="text-xl font-semibold mb-2">How to Buy</h2>
            <p class="text-gray-600">WhatsApp us at +91-XXXXXX-XXXX to purchase this item</p>
        </div>

        <div class="bg-yellow-50 p-4 rounded-lg mt-6">
            <h2 class="text-xl font-semibold mb-2">Want to Edit?</h2>
            <p class="text-gray-600">WhatsApp us with: edit {product_data['id'][:8]} [price|description|image] + new value</p>
        </div>
    </div>
</body>
</html>'''

    with open(f"out/product/{product_data['id']}.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Created HTML: out/product/{product_data['id']}.html")


def update_static_products(product_data):
    """Update static products file"""
    static_file = "src/app/product/static_products.json"
    os.makedirs(os.path.dirname(static_file), exist_ok=True)

    products = []
    if os.path.exists(static_file):
        try:
            with open(static_file, "r") as f:
                for line in f:
                    if line.strip():
                        products.append(json.loads(line))
        except:
            products = []

    products = [p for p in products if p.get('id') != product_data['id']]
    products.append(product_data)

    with open(static_file, "w") as f:
        for p in products:
            f.write(json.dumps(p) + "\n")

    print(f"✅ Updated static products: {len(products)} items")


def update_public_products(product_data):
    """Update public products file"""
    public_file = "public/products.json"
    os.makedirs(os.path.dirname(public_file), exist_ok=True)

    if os.path.exists(public_file):
        try:
            with open(public_file, "r") as f:
                data = json.load(f)
        except:
            data = {"products": []}
    else:
        data = {"products": []}

    data["products"] = [p for p in data["products"] if p.get('id') != product_data['id']]
    data["products"].append(product_data)
    data["products"] = data["products"][-20:]  # Keep only recent 20

    with open(public_file, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Updated public products: {len(data['products'])} items")


def update_products_json(product_data):
    """Update the public products.json file"""
    try:
        shop_dir = "../shop/out"
        products_file = f"{shop_dir}/products.json"

        # Read existing products or create empty array
        if os.path.exists(products_file):
            try:
                with open(products_file, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {"products": []}
        else:
            data = {"products": []}

        # Add new product (or replace if exists)
        data["products"] = [p for p in data["products"] if p.get('id') != product_data['id']]
        data["products"].append(product_data)

        # Keep only recent 20 products
        data["products"] = data["products"][-20:]

        # Write back
        with open(products_file, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✅ Updated products.json with {len(data['products'])} products")

    except Exception as e:
        print(f"❌ Failed to update products.json: {e}")
        # Create basic products.json if it doesn't exist
        with open(products_file, "w") as f:
            json.dump({"products": [product_data]}, f, indent=2)


# Replace the deploy section with this:
# Replace the deploy section with this:
def deploy_to_firebase():
    """Deploy to Firebase Hosting with proper file handling"""
    try:
        print("🚀 Deploying to Firebase...")
        
        # Ensure all files are included
        result = subprocess.run(
            "cd ../shop && firebase deploy --only hosting --non-interactive",
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print("✅ Firebase deployment successful!")
            # Verify the files were deployed
            verify_deployment()
            return True
        else:
            print(f"❌ Firebase deployment failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Firebase deployment timed out")
        return False
    except Exception as e:
        print(f"❌ Firebase deployment error: {e}")
        return False

def verify_deployment():
    """Verify that product files were deployed"""
    try:
        # Check if product directory exists in deployment
        import requests
        test_url = "https://neethi-saarathi-ids.web.app/product/test.html"
        response = requests.head(test_url)
        
        if response.status_code == 404:
            print("⚠️ Product directory not deployed. Creating it...")
            # Create product directory and redeploy
            os.makedirs("../shop/out/product", exist_ok=True)
            # Create a test file to ensure directory is included
            with open("../shop/out/product/test.html", "w") as f:
                f.write("<!-- Test file to ensure product directory is deployed -->")
            
            # Redeploy
            subprocess.run(
                "cd ../shop && firebase deploy --only hosting --non-interactive",
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )
    except:
        pass


# Test function
def test_deployment():
    """Test the complete deployment"""
    print("Testing complete deployment...")

    product_id = str(uuid.uuid4())
    description = "Test product for automated deployment with edit feature"
    image_urls = [
        "https://storage.googleapis.com/craftlink-images/fallback1.jpg",
        "https://storage.googleapis.com/craftlink-images/fallback2.jpg"
    ]

    shop_url = build_and_host(product_id, description, image_urls)
    print(f"Final Shop URL: {shop_url}")
    return shop_url


if __name__ == "__main__":
    test_deployment()
