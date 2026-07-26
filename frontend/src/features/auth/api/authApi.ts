import type {
    LoginRequest,
    LoginResponse,
    User,
} from "../types";

export async function login(
    credentials: LoginRequest
): Promise<LoginResponse> {

    const response = await fetch(
        "/api/accounts/login/",
        {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(credentials),
        }
    );

    if (!response.ok) {
        throw new Error("Login failed");
    }

    return response.json();
}

export async function logout(): Promise<void> {

    await fetch("/api/accounts/logout/", {
        method: "POST",
        credentials: "include",
    });

}

export async function getCurrentUser(): Promise<User> {

    const response = await fetch(
        "/api/accounts/me/",
        {
            credentials: "include",
        }
    );

    if (response.status === 401) {
        throw new Error("Unauthorized");
    }

    if (!response.ok) {
        throw new Error("Unable to load user");
    }

    return response.json();
}