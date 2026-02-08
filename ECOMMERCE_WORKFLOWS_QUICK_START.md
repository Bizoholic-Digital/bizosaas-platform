# E-Commerce Workflows - Quick Start Guide

**Date:** 2026-01-08  
**Status:** Ready for LLM Testing  
**Recommended Approach:** Local Testing First

---

## ✅ What's Already Done

### Workflows Implemented (100%)
1. **ECommerceSourcingWorkflow** - Product sourcing & market entry
2. **ECommerceOperationsWorkflow** - Order processing & management
3. **ECommerceInventoryLogisticsWorkflow** - Inventory & logistics optimization

### Code Status
- ✅ All 3 workflows fully implemented
- ✅ Registered in `refined_agent_registry`
- ✅ Integrated with existing agents
- ✅ Mock testing passed

---

## 🎯 RECOMMENDATION: Start with Local Testing

### Why Local First?
1. **Faster iteration** - Fix issues immediately
2. **Cost control** - Monitor spending easily
3. **Better debugging** - Full access to logs
4. **No production risk** - Safe testing environment
5. **Proven approach** - OnboardingStrategyWorkflow tested locally successfully

### Why NOT Server First?
1. Slower deploy → test → fix cycle
2. Harder to debug
3. Potential production impact
4. More complex setup

---

## 🚀 Quick Start: Local LLM Testing

### Step 1: Set Up Environment (2 minutes)
```bash
# Navigate to ai-agents directory
cd /home/alagiri/projects/bizosaas-platform/bizosaas-brain-core/ai-agents

# Activate virtual environment (already done)
source /home/alagiri/projects/bizosaas-platform/.venv/bin/activate

# Create .env.testing with your real OpenAI API key
cat > .env.testing <<EOF
OPENAI_API_KEY=sk-your-real-openai-key-here
CREWAI_TRACING_ENABLED=true
LOG_LEVEL=DEBUG
EOF

# Load environment
export $(cat .env.testing | xargs)
```

### Step 2: Run Test Script (10-15 minutes)
```bash
# Run the e-commerce workflows test
python test_ecommerce_workflows_llm.py

# This will:
# - Test all 3 workflows sequentially
# - Use real OpenAI API calls
# - Track costs and execution time
# - Save detailed results to JSON
# - Print summary at the end
```

### Step 3: Review Results (5 minutes)
```bash
# Check the output in terminal
# Review the generated JSON file
cat test_results_ecommerce_llm_*.json | jq .

# Expected output:
# ✅ ecommerce_sourcing_workflow : PASS
# ✅ ecommerce_operations_workflow : PASS
# ✅ ecommerce_inventory_workflow : PASS
# 
# Total Cost: ~$5.50
# Total Time: ~8-12 minutes
```

---

## 💰 Expected Costs

### Per Test Run
| Workflow | Agents | Est. Cost |
|----------|--------|-----------|
| Sourcing | 5 | $2.50 |
| Operations | 3 | $1.50 |
| Inventory | 3 | $1.50 |
| **TOTAL** | **11** | **~$5.50** |

### Budget Recommendations
- **First Test Run:** $5-10 (may have retries)
- **Optimization Runs:** $10-20 (2-3 iterations)
- **Total Local Testing:** $15-30

---

## 📋 Testing Checklist

### Before Running
- [ ] Virtual environment activated
- [ ] Real OpenAI API key set in `.env.testing`
- [ ] Budget alert set in OpenAI dashboard ($25 recommended)
- [ ] Enough time allocated (15-20 minutes)

### During Testing
- [ ] Monitor terminal output
- [ ] Watch for errors or warnings
- [ ] Check execution time per workflow
- [ ] Note any quality issues in outputs

### After Testing
- [ ] Review JSON results file
- [ ] Verify output quality and relevance
- [ ] Check total costs
- [ ] Document any issues found
- [ ] Decide on next steps (optimize or deploy)

---

## 🔄 After Local Testing

### If Tests Pass ✅
**Next Steps:**
1. Optimize prompts if needed
2. Prepare for server deployment
3. Build Docker image
4. Deploy to KVM8 staging
5. Run integration tests
6. Deploy to production

**Timeline:** 2-3 days

### If Tests Fail ❌
**Next Steps:**
1. Review error messages
2. Fix code issues
3. Optimize prompts
4. Re-run tests locally
5. Iterate until passing

**Timeline:** 1-2 days

---

## 🆘 Troubleshooting

### Error: "OPENAI_API_KEY required"
**Solution:** Set real API key in `.env.testing`
```bash
export OPENAI_API_KEY=sk-your-key-here
```

### Error: "Rate limit exceeded"
**Solution:** Wait 60 seconds and retry, or reduce concurrent requests

### Error: "Workflow not found"
**Solution:** Ensure agents are initialized:
```bash
python -c "from main import setup_centralized_agents; import asyncio; asyncio.run(setup_centralized_agents())"
```

### High Costs
**Solution:** 
- Use GPT-3.5-turbo instead of GPT-4
- Reduce max_tokens in agent configs
- Limit retries to 1-2

---

## 📊 What Success Looks Like

### Technical Success
- ✅ All 3 workflows execute without errors
- ✅ Execution time < 5 minutes per workflow
- ✅ Cost per workflow < $3
- ✅ Outputs are well-structured JSON

### Business Success
- ✅ Outputs are coherent and relevant
- ✅ Recommendations are actionable
- ✅ Data flows correctly between agents
- ✅ Results match expected format

---

## 🚀 Deployment Path (After Local Testing)

```
Local Testing → Optimization → Docker Build → Staging Deploy → Integration Tests → Production
    (Day 1)        (Day 1-2)      (Day 2)        (Day 2-3)         (Day 3)         (Day 3-4)
```

---

## 📚 Related Documents

1. **ECOMMERCE_WORKFLOWS_TESTING_STRATEGY.md** - Full testing strategy
2. **ONBOARDING_WORKFLOW_TEST_RESULTS.md** - Example test results
3. **AI_AGENT_IMPLEMENTATION_PLAN.md** - Overall implementation plan

---

## 🎯 Decision Matrix

| Scenario | Recommendation |
|----------|----------------|
| **First time testing workflows** | ✅ Local Testing |
| **Need quick iteration** | ✅ Local Testing |
| **Testing with production data** | ⚠️ Server Staging |
| **Load/performance testing** | ⚠️ Server Staging |
| **Final pre-production validation** | ⚠️ Server Staging |
| **Production deployment** | ⚠️ Server Production |

---

## ⏭️ Next Immediate Action

**Run this command to start local LLM testing:**

```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas-brain-core/ai-agents
export OPENAI_API_KEY=sk-your-real-key-here
python test_ecommerce_workflows_llm.py
```

**Estimated Time:** 15-20 minutes  
**Estimated Cost:** $5-10  
**Risk Level:** 🟢 Low (local testing, controlled environment)

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-08T10:55:00Z  
**Recommended Action:** Start Local LLM Testing Now
