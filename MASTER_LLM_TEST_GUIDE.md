# Master LLM Test Suite - Execution Guide

**Date:** 2026-01-08  
**Scope:** All Major AI Workflows  
**Infrastructure:** OpenRouter / OpenAI

---

## 🎯 Objective
This unified test suite (`test_master_llm.py`) executes **11 key workflows** using live Large Language Models (LLMs) via OpenRouter. This provides the ultimate "smoke test" for the entire AI agent system.

## 📋 Included Workflows
1. **Content Creation** (Blog Posts)
2. **Marketing Campaign** (Strategy)
3. **Competitive Analysis** (Market Research)
4. **Development Sprint** (Planning)
5. **E-commerce Sourcing** (Product Finding)
6. **E-commerce Operations** (Order Processing)
7. **E-commerce Inventory** (Logistics)
8. **Digital Marketing 360** (Full Scope)
9. **Gaming Event** (Community/Experience)
10. **Trading Strategy** (Financial Analysis)
11. **Onboarding Strategy** (New User Workflow)

---

## 🚀 How to Run

### 1. Set Environment Variables
The script automatically detects if you are using OpenRouter or OpenAI updates the agent configuration accordingly.

**For OpenRouter (Recommended):**
```bash
export OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxx
export OPENAI_MODEL_NAME=openai/gpt-4-turbo     # Or anthropic/claude-3-opus
```

**For OpenAI Direct:**
```bash
export OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxx
export OPENAI_MODEL_NAME=gpt-4-turbo-preview
```

### 2. Execute the Master Test
Run the script from the `ai-agents` directory:

```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas-brain-core/ai-agents
source /home/alagiri/projects/bizosaas-platform/.venv/bin/activate
python test_master_llm.py
```

### 3. Execution Options

**Run a Single Workflow:**
Isolate testing to one specific workflow (e.g., e-commerce sourcing).
```bash
python test_master_llm.py --wf ecommerce_sourcing_workflow
```

**Limit Test Count:**
Run only the first 3 defined workflows to save costs during setup.
```bash
python test_master_llm.py --limit 3
```

---

## 💰 Resource Estimation

| Metric | Estimate (Full Suite) | Estimate (Per Workflow) |
|--------|----------------------|-------------------------|
| **Total Duration** | 15 - 25 minutes | 1 - 3 minutes |
| **Total Cost** | ~$15.00 - $20.00 | ~$1.50 - $2.50 |
| **LLM Calls** | ~40-50 calls | ~4 calls |

*estimates based on GPT-4 pricing; lighter models like GPT-3.5 or Haiku will be significantly cheaper.*

---

## 📊 Reports & Logs
- **Console Output:** Real-time status updates and pass/fail indicators.
- **JSON Report:** A detailed file `master_test_results_YYYYMMDD_HHMMSS.json` is generated with full inputs, outputs, errors, and timings.

## 🛠 Troubleshooting
- **Timeout:** Each workflow has a 5-minute hard limit. If complex tasks timeout, check your internet connection or model latency.
- **Rate Limits:** The script has a built-in 2s delay between tests. If you hit OpenRouter limits, increase this delay in lines 177 (`asyncio.sleep(2)`).
