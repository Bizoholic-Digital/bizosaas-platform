# Onboarding Automation & Connector Strategy

## 1. Temporal Cloud Connection Strategy
To resolve the mTLS vs API Key confusion:

### **Choice A: API Key (Recommended)**
Use an API Key namespace for your Staging/Dev environment. This avoids complex certificate management.
*   **Action**: Update `TEMPORAL_NAMESPACE` in Dokploy to the Namespace ID that supports API Keys.
*   **Action**: Ensure `TEMPORAL_HOST` matches that namespace's region.

### **Choice B: mTLS (Production/Enterprise)**
If you MUST use mTLS:
1.  **Where to add variables**: Dokploy -> BizOSaaS Core -> Environment.
2.  **Variable Names**: `TEMPORAL_MTLS_CERT` and `TEMPORAL_MTLS_KEY`.
3.  **Format**: Paste the entire PEM content (including `-----BEGIN CERTIFICATE-----`).

## 2. Dynamic Onboarding Wizard Implementation

We will upgrade the Onboarding Wizard to automatically prompt for credentials based on selected tools.

### **Workflow**
1.  **Step 3: Select Tools**: User selects "WordPress", "HubSpot", etc.
2.  **Step 4: Configure Connections (New)**:
    *   System iterates through selected tools.
    *   Displays a dynamic form for each (User/Pass for WP, OAuth Button for HubSpot).
    *   **Automation**: On "Connect" click, we call `BrainGateway` directly.
    *   `BrainGateway` tests the connection immediately.
    *   If successful, it saves the credentials to the backend `ConnectorRegistry`.

### **Implementation Plan**
1.  **Backend**: Ensure `POST /api/connectors/{id}/connect` accepts credentials and verifies them.
2.  **Frontend**: Create `DynamicCredentialsStep.tsx`.
    *   Validates input.
    *   Calls API.
    *   Shows "Connected" status.

## 3. Next Steps
1.  **User**: Update Temporal Namespace in Dokploy (recommended) or add Certs.
2.  **Dev**: Build `DynamicCredentialsStep.tsx` and integrate into Wizard.
