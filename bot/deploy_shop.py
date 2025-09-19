import subprocess
import os
import json
import uuid
from datetime import datetime

def build_and_host(product_id: str, description: str, image_urls: list, title: str = None, price: int = None) -> str:
    """Create HTML product page with enhanced design"""
    try:
        shop_dir = "../shop"
        product_dir = f"{shop_dir}/out/product"
        
        # Ensure product directory exists
        os.makedirs(product_dir, exist_ok=True)
        
        # Load product data to get all details
        products_file = f"{shop_dir}/out/products.json"
        product_data = None
        
        if os.path.exists(products_file):
            with open(products_file, "r") as f:
                data = json.load(f)
                for product in data.get("products", []):
                    if product.get("id") == product_id:
                        product_data = product
                        break
        
        # Use fallback if product data not found
        if not product_data:
            product_data = {
                "id": product_id,
                "title": title or f"Handmade Craft #{product_id[:6]}",
                "description": description,
                "price": price or 350,
                "images": image_urls,
                "category": "handmade",
                "artisan_name": "Local Artisan",
                "artisan_region": "India"
            }
        
        # Create enhanced HTML product page
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
        
        .product-image {{
            transition: transform 0.3s ease;
        }}
        
        .product-image:hover {{
            transform: scale(1.05);
        }}
        
        .image-gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        
        .main-image {{
            grid-column: 1 / -1;
            height: 300px;
            object-fit: cover;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .thumbnail {{
            height: 100px;
            object-fit: cover;
            border-radius: 8px;
            cursor: pointer;
            transition: opacity 0.3s ease;
        }}
        
        .thumbnail:hover {{
            opacity: 0.8;
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
                    <div class="image-gallery">
                        <img src="{image_urls[0]}" id="mainImage" class="main-image product-image" alt="{product_data['title']}">
                        <div class="grid grid-cols-4 gap-2">
                            {"".join([f'<img src="{url}" class="thumbnail" onclick="changeImage(this.src)" alt="Product image {i+1}">' for i, url in enumerate(image_urls[:4])])}
                        </div>
                    </div>
                </div>

                <!-- Details -->
                <div class="p-8 bg-amber-50">
                    <h1 class="text-3xl font-bold text-amber-800 mb-4">{product_data['title']}</h1>
                    
                    <div class="bg-white p-6 rounded-lg mb-6">
                        <div class="flex items-center mb-4">
                            <div class="flex items-center text-amber-400">
                                {"".join(['<i class="fas fa-star"></i>' for _ in range(5)])}
                                <span class="ml-2 text-gray-600">({product_data.get('reviews_count', 12)} reviews)</span>
                            </div>
                        </div>
                        
                        <p class="text-gray-700 text-lg leading-relaxed mb-4">{product_data['description']}</p>
                        
                        <div class="grid grid-cols-2 gap-4 mb-4">
                            <div>
                                <span class="text-sm text-gray-500">Category</span>
                                <p class="font-semibold">{product_data.get('category', 'Handmade').title()}</p>
                            </div>
                            <div>
                                <span class="text-sm text-gray-500">Material</span>
                                <p class="font-semibold">{product_data.get('material', 'Natural Materials')}</p>
                            </div>
                        </div>
                        
                        <div class="flex items-center justify-between mt-6">
                            <div>
                                <span class="text-3xl font-bold text-amber-600">₹{product_data['price']}</span>
                                {f'<span class="ml-2 text-sm text-gray-500 line-through">₹{product_data.get("original_price", product_data["price"] + 100)}</span>' if product_data.get('original_price') else ''}
                            </div>
                            <span class="px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-sm">Handmade</span>
                        </div>
                    </div>

                    <!-- Artisan Info -->
                    <div class="bg-amber-100 p-4 rounded-lg mb-6">
                        <h3 class="text-lg font-semibold text-amber-800 mb-2">Crafted by Artisan</h3>
                        <p class="text-amber-700">{product_data.get('artisan_name', 'Local Artisan')} from {product_data.get('artisan_region', 'India')}</p>
                        <p class="text-sm text-amber-600 mt-1">{product_data.get('orders_completed', 25)} orders completed • {product_data.get('rating', 4.8)}/5 rating</p>
                    </div>

                    <!-- Action Box -->
                    <div class="bg-green-50 p-6 rounded-lg">
                        <h3 class="text-lg font-semibold text-green-800 mb-3">How to Purchase</h3>
                        <p class="text-green-700 mb-4">Contact us directly on WhatsApp to own this beautiful handmade piece</p>
                        <a href="https://wa.me/14155238886?text=I%20want%20to%20buy%20{product_data['id']}" 
                        class="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-semibold inline-flex items-center space-x-2 transition-colors w-full justify-center">
                            <i class="fab fa-whatsapp text-xl"></i>
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

    <script>
        function changeImage(src) {{
            document.getElementById('mainImage').src = src;
        }}
    </script>
</body>
</html>'''
        
        # Save HTML file
        html_file = f"{product_dir}/{product_id}.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"✅ Created HTML: {html_file}")
        
        return f"https://neethi-saarathi-ids.web.app/product/{product_id}.html"
        
    except Exception as e:
        print(f"Error: {e}")
        return f"https://neethi-saarathi-ids.web.app/product/{product_id}.html"

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

        # Keep only recent 50 products
        data["products"] = data["products"][-50:]

        # Write back
        with open(products_file, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✅ Updated products.json with {len(data['products'])} products")

    except Exception as e:
        print(f"❌ Failed to update products.json: {e}")
        # Create basic products.json if it doesn't exist
        with open(products_file, "w") as f:
            json.dump({"products": [product_data]}, f, indent=2)

def get_all_products():
    """Get all products from products.json"""
    try:
        shop_dir = "../shop/out"
        products_file = f"{shop_dir}/products.json"
        
        if os.path.exists(products_file):
            with open(products_file, "r") as f:
                data = json.load(f)
                return data.get("products", [])
        return []
    except:
        return []

def get_product_by_id(product_id):
    """Get a specific product by ID"""
    products = get_all_products()
    for product in products:
        if product.get("id") == product_id:
            return product
    return None

def update_seller_profile(phone, profile_data):
    """Update seller profile"""
    try:
        shop_dir = "../shop/out"
        sellers_file = f"{shop_dir}/sellers.json"

        # Read existing sellers or create empty array
        if os.path.exists(sellers_file):
            try:
                with open(sellers_file, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {"sellers": []}
        else:
            data = {"sellers": []}

        # Add or update seller profile
        updated = False
        for i, seller in enumerate(data["sellers"]):
            if seller.get("phone") == phone:
                data["sellers"][i] = {**seller, **profile_data}
                updated = True
                break
        
        if not updated:
            data["sellers"].append(profile_data)

        # Write back
        with open(sellers_file, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✅ Updated sellers.json for {phone}")

    except Exception as e:
        print(f"❌ Failed to update sellers.json: {e}")

def get_seller_profile(phone):
    """Get seller profile by phone number"""
    try:
        shop_dir = "../shop/out"
        sellers_file = f"{shop_dir}/sellers.json"
        
        if os.path.exists(sellers_file):
            with open(sellers_file, "r") as f:
                data = json.load(f)
                for seller in data.get("sellers", []):
                    if seller.get("phone") == phone:
                        return seller
        return None
    except:
        return None

def add_reel(reel_data):
    """Add a new reel"""
    try:
        shop_dir = "../shop/out"
        reels_file = f"{shop_dir}/reels.json"

        # Read existing reels or create empty array
        if os.path.exists(reels_file):
            try:
                with open(reels_file, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {"reels": []}
        else:
            data = {"reels": []}

        # Add new reel
        data["reels"].append(reel_data)

        # Keep only recent 100 reels
        data["reels"] = data["reels"][-100:]

        # Write back
        with open(reels_file, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✅ Added reel to reels.json")

    except Exception as e:
        print(f"❌ Failed to update reels.json: {e}")

def get_all_reels():
    """Get all reels"""
    try:
        shop_dir = "../shop/out"
        reels_file = f"{shop_dir}/reels.json"
        
        if os.path.exists(reels_file):
            with open(reels_file, "r") as f:
                data = json.load(f)
                return data.get("reels", [])
        return []
    except:
        return []

def create_seller_pages():
    """Create HTML pages for each seller"""
    try:
        shop_dir = "../shop/out"
        sellers_file = f"{shop_dir}/sellers.json"
        products_file = f"{shop_dir}/products.json"
        
        if not os.path.exists(sellers_file):
            return
        
        with open(sellers_file, "r") as f:
            sellers = json.load(f).get("sellers", [])
        
        with open(products_file, "r") as f:
            all_products = json.load(f).get("products", [])
        
        for seller in sellers:
            seller_phone = seller.get("phone")
            if not seller_phone:
                continue
                
            # Get seller's products
            seller_products = [p for p in all_products if p.get("artisan_phone") == seller_phone]
            
            # Create seller page HTML
            html_content = f'''<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{seller.get('name', 'Artisan')} - KalaaSaarathi</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Hind:wght@400;500;600&display=swap');
        
        body {{
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #fff5e6 0%, #ffecc7 100%);
        }}
    </style>
</head>
<body class="min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <a href="/" class="text-amber-600 hover:text-amber-700 font-semibold flex items-center mb-6">
            <i class="fas fa-arrow-left mr-2"></i> Back to KalaaSaarathi
        </a>
        
        <div class="bg-white rounded-2xl shadow-xl p-6 mb-6">
            <div class="flex items-center space-x-6">
                <img src="{seller.get('profile_image', 'https://storage.googleapis.com/craftlink-images/fallback1.jpg')}" 
                     alt="{seller.get('name')}" class="w-32 h-32 rounded-full object-cover border-4 border-amber-100">
                <div class="flex-1">
                    <h1 class="text-3xl font-bold text-amber-800 mb-2">{seller.get('name', 'Artisan')}</h1>
                    <p class="text-amber-600 text-lg mb-3">{seller.get('region', 'India')}</p>
                    <p class="text-gray-700 mb-4">{seller.get('bio', 'Talented artisan creating beautiful handmade crafts.')}</p>
                    <div class="flex flex-wrap gap-2">
                        {''.join([f'<span class="inline-block bg-amber-100 text-amber-700 px-3 py-1 rounded-full text-sm">{skill}</span>' for skill in seller.get('skills', [])])}
                    </div>
                </div>
            </div>
        </div>

        <h2 class="text-2xl font-bold text-amber-800 mb-6">Products by this Artisan</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
'''

            # Add seller's products
            for product in seller_products[:9]:  # Show first 9 products
                html_content += f'''
            <div class="bg-white rounded-xl shadow-md overflow-hidden product-card" data-category="{product.get('category', 'handmade')}">
                <img src="{product['images'][0]}" alt="{product['title']}" class="w-full h-48 object-cover">
                <div class="p-4">
                    <h3 class="font-semibold text-lg mb-2">{product['title'][:40]}{'...' if len(product['title']) > 40 else ''}</h3>
                    <p class="text-gray-600 text-sm mb-3">{product['description'][:70]}{'...' if len(product['description']) > 70 else ''}</p>
                    <div class="flex items-center justify-between">
                        <span class="text-amber-600 font-bold">₹{product['price']}</span>
                        <a href="/product/{product['id']}.html" class="text-amber-500 hover:text-amber-600">View →</a>
                    </div>
                </div>
            </div>
'''

            html_content += '''
        </div>
        
        <div class="text-center">
            <a href="/" class="inline-block bg-amber-500 text-white px-6 py-2 rounded-lg font-semibold">
                <i class="fas fa-arrow-left mr-2"></i>Back to Home
            </a>
        </div>
    </div>
</body>
</html>'''
            
            # Save seller page
            seller_dir = f"{shop_dir}/seller"
            os.makedirs(seller_dir, exist_ok=True)
            with open(f"{seller_dir}/{seller_phone}.html", "w", encoding="utf-8") as f:
                f.write(html_content)
        
        print("✅ Created seller profile pages")
        
    except Exception as e:
        print(f"❌ Error creating seller pages: {e}")

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

# Create a complete shop index with products, sellers, and reels
def create_shop_index():
    """Create the main shop index page with all products, sellers, and reels"""
    try:
        shop_dir = "../shop/out"
        products = get_all_products()
        reels = get_all_reels()
        
        html_content = '''<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KalaaSaarathi - Handmade Crafts Marketplace</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Hind:wght@400;500;600&display=swap');
        
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #fff5e6 0%, #ffecc7 100%);
        }
        
        .hindi-font {
            font-family: 'Hind', 'Noto Sans Devanagari', sans-serif;
        }
        
        .artisan-pattern {
            background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M50 50L100 0H0L50 50Z' fill='%23d97706' fill-opacity='0.05'/%3E%3C/svg%3E");
        }
        
        .product-card {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }
        
        .reel-card {
            transition: transform 0.3s ease;
        }
        
        .reel-card:hover {
            transform: scale(1.02);
        }
        
        .seller-card {
            transition: all 0.3s ease;
        }
        
        .seller-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body class="min-h-screen artisan-pattern">
    <div class="container mx-auto px-4 py-8">
        <!-- Header -->
        <div class="flex items-center justify-between mb-8">
            <div class="flex items-center space-x-2">
                <div class="w-10 h-10 bg-amber-500 rounded-full flex items-center justify-center">
                    <i class="fas fa-hands text-white"></i>
                </div>
                <span class="text-2xl font-bold text-amber-800">KalaaSaarathi</span>
            </div>
            <div class="flex items-center space-x-4">
                <a href="#products" class="text-amber-600 hover:text-amber-700">Products</a>
                <a href="#sellers" class="text-amber-600 hover:text-amber-700">Artisans</a>
                <a href="#reels" class="text-amber-600 hover:text-amber-700">Reels</a>
                <a href="https://wa.me/14155238886" class="bg-green-600 text-white px-4 py-2 rounded-lg">
                    <i class="fab fa-whatsapp mr-2"></i> WhatsApp Us
                </a>
            </div>
        </div>

        <!-- Hero Section -->
        <div class="bg-white rounded-2xl shadow-lg p-8 mb-12 text-center">
            <h1 class="text-4xl font-bold text-amber-800 mb-4">Handmade Crafts Marketplace</h1>
            <p class="text-gray-600 text-lg mb-6">Discover unique handmade creations from talented artisans across India</p>
            
            <!-- Search Bar -->
            <div class="max-w-md mx-auto mb-6">
                <div class="relative">
                    <input type="text" id="searchInput" placeholder="Search products..." class="w-full px-4 py-2 border border-amber-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500">
                    <button onclick="searchProducts()" class="absolute right-2 top-2 text-amber-600">
                        <i class="fas fa-search"></i>
                    </button>
                </div>
            </div>
            
            <!-- Category Filters -->
            <div class="flex flex-wrap justify-center gap-2 mb-6">
'''

        # Category buttons
        categories = [
            "all", "pottery", "textiles", "jewelry", "paintings", 
            "wooden", "metalwork", "leather", "papercraft", "home-decor", "accessories"
        ]
        
        for category in categories:
            display_name = "All" if category == "all" else category.title()
            btn_class = "bg-amber-500 text-white" if category == "all" else "bg-amber-100 text-amber-700"
            html_content += f'''
                <button onclick="filterByCategory('{category}')" 
                        class="category-btn px-3 py-1 rounded-full text-sm {btn_class}" 
                        data-category="{category}">
                    {display_name}
                </button>
'''

        html_content += '''
            </div>
            
            <div class="flex justify-center space-x-4">
                <a href="#products" class="bg-amber-500 text-white px-6 py-3 rounded-lg font-semibold">Browse Products</a>
                <a href="https://wa.me/14155238886" class="border border-amber-500 text-amber-500 px-6 py-3 rounded-lg font-semibold">Become a Seller</a>
            </div>
        </div>

        <!-- Reels Section -->
        <h2 id="reels" class="text-3xl font-bold text-amber-800 mb-8 text-center">Featured Reels</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12" id="reelsContainer">
'''

        # Add reel cards (show latest 6 reels)
        for reel in reels[-6:]:
            html_content += f'''
            <div class="reel-card bg-white rounded-xl shadow-md overflow-hidden">
                <video src="{reel['video_url']}" class="w-full h-48 object-cover" controls></video>
                <div class="p-4">
                    <p class="text-gray-700 mb-2">{reel['caption']}</p>
                    <div class="flex items-center justify-between text-sm text-gray-500">
                        <span>By {reel['seller_name']}</span>
                        <div class="flex items-center space-x-3">
                            <span><i class="fas fa-heart text-red-500"></i> {reel.get('likes', 0)}</span>
                            <span><i class="fas fa-comment text-blue-500"></i> {reel.get('comments', 0)}</span>
                        </div>
                    </div>
                </div>
            </div>
'''

        html_content += '''
        </div>

        <!-- Products Grid -->
        <h2 id="products" class="text-3xl font-bold text-amber-800 mb-8 text-center">Featured Products</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-12" id="productsContainer">
'''

        # Add product cards (show latest 12 products)
        for product in products[-12:]:
            html_content += f'''
            <div class="product-card bg-white rounded-xl shadow-md overflow-hidden" data-category="{product.get('category', 'handmade')}">
                <img src="{product['images'][0]}" alt="{product['title']}" class="w-full h-48 object-cover">
                <div class="p-4">
                    <h3 class="font-semibold text-lg mb-2">{product['title'][:50]}{'...' if len(product['title']) > 50 else ''}</h3>
                    <p class="text-gray-600 text-sm mb-3">{product['description'][:80]}{'...' if len(product['description']) > 80 else ''}</p>
                    <div class="flex items-center justify-between">
                        <span class="text-amber-600 font-bold">₹{product['price']}</span>
                        <a href="/product/{product['id']}.html" class="text-amber-500 hover:text-amber-600">View →</a>
                    </div>
                </div>
            </div>
'''

        html_content += '''
        </div>

        <!-- No results message -->
        <div id="noResults" class="text-center py-8 hidden">
            <p class="text-gray-500 text-lg mb-4">No products found matching your search.</p>
            <button onclick="filterByCategory('all'); document.getElementById('searchInput').value = ''; searchProducts();" 
                    class="px-4 py-2 bg-amber-500 text-white rounded-lg font-semibold">
                Show All Products
            </button>
        </div>

        <!-- Sellers Section -->
        <h2 id="sellers" class="text-3xl font-bold text-amber-800 mb-8 text-center">Featured Artisans</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
'''

        # Get unique sellers from products
        sellers = {}
        for product in products:
            phone = product.get('artisan_phone')
            if phone and phone not in sellers:
                sellers[phone] = {
                    'name': product.get('artisan_name', 'Local Artisan'),
                    'region': product.get('artisan_region', 'India'),
                    'products_count': 1,
                    'image': product.get('images', [])[0] if product.get('images') else 'https://storage.googleapis.com/craftlink-images/fallback1.jpg'
                }
            elif phone:
                sellers[phone]['products_count'] += 1

        # Add seller cards (show up to 6 sellers)
        for i, (phone, seller) in enumerate(list(sellers.items())[:6]):
            html_content += f'''
            <div class="seller-card bg-white rounded-xl shadow-md overflow-hidden">
                <img src="{seller['image']}" alt="{seller['name']}" class="w-full h-48 object-cover">
                <div class="p-4">
                    <h3 class="font-semibold text-lg mb-1">{seller['name']}</h3>
                    <p class="text-gray-600 text-sm mb-2">{seller['region']}</p>
                    <div class="flex items-center justify-between">
                        <span class="text-amber-600 text-sm">{seller['products_count']} products</span>
                        <a href="/seller/{phone}.html" class="text-amber-500 hover:text-amber-600 text-sm">View Profile →</a>
                    </div>
                </div>
            </div>
'''

        html_content += '''
        </div>

        <!-- Footer -->
        <div class="text-center text-gray-600 mt-12">
            <p>© 2023 KalaaSaarathi. All rights reserved.</p>
            <p class="text-sm mt-2">Supporting Indian artisans one craft at a time</p>
        </div>
    </div>

    <script>
        let currentCategory = 'all';
        
        function searchProducts() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const products = document.querySelectorAll('.product-card');
            let visibleCount = 0;
            
            products.forEach(product => {
                const title = product.querySelector('h3').textContent.toLowerCase();
                const description = product.querySelector('p').textContent.toLowerCase();
                const category = product.getAttribute('data-category');
                
                if ((title.includes(searchTerm) || description.includes(searchTerm)) && 
                    (currentCategory === 'all' || category === currentCategory)) {
                    product.style.display = 'block';
                    visibleCount++;
                } else {
                    product.style.display = 'none';
                }
            });
            
            // Show message if no products found
            const noResults = document.getElementById('noResults');
            if (visibleCount === 0) {
                noResults.style.display = 'block';
            } else {
                noResults.style.display = 'none';
            }
        }
        
        function filterByCategory(category) {
            currentCategory = category;
            searchProducts(); // This will apply both category filter and search term
            
            // Update active category button
            document.querySelectorAll('.category-btn').forEach(btn => {
                if (btn.getAttribute('data-category') === category) {
                    btn.classList.add('bg-amber-500', 'text-white');
                    btn.classList.remove('bg-amber-100', 'text-amber-700');
                } else {
                    btn.classList.remove('bg-amber-500', 'text-white');
                    btn.classList.add('bg-amber-100', 'text-amber-700');
                }
            });
        }
        
        // Make search work on Enter key
        document.getElementById('searchInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchProducts();
            }
        });
        
        // Initialize with all products shown
        filterByCategory('all');
    </script>
</body>
</html>'''

        # Save index.html
        index_file = f"{shop_dir}/index.html"
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        # Create seller pages
        create_seller_pages()
        
        print("✅ Created shop index.html with search, categories, products, reels, and sellers")
        
    except Exception as e:
        print(f"❌ Error creating index.html: {e}")

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
    # Create shop index when this module is run directly
    create_shop_index()
    test_deployment()