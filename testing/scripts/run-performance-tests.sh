#!/bin/bash

# Performance & Load Testing Script using k6
# Tests: PERF-001 through PERF-006

set -e

echo "🚀 BizOSaaS Performance & Load Testing"
echo "========================================"

# Configuration
BASE_URL="${BASE_URL:-http://localhost:3003}"
ADMIN_URL="${ADMIN_URL:-http://localhost:3004}"
API_URL="${API_URL:-http://localhost:8001}"
DURATION="${DURATION:-5m}"
VUS="${VUS:-50}"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if k6 is installed
if ! command -v k6 &> /dev/null; then
    echo -e "${RED}❌ k6 is not installed${NC}"
    echo "Install k6: https://k6.io/docs/getting-started/installation/"
    exit 1
fi

# Create results directory
RESULTS_DIR="./reports/performance/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULTS_DIR"

echo -e "${GREEN}✓ Results will be saved to: $RESULTS_DIR${NC}"
echo ""

# Test 1: PERF-001 - Peak login spike
echo "📊 Test 1: Peak Login Spike (1000 concurrent users)"
echo "Target: p95 < 500ms"
cat > "$RESULTS_DIR/test-login-spike.js" << 'EOF'
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '30s', target: 100 },
    { duration: '1m', target: 500 },
    { duration: '1m', target: 1000 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    errors: ['rate<0.01'],
  },
};

