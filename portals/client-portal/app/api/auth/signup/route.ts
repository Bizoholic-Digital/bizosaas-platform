import { NextRequest, NextResponse } from 'next/server'
import { hash } from 'bcryptjs'

export async function POST(request: NextRequest) {
    try {
        const body = await request.json()
        const { firstName, lastName, email, password, companyName } = body

        // Validation
        if (!firstName || !lastName || !email || !password) {
            return NextResponse.json(
                { error: 'Missing required fields' },
                { status: 400 }
            )
        }

        if (password.length < 8) {
            return NextResponse.json(
                { error: 'Password must be at least 8 characters long' },
                { status: 400 }
            )
        }

        // Hash password
        const hashedPassword = await hash(password, 12)

        // Call Brain Gateway to create user
        const brainGatewayUrl = process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'http://localhost:8000'

        const response = await fetch(`${brainGatewayUrl}/api/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email,
                password: hashedPassword,
                first_name: firstName,
                last_name: lastName,
                company_name: companyName || null,
                role: 'user', // Default role
            }),
        })

        if (!response.ok) {
            const error = await response.json()
            return NextResponse.json(
                { error: error.detail || 'Failed to create account' },
                { status: response.status }
            )
        }

        const user = await response.json()

        return NextResponse.json(
            {
                success: true,
                message: 'Account created successfully',
                user: {
                    id: user.id,
                    email: user.email,
                    firstName: user.first_name,
                    lastName: user.last_name,
                },
            },
            { status: 201 }
        )
    } catch (error) {
        console.error('Signup error:', error)
        return NextResponse.json(
            { error: 'Internal server error' },
            { status: 500 }
        )
    }
}
