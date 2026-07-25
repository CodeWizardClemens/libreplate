import {
    useState,
} from "react";

import {
    useNavigate,
} from "react-router-dom";

import {
    login,
} from "../api/authApi";


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

            navigate("/groceries");

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
        <main>
            <h1>
                Login
            </h1>

            <form onSubmit={handleSubmit}>

                <div>
                    <label htmlFor="username">
                        Username
                    </label>

                    <input
                        id="username"
                        type="text"
                        value={username}
                        onChange={(event) =>
                            setUsername(event.target.value)
                        }
                        autoComplete="username"
                        required
                    />
                </div>


                <div>
                    <label htmlFor="password">
                        Password
                    </label>

                    <input
                        id="password"
                        type="password"
                        value={password}
                        onChange={(event) =>
                            setPassword(event.target.value)
                        }
                        autoComplete="current-password"
                        required
                    />
                </div>


                {error && (
                    <p>
                        {error}
                    </p>
                )}


                <button
                    type="submit"
                    disabled={loading}
                >
                    {loading
                        ? "Logging in..."
                        : "Login"
                    }
                </button>

            </form>
        </main>
    );
}