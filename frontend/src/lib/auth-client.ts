import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
    // baseURL is deliberately omitted to ensure it uses the current origin (Vercel)
    // rather than accidentally hitting the Python backend.
    plugins: [
        jwtClient()
    ]
});
