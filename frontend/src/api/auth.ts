import type { User } from "../types/user";
import { API_BASE_URL } from "./config";
import { apiFetch } from "./apiFetch";

export async function registerUser(
  email: string,
  name: string,
  password: string,
): Promise<User> {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, name, password }),
  });

  if (!response.ok) {
    throw new Error("Registration failed");
  }

  return response.json();
}

export async function loginUser(
  email: string,
  password: string,
): Promise<User> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    throw new Error("Invalid email or password");
  }

  return response.json();
}

export async function logoutUser(): Promise<void> {
  await fetch(`${API_BASE_URL}/auth/logout`, {
    method: "POST",
    credentials: "include",
  });
}

export async function getCurrentUser(): Promise<User | null> {
  // Uses apiFetch (not raw fetch) deliberately: this is the call that
  // checks session validity on app load, so it's exactly the case where a
  // just-expired access token should trigger a silent refresh instead of
  // treating the user as logged out.
  const response = await apiFetch("/auth/me");

  if (!response.ok) {
    return null;
  }

  return response.json();
}
