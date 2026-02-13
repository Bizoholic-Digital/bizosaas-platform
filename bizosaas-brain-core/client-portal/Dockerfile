# ═══════════════════════════════════════════════════════════════════════════
# BizOSaaS Frontend - Optimized Multi-Stage Dockerfile
# ═══════════════════════════════════════════════════════════════════════════
#
# This is the standard Dockerfile for all BizOSaaS frontend microservices.
# Copy this to each frontend service directory.
#
# Key Optimizations:
# - Multi-stage build (3 stages) reduces final image size by ~70%
# - Dependency caching speeds up rebuilds
# - Clean npm cache saves 50-100MB
# - Standalone output includes only necessary files
# - Non-root user for security
# - Built-in healthcheck
#
# Expected final image size: ~110-120MB
# Build time (with cache): ~1-2 minutes
# ═══════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════
# Stage 1: Dependencies
# ═══════════════════════════════════════════════════════════════════════════
FROM node:20-alpine AS deps

WORKDIR /app

# Install dependencies for node-gyp
RUN apk add --no-cache libc6-compat

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies with clean cache
RUN npm install --legacy-peer-deps && \
    npm cache clean --force

# ═══════════════════════════════════════════════════════════════════════════
# Stage 2: Builder
# ═══════════════════════════════════════════════════════════════════════════
FROM node:20-alpine AS builder

WORKDIR /app

# Copy node_modules from deps stage
COPY --from=deps /app/node_modules ./node_modules

# Copy application code
COPY . .

# Build configuration
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

# Build the application
RUN npm run build

# ═══════════════════════════════════════════════════════════════════════════
# Stage 3: Production Runner
# ═══════════════════════════════════════════════════════════════════════════
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Install curl for healthchecks (before switching user)
RUN apk add --no-cache curl

# Create .next directory with correct permissions
RUN mkdir .next && chown nextjs:nodejs .next

# Copy built application
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1

# Start application
CMD ["node", "server.js"]
