import React, { useEffect, useState } from "react";

import api from "../../components/api/axios";

import {
    DOCTOR_DASHBOARD_ENDPOINTS,
} from "../../components/api/endpoints";

import {
    FaCalendarCheck,
    FaCalendarDay,
    FaClock,
    FaCheckCircle,
} from "react-icons/fa";


const DoctorDashboard = () => {

    const [dashboard, setDashboard] = useState(null);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");


    useEffect(() => {

        const fetchDashboard = async () => {

            try {

                setLoading(true);

                const response = await api.get(
                    DOCTOR_DASHBOARD_ENDPOINTS.dashboard
                );

                setDashboard(response.data);

            } catch (error) {

                console.error(
                    "Failed to fetch doctor dashboard:",
                    error
                );

                setError(
                    "Unable to load dashboard."
                );

            } finally {

                setLoading(false);

            }

        };


        fetchDashboard();

    }, []);


    if (loading) {

        return (
            <div className="
                min-h-screen
                bg-light
                p-6
            ">

                <div className="
                    mx-auto
                    max-w-7xl
                ">

                    <div className="
                        h-10
                        w-64
                        animate-pulse
                        rounded
                        bg-gray-200
                    " />

                    <div className="
                        mt-8
                        grid
                        grid-cols-1
                        gap-6
                        sm:grid-cols-2
                        lg:grid-cols-4
                    ">

                        {[1, 2, 3, 4].map(
                            (item) => (

                                <div
                                    key={item}
                                    className="
                                        h-32
                                        animate-pulse
                                        rounded-2xl
                                        bg-gray-200
                                    "
                                />

                            )
                        )}

                    </div>

                </div>

            </div>
        );

    }


    if (error) {

        return (
            <div className="
                flex
                min-h-screen
                items-center
                justify-center
            ">

                <p className="text-red-500">
                    {error}
                </p>

            </div>
        );

    }


    const statistics =
        dashboard?.statistics || {};

    const appointments =
        dashboard?.today_appointments || [];


    return (

        <main className="
            min-h-screen
            bg-light
            p-6
            md:p-8
        ">

            <div className="
                mx-auto
                max-w-7xl
            ">


                {/* ==========================
                    Welcome
                ========================== */}

                <div className="mb-8">

                    <p className="
                        text-sm
                        font-medium
                        text-primary
                    ">
                        Doctor Dashboard
                    </p>

                    <h1 className="
                        mt-1
                        text-3xl
                        font-bold
                        text-secondary
                    ">

                        Welcome back,
                        {" "}
                        {dashboard?.doctor?.doctor_name}

                    </h1>

                    <p className="
                        mt-2
                        text-gray-500
                    ">

                        Here is what's happening
                        with your appointments today.

                    </p>

                </div>


                {/* ==========================
                    Statistics
                ========================== */}

                <div className="
                    grid
                    grid-cols-1
                    gap-6
                    sm:grid-cols-2
                    lg:grid-cols-4
                ">


                    {/* Total */}

                    <StatisticCard
                        title="Total Appointments"
                        value={
                            statistics.total_appointments
                        }
                        icon={<FaCalendarCheck />}
                    />


                    {/* Today */}

                    <StatisticCard
                        title="Today's Appointments"
                        value={
                            statistics.today_appointments
                        }
                        icon={<FaCalendarDay />}
                    />


                    {/* Pending */}

                    <StatisticCard
                        title="Pending"
                        value={
                            statistics.pending_appointments
                        }
                        icon={<FaClock />}
                    />


                    {/* Completed */}

                    <StatisticCard
                        title="Completed"
                        value={
                            statistics.completed_appointments
                        }
                        icon={<FaCheckCircle />}
                    />

                </div>


                {/* ==========================
                    Today's Appointments
                ========================== */}

                <div className="
                    mt-8
                    rounded-2xl
                    bg-white
                    p-6
                    shadow-sm
                ">

                    <div className="
                        mb-6
                        flex
                        items-center
                        justify-between
                    ">

                        <div>

                            <h2 className="
                                text-xl
                                font-bold
                                text-secondary
                            ">
                                Today's Appointments
                            </h2>

                            <p className="
                                mt-1
                                text-sm
                                text-gray-500
                            ">
                                Your appointments for today.
                            </p>

                        </div>

                    </div>


                    {appointments.length === 0 ? (

                        <div className="
                            py-10
                            text-center
                        ">

                            <p className="
                                text-gray-500
                            ">
                                No appointments today.
                            </p>

                        </div>

                    ) : (

                        <div className="
                            overflow-x-auto
                        ">

                            <table className="
                                w-full
                                text-left
                            ">

                                <thead>

                                    <tr className="
                                        border-b
                                        border-gray-100
                                    ">

                                        <th className="
                                            px-4
                                            py-3
                                            text-sm
                                            font-semibold
                                            text-gray-500
                                        ">
                                            Patient
                                        </th>

                                        <th className="
                                            px-4
                                            py-3
                                            text-sm
                                            font-semibold
                                            text-gray-500
                                        ">
                                            Service
                                        </th>

                                        <th className="
                                            px-4
                                            py-3
                                            text-sm
                                            font-semibold
                                            text-gray-500
                                        ">
                                            Time
                                        </th>

                                        <th className="
                                            px-4
                                            py-3
                                            text-sm
                                            font-semibold
                                            text-gray-500
                                        ">
                                            Status
                                        </th>

                                    </tr>

                                </thead>


                                <tbody>

                                    {appointments.map(
                                        (appointment) => (

                                            <tr
                                                key={
                                                    appointment.id
                                                }
                                                className="
                                                    border-b
                                                    border-gray-50
                                                    last:border-0
                                                "
                                            >

                                                <td className="
                                                    px-4
                                                    py-4
                                                    font-medium
                                                    text-secondary
                                                ">

                                                    {
                                                        appointment.patient_name
                                                    }

                                                </td>


                                                <td className="
                                                    px-4
                                                    py-4
                                                    text-gray-600
                                                ">

                                                    {
                                                        appointment.service_name
                                                    }

                                                </td>


                                                <td className="
                                                    px-4
                                                    py-4
                                                    text-gray-600
                                                ">

                                                    {
                                                        appointment.appointment_time
                                                    }

                                                </td>


                                                <td className="
                                                    px-4
                                                    py-4
                                                ">

                                                    <span className="
                                                        rounded-full
                                                        bg-primary/10
                                                        px-3
                                                        py-1
                                                        text-xs
                                                        font-semibold
                                                        text-primary
                                                    ">

                                                        {
                                                            appointment.status
                                                        }

                                                    </span>

                                                </td>

                                            </tr>

                                        )
                                    )}

                                </tbody>

                            </table>

                        </div>

                    )}

                </div>

            </div>

        </main>

    );

};


const StatisticCard = ({
    title,
    value,
    icon,
}) => {

    return (

        <div className="
            rounded-2xl
            bg-white
            p-6
            shadow-sm
            transition
            duration-300
            hover:-translate-y-1
            hover:shadow-md
        ">

            <div className="
                flex
                items-center
                justify-between
            ">

                <div>

                    <p className="
                        text-sm
                        text-gray-500
                    ">
                        {title}
                    </p>

                    <p className="
                        mt-2
                        text-3xl
                        font-bold
                        text-secondary
                    ">
                        {value ?? 0}
                    </p>

                </div>


                <div className="
                    flex
                    h-12
                    w-12
                    items-center
                    justify-center
                    rounded-xl
                    bg-primary/10
                    text-xl
                    text-primary
                ">

                    {icon}

                </div>

            </div>

        </div>

    );

};


export default DoctorDashboard;
