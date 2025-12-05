# Development Dockerfile for CorelDove Frontend
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
EXPOSE 3002

# Set environment
ENV NODE_ENV=development
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3002
ENV NEXT_PUBLIC_API_BASE_URL=http://localhost:8005

# Start development server
CMD ["npm", "run", "dev", "--", "--port", "3002"]
