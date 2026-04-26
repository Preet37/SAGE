/** @type {import('next').NextConfig} */
const nextConfig = {
  // "standalone" is for Docker/self-hosted. Vercel uses its own output format.
  ...(process.env.VERCEL ? {} : { output: "standalone" }),
  basePath: process.env.NEXT_PUBLIC_BASE_PATH || "",
  turbopack: {},
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "img.youtube.com" },
      { protocol: "https", hostname: "i.ytimg.com" },
      { protocol: "https", hostname: "**.github.io" },
      { protocol: "https", hostname: "**.wikipedia.org" },
    ],
  },
};

export default nextConfig;
