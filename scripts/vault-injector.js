/**
 * vault-injector.js
 * Fetches secrets from HashiCorp Vault and prints them as export commands.
 * Usage: eval $(node scripts/vault-injector.js)
 */

const http = require('http');
const https = require('https');

const vaultAddr = process.env.VAULT_ADDR || 'http://127.0.0.1:8200';
const vaultToken = process.env.VAULT_TOKEN;
const secretPath = process.env.VAULT_SECRET_PATH; // e.g., 'bizosaas/stg/client-portal'
const mountPoint = process.env.VAULT_MOUNT_POINT || 'secret';

if (!vaultToken || !secretPath) {
    console.error('Error: VAULT_TOKEN and VAULT_SECRET_PATH must be set');
    process.exit(0); // Exit gracefully to not break standard builds if Vault is optional
}

const url = new URL(`${vaultAddr}/v1/${mountPoint}/data/${secretPath}`);
const client = url.protocol === 'https:' ? https : http;

const options = {
    method: 'GET',
    headers: {
        'X-Vault-Token': vaultToken,
        'Content-Type': 'application/json'
    }
};

const req = client.request(url, options, (res) => {
    let data = '';

    res.on('data', (chunk) => {
        data += chunk;
    });

    res.on('end', () => {
        if (res.statusCode === 200) {
            try {
                const json = JSON.parse(data);
                const secrets = json.data.data;

                Object.entries(secrets).forEach(([key, value]) => {
                    // Escape values for shell
                    const escapedValue = String(value).replace(/"/g, '\\"');
                    console.log(`export ${key}="${escapedValue}"`);
                });
            } catch (e) {
                console.error('Error parsing Vault response:', e.message);
            }
        } else {
            console.error(`Error fetching secrets: Vault returned ${res.statusCode}`);
            console.error(data);
        }
    });
});

req.on('error', (e) => {
    console.error(`Problem with Vault request: ${e.message}`);
});

req.end();
