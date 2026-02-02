import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { Pool } from "pg";

// CRITICAL FIX: Singleton pattern with proper global caching for Vercel
declare global {
    var __authPool: Pool | undefined;
}

// Initialize pool only once across all serverless invocations
if (!global.__authPool) {
    global.__authPool = new Pool({
        connectionString: process.env.DATABASE_URL || "postgresql://neondb_owner:npg_O1mLbVXkfEY5@ep-broad-fog-a4ba5mi3-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require",
        max: 1, // CRITICAL: Use only 1 connection to prevent exhaustion on Neon free tier
        idleTimeoutMillis: 30000,
        connectionTimeoutMillis: 5000,
    });

    // Graceful error handling
    global.__authPool.on('error', (err) => {
        console.error('Unexpected database pool error:', err);
    });
}

export const pool = global.__authPool;

// Fixed base URL - no dynamic detection to avoid errors
const BASE_URL = "https://frontend-eight-gilt-98.vercel.app";

// CRITICAL: Use hardcoded secret to ensure consistency
const AUTH_SECRET = "my_ultra_secure_secret_123";

// Server side config with error resilience
export const auth = betterAuth({
    database: pool,
    user: { modelName: "auth_user" },
    session: {
        modelName: "auth_session",
        cookieCache: {
            enabled: true,
            maxAge: 300 // 5 minutes
        }
    },
    account: { modelName: "auth_account" },
    verification: { modelName: "auth_verification" },
    emailAndPassword: {
        enabled: true,
        requireEmailVerification: false // Disable to avoid extra DB calls
    },
    plugins: [jwt()],
    secret: AUTH_SECRET,
    baseURL: BASE_URL,
    trustedOrigins: [
        "https://frontend-eight-gilt-98.vercel.app",
        "https://todo-ai-professional-fiza.vercel.app",
        "https://fizu123-todo-backend.hf.space",
        "http://localhost:3000",
        "https://*.vercel.app" // Allow all Vercel preview deployments
    ]
});
