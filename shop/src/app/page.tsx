'use client'
import React, { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";

interface Product {
  id: string;
  title: string;
  description: string;
  price: number;
  images: string[];
  created_at: string;
}

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        // Fetch from public JSON file (updated by deploy script)
        const response = await fetch('/products.json?t=' + Date.now());
        if (!response.ok) throw new Error('Failed to fetch products');
        
        const data = await response.json();
        setProducts(data.products || []);
      } catch (err) {
        setError('Failed to load products');
        setProducts([]);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
    
    // Refresh every 30 seconds
    const interval = setInterval(fetchProducts, 30000);
    return () => clearInterval(interval);
  }, []);

  const totalProducts = products.length;
  const totalArtisans = new Set(products.map(p => p.id.slice(0, 8))).size;

  if (loading) {
    return (
      <main className="p-8 min-h-screen bg-gradient-to-b from-orange-50 to-white">
        <div className="max-w-6xl mx-auto text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600 mx-auto mb-4"></div>
          <p>Loading marketplace...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="p-8 min-h-screen bg-gradient-to-b from-orange-50 to-white">
      <div className="max-w-6xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-orange-800 mb-2">
            CraftLink Marketplace
          </h1>
          <p className="text-gray-600">
            Discover {totalProducts} handmade treasures from {totalArtisans} local artisans
          </p>
        </header>

        {error && (
          <div className="bg-red-50 p-4 rounded-lg mb-8 text-center">
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {/* Products Grid */}
        {products.length > 0 ? (
          <div className="mb-12">
            <h2 className="text-2xl font-semibold mb-6">Recently Created Products</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {products.map((product) => (
                <Link key={product.id} href={`/product/${product.id}.html`}>
                  <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer">
                    <div className="relative h-48 bg-gray-200">
                      <Image
                        src={product.images[0] || "/fallback1.jpg"}
                        fill
                        className="object-cover"
                        alt={product.title}
                      />
                    </div>
                    <div className="p-4">
                      <h3 className="font-semibold text-lg mb-2 line-clamp-2">{product.title}</h3>
                      <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                        {product.description.replace(/<br>/g, ' ').substring(0, 100)}...
                      </p>
                      <div className="flex justify-between items-center">
                        <span className="text-green-600 font-semibold">₹{product.price}</span>
                        <span className="text-xs text-gray-500">#{product.id.slice(0, 6)}</span>
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        ) : (
          <div className="bg-yellow-50 p-8 rounded-lg text-center mb-8">
            <h2 className="text-2xl font-semibold mb-4">No Products Yet</h2>
            <p className="text-gray-600 mb-4">Be the first to create a beautiful craft listing!</p>
          </div>
        )}

        {/* How It Works */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-semibold mb-6">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <span className="text-2xl">📸</span>
              </div>
              <h3 className="font-semibold mb-2">1. Send Photo</h3>
              <p className="text-gray-600 text-sm">WhatsApp a photo of your craft</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <span className="text-2xl">🛍️</span>
              </div>
              <h3 className="font-semibold mb-2">2. Get Online Shop</h3>
              <p className="text-gray-600 text-sm">AI creates your product page instantly</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <span className="text-2xl">📦</span>
              </div>
              <h3 className="font-semibold mb-2">3. Sell & Ship</h3>
              <p className="text-gray-600 text-sm">We handle payments and shipping</p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center">
          <p className="text-gray-600 mb-4">Ready to sell your crafts?</p>
          <a 
            href="https://wa.me/14155238886?text=Hi%20CraftLink"
            className="bg-green-500 text-white px-6 py-3 rounded-full font-semibold inline-flex items-center hover:bg-green-600 transition-colors"
          >
            <span className="mr-2">💬</span>
            Start on WhatsApp
          </a>
        </div>
      </div>
    </main>
  );
}
