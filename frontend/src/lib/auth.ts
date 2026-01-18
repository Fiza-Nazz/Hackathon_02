import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { Pool } from "pg";

// Server side database connection
const pool = new Pool({
    connectionString: "postgresql://neondb_owner:npg_O1mLbVXkfEY5@ep-broad-fog-a4ba5mi3-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require",
});

// Professional Base URL Detection for Server
const getBaseURL = () => {
    if (process.env.NEXT_PUBLIC_APP_URL) return process.env.NEXT_PUBLIC_APP_URL;
    if (process.env.BETTER_AUTH_URL) return process.env.BETTER_AUTH_URL;
    if (process.env.VERCEL_URL) return `https://${process.env.VERCEL_URL}`;
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
