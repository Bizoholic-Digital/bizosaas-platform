# BizOSaaS Admin Dashboard - Standardized Dockerfile
# Build Cache Bust: 2025-12-24T15:20:00Z
# ═══════════════════════════════════════════════════════════════════════════

# Stage 1: Dependencies
FROM node:20-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Copy package files
COPY portals/admin-dashboard/package.json portals/admin-dashboard/package-lock.json* ./portals/admin-dashboard/
# Copy shared-ui package.json (if needed for install context, though we use legacy-peer-deps)
COPY packages/shared-ui/package.json ./packages/shared-ui/

# Install dependencies in the portal directory
WORKDIR /app/portals/admin-dashboard
RUN npm install --legacy-peer-deps

# Stage 2: Builder
FROM node:20-alpine AS builder
WORKDIR /app

# Copy node_modules from deps
COPY --from=deps /app/portals/admin-dashboard/node_modules ./portals/admin-dashboard/node_modules

# Copy source code
COPY portals/admin-dashboard ./portals/admin-dashboard
# Copy shared-ui INTO the portal directory to match tsconfig paths
COPY packages/shared-ui ./portals/admin-dashboard/packages/shared-ui

# Define build arguments
ARG NEXT_PUBLIC_API_BASE_URL
ARG NEXT_PUBLIC_BRAIN_GATEWAY_URL
ARG NEXT_PUBLIC_GRAPHQL_URL
ARG NEXTAUTH_URL
ARG NEXTAUTH_SECRET

# Set environment variables
ENV NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL
ENV NEXT_PUBLIC_BRAIN_GATEWAY_URL=$NEXT_PUBLIC_BRAIN_GATEWAY_URL
ENV NEXT_PUBLIC_GRAPHQL_URL=$NEXT_PUBLIC_GRAPHQL_URL
ENV NEXTAUTH_URL=$NEXTAUTH_URL
ENV NEXTAUTH_SECRET=$NEXTAUTH_SECRET

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
ENV PORT=3000

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Install curl
RUN apk add --no-cache curl

# Create .next directory
RUN mkdir .next && chown nextjs:nodejs .next

# Copy built application
COPY --from=builder /app/portals/admin-dashboard/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/portals/admin-dashboard/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/portals/admin-dashboard/.next/static ./.next/static
# Copy vault injector (Note: Copying from context root)
COPY scripts/vault-injector.js ./scripts/vault-injector.js

USER nextjs

EXPOSE 3000

ENV HOSTNAME="0.0.0.0"

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1

# Start with Vault secret injection
CMD ["sh", "-c", "eval $(node scripts/vault-injector.js) && node server.js"]
