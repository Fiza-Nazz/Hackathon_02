import { NextRequest, NextResponse } from 'next/server';

// Direct login endpoint that bypasses Better Auth database issues
export async function POST(request: NextRequest) {
    try {
        const body = await request.json();
        const { email, password } = body;

        // Call backend directly for authentication
        const backendResponse = await fetch('https://fizu123-todo-backend.hf.space/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        if (!backendResponse.ok) {
            return NextResponse.json(
                { error: 'Invalid credentials' },
                { status: 401 }
            );
        }

        const data = await backendResponse.json();

        // Return the token directly to frontend
        return NextResponse.json({
            success: true,
            token: data.access_token,
            user: data.user || { email }
        });

    } catch (error) {
        console.error('Login error:', error);
        return NextResponse.json(
            { error: 'Login failed' },
            { status: 500 }
        );
    }
}
