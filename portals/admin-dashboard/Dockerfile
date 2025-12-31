# ═══════════════════════════════════════════════════════════════════════════
# BizOSaaS Admin Dashboard - Optimized Multi-Stage Dockerfile
# ═══════════════════════════════════════════════════════════════════════════

# Stage 1: Builder
FROM node:20-alpine AS builder

WORKDIR /app

# Define build arguments
ARG SERVICE_PATH
ARG NEXT_PUBLIC_API_BASE_URL
ARG NEXT_PUBLIC_BRAIN_GATEWAY_URL
ARG NEXT_PUBLIC_GRAPHQL_URL
ARG NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
ARG NEXTAUTH_URL
ARG NEXTAUTH_SECRET

# Set environment variables
ENV NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL
ENV NEXT_PUBLIC_BRAIN_GATEWAY_URL=$NEXT_PUBLIC_BRAIN_GATEWAY_URL
ENV NEXT_PUBLIC_GRAPHQL_URL=$NEXT_PUBLIC_GRAPHQL_URL
ENV NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=$NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
ENV NEXTAUTH_URL=$NEXTAUTH_URL
ENV NEXTAUTH_SECRET=$NEXTAUTH_SECRET
ENV NEXT_TELEMETRY_DISABLED=1

# Install global dependencies
RUN apk add --no-cache libc6-compat

# Copy source code
COPY . .

# Switch to the service directory
WORKDIR /app/${SERVICE_PATH}

# Install dependencies
RUN npm install --legacy-peer-deps

# Build Next.js
RUN npm run build

# Stage 2: Production Runner
FROM node:20-alpine AS runner

WORKDIR /app

# Re-declare SERVICE_PATH for this stage
ARG SERVICE_PATH=portals/admin-dashboard
ENV SERVICE_PATH=$SERVICE_PATH

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Create .next directory
RUN mkdir .next && chown nextjs:nodejs .next

# Install curl early in the runner stage
RUN apk add --no-cache curl

# Copy built application
# Standalone output in monorepos can be tricky - we copy contents to /app
COPY --from=builder --chown=nextjs:nodejs /app/${SERVICE_PATH}/.next/standalone ./

# Ensure static files and public assets are available where server.js expects them
# We copy them to both root and the service-specific path to be safe
COPY --from=builder /app/${SERVICE_PATH}/public ./public
COPY --from=builder /app/${SERVICE_PATH}/public ./${SERVICE_PATH}/public
COPY --from=builder --chown=nextjs:nodejs /app/${SERVICE_PATH}/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/${SERVICE_PATH}/.next/static ./${SERVICE_PATH}/.next/static

# Copy vault injector
COPY --from=builder /app/scripts/vault-injector.js ./scripts/vault-injector.js

USER nextjs

EXPOSE 3000

ENV HOSTNAME="0.0.0.0"

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1

# Start with Vault secret injection
# We prefer using the service-specific server.js if it exists, otherwise the root one
CMD ["sh", "-c", "eval $(node scripts/vault-injector.js) && if [ -f server.js ]; then node server.js; else node ${SERVICE_PATH}/server.js; fi"]
