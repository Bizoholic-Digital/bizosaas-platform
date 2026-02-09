/**
 * BizOSaaS Vault Secret Injector
 * 
 * This script connects to HashiCorp Vault, retrieves secrets for a specific path,
 * and outputs them in a format that can be used by `eval` to set environment variables.
 * 
 * Usage in Dockerfile:
 * CMD ["sh", "-c", "eval $(node scripts/vault-injector.js) && npm start"]
 */

const https = require('https');

// Configuration from environment
const vaultAddr = process.env.VAULT_ADDR || 'http://vault.bizoholic.net:8200';
const vaultToken = process.env.VAULT_TOKEN;
const secretPath = process.env.VAULT_SECRET_PATH; // e.g., 'secret/data/bizosaas/portals/client-portal'

if (!vaultToken || !secretPath) {
    console.error('Error: VAULT_TOKEN and VAULT_SECRET_PATH must be set');
    process.exit(1);
}

const options = {
    hostname: new URL(vaultAddr).hostname,
    port: new URL(vaultAddr).port || (vaultAddr.startsWith('https') ? 443 : 80),
    path: `/v1/${secretPath}`,
    method: 'GET',
    headers: {
        'X-Vault-Token': vaultToken,
        'Content-Type': 'application/json'
    }
};

const req = https.request(options, (res) => {
    let data = '';

    res.on('data', (chunk) => {
        data += chunk;
    });

    res.on('end', () => {
        if (res.statusCode === 200) {
            try {
                const response = JSON.parse(data);
                const secrets = response.data.data; // KV V2 uses .data.data

                if (!secrets) {
                    console.error('Error: No secrets found in response');
                    process.exit(1);
                }

                // Output exports for eval
                Object.entries(secrets).forEach(([key, value]) => {
                    // Escape double quotes in value
                    const escapedValue = String(value).replace(/"/g, '\\"');
                    console.log(`export ${key}="${escapedValue}"`);
                });
            } catch (err) {
                console.error('Error parsing Vault response:', err.message);
                process.exit(1);
            }
        } else {
            console.error(`Error: Vault returned status code ${res.statusCode}`);
            console.error('Response:', data);
            process.exit(1);
        }
    });
});

req.on('error', (err) => {
    console.error('Error connecting to Vault:', err.message);
    process.exit(1);
});

req.end();
