# BizOSaaS Admin Dashboard - Standardized Dockerfile
# Build Cache Bust: 2026-02-02T15:25:00Z
# ═══════════════════════════════════════════════════════════════════════════

# Stage 1: Builder
FROM node:20-alpine AS builder
RUN apk add --no-cache libc6-compat
WORKDIR /app/build

# Define build arguments
ARG SERVICE_PATH
ARG NEXT_PUBLIC_API_BASE_URL
ARG NEXT_PUBLIC_BRAIN_GATEWAY_URL
ARG NEXT_PUBLIC_GRAPHQL_URL
ARG NEXT_PUBLIC_AUTH_AUTHENTIK_ID
ARG NEXTAUTH_URL

# Set environment variables for build-time
ENV NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL
ENV NEXT_PUBLIC_BRAIN_GATEWAY_URL=$NEXT_PUBLIC_BRAIN_GATEWAY_URL
ENV NEXT_PUBLIC_GRAPHQL_URL=$NEXT_PUBLIC_GRAPHQL_URL
ENV NEXTAUTH_URL=$NEXTAUTH_URL
ENV NEXT_TELEMETRY_DISABLED=1

# Copy the entire repository
COPY . .

# CLEANUP and CONSOLIDATION
RUN if [ -d "${SERVICE_PATH}" ]; then \
    echo "Root context detected at ${SERVICE_PATH}"; \
    mkdir -p /tmp/service/scripts; \
    # Preserve critical scripts from root if we are in root context
    [ -f scripts/vault-injector.js ] && cp scripts/vault-injector.js /tmp/service/scripts/ || true; \
    # Copy service files
    cp -a ${SERVICE_PATH}/. /tmp/service/; \
    # Clear current directory
    rm -rf ./*; \
    # Restore service files
    cp -a /tmp/service/. ./; \
    rm -rf /tmp/service; \
    fi

# Re-ensure package.json
RUN if [ ! -f "package.json" ]; then \
    echo "CRITICAL ERROR: package.json not found"; \
    ls -F; \
    exit 1; \
    fi

# Standardized install
RUN npm install --legacy-peer-deps

# Now set production env for build stage
ENV NODE_ENV=production

# Build Next.js
RUN npm run build

# Stage 2: Runner
FROM node:20-alpine AS runner
WORKDIR /app

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Install curl
RUN apk add --no-cache curl

# Create .next directory
RUN mkdir .next && chown nextjs:nodejs .next

# Copy built application and assets
COPY --from=builder --chown=nextjs:nodejs /app/build/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/build/.next/static ./.next/static/
COPY --from=builder /app/build/public ./public/
# Check for vault-injector.js in both common locations
RUN mkdir -p scripts
COPY --from=builder /app/build/scripts/vault-injector.js ./scripts/ 2>/dev/null || \
    COPY --from=builder /app/build/portals/admin-dashboard/scripts/vault-injector.js ./scripts/

USER nextjs

EXPOSE 3004
ENV PORT=3004
ENV HOSTNAME="0.0.0.0"

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3004/api/health || exit 1

# Start
CMD ["sh", "-c", "if [ -n \"$VAULT_TOKEN\" ] && [ -n \"$VAULT_SECRET_PATH\" ]; then eval $(node ./scripts/vault-injector.js 2>/dev/null || echo ''); fi && node server.js"]
