import packageJson from "../package.json";

export const APP_VERSION: string = packageJson.version;

export const API_BASE = import.meta.env.VITE_API_BASE || "/api";

export const AUTH_TOKEN_KEY = "auth_token";

export const EXTERNAL_LINKS = {
  ADMIN: "/admin/",
  SWAGGER_UI: "/api/schema/swagger-ui/",
} as const;

export const ROUTES = {
  HOME: "/",
  LOGIN: "/login",
} as const;

export const ENDPOINTS = {
  AUTH_TOKEN: `${API_BASE}/auth/token/v1/`,
} as const;