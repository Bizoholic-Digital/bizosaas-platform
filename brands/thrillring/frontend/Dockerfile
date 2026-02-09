# BizOSaaS Thrillring Gaming - Standardized Dockerfile
# ═══════════════════════════════════════════════════════════════════════════

# Stage 1: Builder
FROM node:20-alpine AS builder
RUN apk add --no-cache libc6-compat
WORKDIR /app/build

# Define build arguments
ARG SERVICE_PATH
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_BRAIN_API_URL
ARG NEXT_PUBLIC_GRAPHQL_URL
ARG NEXT_PUBLIC_WAGTAIL_URL
ARG NEXT_PUBLIC_IDENTITY_SERVICE_URL
ARG NEXT_PUBLIC_AI_SERVICE_URL
ARG NEXT_PUBLIC_API_BASE_URL
ARG NEXTAUTH_URL

# Set environment variables
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_BRAIN_API_URL=$NEXT_PUBLIC_BRAIN_API_URL
ENV NEXT_PUBLIC_GRAPHQL_URL=$NEXT_PUBLIC_GRAPHQL_URL
ENV NEXT_PUBLIC_WAGTAIL_URL=$NEXT_PUBLIC_WAGTAIL_URL
ENV NEXT_PUBLIC_IDENTITY_SERVICE_URL=$NEXT_PUBLIC_IDENTITY_SERVICE_URL
ENV NEXT_PUBLIC_AI_SERVICE_URL=$NEXT_PUBLIC_AI_SERVICE_URL
ENV NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL
ENV NEXTAUTH_URL=$NEXTAUTH_URL
ENV NEXT_TELEMETRY_DISABLED=1

# Copy the entire repository
COPY . .

# CLEANUP and CONSOLIDATION
RUN if [ -d "${SERVICE_PATH}" ]; then \
    echo "Root context detected at ${SERVICE_PATH}"; \
    mkdir -p /tmp/service/scripts; \
    # Preserve critical scripts from root
    [ -f scripts/vault-injector.js ] && cp scripts/vault-injector.js /tmp/service/scripts/ || true; \
    # Copy service files
    cp -a ${SERVICE_PATH}/. /tmp/service/; \
    # Clear current directory
    rm -rf ./*; \
    # Restore service files
    cp -a /tmp/service/. ./; \
    rm -rf /tmp/service; \
    fi

# Standardized install
RUN npm install --legacy-peer-deps

# Now set production env for build stage
ENV NODE_ENV=production

# Build the application
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
COPY --from=builder /app/build/scripts/vault-injector.js ./scripts/

USER nextjs

EXPOSE 3007
ENV PORT=3007
ENV HOSTNAME="0.0.0.0"

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3007/api/health || exit 1

# Start
CMD ["sh", "-c", "if [ -n \"$VAULT_TOKEN\" ] && [ -n \"$VAULT_SECRET_PATH\" ]; then eval $(node ./scripts/vault-injector.js 2>/dev/null || echo ''); fi && node server.js"]
