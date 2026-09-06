import {
    createContext,
    useContext,
    useEffect,
    useState,
} from "react";


import api from "../components/api/axios";


const AuthContext =
    createContext(null);


export function AuthProvider({
    children,
}) {


    const [user, setUser] =
        useState(null);


    const [loading, setLoading] =
        useState(true);



    // =========================================
    // GET CURRENT USER
    // =========================================

    const fetchUser = async () => {

        try {

            const response =
                await api.get(
                    "/auth/me/"
                );


            setUser(
                response.data
            );


        } catch (error) {

            console.error(
                "Fetch user error:",
                error
            );


            localStorage.removeItem(
                "access"
            );

            localStorage.removeItem(
                "refresh"
            );


            setUser(null);

        } finally {

            setLoading(false);

        }

    };



    // =========================================
    // CHECK AUTH WHEN APP STARTS
    // =========================================

    useEffect(() => {

        const accessToken =
            localStorage.getItem(
                "access"
            );


        if (accessToken) {

            fetchUser();

        } else {

            setLoading(false);

        }

    }, []);



    // =========================================
    // LOGIN
    // =========================================

    const login = async (
        email,
        password
    ) => {

        const response =
            await api.post(

                "/auth/login/",

                {
                    email,
                    password,
                }

            );


        // Save JWT tokens

        localStorage.setItem(
            "access",
            response.data.access
        );


        localStorage.setItem(
            "refresh",
            response.data.refresh
        );


        // Get current user

        await fetchUser();


        return response.data;

    };



    // =========================================
    // LOGOUT
    // =========================================

    const logout = async () => {

        const refreshToken =
            localStorage.getItem(
                "refresh"
            );


        try {

            if (refreshToken) {

                await api.post(

                    "/auth/logout/",

                    {
                        refresh:
                            refreshToken,
                    }

                );

            }

        } catch (error) {

            console.error(
                "Logout error:",
                error
            );

        } finally {

            localStorage.removeItem(
                "access"
            );

            localStorage.removeItem(
                "refresh"
            );


            setUser(null);

        }

    };



    return (

        <AuthContext.Provider
            value={{

                user,

                loading,

                login,

                logout,

                fetchUser,

                isAuthenticated:
                    !!user,

            }}
        >

            {children}

        </AuthContext.Provider>

    );

}



export function useAuth() {

    return useContext(
        AuthContext
    );

}
