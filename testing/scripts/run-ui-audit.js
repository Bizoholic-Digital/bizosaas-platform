const lighthouse = require('lighthouse');
const chromeLauncher = require('chrome-launcher');
const fs = require('fs');

async function runAudit(url, name) {
    console.log(`Running UI/UX Audit for ${name} at ${url}...`);

    const chrome = await chromeLauncher.launch({ chromeFlags: ['--headless'] });
    const options = { logLevel: 'info', output: 'html', port: chrome.port };

    const runnerResult = await lighthouse(url, options);

    const reportHtml = runnerResult.report;
    const reportPath = `./reports/audit-${name}.html`;

    if (!fs.existsSync('./reports')) {
        fs.mkdirSync('./reports');
    }

    fs.writeFileSync(reportPath, reportHtml);

    console.log('Report is done for', runnerResult.lhr.finalUrl);
    console.log('Performance score was', runnerResult.lhr.categories.performance.score * 100);
    console.log('Accessibility score was', runnerResult.lhr.categories.accessibility.score * 100);
    console.log('Best Practices score was', runnerResult.lhr.categories['best-practices'].score * 100);
    console.log('SEO score was', runnerResult.lhr.categories.seo.score * 100);

    await chrome.kill();
}

(async () => {
    try {
        await runAudit('http://localhost:3003', 'client-portal');
        await runAudit('http://localhost:3004', 'admin-dashboard');
    } catch (e) {
        console.error('Audit failed:', e);
    }
})();
