# Development Dockerfile for BizOSaaS Admin
FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copy source code
COPY . .

# Create nextjs user with proper permissions
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs && \
    chown -R nextjs:nodejs /app && \
    mkdir -p /app/.next && \
    chown -R nextjs:nodejs /app/.next

USER nextjs

# Expose port
EXPOSE 3009

# Set environment
ENV NODE_ENV=development
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3009
ENV HOSTNAME=0.0.0.0

# Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://0.0.0.0:3009/ || exit 1

# Start development server
CMD ["npm", "run", "dev"]
