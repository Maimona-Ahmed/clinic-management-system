import {
    Navigate,
} from "react-router-dom";


import {
    useAuth,
} from "../context/AuthContext";


export default function ProtectedRoute({
    children,
}) {

    const {
        isAuthenticated,
        loading,
    } = useAuth();



    // Authentication is still being checked

    if (loading) {

        return (

            <div className="flex min-h-screen items-center justify-center">

                <p>
                    Loading...
                </p>

            </div>

        );

    }



    // User is not authenticated

    if (!isAuthenticated) {

        return (

            <Navigate
                to="/"
                replace
            />

        );

    }



    // User is authenticated

    return children;

}
