# Production Dockerfile for Admin Dashboard
# Build Context: Monorepo Root

FROM node:20-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Copy package files (adjusting for monorepo structure)
COPY portals/admin-dashboard/package.json portals/admin-dashboard/package-lock.json* ./portals/admin-dashboard/
COPY packages/shared-ui/package.json ./packages/shared-ui/

# Install dependencies
WORKDIR /app/portals/admin-dashboard
RUN npm ci --legacy-peer-deps

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app

# Copy node_modules from deps
COPY --from=deps /app/portals/admin-dashboard/node_modules ./portals/admin-dashboard/node_modules


# Copy source code
COPY portals/admin-dashboard ./portals/admin-dashboard
COPY packages/shared-ui ./packages/shared-ui
COPY tsconfig.json ./tsconfig.json

# Set build-time environment variables
ENV NEXT_TELEMETRY_DISABLED 1

# Build the application
WORKDIR /app/portals/admin-dashboard
RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built application - Next.js standalone structure
COPY --from=builder /app/portals/admin-dashboard/public ./public

# Copy the standalone server and dependencies
COPY --from=builder --chown=nextjs:nodejs /app/portals/admin-dashboard/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/portals/admin-dashboard/.next/static ./.next/static

# The standalone build creates server.js in the root, but we need to ensure
# all required files from .next are available
RUN mkdir -p .next/server
COPY --from=builder --chown=nextjs:nodejs /app/portals/admin-dashboard/.next/server ./.next/server

USER nextjs

EXPOSE 3004

ENV PORT 3004
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
