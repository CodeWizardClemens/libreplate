export interface LoginRequest {
    username: string;
    password: string;
}


export interface LoginResponse {
    message: string;
    username: string;
}


export interface User {
    id: number;
    username: string;
    email?: string;
}