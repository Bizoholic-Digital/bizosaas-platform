# Optimized Development Dockerfile for Bizoholic Frontend
FROM node:20-alpine

WORKDIR /app

# Create nextjs user BEFORE copying files
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs && \
    chown nextjs:nodejs /app

# Switch to nextjs user
USER nextjs

# Install dependencies
COPY --chown=nextjs:nodejs package*.json ./
RUN npm install --legacy-peer-deps

# Copy source code with correct ownership
COPY --chown=nextjs:nodejs . .

# Create .next directory
RUN mkdir -p /app/.next

# Expose port
EXPOSE 3001

# Set environment
ENV NODE_ENV=development
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3001
ENV HOSTNAME=0.0.0.0
ENV NEXT_PUBLIC_API_BASE_URL=http://localhost:8001

# Start development server
CMD ["npm", "run", "dev"]
