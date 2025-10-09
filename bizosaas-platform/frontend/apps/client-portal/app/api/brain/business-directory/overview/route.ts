import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// Fallback data for development
const fallbackData = {
  stats: {
    activeListings: 3,
    totalViews: 12456,
    averageRating: 4.8,
    totalReviews: 234,
    events: 5,
    activeCoupons: 2,
    products: 15
  },
  recentActivity: [
    {
      id: '1',
      type: 'review',
      message: 'New 5-star review received for Acme Restaurant',
      timestamp: '2024-01-15T10:30:00Z'
    },
    {
      id: '2',
      type: 'listing',
      message: 'Acme Restaurant listing views increased by 15%',
      timestamp: '2024-01-14T14:22:00Z'
    },
    {
      id: '3',
      type: 'event',
      message: 'Wine Tasting Event created successfully',
      timestamp: '2024-01-13T09:15:00Z'
    }
  ],
  topPerformingListings: [
    {
      id: '1',
      name: 'Acme Restaurant',
      category: 'Fine Dining',
      views: 1234,
      rating: 4.8,
      reviews: 156
    },
    {
      id: '2',
      name: 'Tech Solutions Hub',
      category: 'Technology',
      views: 892,
      rating: 4.6,
      reviews: 78
    }
  ]
};

export async function GET(request: NextRequest) {
  try {
    const response = await fetch(`${BRAIN_API_URL}/api/brain/business-directory/overview`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3006',
      },
    });

    if (!response.ok) {
      console.error('Business Directory Overview API error:', response.status);
      return NextResponse.json(fallbackData, { status: 200 });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Business Directory Overview API error:', error);
    return NextResponse.json(fallbackData, { status: 200 });
  }
}