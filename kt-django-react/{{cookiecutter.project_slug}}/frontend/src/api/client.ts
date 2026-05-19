import { AUTH_TOKEN_KEY, ROUTES } from "../constants";

class ApiError extends Error {
  constructor(
    public status: number,
    public body: Record<string, unknown>,
  ) {
    super(`API error ${status}`);
    this.name = "ApiError";
  }
}

async function request<T>(url: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem(AUTH_TOKEN_KEY);
  const isFormData = options.body instanceof FormData;
  const headers: HeadersInit = {
    ...(isFormData ? {} : { "Content-Type": "application/json" }),
    ...(token ? { Authorization: `Token ${token}` } : {}),
    ...(options.headers as Record<string, string>),
  };

  const response = await fetch(url, { ...options, headers });

  if (response.status === 401) {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    window.location.href = ROUTES.LOGIN;
    throw new ApiError(401, {});
  }

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new ApiError(response.status, body);
  }

  if (response.status === 204) return undefined as T;
  return response.json();
}

export const api = {
  get: <T>(url: string) => request<T>(url),
  post: <T>(url: string, body: unknown) =>
    request<T>(url, { method: "POST", body: body instanceof FormData ? body : JSON.stringify(body) }),
  put: <T>(url: string, body: unknown) =>
    request<T>(url, { method: "PUT", body: body instanceof FormData ? body : JSON.stringify(body) }),
  patch: <T>(url: string, body: unknown) =>
    request<T>(url, { method: "PATCH", body: body instanceof FormData ? body : JSON.stringify(body) }),
  delete: <T>(url: string) => request<T>(url, { method: "DELETE" }),
};

export function extractApiError(err: unknown, fallback: string): string {
  if (!(err instanceof ApiError)) return fallback;
  const { body } = err;
  if (typeof body.detail === "string") return body.detail;
  if (Array.isArray(body.non_field_errors) && body.non_field_errors.length > 0)
    return String(body.non_field_errors[0]);
  for (const key of Object.keys(body)) {
    const val = body[key];
    if (Array.isArray(val) && val.length > 0) return String(val[0]);
    if (typeof val === "string") return val;
  }
  return fallback;
}

export { ApiError };