import { NextResponse } from 'next/server';

// Deactivating Better Auth session endpoints to prevent 500 errors
// Everything is now handled by auth-direct routes
export async function GET() {
    return NextResponse.json({ message: "Better Auth observer deactivated." }, { status: 200 });
}

export async function POST() {
    return NextResponse.json({ message: "Better Auth observer deactivated." }, { status: 200 });
}
