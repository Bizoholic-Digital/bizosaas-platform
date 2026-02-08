const http = require('http');
const https = require('https');

/**
 * Vault Secret Injector
 * Fetches secrets from Vault KV v2 and prints them as shell export statements.
 * Usage: eval $(node vault-injector.js)
 */

const VAULT_ADDR = process.env.VAULT_ADDR || 'http://vault:8200';
const VAULT_TOKEN = process.env.VAULT_TOKEN;
const VAULT_SECRET_PATH = process.env.VAULT_SECRET_PATH; // e.g., bizosaas/data/platform/client-portal

if (!VAULT_TOKEN || !VAULT_SECRET_PATH) {
    // Silently skip if not configured, allowing fallback to standard env vars
    process.exit(0);
}

const client = VAULT_ADDR.startsWith('https') ? https : http;

function getSecrets() {
    const url = `${VAULT_ADDR}/v1/${VAULT_SECRET_PATH}`;

    const options = {
        headers: {
            'X-Vault-Token': VAULT_TOKEN
        },
        timeout: 5000
    };

    const req = client.get(url, options, (res) => {
        let data = '';
        res.on('data', (chunk) => { data += chunk; });
        res.on('end', () => {
            if (res.statusCode === 200) {
                try {
                    const json = JSON.parse(data);
                    // Vault KV v2 response structure: data.data
                    const secrets = json.data.data;
                    if (secrets) {
                        for (const [key, value] of Object.entries(secrets)) {
                            // Escape single quotes for shell safety
                            const escapedValue = String(value).replace(/'/g, "'\\''");
                            console.log(`export ${key}='${escapedValue}'`);
                        }
                    }
                } catch (e) {
                    console.error(`Error parsing Vault response: ${e.message}`);
                    process.exit(1);
                }
            } else if (res.statusCode === 404) {
                console.error(`Vault secret not found at path: ${VAULT_SECRET_PATH}`);
                process.exit(1);
            } else {
                console.error(`Vault error: ${res.statusCode} ${data}`);
                process.exit(1);
            }
        });
    });

    req.on('error', (err) => {
        console.error(`Vault connection error: ${err.message}`);
        process.exit(1);
    });

    req.on('timeout', () => {
        req.destroy();
        console.error('Vault request timed out');
        process.exit(1);
    });
}

getSecrets();
