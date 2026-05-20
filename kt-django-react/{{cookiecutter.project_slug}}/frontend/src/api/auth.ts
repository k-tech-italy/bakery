import { ENDPOINTS } from "../constants";

interface TokenResponse {
  token: string;
}

export async function login(username: string, password: string): Promise<string> {
  const response = await fetch(ENDPOINTS.AUTH_TOKEN, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!response.ok) {
    throw new Error("Invalid credentials");
  }

  const data: TokenResponse = await response.json();
  return data.token;
}