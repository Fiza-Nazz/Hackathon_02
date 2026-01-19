import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  // baseURL must be the Frontend URL. 
  // Omit it to use current origin, which is correct for Vercel.
  // We add a check for window.location to be safe.
  baseURL: typeof window !== 'undefined' ? window.location.origin : undefined,
  plugins: [
    jwtClient()
  ]
});
