import { useState } from "react";

import api from "../api/axios";


export default function RegisterModal({
    onClose,
    onLogin,
}) {

    const [formData, setFormData] = useState({

        email: "",
        first_name: "",
        last_name: "",
        password: "",
        password_confirm: "",

    });


    const [error, setError] =
        useState("");

    const [loading, setLoading] =
        useState(false);

    const [success, setSuccess] =
        useState(false);


    // =========================================
    // HANDLE INPUT
    // =========================================

    const handleChange = (event) => {

        const {
            name,
            value,
        } = event.target;


        setFormData((previous) => ({

            ...previous,

            [name]: value,

        }));

    };


    // =========================================
    // SUBMIT
    // =========================================

    const handleSubmit = async (event) => {

        event.preventDefault();

        setError("");

        setSuccess(false);

        setLoading(true);


        try {

            await api.post(
                "/auth/register/",
                formData
            );


            setSuccess(true);


            // بعد التسجيل ننتظر قليلاً
            // ثم نفتح Login

            setTimeout(() => {

                onLogin();

            }, 800);


        } catch (error) {

            console.error(
                "Registration error:",
                error
            );


            const data =
                error.response?.data;


            if (data) {

                if (typeof data === "string") {

                    setError(data);

                } else {

                    const messages =
                        Object.values(data)
                            .flat()
                            .join(" ");

                    setError(
                        messages ||
                        "Registration failed."
                    );

                }

            } else {

                setError(
                    "Unable to connect to the server."
                );

            }


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
                    max-h-[90vh]
                    w-full
                    max-w-md
                    overflow-y-auto
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
                        Create Account
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


                {/* Success */}

                {success && (

                    <div
                        className="
                            mb-4
                            rounded-lg
                            bg-green-50
                            px-4
                            py-3
                            text-sm
                            text-green-600
                        "
                    >
                        Account created successfully!
                        <br />
                        Opening login...
                    </div>

                )}


                {/* Form */}

                <form
                    onSubmit={handleSubmit}
                    className="space-y-4"
                >


                    {/* First Name */}

                    <div>

                        <label className="form-label">
                            First Name
                        </label>

                        <input
                            type="text"
                            name="first_name"
                            value={
                                formData.first_name
                            }
                            onChange={handleChange}
                            className="form-input"
                            required
                        />

                    </div>


                    {/* Last Name */}

                    <div>

                        <label className="form-label">
                            Last Name
                        </label>

                        <input
                            type="text"
                            name="last_name"
                            value={
                                formData.last_name
                            }
                            onChange={handleChange}
                            className="form-input"
                            required
                        />

                    </div>


                    {/* Email */}

                    <div>

                        <label className="form-label">
                            Email
                        </label>

                        <input
                            type="email"
                            name="email"
                            value={
                                formData.email
                            }
                            onChange={handleChange}
                            className="form-input"
                            placeholder="patient@example.com"
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
                            name="password"
                            value={
                                formData.password
                            }
                            onChange={handleChange}
                            className="form-input"
                            required
                        />

                    </div>


                    {/* Confirm Password */}

                    <div>

                        <label className="form-label">
                            Confirm Password
                        </label>

                        <input
                            type="password"
                            name="password_confirm"
                            value={
                                formData.password_confirm
                            }
                            onChange={handleChange}
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
                            ? "Creating account..."
                            : "Create Account"
                        }

                    </button>

                </form>


                {/* Login */}

                <div className="mt-6 text-center text-sm">

                    <span className="text-gray-500">
                        Already have an account?
                    </span>

                    <button
                        type="button"
                        onClick={onLogin}
                        className="
                            ml-2
                            font-medium
                            text-primary
                            hover:underline
                        "
                    >
                        Login
                    </button>

                </div>

            </div>

        </div>

    );
}
