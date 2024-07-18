/** @type {import('next').NextConfig} */
const cloudFrontUrl = process.env.NEXT_PUBLIC_CLOUDFRONT_URL;
const filePath = process.env.NEXT_PUBLIC_FILE_UPLOAD_FOLDER;
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: cloudFrontUrl,
        port: '',
        pathname: `/${filePath}/**`,
      },
    ],
  },
  reactStrictMode: false,
};

export default nextConfig;