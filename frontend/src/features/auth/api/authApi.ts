import type { LoginRequest, LoginResponse, User } from "../types";

async function getCsrfToken(): Promise<string> {
  const response = await fetch("/api/accounts/csrf/", {
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error("Unable to get CSRF token");
  }

  const data = await response.json();

  return data.csrfToken;
}

export async function login(credentials: LoginRequest): Promise<LoginResponse> {
  const csrfToken = await getCsrfToken();

  const response = await fetch("/api/accounts/login/", {
    method: "POST",

    credentials: "include",

    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },

    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    throw new Error("Login failed");
  }

  return response.json();
}

export async function logout(): Promise<void> {
  const csrfToken = await getCsrfToken();

  await fetch("/api/accounts/logout/", {
    method: "POST",

    credentials: "include",

    headers: {
      "X-CSRFToken": csrfToken,
    },
  });
}

export async function getCurrentUser(): Promise<User | null> {
  const response = await fetch("/api/accounts/me/", {
    credentials: "include",
  });

  if (response.status === 401 || response.status === 403) {
    return null;
  }

  if (!response.ok) {
    throw new Error(`Unable to load user (${response.status})`);
  }

  return response.json();
}
