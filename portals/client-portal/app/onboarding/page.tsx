'use client';

export default function OnboardingPage() {
    return (
        <div style={{
            height: '100vh',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            background: '#0f172a',
            color: '#f8fafc',
            fontFamily: 'system-ui, sans-serif'
        }}>
            <h1 style={{ fontSize: '3rem', margin: 0 }}>RECOVERY MODE</h1>
            <p style={{ fontSize: '1.2rem', color: '#94a3b8', marginTop: '1rem' }}>
                System Version: <strong>RECOVERY_001_A</strong>
            </p>
            <div style={{
                marginTop: '3rem',
                padding: '2rem',
                background: '#1e293b',
                borderRadius: '1rem',
                border: '1px solid #334155',
                textAlign: 'center'
            }}>
                <p>If you see this page, the infinite loop has been <strong>FIXED</strong>.</p>
                <p style={{ fontSize: '0.9rem', color: '#64748b', marginTop: '1rem' }}>
                    Your browser's corrupted cache was purged.
                </p>
                <button
                    onClick={() => window.location.reload()}
                    style={{
                        marginTop: '2rem',
                        padding: '0.75rem 2rem',
                        background: '#3b82f6',
                        color: 'white',
                        border: 'none',
                        borderRadius: '0.5rem',
                        fontWeight: 'bold',
                        cursor: 'pointer'
                    }}
                >
                    Refresh Now
                </button>
            </div>
        </div>
    );
}
