# Bizoholic Next.js Frontend - Headless Wagtail Consumer
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Accept build arguments
ARG NODE_ENV=production
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_BRAIN_GATEWAY_URL
ARG NEXT_PUBLIC_AUTH_API_URL
ARG NEXT_PUBLIC_APP_URL
ARG BASE_PATH

# Set environment variables for build
ENV NEXT_TELEMETRY_DISABLED=1
ENV WAGTAIL_API_BASE_URL=http://wagtail-headless:4000/api
ENV NODE_ENV=$NODE_ENV
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_BRAIN_GATEWAY_URL=$NEXT_PUBLIC_BRAIN_GATEWAY_URL
ENV NEXT_PUBLIC_AUTH_API_URL=$NEXT_PUBLIC_AUTH_API_URL
ENV NEXT_PUBLIC_APP_URL=$NEXT_PUBLIC_APP_URL
ENV BASE_PATH=$BASE_PATH

# Build the application
RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

# Create nextjs user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built application
COPY --from=builder /app/public ./public

# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Automatically leverage output traces to reduce image size
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3001

ENV PORT 3001
ENV HOSTNAME "0.0.0.0"

# Runtime environment variables (can be overridden by Dokploy)
# These are defaults - Dokploy should override with actual values
ENV NEXT_PUBLIC_API_URL=https://api.bizoholic.com/api
ENV NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.com/api
ENV NEXT_PUBLIC_AUTH_API_URL=https://api.bizoholic.com/api/auth
ENV NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com/portal
ENV BASE_PATH=/portal
ENV BRAIN_API_BASE_URL=https://api.bizoholic.com/api

# Run the application
CMD ["node", "server.js"]