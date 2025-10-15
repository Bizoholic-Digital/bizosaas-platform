# QuantTrade Frontend - Frontend Service

## Service Identity
- **Name**: QuantTrade Trading Dashboard
- **Type**: Frontend - Trading Platform (Next.js 15)
- **Container**: `bizosaas-quanttrade-frontend-staging`
- **Image**: `ghcr.io/bizoholic-digital/bizosaas-quanttrade-frontend:staging`
- **Port**: `3012:3000`
- **Domain**: `stg.bizoholic.com/quanttrade`
- **Status**: ❌ Unhealthy Container

## Purpose
Algorithmic trading dashboard with real-time market data, strategy management, portfolio tracking, and trade execution.

## Container Architecture
```
QuantTrade Frontend Container
├── Next.js 15 (Trading UI)
├── Real-time Charts (TradingView)
├── WebSocket (Market Data)
└── Strategy Builder
```

## Key Features
- Real-time market data visualization
- Strategy backtesting interface
- Portfolio management
- Trade execution panel
- Performance analytics
- Risk management dashboard

## API Integration
```typescript
// Brain Gateway routing
const BRAIN_API = process.env.NEXT_PUBLIC_API_BASE_URL

// Market data
GET /api/brain/quanttrade/market-data/{symbol}

// Trading strategies
GET /api/brain/quanttrade/strategies
POST /api/brain/quanttrade/strategies/backtest

// Portfolio
GET /api/brain/quanttrade/portfolio
POST /api/brain/quanttrade/trades
```

## Deployment Pipeline
```
Local WSL2 → GitHub → GHCR → Dokploy Staging → Dokploy Production
```

---
**Status**: ❌ Needs Health Check Fix
**Deployment**: Containerized Microservice
**Last Updated**: October 15, 2025
