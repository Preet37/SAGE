import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  basePath: process.env.NEXT_PUBLIC_BASE_PATH || "",
  // Allow @mlc-ai/web-llm WASM assets to be served and not bundled
  webpack(config, { isServer }) {
    if (!isServer) {
      config.experiments = { ...config.experiments, asyncWebAssembly: true };
    }
    // Treat web-llm as external so webpack doesn't try to bundle its WASM
    config.externals = [
      ...(Array.isArray(config.externals) ? config.externals : []),
      ({ request }: { request?: string }, callback: (err?: Error | null, result?: string) => void) => {
        if (request && request.startsWith("@mlc-ai/web-llm")) {
          return callback(undefined, `commonjs ${request}`);
        }
        callback();
      },
    ];
    return config;
  },
};

export default nextConfig;
