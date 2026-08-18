/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Required for the multi-stage Dockerfile, which copies .next/standalone
  // into a slim runtime image instead of shipping node_modules.
  output: "standalone",
};

module.exports = nextConfig;
