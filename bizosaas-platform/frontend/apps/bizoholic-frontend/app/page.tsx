import React from 'react';

async function getHomepageData() {
  try {
    const res = await fetch('https://brain.bizoholic.com/api/cms/pages/home', {
      cache: 'no-store'
    });
    if (!res.ok) return null;
    return res.json();
  } catch (error) {
    return null;
  }
}

export default async function HomePage() {
  const data = await getHomepageData();
  
  return (
    <div style={{padding: '2rem', fontFamily: 'system-ui'}}>
      <h1>Bizoholic - AI Marketing Platform</h1>
      <p>Dynamic content from brain-gateway (FastAPI + CrewAI)</p>
      
      {data ? (
        <div>
          <h2>✅ Connected to Backend!</h2>
          <pre style={{background: '#f5f5f5', padding: '1rem', borderRadius: '4px'}}>
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      ) : (
        <div>
          <h2>⚠️ Connecting to backend...</h2>
          <p>Fetching dynamic content from Wagtail CMS via brain-gateway</p>
        </div>
      )}
    </div>
  );
}
