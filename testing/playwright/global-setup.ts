import { FullConfig } from '@playwright/test';
import * as dotenv from 'dotenv';
import * as path from 'path';

async function globalSetup(config: FullConfig) {
    // Load environment variables
    dotenv.config({
        path: path.resolve(__dirname, '.env.test'),
        override: true
    });

    console.log('🚀 Starting Global Setup...');
    console.log(`Environment: ${process.env.NODE_ENV || 'test'}`);
    console.log(`Base URL: ${process.env.CLIENT_PORTAL_URL || 'http://localhost:3003'}`);

    // Create auth directory if it doesn't exist
    const fs = require('fs');
    const authDir = path.join(__dirname, '.auth');
    if (!fs.existsSync(authDir)) {
        fs.mkdirSync(authDir, { recursive: true });
        console.log('✅ Created .auth directory');
    }

    // You could add logic here to:
    // 1. Seed the database
    // 2. Wait for services to be healthy
    // 3. Clear existing screenshots/videos
}

export default globalSetup;
