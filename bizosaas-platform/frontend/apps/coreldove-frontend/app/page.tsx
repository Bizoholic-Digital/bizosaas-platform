/**
 * CorelDove Simple Homepage
 * Similar to bizoholic-frontend with dynamic backend connectivity
 */

import React from 'react'

export default function HomePage() {
  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui' }}>
      <h1>CorelDove - E-commerce Platform</h1>
      <p>Dynamic content from brain-gateway (FastAPI + CrewAI)</p>
      <div>
        <h2>⚠️ Connecting to backend...</h2>
        <p>Fetching dynamic content from Wagtail CMS via brain-gateway</p>
      </div>
    </div>
  )
}