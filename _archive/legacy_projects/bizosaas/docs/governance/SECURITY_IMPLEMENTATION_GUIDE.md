# BizOSaaS Comprehensive Security Implementation Guide

## 🛡️ Enterprise-Grade Authentication & Access Control System

This document provides a complete guide to the comprehensive security system implemented for the BizOSaaS platform, including secure Saleor dashboard access and multi-tenant authorization.

## 🏗️ Architecture Overview

The security system consists of several integrated components:

### Core Components

1. **Authentication Service** (`auth-service-v2`)
   - Multi-factor authentication (TOTP)
   - JWT token management
   - Password policy enforcement
   - Session management with hijacking protection
   - API key management for service-to-service communication

2. **Saleor Secure Proxy** (`saleor-secure-proxy`)
   - Authenticated access to Saleor dashboard (localhost:9020 → localhost:9021)
   - Role-based permission checking
   - GraphQL query analysis and rate limiting
   - Request/response security headers

3. **Security Dashboard** (`security-dashboard`)
   - Real-time security monitoring
   - Threat detection and risk scoring
   - Security event correlation
   - Automated alerting system

4. **Infrastructure Security**
   - Nginx reverse proxy with SSL/TLS
   - PostgreSQL with row-level security (RLS)
   - Redis with security configuration
   - Vault for secret management
   - Prometheus/Grafana monitoring

## 🚀 Quick Deployment

### Prerequisites

- Docker & Docker Compose
- OpenSSL (for certificate generation)
- curl (for health checks)

### One-Command Deployment

```bash
cd /home/alagiri/projects/bizoholic/bizosaas
./deploy-secure-auth.sh
```

### Manual Deployment

```bash
# Deploy core security services
docker-compose -f docker-compose.auth-security.yml up -d

# Check service health
docker-compose -f docker-compose.auth-security.yml ps
```

## 📊 Access Points

After deployment, the following services are available:

| Service | URL | Description |
|---------|-----|-------------|
| Authentication API | http://localhost:8003 | Core auth service |
| Saleor Secure Proxy | http://localhost:9021 | Protected Saleor access |
| Security Dashboard | http://localhost:8004 | Real-time monitoring |
| Grafana | http://localhost:3001 | Security metrics |
| Prometheus | http://localhost:9090 | Metrics collection |
| Vault | http://localhost:8200 | Secret management |

### HTTPS Access (Development)

| Service | HTTPS URL | Description |
|---------|-----------|-------------|
| Main Platform | https://bizosaas.local | Unified dashboard |
| Saleor Dashboard | https://saleor.bizosaas.local | E-commerce admin |
| Security Dashboard | https://dashboard.bizosaas.local | Security monitoring |

## 🔐 Authentication Features

### Multi-Factor Authentication (MFA)

1. **Setup MFA**:
```bash
curl -X POST http://localhost:8003/api/auth/mfa/setup \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

2. **Verify MFA Setup**:
```bash
curl -X POST http://localhost:8003/api/auth/mfa/verify \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"token": "123456"}'
```

### User Registration

```bash
curl -X POST http://localhost:8003/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@bizosaas.com",
    "password": "SecurePass123!",
    "role": "tenant_admin"
  }'
```

### User Login

```bash
curl -X POST http://localhost:8003/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@bizosaas.com",
    "password": "SecurePass123!",
    "remember_me": true
  }'
```

## 🔒 Role-Based Access Control (RBAC)

### User Roles

| Role | Permissions | Saleor Access | Description |
|------|------------|---------------|-------------|
| `super_admin` | admin:* | Full access | Platform administrator |
| `tenant_admin` | tenant:*, user:*, saleor:* | Full tenant access | Organization admin |
| `manager` | tenant:read, saleor:manage_* | Product/order management | Business manager |
| `staff` | tenant:read, saleor:read | Read-only access | Support staff |
| `client` | tenant:read_own | No access | End customer |

### Permission System

Permissions follow a hierarchical pattern:
- `admin:*` - Full platform access
- `saleor:read` - Read Saleor data
- `saleor:write` - Modify Saleor data
- `saleor:graphql` - GraphQL access
- `dashboard:access` - Dashboard access

## 🛡️ Saleor Dashboard Security

The Saleor dashboard is protected through a secure proxy that:

1. **Authentication Required**: All access requires valid session/JWT
2. **Permission Checking**: Verifies user has `saleor:read` + `dashboard:access`
3. **Rate Limiting**: Prevents abuse with configurable limits
4. **Request Filtering**: Analyzes GraphQL queries for security
5. **Audit Logging**: Logs all access attempts and activities

### Accessing Saleor Dashboard

1. **Direct Access** (with authentication):
```
http://localhost:9021/saleor/dashboard/
```

2. **HTTPS Access**:
```
https://saleor.bizosaas.local/
```

3. **API Access**:
```bash
curl -X GET http://localhost:9021/saleor/api/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 📈 Security Monitoring

