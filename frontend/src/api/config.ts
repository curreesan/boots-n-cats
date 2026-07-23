export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// Derived from API_BASE_URL rather than a separate env var, so the two
// can never point at different backends — http(s):// becomes ws(s)://.
export const WS_BASE_URL = API_BASE_URL.replace(/^http/, "ws");
