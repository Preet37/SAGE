import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  basePath: process.env.NEXT_PUBLIC_BASE_PATH || "",
  // Turbopack handles WASM natively in Next.js 16
  turbopack: {},
};

export default nextConfig;
