import { NextResponse } from 'next/server';

// Mock MedusaJS API for immediate functionality
export async function GET() {
  const mockProducts = [
    {
      id: 'prod_01HJGZQR8V6X2FK4GD3BTZMXHP',
      title: 'Premium Marketing Strategy Package',
      description: 'Complete digital marketing strategy with AI-powered insights',
      handle: 'premium-marketing-strategy',
      status: 'published',
      images: [
        {
          id: 'img_01HJGZQR8V6X2FK4GD3BTZMXHP',
          url: '/logo-color.png',
          alt: 'Premium Marketing Strategy'
        }
      ],
      variants: [
        {
          id: 'variant_01HJGZQR8V6X2FK4GD3BTZMXHP',
          title: 'Monthly Subscription',
          prices: [
            {
              id: 'price_01HJGZQR8V6X2FK4GD3BTZMXHP',
              amount: 29700, // $297.00
              currency_code: 'usd'
            }
          ],
          inventory_quantity: 999
        }
      ],
      categories: [
        {
          id: 'cat_marketing',
          name: 'Marketing Services'
        }
      ]
    },
    {
      id: 'prod_01HJGZQR8V6X2FK4GD3BTZMXHT',
      title: 'Agency Complete Package',
      description: 'Full-service digital marketing with dedicated account manager',
      handle: 'agency-complete-package',
      status: 'published',
      images: [
        {
          id: 'img_01HJGZQR8V6X2FK4GD3BTZMXHT',
          url: '/logo-color.png',
          alt: 'Agency Complete Package'
        }
      ],
      variants: [
        {
          id: 'variant_01HJGZQR8V6X2FK4GD3BTZMXHT',
          title: 'Monthly Subscription',
          prices: [
            {
              id: 'price_01HJGZQR8V6X2FK4GD3BTZMXHT',
              amount: 99700, // $997.00
              currency_code: 'usd'
            }
          ],
          inventory_quantity: 999
        }
      ]
    }
  ];

  return NextResponse.json({
    products: mockProducts,
    count: mockProducts.length,
    offset: 0,
    limit: 20
  });
}