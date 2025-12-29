# ═══════════════════════════════════════════════════════════════════════════
# BizOSaaS Admin Dashboard - Optimized Multi-Stage Dockerfile
# ═══════════════════════════════════════════════════════════════════════════

# Stage 1: Builder
FROM node:20-alpine AS builder

WORKDIR /app

# Define build arguments
ARG SERVICE_PATH=portals/admin-dashboard
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

# Install global dependencies
RUN apk add --no-cache libc6-compat

# Copy source code
COPY . .

# Switch to the service directory
WORKDIR /app/${SERVICE_PATH}

# Remove root configuration files to prevent Next.js from detecting workspace root incorrectly
RUN rm -f /app/package-lock.json /app/package.json /app/tsconfig.json

# Install dependencies
RUN npm install --legacy-peer-deps

# Build Next.js
RUN npm run build

# Stage 2: Production Runner
FROM node:20-alpine AS runner

WORKDIR /app

# Re-declare SERVICE_PATH for this stage
ARG SERVICE_PATH=portals/admin-dashboard

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
COPY --from=builder /app/${SERVICE_PATH}/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/${SERVICE_PATH}/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/${SERVICE_PATH}/.next/static ./.next/static
# Copy vault injector
COPY --from=builder /app/scripts/vault-injector.js ./scripts/vault-injector.js

USER nextjs

EXPOSE 3000

ENV HOSTNAME="0.0.0.0"

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1

# Start with Vault secret injection
CMD ["sh", "-c", "eval $(node scripts/vault-injector.js) && node server.js"]
