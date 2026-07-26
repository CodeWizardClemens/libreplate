import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../api/authApi";

export default function LoginPage() {
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSubmit(
        event: React.FormEvent<HTMLFormElement>
    ) {
        event.preventDefault();

        setError("");
        setLoading(true);

        try {
            await login({
                username,
                password,
            });

            navigate("/diary");
        } catch (err) {
            if (err instanceof Error) {
                setError(err.message);
            } else {
                setError("Login failed");
            }
        } finally {
            setLoading(false);
        }
    }

    return (
        <main className="container vh-100 d-flex justify-content-center align-items-center">
            <div
                className="card shadow-sm"
                style={{ maxWidth: "420px", width: "100%" }}
            >
                <div className="card-body p-4">
                    <h1 className="h3 text-center mb-4">
                        Login
                    </h1>

                    <form onSubmit={handleSubmit}>

                        <div className="mb-3">
                            <label
                                htmlFor="username"
                                className="form-label"
                            >
                                Username
                            </label>

                            <input
                                id="username"
                                type="text"
                                className="form-control"
                                value={username}
                                onChange={(event) =>
                                    setUsername(event.target.value)
                                }
                                autoComplete="username"
                                required
                            />
                        </div>

                        <div className="mb-3">
                            <label
                                htmlFor="password"
                                className="form-label"
                            >
                                Password
                            </label>

                            <input
                                id="password"
                                type="password"
                                className="form-control"
                                value={password}
                                onChange={(event) =>
                                    setPassword(event.target.value)
                                }
                                autoComplete="current-password"
                                required
                            />
                        </div>

                        {error && (
                            <div
                                className="alert alert-danger"
                                role="alert"
                            >
                                {error}
                            </div>
                        )}

                        <button
                            type="submit"
                            className="btn btn-primary w-100"
                            disabled={loading}
                        >
                            {loading
                                ? "Logging in..."
                                : "Login"}
                        </button>

                    </form>
                </div>
            </div>
        </main>
    );
}