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
# Stage 1: Builder (and Dependencies)
# ═══════════════════════════════════════════════════════════════════════════
FROM node:20-alpine AS builder

WORKDIR /app

# Define build arguments
ARG NEXT_PUBLIC_BRAIN_GATEWAY_URL
ARG NEXT_PUBLIC_GRAPHQL_URL
ARG NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
ARG NEXTAUTH_URL
ARG NEXTAUTH_SECRET

# Set as environment variables for the build
ENV NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL
ENV NEXT_PUBLIC_CRM_API_URL=$NEXT_PUBLIC_CRM_API_URL
ENV NEXT_PUBLIC_CMS_API_URL=$NEXT_PUBLIC_CMS_API_URL
ENV NEXT_PUBLIC_ECOM_API_URL=$NEXT_PUBLIC_ECOM_API_URL
ENV NEXT_PUBLIC_BRAIN_GATEWAY_URL=$NEXT_PUBLIC_BRAIN_GATEWAY_URL
ENV NEXT_PUBLIC_GRAPHQL_URL=$NEXT_PUBLIC_GRAPHQL_URL
ENV NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=$NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
ENV NEXTAUTH_URL=$NEXTAUTH_URL
ENV NEXTAUTH_SECRET=$NEXTAUTH_SECRET

ENV NEXT_TELEMETRY_DISABLED=1
# NODE_ENV will be default (development) during build to install devDependencies like TypeScript

# Install global dependencies
RUN apk add --no-cache libc6-compat

# Copy the entire repository to ensure access to shared packages and correct paths
COPY . .

# Switch to the service directory
WORKDIR /app/${SERVICE_PATH}

# Remove root configuration files to prevent Next.js from detecting workspace root incorrectly
# and using the wrong tsconfig.json/package-lock.json
RUN rm -f /app/package-lock.json /app/package.json /app/tsconfig.json

# Install dependencies
RUN npm ci --legacy-peer-deps

# Build the application
RUN npm run build

# ═══════════════════════════════════════════════════════════════════════════
# Stage 2: Production Runner
# ═══════════════════════════════════════════════════════════════════════════
FROM node:20-alpine AS runner

WORKDIR /app

# Re-declare SERVICE_PATH for this stage (ARGs don't persist across stages)
ARG SERVICE_PATH

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Install curl for healthchecks
RUN apk add --no-cache curl

# Create .next directory
RUN mkdir .next && chown nextjs:nodejs .next

# Copy built application from builder stage
# Note: standalone output puts everything in .next/standalone
COPY --from=builder /app/${SERVICE_PATH}/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/${SERVICE_PATH}/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/${SERVICE_PATH}/.next/static ./.next/static
# Copy vault injector
COPY --from=builder /app/scripts/vault-injector.js ./scripts/vault-injector.js

# Switch to non-root user
USER nextjs

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1

# Start with Vault secret injection
CMD ["sh", "-c", "eval $(node scripts/vault-injector.js) && node server.js"]
