#!/bin/bash

PROJECT_NAME=$1
PROJECT_TYPE=$2  # wordpress, nextjs, trading-bot, infrastructure

if [ -z "$PROJECT_NAME" ] || [ -z "$PROJECT_TYPE" ]; then
    echo "Usage: $0 <project_name> <project_type>"
    echo "Project types: wordpress, nextjs, trading-bot, infrastructure"
    exit 1
fi

echo "🚀 Setting up new project: $PROJECT_NAME (type: $PROJECT_TYPE)"

# Create project structure
mkdir -p /home/alagiri/projects/$PROJECT_NAME/.claude/{agents,commands,bmad-config}
mkdir -p /home/alagiri/projects/$PROJECT_NAME/{src,docs,tests,deploy}

# Initialize Claude Code
cd /home/alagiri/projects/$PROJECT_NAME && claude init

# Copy shared configurations
cp ~/.claude/shared-config/agents/* /home/alagiri/projects/$PROJECT_NAME/.claude/agents/
cp ~/.claude/shared-config/commands/* /home/alagiri/projects/$PROJECT_NAME/.claude/commands/
cp ~/.claude/shared-config/bmad-config/* /home/alagiri/projects/$PROJECT_NAME/.claude/bmad-config/

# Project-specific configurations based on type
case $PROJECT_TYPE in
  "wordpress")
    echo "📝 Setting up WordPress-specific configuration..."
    cat > /home/alagiri/projects/$PROJECT_NAME/.claude/CLAUDE.md << EOF
# $PROJECT_NAME WordPress Project

## Domain Knowledge
- WordPress-based website
- WooCommerce integration (if e-commerce)
- Plugin and theme management
- Performance optimization focus

## Current Architecture
- WordPress frontend
- MySQL/PostgreSQL database
- CDN and caching layers
- Plugin ecosystem

## Development Priorities
1. Performance optimization
2. Security hardening
3. SEO optimization
4. Mobile responsiveness

## Migration Plan
- Phase 1: Current WordPress optimization
- Phase 2: Content audit and cleanup
- Phase 3: NextJS + Supabase migration planning
- Phase 4: Progressive migration execution
EOF
    ;;
  "nextjs")
    echo "⚛️ Setting up NextJS + Supabase configuration..."
    cat > /home/alagiri/projects/$PROJECT_NAME/.claude/CLAUDE.md << EOF
# $PROJECT_NAME NextJS + Supabase Project

## Domain Knowledge
- NextJS framework with React
- Supabase backend integration
- PostgreSQL + pgvector database
- Real-time features and APIs

## Current Architecture
- NextJS frontend (SSR/SSG)
- Supabase backend services
- PostgreSQL with pgvector
- Real-time subscriptions

## Development Priorities
1. Component library development
2. Database schema optimization
3. Real-time feature implementation
4. Performance monitoring

## Integration Points
- Supabase Auth
- Real-time database
- Edge functions
- Storage management
EOF
    ;;
  "trading-bot")
    echo "📈 Setting up Trading Bot configuration..."
    cat > /home/alagiri/projects/$PROJECT_NAME/.claude/CLAUDE.md << EOF
# $PROJECT_NAME Trading Bot Project

## Domain Knowledge
- Algorithmic trading strategies
- Risk management systems
- Real-time market data processing
- Portfolio optimization

## Current Architecture
- Python-based trading algorithms
- FastAPI for API endpoints
- PostgreSQL for data storage
- Real-time data feeds

## Development Priorities
1. Strategy development and backtesting
2. Risk management implementation
3. Real-time execution system
4. Performance monitoring

## Safety Protocols
- Paper trading validation
- Position size limits
- Stop-loss mechanisms
- Emergency shutdown procedures
EOF
    ;;
  "infrastructure")
    echo "🏗️ Setting up Infrastructure configuration..."
    cat > /home/alagiri/projects/$PROJECT_NAME/.claude/CLAUDE.md << EOF
# $PROJECT_NAME Infrastructure Project

## Domain Knowledge
- K3s cluster management
- Container orchestration
- Microservices architecture
- DevOps automation

## Current Architecture
- K3s Kubernetes cluster
- Docker containerization
- Dokploy deployment platform
- Infrastructure as Code

## Development Priorities
1. Cluster optimization
2. Service mesh implementation
3. Monitoring and logging
4. Security hardening

## Management Tools
- kubectl for cluster operations
- Docker for containerization
- Dokploy for deployment
- Helm for package management
EOF
    ;;
  *)
    echo "❓ Unknown project type: $PROJECT_TYPE"
    echo "Creating generic configuration..."
    cat > /home/alagiri/projects/$PROJECT_NAME/.claude/CLAUDE.md << EOF
# $PROJECT_NAME Project

## Domain Knowledge
- Add project-specific domain knowledge here

## Current Architecture
- Add current architecture details here

## Development Priorities
1. Add development priorities here

## Integration Points
- Add integration points here
EOF
    ;;
esac

echo "✅ Project $PROJECT_NAME configured with Claude Code"
echo "📁 Project location: /home/alagiri/projects/$PROJECT_NAME"
echo "⚙️ Claude config: /home/alagiri/projects/$PROJECT_NAME/.claude/"