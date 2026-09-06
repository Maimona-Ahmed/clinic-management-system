import {
    Routes,
    Route,
    Navigate,
} from "react-router-dom";

import MainLayout from "../layouts/MainLayout";

import Home from "../pages/home/Home";

import ProtectedRoute from "./ProtectedRoute";

import ServicesPage
    from "../pages/home/services/ServicesPage";

import ServiceDetailsPage
    from "../pages/home/services/ServiceDetailsPage";

import DoctorsPage
    from "../pages/doctors/DoctorsPage";

import DoctorDetailsPage
    from "../pages/doctors/DoctorDetailsPage";

import AppointmentCreatePage
    from "../pages/appointemnts/AppointmentCreatePage";

import AppointmentsPage
    from "../pages/appointemnts/AppointmnetPage";


// ==========================================
// Doctor Dashboard
// ==========================================

import DoctorDashboardLayout
    from "../layouts/DoctorDashboardLayout";

import DoctorDashboardPage
    from "../pages/doctors/DoctorDashboardPage";
import DoctorAppointmentPage from "../pages/doctors/DoctorAppointmnetPage";

// import DoctorAppointmentsPage
//     from "../pages/doctors/DoctorAppointmentsPage";


export default function AppRoutes() {

    return (

        <Routes>


            {/* ==================================
                Main Layout
            ================================== */}

            <Route
                element={<MainLayout />}
            >

                {/* ==============================
                    Public
                ============================== */}

                <Route
                    path="/"
                    element={<Home />}
                />


                {/* Services */}

                <Route
                    path="/services"
                    element={<ServicesPage />}
                />

                <Route
                    path="/services/:id"
                    element={
                        <ServiceDetailsPage />
                    }
                />


                {/* Doctors */}

                <Route
                    path="/doctors"
                    element={<DoctorsPage />}
                />

                <Route
                    path="/doctors/:id"
                    element={
                        <DoctorDetailsPage />
                    }
                />


                {/* Create Appointment */}

                <Route
                    path="/appointments/create"
                    element={
                        <AppointmentCreatePage />
                    }
                />


                {/* ==============================
                    Protected
                ============================== */}

                <Route
                    path="/appointments"
                    element={
                        <ProtectedRoute>
                            <AppointmentsPage />
                        </ProtectedRoute>
                    }
                />

            </Route>


            {/* ==================================
                Doctor Dashboard
            ================================== */}

            <Route
                path="/doctor"
                element={
                    <ProtectedRoute>
                        <DoctorDashboardLayout />
                    </ProtectedRoute>
                }
            >

                {/* Dashboard */}

                <Route
                    path="dashboard"
                    element={
                        <DoctorDashboardPage />
                    }
                />
                


                {/* Appointments */}

                <Route
                    path="appointments"
                    element={
                        <DoctorAppointmentPage/>
                    }
                />

            </Route>


            {/* ==================================
                Unknown Route
            ================================== */}

            <Route
                path="*"
                element={
                    <Navigate
                        to="/"
                        replace
                    />
                }
            />

        </Routes>

    );

}

