# Logic for Magic Service Discovery with Consent

## User Flow
1. **User grants consent**: Before any discovery happens, the user must explicitly click "Allow Site Discovery" in their Settings or Onboarding. This is saved in `consent_records`.
2. **WordPress Connection**: When WordPress is connected, the `WordPressConnector` scans for plugins.
3. **Detection**:
   - If `FluentCRM` is detected, it's added to `detected_plugins`.
4. **Prompting**:
   - The Frontend calls `GET /api/connectors`.
   - The response includes `suggested_activations: [{slug: 'fluent-crm', type: 'crm'}]`.
   - The UI displays a toast or banner: "We detected FluentCRM on your WordPress site. Would you like to enable the CRM features?"
5. **Activation**:
   - User clicks "Enable".
   - The system re-uses the WordPress credentials (since it's a plugin on the same site) to finalize the CRM connector.

## Technical Implementation
### 1. Consent Gating
All discovery methods must now check:
```python
consent = db.query(ConsentRecord).filter(
    ConsentRecord.user_id == user.id,
    ConsentRecord.consent_type == "third_party_sync",
    ConsentRecord.granted == True
).first()
if not consent: return []
```

### 2. Audit Logging
Every discovery and activation is logged:
```python
AuditLog.log(action="plugin_detected", resource_id="fluent-crm", tenant_id=tenant_id)
```

### 3. Telemetry (Implemented)
- Traces are exported to **Tempo** (localhost:4317).
- Logs go to **Loki** (via standard stdout/promtail).
- Metrics go to **Prometheus** (localhost:8000/metrics).
