import { NextRequest, NextResponse } from 'next/server';

const GOOGLE_MAPS_API_KEY = process.env.GOOGLE_MAPS_API_KEY || "AIzaSyBZxfvuglTrcCIZZfSVDTltjBWTgEuRLto";

export async function GET(request: NextRequest) {
    const { searchParams } = new URL(request.url);
    const input = searchParams.get('input');
    const types = searchParams.get('types') || 'establishment';

    if (!input) {
        return NextResponse.json({ predictions: [] });
    }

    try {
        const response = await fetch(
            `https://maps.googleapis.com/maps/api/place/autocomplete/json?input=${encodeURIComponent(input)}&key=${GOOGLE_MAPS_API_KEY}&types=${types}`
        );

        if (!response.ok) {
            throw new Error(`Google API responded with status: ${response.status}`);
        }

        const data = await response.json();
        return NextResponse.json({ predictions: data.predictions || [] });
    } catch (error: any) {
        console.error("Places Autocomplete API Error:", error);
        return NextResponse.json({ error: "Failed to fetch from Google Places API", details: error.message }, { status: 500 });
    }
}
