# BizOSaaS Admin Dashboard - Standardized Dockerfile
# Build Cache Bust: 2026-01-05T12:55:00Z
# ═══════════════════════════════════════════════════════════════════════════

# Stage 1: Dependencies
FROM node:20-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Copy package files
COPY portals/admin-dashboard/package.json portals/admin-dashboard/package-lock.json* ./portals/admin-dashboard/

# Install dependencies in the portal directory
WORKDIR /app/portals/admin-dashboard
RUN npm install --legacy-peer-deps

# Stage 2: Builder
FROM node:20-alpine AS builder
WORKDIR /app

# Copy node_modules from deps
COPY --from=deps /app/portals/admin-dashboard/node_modules ./portals/admin-dashboard/node_modules

# Copy source code
COPY . .

# Define build arguments
ARG NEXT_PUBLIC_API_BASE_URL
ARG NEXT_PUBLIC_BRAIN_GATEWAY_URL
ARG NEXT_PUBLIC_GRAPHQL_URL
ARG NEXTAUTH_URL
ARG NEXTAUTH_SECRET
ARG NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
ARG CLERK_SECRET_KEY

# Set environment variables
ENV NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL
ENV NEXT_PUBLIC_BRAIN_GATEWAY_URL=$NEXT_PUBLIC_BRAIN_GATEWAY_URL
ENV NEXT_PUBLIC_GRAPHQL_URL=$NEXT_PUBLIC_GRAPHQL_URL
ENV NEXTAUTH_URL=$NEXTAUTH_URL
ENV NEXTAUTH_SECRET=$NEXTAUTH_SECRET
ENV NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=$NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
ENV CLERK_SECRET_KEY=$CLERK_SECRET_KEY

ENV NEXT_TELEMETRY_DISABLED=1
# NODE_ENV will be default (development) during build to install devDependencies like TypeScript

# Build Next.js
WORKDIR /app/portals/admin-dashboard
RUN npm run build

# Stage 3: Runner
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=${PORT:-3000}

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Install curl
RUN apk add --no-cache curl

# Create .next directory
RUN mkdir .next && chown nextjs:nodejs .next

# Copy built application
# Next.js standalone output in monorepo includes the service path
COPY --from=builder --chown=nextjs:nodejs /app/portals/admin-dashboard/.next/standalone ./
# We need to copy static and public to the subfolder where server.js will look for them
COPY --from=builder --chown=nextjs:nodejs /app/portals/admin-dashboard/.next/static ./portals/admin-dashboard/.next/static
COPY --from=builder /app/portals/admin-dashboard/public ./portals/admin-dashboard/public

# Copy vault injector (Note: Copying from context root)
COPY scripts/vault-injector.js ./scripts/vault-injector.js

USER nextjs

EXPOSE 3000
# Ensure runtime port flexibility
ENV PORT=${PORT:-3000}

ENV HOSTNAME="0.0.0.0"

# Healthcheck targeting the internal server.js path
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT:-3000}/api/health || exit 1

# Start from the service directory to ensure paths match
WORKDIR /app/portals/admin-dashboard
CMD ["sh", "-c", "eval $(node ../../scripts/vault-injector.js) && node server.js"]

