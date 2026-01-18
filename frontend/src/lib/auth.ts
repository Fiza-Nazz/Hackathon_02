import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { Pool } from "pg";

// Server side database connection
const pool = new Pool({
    connectionString: "postgresql://neondb_owner:npg_O1mLbVXkfEY5@ep-broad-fog-a4ba5mi3-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require",
});

// Professional Base URL Detection for Server
const getBaseURL = () => {
    // Priority 1: Use APP_URL if it's set and NOT pointing to Hugging Face
    if (process.env.NEXT_PUBLIC_APP_URL && !process.env.NEXT_PUBLIC_APP_URL.includes('hf.space')) {
        return process.env.NEXT_PUBLIC_APP_URL;
    }
    // Priority 2: Use BETTER_AUTH_URL if it's set and NOT pointing to Hugging Face
    if (process.env.BETTER_AUTH_URL && !process.env.BETTER_AUTH_URL.includes('hf.space')) {
        return process.env.BETTER_AUTH_URL;
    }
    // Priority 3: Use VERCEL_URL (auto-set by Vercel)
    if (process.env.VERCEL_URL) {
        return `https://${process.env.VERCEL_URL}`;
    }
    // Fallback: Localhost
    return "http://localhost:3000";
};

// Server side config
export const auth = betterAuth({
    database: pool,
    // Avoid conflict with backend 'user' table
    user: {
        modelName: "auth_user",
    },
    session: {
        modelName: "auth_session",
    },
    account: {
        modelName: "auth_account",
    },
    verification: {
        modelName: "auth_verification",
    },
    emailAndPassword: {
        enabled: true
    },
    plugins: [
        jwt()
    ],
    secret: process.env.BETTER_AUTH_SECRET || "development-secret-key-1234567890",
    baseURL: getBaseURL(),
    trustedOrigins: [
        "https://frontend-eight-gilt-98.vercel.app",
        "https://frontend-fiza-qureshis-projects.vercel.app",
        "http://localhost:3000"
    ]
});
