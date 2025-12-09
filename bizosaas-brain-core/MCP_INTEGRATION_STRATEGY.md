# Hybrid MCP & Direct Integration Strategy

## 1. Philosophy: "The Right Tool for the Latency"

We adopt a hybrid approach that balances the flexibility of MCP (Model Context Protocol) with the performance and control of direct API integrations.

| Integration Type | Primary Protocol | Reason |
|-----------------|------------------|--------|
| **Core Platform** | Direct HTTP/gRPC | Millisecond latency required for Auth, DB, Temporal |
| **High-Volume Data** | Direct Connectors | Fetching 10k+ CRM records or analytics events |
| **Agent Capabilities** | MCP Servers | Empowering agents with tools (GitHub, Filesystem, Search) |
| **Long-Tail Integrations** | MCP Servers | Rapidly adding support for new SaaS via community servers |

## 2. Integration Decision Matrix

| Feature | Recommended Approach | Implementation Details |
|---------|---------------------|------------------------|
| **GitHub Integration** | **MCP (github-mcp-server)** | Use for managing PRs, Issues, and reading code. Agents can natively "use" GitHub tools without custom code. |
| **Google Analytics** | Hybrid | **Auth:** Direct OAuth flow (user convenience). **Data:** MCP-style tools wrapped around direct API calls for agents. |
| **CRM (Zoho/HubSpot)** | **Direct Adapter** | Already implemented as `ZohoCRMConnector`. Keeping this allows tight UI integration in the dashboard. |
| **CMS (WordPress)** | **Direct Adapter** | Already implemented. Needs high performance for page rendering. |
| **File System** | **MCP (filesystem)** | Agents need safe, sandboxed access to read/write config files. |
| **Web Search** | **MCP (brave-search)** | Give agents ability to research competitors live. |

## 3. Architecture Deep Dive

### A. The Direct Connector Layer (Speed & UI)
Used for:
- Rendering the Client Portal Dashboard
- Syncing large datasets
- Real-time user interactions

*Pattern:* Hexagonal Ports & Adapters
`Brain Gateway -> Port Interface -> Zoho Adapter -> Zoho API`

### B. The MCP Layer (Agent Agency)
Used for:
- "Agent, fix this bug in the repo" (GitHub MCP)
- "Agent, research this competitor" (Search MCP)
- "Agent, update the deployment config" (Filesystem MCP)

*Pattern:*
`AI Agent -> MCP Client -> [MCP Server] -> External API`

## 4. Implementation Plan for MCP

1.  **Deploy MCP Servers**: Dockerize official MCP servers (GitHub, Filesystem, etc.)
2.  **MCP Client in Brain**: Update `Brain Gateway` to initialize MCP clients on startup.
3.  **Tool Registration**: Expose MCP tools to LangChain/CrewAI agents automatically.

## 5. github-mcp-server Specifics

- **Role**: DevOps & Code Management
- **Capabilities**:
    - `read_file`, `list_directory`: Explore codebases
    - `create_issue`, `update_pull_request`: Manage workflow
    - `search_code`: Semantic code search
- **Setup**: Requires `GITHUB_PERSONAL_ACCESS_TOKEN` in Vault/Env.

## 6. Future Roadmap

- Migrating long-tail connectors (Twitter, TikTok) to MCP if official servers become robust.
- Creating a "Connector-to-MCP" bridge so our existing Direct Adapters can be used by generic MCP clients.
