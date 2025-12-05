# BizOSaaS Brain Core 🧠

**Modular Plug-and-Play API Gateway & AI Orchestrator**

This repository contains the core "Brain" of the BizOSaaS platform, designed to be a lightweight, modular hub that connects existing business tools (WordPress, Zoho CRM, Shopify, etc.) with advanced AI agents.

## 🏗️ Architecture

- **Brain Gateway**: FastAPI-based central API gateway (Port 8000).
- **AI Agents**: CrewAI orchestration service for 93+ specialized agents.
- **Auth Service**: Centralized SSO and identity management.
- **Client Portal**: Next.js dashboard for managing connectors and AI tasks.
- **Connectors**: Plug-and-play integration framework (WordPress, Zoho, GA4).

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+

### Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd bizosaas-brain-core
   ```

2. **Start the Core Services**
   ```bash
   docker compose up -d
   ```

3. **Access the Client Portal**
   Open [http://localhost:3000](http://localhost:3000)

## 🔌 Connectors

Configure your integrations in the Client Portal > Connectors tab.
- **WordPress**: Install the BizOSaaS plugin on your WP site.
- **Zoho CRM**: Authenticate via OAuth.
- **Google Analytics**: Connect your GA4 property.

## 🤖 AI Agents

Access the AI Assistant via the Client Portal to trigger workflows:
- "Audit my website SEO"
- "Create a marketing campaign for Black Friday"
- "Analyze my sales data from Zoho"
