import { useState } from "react";

import { useAuth } from "../../context/AuthContext";


export default function LoginModal({
    onClose,
    onRegister,
}) {

    const { login } = useAuth();


    const [email, setEmail] =
        useState("");

    const [password, setPassword] =
        useState("");


    const [error, setError] =
        useState("");

    const [loading, setLoading] =
        useState(false);


    // =========================================
    // SUBMIT
    // =========================================

    const handleSubmit = async (event) => {

        event.preventDefault();

        setError("");

        setLoading(true);


        try {

            await login(
                email,
                password
            );


            // Login successful

            onClose();


        } catch (error) {

            console.error(
                "Login error:",
                error
            );


            const message =
                error.response?.data?.detail ||
                error.response?.data ||
                "Invalid email or password";


            setError(
                typeof message === "string"
                    ? message
                    : "Invalid email or password"
            );


        } finally {

            setLoading(false);

        }
    };


    return (

        <div
            className="
                fixed
                inset-0
                z-50
                flex
                items-center
                justify-center
                bg-black/50
                px-4
            "
            onClick={onClose}
        >

            <div
                className="
                    w-full
                    max-w-md
                    rounded-2xl
                    bg-white
                    p-6
                    shadow-xl
                "
                onClick={(event) =>
                    event.stopPropagation()
                }
            >


                {/* Header */}

                <div className="mb-6 flex items-center justify-between">

                    <h2 className="text-2xl font-bold">
                        Login
                    </h2>


                    <button
                        type="button"
                        onClick={onClose}
                        className="
                            text-2xl
                            text-gray-400
                            hover:text-gray-700
                        "
                    >
                        ×
                    </button>

                </div>


                {/* Error */}

                {error && (

                    <div
                        className="
                            mb-4
                            rounded-lg
                            bg-red-50
                            px-4
                            py-3
                            text-sm
                            text-red-600
                        "
                    >
                        {error}
                    </div>

                )}


                {/* Form */}

                <form
                    onSubmit={handleSubmit}
                    className="space-y-4"
                >


                    {/* Email */}

                    <div>

                        <label className="form-label">
                            Email
                        </label>

                        <input
                            type="email"
                            value={email}
                            onChange={(event) =>
                                setEmail(
                                    event.target.value
                                )
                            }
                            placeholder="patient@example.com"
                            className="form-input"
                            required
                        />

                    </div>


                    {/* Password */}

                    <div>

                        <label className="form-label">
                            Password
                        </label>

                        <input
                            type="password"
                            value={password}
                            onChange={(event) =>
                                setPassword(
                                    event.target.value
                                )
                            }
                            placeholder="••••••••"
                            className="form-input"
                            required
                        />

                    </div>


                    {/* Submit */}

                    <button
                        type="submit"
                        disabled={loading}
                        className="
                            btn-primary
                            w-full
                            disabled:cursor-not-allowed
                            disabled:opacity-60
                        "
                    >

                        {loading
                            ? "Logging in..."
                            : "Login"
                        }

                    </button>

                </form>


                {/* Register */}

                <div className="mt-6 text-center text-sm">

                    <span className="text-gray-500">
                        Don't have an account?
                    </span>

                    <button
                        type="button"
                        onClick={onRegister}
                        className="
                            ml-2
                            font-medium
                            text-primary
                            hover:underline
                        "
                    >
                        Register
                    </button>

                </div>

            </div>

        </div>

    );
}


