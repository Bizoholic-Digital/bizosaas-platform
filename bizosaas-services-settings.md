## brain-gateway



Compose Path - docker-compose.core.yml



#### environment settings



\# Database (Neon Cloud)

DATABASE\_URL=postgresql://neondb\_owner:npg\_puEbTnkSO9F8@ep-gentle-flower-a15rdh2r-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require



\# Vector DB (Same as Database, required for RAG)

VECTOR\_DB\_URL=postgresql://neondb\_owner:npg\_puEbTnkSO9F8@ep-gentle-flower-a15rdh2r-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require



\# Redis (Redis Cloud)

REDIS\_URL=redis://default:Gt7QxXA4ybMzYzD9e6KIBULfnv1IU6f9@redis-10690.c264.ap-south-1-1.ec2.cloud.redislabs.com:10690/0



\# Temporal (Temporal Cloud)

TEMPORAL\_HOST=ap-south-2.aws.api.temporal.io:7233

TEMPORAL\_NAMESPACE=bizosaas-platform-mtls.mdqxv

\# (Add TLS cert/key env vars if your code requires mTLS for Temporal)



\# Vault (Internal)

USE\_VAULT=true

VAULT\_ADDR=http://vault:8200

VAULT\_TOKEN=staging-root-token-bizosaas-2025



\# Plans.so Cloud settings

PLANE\_WEBHOOK\_SECRET=plane\_wh\_a3cadefb02fd418a8c19fd2434292f61

PLANE\_WEBHOOK\_URL=https://silo.plane.so/api/github/plane-webhook



\# API Keys (Keep existing)

JWT\_SECRET=vdMxrD6bZpZk6lClpkSP56+WNapkPAG5lY+BojEA/u7ffehUKcVL7re6xRaPWUCZffoxXF9ZFuU+KcZSWpz6CA==

OPENAI\_API\_KEY=sk-proj-Mtx5Ivvc5x4yEcMcRsYasjpDgVr3PkuQFu0IlcNHjPmpt2GhHp3jLOJOkRBnL471bsAII\_fEtcT3BlbkFJicn-ZbvvgdwUOwyzgZoO78Y391FQg-Qq-AYKQDPWZ1b5Jlf4ax8OSl0sNUhXqr9jYWzuPUU0kA

ANTHROPIC\_API\_KEY=sk-ant-api03-BjETgwPAmQJiX4raHQRc9gRhBFkrjojIPQKx99PSnonY-VUKqov1sUm57Gv8IgBXYTyqopCq\_skDLmx2exWfDQ-Ip2EcQAA

GOOGLE\_API\_KEY=AIzaSyAYDIx5BI6DNLcMqwoyU8NUiytdBlwbYOE

OPENROUTER\_API\_KEY=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

GITHUB\_TOKEN=ghp\_6KHWTnnFHmQNDlrWIGVjmi1J1Gq2fW2uD1Ks







---------------------------------------------------







## **vault**



version: "3.8"



services:

&nbsp; vault:

&nbsp;   image: hashicorp/vault:latest

&nbsp;   container\_name: vault

&nbsp;   cap\_add:

&nbsp;     - IPC\_LOCK

&nbsp;   environment:

&nbsp;     VAULT\_DEV\_ROOT\_TOKEN\_ID: "${VAULT\_DEV\_ROOT\_TOKEN\_ID}"

&nbsp;     VAULT\_DEV\_LISTEN\_ADDRESS: "${VAULT\_DEV\_LISTEN\_ADDRESS}"

&nbsp;   ports:

&nbsp;     - "8200"

&nbsp;   volumes:

&nbsp;     - vault-data:/vault/file

&nbsp;   command: "server -dev -dev-root-token-id=${VAULT\_DEV\_ROOT\_TOKEN\_ID} -dev-listen-address=${VAULT\_DEV\_LISTEN\_ADDRESS}"



volumes:

&nbsp; vault-data:



--------------------------------------------

## admin portal



compose path - docker-compose.admin-portal.yml



#### environment settings



\# Clerk Authentication (REQUIRED)

NEXT\_PUBLIC\_CLERK\_PUBLISHABLE\_KEY=pk\_test\_ZWFzeS1rb2RpYWstNzguY2xlcmsuYWNjb3VudHMuZGV2JA

CLERK\_SECRET\_KEY=sk\_test\_hsYzctm4bTgGxWB5Z6f7GT2OgnJ1biw7t21Q8NJvjv

NEXT\_PUBLIC\_CLERK\_SIGN\_IN\_URL=/login

NEXT\_PUBLIC\_CLERK\_SIGN\_UP\_URL=/signup

NEXT\_PUBLIC\_CLERK\_AFTER\_SIGN\_IN\_URL=/dashboard

NEXT\_PUBLIC\_CLERK\_AFTER\_SIGN\_UP\_URL=/dashboard



\# Brain Gateway

NEXT\_PUBLIC\_BRAIN\_GATEWAY\_URL=https://api.bizoholic.net

NEXT\_PUBLIC\_API\_BASE\_URL=https://api.bizoholic.net



\# Internal Brain Gateway connection (Needed for server actions)

BRAIN\_GATEWAY\_URL=http://bizosaas-brain-staging:8000



\# Infrastructure UIs

NEXT\_PUBLIC\_TEMPORAL\_UI\_URL=https://temporal.bizoholic.net

NEXT\_PUBLIC\_VAULT\_UI\_URL=https://vault.bizoholic.net



\# NextAuth (Optional, but kept for session stability)

NEXTAUTH\_URL=https://admin.bizoholic.net

NEXTAUTH\_SECRET=vc+i1safx5PvOaK9gc6PYLwetF4UFFWX/exE+OtzNP0=



\# Application Settings

NODE\_ENV=production

PORT=3004 



---



client portal



Compose path - docker-compose.client-portal.yml



environment settings



\# Clerk Authentication (REQUIRED)

NEXT\_PUBLIC\_CLERK\_PUBLISHABLE\_KEY=pk\_test\_ZWFzeS1rb2RpYWstNzguY2xlcmsuYWNjb3VudHMuZGV2JA

CLERK\_SECRET\_KEY=sk\_test\_hsYzctm4bTgGxWB5Z6f7GT2OgnJ1biw7t21Q8NJvjv

NEXT\_PUBLIC\_CLERK\_SIGN\_IN\_URL=/login

NEXT\_PUBLIC\_CLERK\_SIGN\_UP\_URL=/signup

NEXT\_PUBLIC\_CLERK\_AFTER\_SIGN\_IN\_URL=/dashboard

NEXT\_PUBLIC\_CLERK\_AFTER\_SIGN\_UP\_URL=/dashboard



\# Internal Networking

PORT=3003

NODE\_ENV=production

BRAIN\_GATEWAY\_URL=http://bizosaas-brain-staging:8000



\# Public API Endpoints

NEXT\_PUBLIC\_API\_URL=https://api.bizoholic.net

NEXT\_PUBLIC\_API\_BASE\_URL=https://api.bizoholic.net

NEXT\_PUBLIC\_BRAIN\_GATEWAY\_URL=https://api.bizoholic.net

NEXT\_PUBLIC\_TEMPORAL\_UI\_URL=https://temporal.bizoholic.net

NEXT\_PUBLIC\_VAULT\_UI\_URL=https://vault.bizoholic.net