### Security Dashboard Features

1. **Real-time Overview**: Security events, failed logins, active sessions
2. **Risk Analysis**: Risk score calculation and threat detection
3. **User Behavior**: Login patterns and suspicious activities
4. **Alert Management**: Automated alerts for security events

### Key Metrics Monitored

- Failed login attempts per IP/user
- Session hijacking attempts
- Rate limit violations
- High-risk security events
- Unusual access patterns

### Alert Thresholds

```yaml
Failed Login Threshold: 10 attempts/hour
Suspicious IP Threshold: 5 security events/hour
Session Hijack Attempts: 1 (immediate alert)
Rate Limit Violations: 20/hour
```

## 🔧 Configuration

### Environment Variables

```bash
# Core Authentication
JWT_SECRET=your-super-secret-jwt-key-32-chars-minimum
ENCRYPTION_KEY=your-32-byte-base64-encoded-key
SESSION_TIMEOUT=3600
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION=900

# Database
POSTGRES_HOST=host.docker.internal
POSTGRES_PASSWORD=securepassword123!

# Saleor Integration
SALEOR_API_URL=http://localhost:8024
SALEOR_DASHBOARD_URL=http://localhost:9020

# Security Features
CORS_ORIGINS=http://localhost:3000,https://bizosaas.local
```

### Password Policy

```python
MIN_LENGTH = 12
REQUIRE_UPPERCASE = True
REQUIRE_LOWERCASE = True  
REQUIRE_DIGITS = True
REQUIRE_SPECIAL = True
MAX_AGE_DAYS = 90
HISTORY_COUNT = 12
```

### Rate Limiting

```python
rate_limits = {
    'login': (5, 300),      # 5 attempts per 5 minutes
    'api': (100, 60),       # 100 requests per minute
    'password_reset': (3, 3600)  # 3 attempts per hour
}
```

## 🏥 Health Monitoring

### Health Check Endpoints

```bash
# Core services
curl http://localhost:8003/health  # Auth service
curl http://localhost:9021/health  # Saleor proxy
curl http://localhost:8004/health  # Security dashboard

# Infrastructure
curl http://localhost:9090/-/healthy  # Prometheus
curl http://localhost:3001/api/health # Grafana
```

### Service Dependencies

1. **PostgreSQL**: Core data storage with RLS
2. **Redis**: Session storage and caching
3. **Vault**: Secret management (optional)
4. **Nginx**: Reverse proxy and SSL termination

## 🔍 Security Testing

### Automated Security Tests

The deployment script includes basic security tests:

```bash
./deploy-secure-auth.sh
```

### Manual Security Testing

1. **Authentication Testing**:
```bash
# Test failed login protection
for i in {1..10}; do
  curl -X POST http://localhost:8003/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"wrong"}'
done
```

2. **Rate Limiting Testing**:
```bash
# Test API rate limiting
for i in {1..150}; do
  curl http://localhost:8003/api/auth/profile \
    -H "Authorization: Bearer invalid_token"
done
```

3. **Session Security Testing**:
```bash
# Test session hijacking protection
curl http://localhost:8003/api/auth/profile \
  -H "Cookie: session_id=stolen_session_id" \
  -H "X-Forwarded-For: 192.168.1.100"
```

## 📋 Security Audit Checklist

### Authentication Security
- [x] Strong password policy enforcement
- [x] Multi-factor authentication (TOTP)
- [x] Account lockout after failed attempts
- [x] Secure session management
- [x] Session hijacking protection
- [x] JWT token security

