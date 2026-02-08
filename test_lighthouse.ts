import { LighthouseService } from './portals/client-portal/lib/services/lighthouse-service';

async function test() {
    console.log("Running Lighthouse Audit test...");
    const service = new LighthouseService();
    // Use a public URL for testing
    const result = await service.audit("https://www.google.com");
    console.log("Audit Result:", JSON.stringify(result, null, 2));
}

test().catch(console.error);
