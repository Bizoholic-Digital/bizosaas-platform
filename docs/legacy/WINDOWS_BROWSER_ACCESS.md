# Windows Browser Access to BizoSaaS Services

## ✅ WORKING SERVICES STATUS

The following BizoSaaS services are **fully functional** and accessible from Windows browsers:

| Service | URL | Status | Functionality |
|---------|-----|---------|---------------|
| **Backend API** | `http://172.25.198.116:30081/` | ✅ Working | Core platform API |
| **Agent Orchestration** | `http://172.25.198.116:30320/` | ✅ Working | AI task coordination |
| **Marketing AI** | `http://172.25.198.116:30307/` | ✅ Working | Marketing strategy & content |
| **Analytics AI** | `http://172.25.198.116:30308/` | ✅ Working | SEO analysis & lead scoring |

## 🌐 Windows Browser Setup

### Method 1: Direct IP Access (Immediate)
Simply open these URLs directly in your Windows browser:

- **Backend API**: `http://172.25.198.116:30081/`
- **Agent Orchestration**: `http://172.25.198.116:30320/`
- **Marketing AI**: `http://172.25.198.116:30307/`
- **Analytics AI**: `http://172.25.198.116:30308/`

### Method 2: Domain Names (Recommended)

1. **Edit Windows hosts file** as Administrator:
   - Open Notepad as Administrator
   - Open file: `C:\Windows\System32\drivers\etc\hosts`
   - Add these lines:
   ```
   172.25.198.116 api.bizosaas.local
   172.25.198.116 app.bizosaas.local
   172.25.198.116 bizosaas.local
   ```
   - Save the file

2. **Access via friendly URLs**:
   - **Main API**: `http://api.bizosaas.local/`
   - **Services**: Still use direct IP:port for individual services

## 🧪 Testing Service Functionality

### Backend API
```bash
# Health check
GET http://172.25.198.116:30081/health
# Response: {"status":"healthy","service":"bizosaas-backend"}

# Main endpoint  
GET http://172.25.198.116:30081/
# Response: {"message":"BizoSaaS Backend Running","version":"1.0.0"}
```

### Agent Orchestration
```bash
# Health check
GET http://172.25.198.116:30320/health
# Response: {"status":"healthy","service":"agent-orchestration"}

# Create task
POST http://172.25.198.116:30320/orchestrate
Content-Type: application/json
{
  "tenant_id": 1,
  "agent_type": "marketing_strategist", 
  "task_description": "Test task"
}
```

### Marketing AI
```bash
# Health check
GET http://172.25.198.116:30307/health
# Response: {"status":"healthy","service":"marketing-ai"}

# Generate strategy
POST http://172.25.198.116:30307/marketing/strategy
Content-Type: application/json
{
  "tenant_id": 1,
  "company_name": "TestCorp",
  "industry": "Technology",
  "target_audience": "SME businesses"
}
```

### Analytics AI
```bash
# Health check
GET http://172.25.198.116:30308/health
# Response: {"status":"healthy","service":"analytics-ai"}

# Score lead
POST http://172.25.198.116:30308/leads/score
Content-Type: application/json
{
  "tenant_id": 1,
  "lead_data": {
    "id": "lead123",
    "company_size": "medium"
  }
}
```

## ❌ Non-Working Services

The following services are deployed but **not functional** and require fixes:

- **Frontend Dashboard** (30400) - CrashLoopBackOff
- **Auth Service** (30301) - Directory creation errors
- **Payment Gateway** (30306) - Directory creation errors  
- **CRM Service** (30304) - CrashLoopBackOff
- **Identity Service** (30201) - No pod deployed
- **AI Orchestrator** (30203) - No pod deployed

## 🔧 Troubleshooting

### If services are not accessible:

1. **Check WSL2 is running**: Ensure WSL2 and K3s cluster are running
2. **Verify IP address**: Run `hostname -I` in WSL2 to confirm IP is still `172.25.198.116`
3. **Check Windows Firewall**: Ensure Windows firewall allows connections to WSL2
4. **Try different browser**: Test with Chrome, Firefox, or Edge
5. **Clear DNS cache**: Run `ipconfig /flushdns` in Windows Command Prompt

### Network Configuration
- **WSL2 IP**: `172.25.198.116` (current)
- **K3s NodePort range**: 30000-32767
- **Traefik LoadBalancer**: `172.25.198.116:80`

## 🎯 Next Steps

To complete the BizoSaaS platform:

1. **Fix Frontend Dashboard** - Resolve CrashLoopBackOff to enable browser UI
2. **Fix Auth Service** - Resolve directory creation issues for user authentication
3. **Fix Payment Gateway** - Resolve directory issues for payment processing
4. **Fix CRM Service** - Resolve CrashLoopBackOff for customer management
5. **Deploy missing services** - Identity and AI Orchestrator pods

**Current Status**: 4/10 services fully functional and browser-accessible from Windows!