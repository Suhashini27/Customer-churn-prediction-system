/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
        return [
            {
                source: '/api/fastapi/:path*',
                destination: 'http://localhost:8000/:path*' // Proxy to Backend
            }
        ]
    }
}

module.exports = nextConfig