### Authorization Security
- [x] Role-based access control (RBAC)
- [x] Multi-tenant data isolation
- [x] Row-level security (RLS) in database
- [x] API permission validation
- [x] GraphQL query analysis

### Infrastructure Security
- [x] SSL/TLS encryption
- [x] Security headers injection
- [x] Rate limiting and DDoS protection
- [x] Secure reverse proxy configuration
- [x] Network segmentation
- [x] Container security best practices

### Monitoring & Logging
- [x] Comprehensive security event logging
- [x] Real-time threat detection
- [x] Security metrics collection
- [x] Automated alerting system
- [x] Audit trail maintenance
- [x] Incident response procedures

## 🚨 Security Incident Response

### Incident Types & Responses

1. **Failed Login Spike**
   - Automatic account lockout
   - IP-based rate limiting
   - Alert security team

2. **Session Hijacking Attempt**
   - Immediate session invalidation
   - User notification
   - Enhanced logging

3. **Privilege Escalation**
   - Account suspension
   - Admin notification
   - Full audit review

4. **Data Breach Indicators**
   - Emergency lockdown procedures
   - Forensic analysis initiation
   - Compliance notification

### Emergency Procedures

```bash
# Emergency shutdown
./deploy-secure-auth.sh stop

# Review security logs
docker-compose -f docker-compose.auth-security.yml logs security-dashboard

# Check for compromised accounts
curl http://localhost:8004/api/security/alerts
```

## 🔧 Maintenance & Updates

### Regular Maintenance Tasks

1. **Weekly**:
   - Review security alerts
   - Update threat intelligence
   - Rotate API keys

2. **Monthly**:
   - Security configuration review
   - Update dependencies
   - Penetration testing

3. **Quarterly**:
   - Full security audit
   - Disaster recovery testing
   - Compliance assessment

### Update Procedures

```bash
# Update security services
docker-compose -f docker-compose.auth-security.yml pull
docker-compose -f docker-compose.auth-security.yml up -d

# Backup security data
docker-compose -f docker-compose.auth-security.yml exec postgres pg_dump -U admin bizosaas > security_backup.sql
```

## 📚 API Documentation

### Authentication Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/login` | POST | User authentication |
| `/api/auth/register` | POST | User registration |
| `/api/auth/logout` | POST | Session termination |
| `/api/auth/change-password` | POST | Password update |
| `/api/auth/mfa/setup` | POST | MFA configuration |
| `/api/auth/mfa/verify` | POST | MFA verification |
| `/api/auth/profile` | GET | User profile |
| `/api/auth/security-events` | GET | Security audit log |

### Security Dashboard Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/security/overview` | GET | Security overview |
| `/api/security/alerts` | GET | Active alerts |
| `/api/security/metrics` | GET | Security metrics |
| `/api/security/user/{id}` | GET | User security report |

## 🐛 Troubleshooting

### Common Issues

1. **Service Won't Start**
```bash
# Check logs
docker-compose -f docker-compose.auth-security.yml logs auth-service

# Verify environment
cat .env

# Check ports
netstat -tulpn | grep -E ':(8003|9021|8004)'
```

2. **Authentication Fails**
```bash
# Check database connection
docker-compose -f docker-compose.auth-security.yml exec postgres psql -U admin -d bizosaas -c "SELECT 1;"

# Verify JWT secret
echo $JWT_SECRET | wc -c  # Should be >32 characters
```

3. **Saleor Proxy Issues**
```bash
# Test Saleor connectivity
curl http://localhost:8024/health/

# Check proxy logs
docker-compose -f docker-compose.auth-security.yml logs saleor-proxy
```

### Support & Documentation

- **Technical Support**: security@bizosaas.com
- **Bug Reports**: GitHub Issues
- **Security Issues**: security@bizosaas.com (encrypted)

## 📖 Additional Resources

- [OWASP Security Guidelines](https://owasp.org/www-project-top-ten/)
- [JWT Security Best Practices](https://tools.ietf.org/html/rfc8725)
- [PostgreSQL Row-Level Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [Nginx Security Configuration](https://nginx.org/en/docs/http/ngx_http_ssl_module.html)

---

**Last Updated**: September 2025  
**Version**: 2.0.0  
**Security Level**: Enterprise-Grade