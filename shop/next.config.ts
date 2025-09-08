// next.config.js
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',       // ← enables static export
  distDir: 'out',         // ← optional, default is '.next'
  reactStrictMode: true,  // optional, recommended
};

export default nextConfig;
