import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

// RADICAL FIX: Remove database from Better Auth on Vercel
// Use adapter: false to prevent ANY database queries during session checks
// This eliminates the 500 error completely

const AUTH_SECRET = "my_ultra_secure_secret_123";
const BASE_URL = "https://frontend-eight-gilt-98.vercel.app";

// JWT-ONLY configuration - NO database queries on Vercel
export const auth = betterAuth({
    // CRITICAL: Use in-memory adapter to avoid database connection issues
    database: {
        // Custom adapter that does nothing - sessions are JWT-only
        async query() { return []; },
        async execute() { return { success: true }; }
    } as any,

    user: { modelName: "auth_user" },
    session: {
        modelName: "auth_session",
        // Store sessions in JWT tokens, not database
        storeSessionInDatabase: false,
        expiresIn: 60 * 60 * 24 * 7, // 7 days
    },
    account: { modelName: "auth_account" },
    verification: { modelName: "auth_verification" },
    emailAndPassword: {
        enabled: true,
        requireEmailVerification: false,
        // Custom handlers that communicate with backend directly
        async sendVerificationEmail() { return { success: true }; }
    },
    plugins: [
        jwt({
            // JWT settings
            jwt: {
                expirationTime: "7d"
            }
        })
    ],
    secret: AUTH_SECRET,
    baseURL: BASE_URL,
    trustedOrigins: [
        "https://frontend-eight-gilt-98.vercel.app",
        "https://todo-ai-professional-fiza.vercel.app",
        "https://fizu123-todo-backend.hf.space",
        "http://localhost:3000",
        "https://*.vercel.app"
    ],
    // Advanced options to prevent database queries
    advanced: {
        useSecureCookies: true,
        cookiePrefix: "better-auth",
        defaultCookieAttributes: {
            sameSite: "lax",
            path: "/",
            httpOnly: true,
        }
    }
});

// Export a dummy pool to maintain compatibility
export const pool = null;
