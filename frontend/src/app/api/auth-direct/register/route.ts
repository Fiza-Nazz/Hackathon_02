import { NextRequest, NextResponse } from 'next/server';

// Direct register endpoint
export async function POST(request: NextRequest) {
    try {
        const body = await request.json();
        const { email, password } = body;

        // Call backend directly for registration
        const backendResponse = await fetch('https://fizu123-todo-backend.hf.space/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        if (!backendResponse.ok) {
            return NextResponse.json(
                { error: 'Registration failed' },
                { status: 400 }
            );
        }

        const data = await backendResponse.json();

        return NextResponse.json({
            success: true,
            token: data.access_token,
            user: data.user || { email }
        });

    } catch (error) {
        console.error('Registration error:', error);
        return NextResponse.json(
            { error: 'Registration failed' },
            { status: 500 }
        );
    }
}
