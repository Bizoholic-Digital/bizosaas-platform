# Business Directory Frontend - Standardized Dockerfile
# Build Cache Bust: 2026-02-03T07:44:00Z

# Stage 1: Builder
FROM node:20-alpine AS builder
RUN apk add --no-cache libc6-compat
WORKDIR /app/build

# Define build arguments
ARG SERVICE_PATH=portals/business-directory/business-directory
ARG NEXT_PUBLIC_API_BASE_URL
ARG NEXT_PUBLIC_APP_URL

# Set environment variables
ENV NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL
ENV NEXT_PUBLIC_APP_URL=$NEXT_PUBLIC_APP_URL
ENV NEXT_TELEMETRY_DISABLED=1

# Copy the entire repository
COPY . .

# Extract the specific service from the root context
RUN if [ -d "${SERVICE_PATH}" ]; then \
    echo "Root context detected at ${SERVICE_PATH}"; \
    mkdir -p /tmp/service/scripts; \
    # Preserve critical scripts from root
    [ -f scripts/vault-injector.js ] && cp scripts/vault-injector.js /tmp/service/scripts/ || true; \
    # Copy service files
    cp -a ${SERVICE_PATH}/. /tmp/service/; \
    # Clear current directory (Aggressive method)
    rm -rf ./* .[!.]* ..?*; \
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
RUN apk add --no-cache curl wget

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1
ENV PORT 3005
ENV HOSTNAME "0.0.0.0"

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy built application and assets
COPY --from=builder /app/build/public/ ./public/
COPY --from=builder --chown=nextjs:nodejs /app/build/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/build/.next/static/ ./.next/static/
COPY --from=builder /app/build/scripts/vault-injector.js ./scripts/

USER nextjs
EXPOSE 3005

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3005/api/health || exit 1

CMD ["sh", "-c", "if [ -n \"$VAULT_TOKEN\" ] && [ -n \"$VAULT_SECRET_PATH\" ]; then eval $(node ./scripts/vault-injector.js 2>/dev/null || echo ''); fi && node server.js"]