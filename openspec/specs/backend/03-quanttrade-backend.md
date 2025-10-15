# QuantTrade Backend - Backend Service (DDD)

## Service Identity
- **Name**: QuantTrade Trading Backend
- **Type**: Backend - Algorithmic Trading Platform
- **Container**: `bizosaas-quanttrade-backend-staging`
- **Port**: `8012:8012`
- **Status**: ✅ Running

## Purpose
Algorithmic trading platform with AI-powered strategy optimization, real-time market data processing, and automated trade execution.

## Domain Model

### Aggregates
- **TradingStrategy**: Trading algorithm with parameters
- **Trade**: Individual trade execution
- **Portfolio**: User's holdings and positions
- **MarketData**: Real-time price feeds

### Key Features
- AI-powered strategy backtesting
- Real-time trade execution
- Portfolio optimization
- Risk management
- Performance analytics

## API Endpoints
- `POST /strategies` - Create trading strategy
- `GET /strategies/{id}/backtest` - Backtest strategy
- `POST /trades` - Execute trade
- `GET /portfolio` - Get portfolio status
- `GET /market-data/{symbol}` - Real-time market data

---
**Status**: ✅ Running
**Last Updated**: October 15, 2025
