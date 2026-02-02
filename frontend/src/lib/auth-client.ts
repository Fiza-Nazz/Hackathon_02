import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
    baseURL: typeof window !== 'undefined' ? window.location.origin : "https://frontend-eight-gilt-98.vercel.app",
    fetchOptions: {
        credentials: "include"
    },
    plugins: [
        jwtClient()
    ]
});
