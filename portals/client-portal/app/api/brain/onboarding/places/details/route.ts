import { NextRequest, NextResponse } from 'next/server';

const GOOGLE_MAPS_API_KEY = process.env.GOOGLE_MAPS_API_KEY || "AIzaSyBZxfvuglTrcCIZZfSVDTltjBWTgEuRLto";

export async function GET(request: NextRequest) {
    const { searchParams } = new URL(request.url);
    const placeId = searchParams.get('place_id');

    if (!placeId) {
        return NextResponse.json({ error: "Place ID is required" }, { status: 400 });
    }

    try {
        const fields = "name,formatted_address,formatted_phone_number,website,url,geometry,address_components";
        const response = await fetch(
            `https://maps.googleapis.com/maps/api/place/details/json?place_id=${placeId}&fields=${fields}&key=${GOOGLE_MAPS_API_KEY}`
        );

        if (!response.ok) {
            throw new Error(`Google API responded with status: ${response.status}`);
        }

        const data = await response.json();
        const result = data.result || {};

        // Extract country code from address_components
        const countryComponent = result.address_components?.find((c: any) => c.types.includes('country'));
        const countryCode = countryComponent?.short_name || 'US';

        return NextResponse.json({
            companyName: result.name,
            location: result.formatted_address,
            phone: result.formatted_phone_number,
            website: result.website,
            gmbLink: result.url,
            placeId: placeId,
            country: countryCode
        });
    } catch (error: any) {
        console.error("Place Details API Error:", error);
        return NextResponse.json({ error: "Failed to fetch from Google Place Details API", details: error.message }, { status: 500 });
    }
}
