import { NextRequest, NextResponse } from 'next/server';

const GOOGLE_MAPS_API_KEY = process.env.GOOGLE_MAPS_API_KEY || "AIzaSyBZxfvuglTrcCIZZfSVDTltjBWTgEuRLto";

export async function GET(request: NextRequest) {
    const { searchParams } = new URL(request.url);
    const placeId = searchParams.get('place_id');

    if (!placeId) {
        return NextResponse.json({ error: "Place ID is required" }, { status: 400 });
    }

    try {
        const fields = "name,formatted_address,formatted_phone_number,website,url,geometry,address_components,types,business_status";
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

        const industry = mapGoogleTypesToIndustry(result.types || []);

        return NextResponse.json({
            companyName: result.name,
            location: result.formatted_address,
            phone: result.formatted_phone_number,
            website: result.website,
            gmbLink: result.url,
            placeId: placeId,
            country: countryCode,
            industry: industry,
            businessStatus: result.business_status
        });
    } catch (error: any) {
        console.error("Place Details API Error:", error);
        return NextResponse.json({ error: "Failed to fetch from Google Place Details API", details: error.message }, { status: 500 });
    }
}

function mapGoogleTypesToIndustry(types: string[]): string | undefined {
    const mapping: { [key: string]: string } = {
        'restaurant': 'Restaurant & Hospitality',
        'food': 'Restaurant & Hospitality',
        'cafe': 'Restaurant & Hospitality',
        'bar': 'Restaurant & Hospitality',
        'bakery': 'Restaurant & Hospitality',
        'meal_takeaway': 'Restaurant & Hospitality',
        'meal_delivery': 'Restaurant & Hospitality',
        'store': 'Retail & Shopping',
        'clothing_store': 'Retail & Shopping',
        'electronics_store': 'Retail & Shopping',
        'home_goods_store': 'Retail & Shopping',
        'shopping_mall': 'Retail & Shopping',
        'supermarket': 'Retail & Shopping',
        'grocery_or_supermarket': 'Retail & Shopping',
        'health': 'Healthcare & Medical',
        'doctor': 'Healthcare & Medical',
        'dentist': 'Healthcare & Medical',
        'hospital': 'Healthcare & Medical',
        'pharmacy': 'Healthcare & Medical',
        'physiotherapist': 'Healthcare & Medical',
        'gym': 'Health & Fitness',
        'spa': 'Beauty & Wellness',
        'hair_care': 'Beauty & Wellness',
        'beauty_salon': 'Beauty & Wellness',
        'finance': 'Finance & Insurance',
        'bank': 'Finance & Insurance',
        'insurance_agency': 'Finance & Insurance',
        'accounting': 'Finance & Insurance',
        'lawyer': 'Legal Services',
        'real_estate_agency': 'Real Estate',
        'lodging': 'Travel & Hospitality',
        'travel_agency': 'Travel & Hospitality',
        'school': 'Education',
        'university': 'Education',
        'car_repair': 'Automotive',
        'car_dealer': 'Automotive',
        'gas_station': 'Automotive',
        'plumber': 'Home Services',
        'electrician': 'Home Services',
        'painter': 'Home Services',
        'roofing_contractor': 'Home Services',
        'software_company': 'Software & IT', // Custom if available or inferred
        'electronics_company': 'Software & IT'
    };

    for (const type of types) {
        if (mapping[type]) {
            return mapping[type];
        }
    }

    // Fallback for generic terms
    if (types.includes('health') || types.includes('medical')) return 'Healthcare & Medical';
    if (types.includes('finance') || types.includes('financial')) return 'Finance & Insurance';
    if (types.includes('food')) return 'Restaurant & Hospitality';

    return undefined;
}
