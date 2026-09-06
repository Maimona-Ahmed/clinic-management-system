import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../../components/api/axios";

import {
    APPOINTMENTS_ENDPOINTS,
    CONSULTATIONS_ENDPOINTS,
} from "../../components/api/endpoints";

import {
    FaCheck,
    FaTimes,
    FaStethoscope,
    FaEye,
    FaSearch,
} from "react-icons/fa";


const DoctorAppointmentPage = () => {

    const navigate = useNavigate();

    const [appointments, setAppointments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const [search, setSearch] = useState("");
    const [statusFilter, setStatusFilter] = useState("ALL");

    const [actionLoading, setActionLoading] = useState(null);


    // ==================================================
    // Fetch Appointments
    // ==================================================

    const fetchAppointments = async () => {

        try {

            setLoading(true);
            setError("");

            const response = await api.get(
                APPOINTMENTS_ENDPOINTS.list
            );

            const data = response.data;

            setAppointments(
                Array.isArray(data)
                    ? data
                    : data.results || []
            );

        } catch (err) {

            console.error(
                "Failed to fetch appointments:",
                err
            );

            setError(
                "Unable to load appointments."
            );

        } finally {

            setLoading(false);

        }
    };


    useEffect(() => {

        fetchAppointments();

    }, []);


    // ==================================================
    // Confirm
    // ==================================================

    const handleConfirm = async (id) => {

        try {

            setActionLoading(id);

            await api.post(
                APPOINTMENTS_ENDPOINTS.confirm(id)
            );

            await fetchAppointments();

        } catch (err) {

            console.error(err);

            alert(
                err.response?.data?.detail ||
                "Unable to confirm appointment."
            );

        } finally {

            setActionLoading(null);

        }
    };


    // ==================================================
    // Cancel
    // ==================================================

    const handleCancel = async (id) => {

        const confirmed = window.confirm(
            "Are you sure you want to cancel this appointment?"
        );

        if (!confirmed) {
            return;
        }

        try {

            setActionLoading(id);

            await api.post(
                APPOINTMENTS_ENDPOINTS.cancel(id)
            );

            await fetchAppointments();

        } catch (err) {

            console.error(err);

            alert(
                err.response?.data?.detail ||
                "Unable to cancel appointment."
            );

        } finally {

            setActionLoading(null);

        }
    };


    // ==================================================
    // Start Consultation
    // ==================================================

    const handleStartConsultation = async (
        appointmentId
    ) => {

        try {

            setActionLoading(
                `consultation-${appointmentId}`
            );

            const response = await api.post(
                CONSULTATIONS_ENDPOINTS.start,
                {
                    appointment: appointmentId,
                }
            );

            const consultation = response.data;

            navigate(
                `/doctor/consultations/${consultation.id}`
            );

        } catch (err) {

            console.error(err);

            alert(
                err.response?.data?.detail ||
                "Unable to start consultation."
            );

        } finally {

            setActionLoading(null);

        }
    };


    // ==================================================
    // Statistics
    // ==================================================

    const totalAppointments =
        appointments.length;


    const today =
        new Date()
            .toISOString()
            .split("T")[0];


    const todayAppointments =
        appointments.filter(
            (appointment) =>
                appointment.appointment_date === today
        ).length;


    const pendingAppointments =
        appointments.filter(
            (appointment) =>
                appointment.status === "PENDING"
        ).length;


    const completedAppointments =
        appointments.filter(
            (appointment) =>
                appointment.status === "COMPLETED"
        ).length;


    // ==================================================
    // Search + Filter
    // ==================================================

    const filteredAppointments =
        appointments.filter(
            (appointment) => {

                const patientName =
                    appointment.patient_name ||
                    "Unknown Patient";

                const serviceName =
                    appointment.service.name ||
                    "Unknown Service";


                const searchValue =
                    search.toLowerCase();


                const matchesSearch =
                    patientName
                        .toLowerCase()
                        .includes(searchValue) ||
                    serviceName
                        .toLowerCase()
                        .includes(searchValue);


                const matchesStatus =
                    statusFilter === "ALL" ||
                    appointment.status === statusFilter;


                return (
                    matchesSearch &&
                    matchesStatus
                );
            }
        );


    // ==================================================
    // Status Style
    // ==================================================

    const getStatusClass = (status) => {

        if (status === "PENDING") {
            return "bg-yellow-100 text-yellow-700";
        }

        if (status === "CONFIRMED") {
            return "bg-blue-100 text-blue-700";
        }

        if (status === "COMPLETED") {
            return "bg-green-100 text-green-700";
        }

        if (status === "CANCELLED") {
            return "bg-red-100 text-red-700";
        }

        return "bg-gray-100 text-gray-600";
    };


    // ==================================================
    // Loading
    // ==================================================

    if (loading) {

        return (
            <main className="min-h-screen bg-light px-4 py-8 md:px-8">

                <div className="mx-auto max-w-7xl">

                    <div className="mb-8 h-10 w-64 animate-pulse rounded-lg bg-gray-200" />

                    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">

                        {[1, 2, 3, 4].map((item) => (

                            <div
                                key={item}
                                className="h-28 animate-pulse rounded-2xl bg-gray-200"
                            />

                        ))}

                    </div>

                    <div className="mt-8 h-96 animate-pulse rounded-2xl bg-gray-200" />

                </div>

            </main>
        );
    }


    // ==================================================
    // Error
    // ==================================================

    if (error) {

        return (
            <main className="min-h-screen bg-light px-4 py-8">

                <div className="mx-auto max-w-7xl text-center">

                    <p className="text-red-500">
                        {error}
                    </p>

                    <button
                        type="button"
                        onClick={fetchAppointments}
                        className="mt-4 rounded-lg bg-primary px-5 py-2 font-semibold text-white"
                    >
                        Try Again
                    </button>

                </div>

            </main>
        );
    }


    // ==================================================
    // Main
    // ==================================================

    return (

        <main className="min-h-screen bg-light px-4 py-8 md:px-8 md:py-10">

            <div className="mx-auto max-w-7xl">


                {/* Header */}

                <div className="mb-8">

                    <h1 className="text-3xl font-bold text-secondary">
                        Appointments
                    </h1>

                    <p className="mt-2 text-gray-500">
                        Manage your appointments and consultations.
                    </p>

                </div>


                {/* Statistics */}

                <div className="mb-8 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">


                    <div className="rounded-2xl bg-white p-5 shadow-sm">

                        <p className="text-sm text-gray-500">
                            Total Appointments
                        </p>

                        <h2 className="mt-2 text-3xl font-bold text-secondary">
                            {totalAppointments}
                        </h2>

                    </div>


                    <div className="rounded-2xl bg-white p-5 shadow-sm">

                        <p className="text-sm text-gray-500">
                            Today's Appointments
                        </p>

                        <h2 className="mt-2 text-3xl font-bold text-secondary">
                            {todayAppointments}
                        </h2>

                    </div>


                    <div className="rounded-2xl bg-white p-5 shadow-sm">

                        <p className="text-sm text-gray-500">
                            Pending
                        </p>

                        <h2 className="mt-2 text-3xl font-bold text-secondary">
                            {pendingAppointments}
                        </h2>

                    </div>


                    <div className="rounded-2xl bg-white p-5 shadow-sm">

                        <p className="text-sm text-gray-500">
                            Completed
                        </p>

                        <h2 className="mt-2 text-3xl font-bold text-secondary">
                            {completedAppointments}
                        </h2>

                    </div>

                </div>


                {/* Search + Filter */}

                <div className="mb-6 flex flex-col gap-4 rounded-2xl bg-white p-4 shadow-sm md:flex-row md:items-center md:justify-between">


                    <div className="relative w-full md:max-w-md">

                        <FaSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />

                        <input
                            type="text"
                            value={search}
                            onChange={(e) =>
                                setSearch(e.target.value)
                            }
                            placeholder="Search patient or service..."
                            className="w-full rounded-xl border border-gray-200 py-3 pl-11 pr-4 outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/10"
                        />

                    </div>


                    <select
                        value={statusFilter}
                        onChange={(e) =>
                            setStatusFilter(e.target.value)
                        }
                        className="rounded-xl border border-gray-200 bg-white px-4 py-3 outline-none focus:border-primary"
                    >

                        <option value="ALL">
                            All Statuses
                        </option>

                        <option value="PENDING">
                            Pending
                        </option>

                        <option value="CONFIRMED">
                            Confirmed
                        </option>

                        <option value="COMPLETED">
                            Completed
                        </option>

                        <option value="CANCELLED">
                            Cancelled
                        </option>

                    </select>

                </div>


                {/* Table */}

                <div className="overflow-hidden rounded-2xl bg-white shadow-sm">

                    <div className="overflow-x-auto">

                        <table className="min-w-full">

                            <thead className="border-b border-gray-100 bg-gray-50">

                                <tr>

                                    <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
                                        Patient
                                    </th>

                                    <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
                                        Service
                                    </th>

                                    <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
                                        Date
                                    </th>

                                    <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
                                        Time
                                    </th>

                                    <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
                                        Status
                                    </th>

                                    <th className="px-6 py-4 text-right text-xs font-semibold uppercase tracking-wider text-gray-500">
                                        Actions
                                    </th>

                                </tr>

                            </thead>


                            <tbody className="divide-y divide-gray-100">

                                {filteredAppointments.length > 0 ? (

                                    filteredAppointments.map(
                                        (appointment) => {

                                            const patientName =
                                                appointment.patient_name ||
                                                "Unknown Patient";

                                            const serviceName =
                                                appointment.service.name ||
                                                "Unknown Service";


                                            return (

                                                <tr
                                                    key={appointment.id}
                                                    className="transition hover:bg-gray-50"
                                                >

                                                    <td className="whitespace-nowrap px-6 py-5">

                                                        <div className="font-semibold text-secondary">
                                                            {patientName}
                                                        </div>

                                                    </td>


                                                    <td className="whitespace-nowrap px-6 py-5 text-sm text-gray-600">
                                                        {serviceName}
                                                    </td>


                                                    <td className="whitespace-nowrap px-6 py-5 text-sm text-gray-600">
                                                        {appointment.appointment_date}
                                                    </td>


                                                    <td className="whitespace-nowrap px-6 py-5 text-sm text-gray-600">
                                                        {appointment.appointment_time}
                                                    </td>


                                                    <td className="whitespace-nowrap px-6 py-5">

                                                        <span
                                                            className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${getStatusClass(
                                                                appointment.status
                                                            )}`}
                                                        >
                                                            {appointment.status}
                                                        </span>

                                                    </td>


                                                    <td className="whitespace-nowrap px-6 py-5">

                                                        <div className="flex justify-end gap-2">


                                                            {/* Pending */}

                                                            {appointment.status === "PENDING" && (

                                                                <>

                                                                    <button
                                                                        type="button"
                                                                        disabled={
                                                                            actionLoading ===
                                                                            appointment.id
                                                                        }
                                                                        onClick={() =>
                                                                            handleConfirm(
                                                                                appointment.id
                                                                            )
                                                                        }
                                                                        className="inline-flex items-center gap-2 rounded-lg bg-green-50 px-3 py-2 text-xs font-semibold text-green-600 hover:bg-green-100 disabled:opacity-50"
                                                                    >

                                                                        <FaCheck />

                                                                        Confirm

                                                                    </button>


                                                                    <button
                                                                        type="button"
                                                                        disabled={
                                                                            actionLoading ===
                                                                            appointment.id
                                                                        }
                                                                        onClick={() =>
                                                                            handleCancel(
                                                                                appointment.id
                                                                            )
                                                                        }
                                                                        className="inline-flex items-center gap-2 rounded-lg bg-red-50 px-3 py-2 text-xs font-semibold text-red-600 hover:bg-red-100 disabled:opacity-50"
                                                                    >

                                                                        <FaTimes />

                                                                        Cancel

                                                                    </button>

                                                                </>

                                                            )}


                                                            {/* Confirmed */}

                                                            {appointment.status === "CONFIRMED" && (

                                                                <>

                                                                    <button
                                                                        type="button"
                                                                        disabled={
                                                                            actionLoading ===
                                                                            `consultation-${appointment.id}`
                                                                        }
                                                                        onClick={() =>
                                                                            handleStartConsultation(
                                                                                appointment.id
                                                                            )
                                                                        }
                                                                        className="inline-flex items-center gap-2 rounded-lg bg-primary px-3 py-2 text-xs font-semibold text-white hover:opacity-90 disabled:opacity-50"
                                                                    >

                                                                        <FaStethoscope />

                                                                        Start Consultation

                                                                    </button>


                                                                    <button
                                                                        type="button"
                                                                        disabled={
                                                                            actionLoading ===
                                                                            appointment.id
                                                                        }
                                                                        onClick={() =>
                                                                            handleCancel(
                                                                                appointment.id
                                                                            )
                                                                        }
                                                                        className="inline-flex items-center gap-2 rounded-lg bg-red-50 px-3 py-2 text-xs font-semibold text-red-600 hover:bg-red-100 disabled:opacity-50"
                                                                    >

                                                                        <FaTimes />

                                                                        Cancel

                                                                    </button>

                                                                </>

                                                            )}


                                                            {/* Completed */}

                                                            {appointment.status === "COMPLETED" && (

                                                                <button
                                                                    type="button"
                                                                    onClick={() =>
                                                                        navigate(
                                                                            `/doctor/appointments/${appointment.id}`
                                                                        )
                                                                    }
                                                                    className="inline-flex items-center gap-2 rounded-lg bg-gray-100 px-3 py-2 text-xs font-semibold text-gray-600 hover:bg-gray-200"
                                                                >

                                                                    <FaEye />

                                                                    View

                                                                </button>

                                                            )}


                                                            {/* Cancelled */}

                                                            {appointment.status === "CANCELLED" && (

                                                                <span className="text-xs text-gray-400">
                                                                    No actions
                                                                </span>

                                                            )}

                                                        </div>

                                                    </td>

                                                </tr>

                                            );
                                        }
                                    )

                                ) : (

                                    <tr>

                                        <td
                                            colSpan="6"
                                            className="px-6 py-12 text-center text-gray-500"
                                        >
                                            No appointments found.
                                        </td>

                                    </tr>

                                )}

                            </tbody>

                        </table>

                    </div>

                </div>

            </div>

        </main>
    );
};


export default DoctorAppointmentPage;
