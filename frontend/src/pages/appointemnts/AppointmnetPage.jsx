import React, {
    useEffect,
    useState,
} from "react";

import {
    useNavigate,
} from "react-router-dom";

import {
    FaCalendarCheck,
    FaRedo,
} from "react-icons/fa";

import api from "../../components/api/axios";

import { APPOINTMENTS_ENDPOINTS } from "../../components/api/endpoints";

import AppointmentCard from "../../components/appointments/ApointmnetCard";


const AppointmentsPage = () => {

    const navigate = useNavigate();


    // ==========================================
    // State
    // ==========================================

    const [appointments, setAppointments] =
        useState([]);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState("");

    const [cancellingId, setCancellingId] =
        useState(null);


    // ==========================================
    // Fetch Appointments
    // ==========================================

    const fetchAppointments = async () => {

        try {

            setLoading(true);

            setError("");


            const response =
                await api.get(
                    APPOINTMENTS_ENDPOINTS.list
                );


            const data =
                response.data;


            setAppointments(
                Array.isArray(data)
                    ? data
                    : data.results || []
            );


        } catch (error) {

            console.error(
                "Failed to fetch appointments:",
                error
            );


            setError(
                error.response?.data?.detail ||
                "Unable to load appointments."
            );

        } finally {

            setLoading(false);

        }

    };


    // ==========================================
    // Initial Fetch
    // ==========================================

    useEffect(() => {

        fetchAppointments();

    }, []);


    // ==========================================
    // View Details
    // ==========================================

    const handleViewDetails = (
        appointment
    ) => {

        navigate(
            `/appointments/${appointment.id}`
        );

    };


    // ==========================================
    // Cancel Appointment
    // ==========================================

    const handleCancel = async (
        appointment
    ) => {

        const confirmed =
            window.confirm(
                "Are you sure you want to cancel this appointment?"
            );


        if (!confirmed) {
            return;
        }


        try {

            setCancellingId(
                appointment.id
            );


            setError("");


            await api.post(
                APPOINTMENTS_ENDPOINTS.cancel(
                    appointment.id
                )
            );


            // ----------------------------------
            // Update appointment locally
            // ----------------------------------

            setAppointments(
                (currentAppointments) =>
                    currentAppointments.map(
                        (item) =>
                            item.id === appointment.id
                                ? {
                                    ...item,
                                    status: "CANCELLED",
                                }
                                : item
                    )
            );


        } catch (error) {

            console.error(
                "Failed to cancel appointment:",
                error
            );


            setError(
                error.response?.data?.detail ||
                "Unable to cancel appointment."
            );

        } finally {

            setCancellingId(null);

        }

    };


    // ==========================================
    // Loading
    // ==========================================

    if (loading) {

        return (

            <main
                className="
                    min-h-screen
                    bg-light
                    py-12
                    md:py-16
                "
            >

                <div
                    className="
                        container-custom
                    "
                >

                    {/* Header Skeleton */}

                    <div
                        className="
                            mb-10
                            animate-pulse
                        "
                    >

                        <div
                            className="
                                h-4
                                w-32
                                rounded
                                bg-gray-200
                            "
                        />


                        <div
                            className="
                                mt-3
                                h-10
                                w-64
                                rounded
                                bg-gray-200
                            "
                        />


                        <div
                            className="
                                mt-3
                                h-5
                                w-full
                                max-w-xl
                                rounded
                                bg-gray-200
                            "
                        />

                    </div>


                    {/* Cards Skeleton */}

                    <div
                        className="
                            grid
                            grid-cols-1
                            gap-6
                            md:grid-cols-2
                            xl:grid-cols-3
                        "
                    >

                        {[1, 2, 3, 4, 5, 6].map(
                            (item) => (

                                <div
                                    key={item}
                                    className="
                                        h-107
                                        animate-pulse
                                        rounded-2xl
                                        bg-gray-200
                                    "
                                />

                            )
                        )}

                    </div>

                </div>

            </main>

        );

    }


    // ==========================================
    // Page
    // ==========================================

    return (

        <main
            className="
                min-h-screen
                bg-light
                py-12
                md:py-16
            "
        >

            <div
                className="
                    container-custom
                "
            >

                {/* =================================
                    Header
                ================================== */}

                <div
                    className="
                        mb-10
                        flex
                        flex-col
                        gap-5
                        md:flex-row
                        md:items-end
                        md:justify-between
                    "
                >

                    <div>

                        <p
                            className="
                                mb-2
                                text-sm
                                font-semibold
                                uppercase
                                tracking-wider
                                text-primary
                            "
                        >

                            My Healthcare

                        </p>


                        <h1
                            className="
                                text-3xl
                                font-bold
                                text-secondary
                                md:text-5xl
                            "
                        >

                            My Appointments

                        </h1>


                        <p
                            className="
                                mt-3
                                max-w-2xl
                                text-gray-500
                            "
                        >

                            Manage your upcoming and
                            previous appointments
                            with our doctors.

                        </p>

                    </div>


                    {/* Refresh */}

                    <button
                        type="button"
                        onClick={fetchAppointments}
                        className="
                            inline-flex
                            w-fit
                            items-center
                            gap-2
                            rounded-xl
                            border
                            border-gray-200
                            bg-white
                            px-5
                            py-3
                            text-sm
                            font-semibold
                            text-secondary
                            shadow-sm
                            transition
                            hover:border-primary
                            hover:text-primary
                        "
                    >

                        <FaRedo />

                        Refresh

                    </button>

                </div>


                {/* =================================
                    Error
                ================================== */}

                {error && (

                    <div
                        className="
                            mb-8
                            flex
                            items-center
                            justify-between
                            gap-4
                            rounded-xl
                            bg-red-50
                            px-5
                            py-4
                            text-sm
                            text-red-600
                        "
                    >

                        <span>
                            {error}
                        </span>


                        <button
                            type="button"
                            onClick={fetchAppointments}
                            className="
                                font-semibold
                                underline
                            "
                        >

                            Try Again

                        </button>

                    </div>

                )}


                {/* =================================
                    Empty State
                ================================== */}

                {!error &&
                    appointments.length === 0 && (

                        <div
                            className="
                                flex
                                flex-col
                                items-center
                                justify-center
                                rounded-3xl
                                bg-white
                                px-6
                                py-16
                                text-center
                                shadow-md
                            "
                        >

                            <div
                                className="
                                    flex
                                    h-20
                                    w-20
                                    items-center
                                    justify-center
                                    rounded-full
                                    bg-primary/10
                                    text-3xl
                                    text-primary
                                "
                            >

                                <FaCalendarCheck />

                            </div>


                            <h2
                                className="
                                    mt-6
                                    text-2xl
                                    font-bold
                                    text-secondary
                                "
                            >

                                No Appointments Yet

                            </h2>


                            <p
                                className="
                                    mt-3
                                    max-w-md
                                    text-gray-500
                                "
                            >

                                You don't have any
                                appointments yet.
                                Book an appointment with
                                one of our doctors.

                            </p>


                            <button
                                type="button"
                                onClick={() =>
                                    navigate(
                                        "/doctors"
                                    )
                                }
                                className="
                                    btn-primary
                                    mt-6
                                "
                            >

                                Find a Doctor

                            </button>

                        </div>

                    )}


                {/* =================================
                    Appointments Grid
                ================================== */}

                {!error &&
                    appointments.length > 0 && (

                        <div
                            className="
                                grid
                                grid-cols-1
                                gap-6
                                md:grid-cols-2
                                xl:grid-cols-2
                            "
                        >

                            {appointments.map(
                                (appointment) => (

                                    <div
                                        key={
                                            appointment.id
                                        }
                                        className="
                                            relative
                                        "
                                    >

                                        <AppointmentCard
                                            appointment={
                                                appointment
                                            }
                                            onViewDetails={
                                                handleViewDetails
                                            }
                                            onCancel={
                                                handleCancel
                                            }
                                        />


                                        {/* Cancelling Overlay */}

                                        {cancellingId ===
                                            appointment.id && (

                                            <div
                                                className="
                                                    absolute
                                                    inset-0
                                                    flex
                                                    items-center
                                                    justify-center
                                                    rounded-2xl
                                                    bg-white/70
                                                    backdrop-blur-sm
                                                "
                                            >

                                                <div
                                                    className="
                                                        rounded-xl
                                                        bg-white
                                                        px-5
                                                        py-3
                                                        text-sm
                                                        font-semibold
                                                        text-secondary
                                                        shadow-lg
                                                    "
                                                >

                                                    Cancelling...

                                                </div>

                                            </div>

                                        )}

                                    </div>

                                )
                            )}

                        </div>

                    )}

            </div>

        </main>

    );

};


export default AppointmentsPage;



