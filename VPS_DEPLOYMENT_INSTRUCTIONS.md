
# VPS Deployment & Testing Instructions
**Date:** 2026-01-08

## 1. Deploy Latest AI Agents to VPS
Code has been pushed to the `staging` branch. Follow these steps to deploy on your KVM2 (or relevant) VPS.

### Step 1: SSH into VPS
```bash
ssh root@<your-vps-ip>
cd /path/to/bizosaas-platform
```

### Step 2: Pull & Rebuild
```bash
# Pull latest changes
git checkout staging
git pull origin staging

# Rebuild and restart the AI Agents and Gateway services
# Assuming docker-compose setup
docker-compose up -d --build ai-agents brain-gateway
```

### Step 3: Verify Services
```bash
# Check logs for successful startup
docker-compose logs -f ai-agents
# Look for "BizOSaas centralized and refined agents initialized successfully"
```

## 2. Connect Live Websites (Bizoholic & Coreldove)
The AI Agents need access to your sites via the **Brain Gateway**.

### Step 1: Configure Connectors
1.  Log in to your **Admin Dashboard**.
2.  Navigate to **Connectors / Integrations**.
3.  **For Bizoholic.com (WordPress)**:
    *   Select "WordPress".
    *   Enter URL: `https://bizoholic.com`
    *   Enter Admin Username.
    *   Enter **Application Password** (Generate this in WP Admin > Users > Profile > Application Passwords).
4.  **For Coreldove.com (E-commerce)**:
    *   Select "WooCommerce" (or Shopify).
    *   Enter URL: `https://coreldove.com`
    *   Enter Consumer Key (CK) and Consumer Secret (CS).

### Step 2: Run Onboarding Test
1.  Go to **AI Workflows** in Client Portal.
2.  Select **"Onboarding Strategy Workflow"**.
3.  Input:
    *   Business Name: "Coreldove"
    *   Website: "https://coreldove.com"
    *   Goals: "Increase Sales", "Brand Awareness"
4.  **Execute**.

### Step 3: Verify Continuous Improvement
1.  Wait for the Onboarding Strategy to complete.
2.  The **Quality Assurance Agent** will automatically audit the strategy (if configured in the pipeline) or you can manually trigger it via "Audit Output".
3.  The **Cross-Client Learning Engine** will store the successful pattern.

## 3. Architecture Confirmation
- **QA Agent**: ✅ Implemented (`RefinedQualityAssuranceAgent`). Audits outputs for quality.
- **RAG/KAG**: ✅ Implemented (`CrossClientLearningEngine`). Uses vector similarity to recall successful strategies.
- **Continuous Improvement**: ✅ Closed loop established (Generate -> Audit -> Learn -> Improve).