export default function () {
  const payload = JSON.stringify({
    email: `test-${Math.random()}@example.com`,
    password: 'TestPassword123!',
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const res = http.post(`${__ENV.BASE_URL}/api/auth/login`, payload, params);
  
  const success = check(res, {
    'status is 200 or 401': (r) => r.status === 200 || r.status === 401,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  errorRate.add(!success);
  sleep(1);
}
EOF

k6 run --env BASE_URL="$BASE_URL" \
  --out json="$RESULTS_DIR/login-spike-results.json" \
  "$RESULTS_DIR/test-login-spike.js"

echo ""

# Test 2: PERF-002 - Bulk asset upload
echo "📊 Test 2: Bulk Asset Upload (100 x 10MB files)"
echo "Target: < 2min total"
cat > "$RESULTS_DIR/test-asset-upload.js" << 'EOF'
import http from 'k6/http';
import { check } from 'k6';
import { FormData } from 'https://jslib.k6.io/formdata/0.0.2/index.js';

export const options = {
  vus: 10,
  iterations: 100,
  thresholds: {
    http_req_duration: ['p(95)<30000'], // 30s per upload
  },
};

export default function () {
  const fd = new FormData();
  const fileSize = 10 * 1024 * 1024; // 10MB
  const fileData = new Array(fileSize).fill('a').join('');
  
  fd.append('file', http.file(fileData, `test-file-${__VU}-${__ITER}.bin`));
  fd.append('name', `Asset ${__VU}-${__ITER}`);

  const res = http.post(`${__ENV.BASE_URL}/api/assets/upload`, fd.body(), {
    headers: {
      'Content-Type': 'multipart/form-data; boundary=' + fd.boundary,
      'Authorization': `Bearer ${__ENV.AUTH_TOKEN}`,
    },
  });

  check(res, {
    'upload successful': (r) => r.status === 200 || r.status === 201,
    'upload time < 30s': (r) => r.timings.duration < 30000,
  });
}
EOF

echo -e "${YELLOW}⚠ Skipping asset upload test (requires auth token)${NC}"
echo "  Run manually with: k6 run --env AUTH_TOKEN=<token> test-asset-upload.js"
echo ""

# Test 3: PERF-003 - Concurrent campaign edits
echo "📊 Test 3: Concurrent Campaign Edits (50 users)"
echo "Target: p95 < 300ms"
cat > "$RESULTS_DIR/test-campaign-edits.js" << 'EOF'
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 50,
  duration: '2m',
  thresholds: {
    http_req_duration: ['p(95)<300'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const campaignId = `campaign-${Math.floor(Math.random() * 100)}`;
  
  const payload = JSON.stringify({
    name: `Updated Campaign ${Date.now()}`,
    budget: Math.floor(Math.random() * 10000),
    status: 'active',
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${__ENV.AUTH_TOKEN}`,
    },
  };

  const res = http.put(
    `${__ENV.BASE_URL}/api/campaigns/${campaignId}`,
    payload,
    params
  );

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 300ms': (r) => r.timings.duration < 300,
  });

  sleep(1);
}
EOF

echo -e "${YELLOW}⚠ Skipping campaign edits test (requires auth token)${NC}"
echo ""

# Test 4: PERF-004 - Agent burst
echo "📊 Test 4: Agent Job Burst (100 concurrent jobs)"
echo "Target: queue lag < 30s"
cat > "$RESULTS_DIR/test-agent-burst.js" << 'EOF'
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 100,
  iterations: 100,
  thresholds: {
    http_req_duration: ['p(95)<5000'],
  },
};

export default function () {
  const payload = JSON.stringify({
    agentId: 'content-optimizer',
    task: 'optimize',
    parameters: {
      contentId: `content-${__VU}-${__ITER}`,
    },
  });

  const res = http.post(
    `${__ENV.API_URL}/api/agents/jobs`,
    payload,
    {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${__ENV.AUTH_TOKEN}`,
      },
    }
  );

  check(res, {
    'job queued': (r) => r.status === 201 || r.status === 202,
    'queue time < 5s': (r) => r.timings.duration < 5000,
  });
}
EOF

echo -e "${YELLOW}⚠ Skipping agent burst test (requires auth token)${NC}"
echo ""

# Test 5: PERF-005 - Dashboard load
echo "📊 Test 5: Dashboard Load (100 widgets)"
echo "Target: p95 < 1s"
cat > "$RESULTS_DIR/test-dashboard-load.js" << 'EOF'
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 20,
  duration: '2m',
  thresholds: {
    http_req_duration: ['p(95)<1000'],
  },
};

export default function () {
  const res = http.get(`${__ENV.BASE_URL}/dashboard`, {
    headers: {
      'Authorization': `Bearer ${__ENV.AUTH_TOKEN}`,
    },
  });

  check(res, {
    'status is 200': (r) => r.status === 200,
    'load time < 1s': (r) => r.timings.duration < 1000,
    'page contains widgets': (r) => r.body.includes('widget'),
  });

  sleep(2);
}
EOF

echo -e "${YELLOW}⚠ Skipping dashboard load test (requires auth token)${NC}"
echo ""

# Test 6: PERF-006 - Search performance
echo "📊 Test 6: Search Results (10K records)"
echo "Target: p95 < 500ms"
cat > "$RESULTS_DIR/test-search-performance.js" << 'EOF'
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 30,
  duration: '2m',
  thresholds: {
    http_req_duration: ['p(95)<500'],
  },
};

const searchTerms = ['campaign', 'email', 'social', 'analytics', 'report'];

export default function () {
  const term = searchTerms[Math.floor(Math.random() * searchTerms.length)];
  
  const res = http.get(
    `${__ENV.BASE_URL}/api/search?q=${term}&limit=100`,
    {
      headers: {
        'Authorization': `Bearer ${__ENV.AUTH_TOKEN}`,
      },
    }
  );

  check(res, {
    'status is 200': (r) => r.status === 200,
    'search time < 500ms': (r) => r.timings.duration < 500,
    'results returned': (r) => {
      try {
        const data = JSON.parse(r.body);
        return Array.isArray(data.results);
      } catch {
        return false;
      }
    },
  });

  sleep(1);
}
EOF

echo -e "${YELLOW}⚠ Skipping search test (requires auth token)${NC}"
echo ""

# Summary
echo "========================================"
echo -e "${GREEN}✅ Performance test scripts generated${NC}"
echo ""
echo "To run authenticated tests, first get an auth token:"
echo "  export AUTH_TOKEN=\$(curl -X POST $BASE_URL/api/auth/login \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"email\":\"test@example.com\",\"password\":\"password\"}' | jq -r '.token')"
echo ""
echo "Then run individual tests:"
echo "  k6 run --env BASE_URL=$BASE_URL --env AUTH_TOKEN=\$AUTH_TOKEN $RESULTS_DIR/test-campaign-edits.js"
echo ""
echo "Results saved to: $RESULTS_DIR"
