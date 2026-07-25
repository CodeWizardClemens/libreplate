import type {
    LoginRequest,
    LoginResponse,
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
        throw new Error(
            "Login failed"
        );
    }


    return response.json();
}