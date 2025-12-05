import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
    try {
        const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://localhost:8000'
        const controller = new AbortController()
        const timeoutId = setTimeout(() => controller.abort(), 10000)

        console.log(`Fetching about page from Brain API: ${BRAIN_API_URL}/api/v1/cms/about/`)

        const response = await fetch(`${BRAIN_API_URL}/api/v1/cms/about/`, {
            headers: {
                'Content-Type': 'application/json',
            },
            signal: controller.signal,
        })

        clearTimeout(timeoutId)

        if (!response.ok) {
            console.error(`Brain API error (About): ${response.status}`)
            return NextResponse.json({
                about: null,
                source: 'fallback'
            })
        }

        const data = await response.json()
        return NextResponse.json(data)

    } catch (error) {
        console.error('Error fetching about page:', error)
        return NextResponse.json({
            about: null,
            source: 'fallback'
        })
    }
}
