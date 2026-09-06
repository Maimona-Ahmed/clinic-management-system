import React, {
    useState,
} from "react";

import DoctorSidebar from "../components/doctors/DoctorSidbar";

import DoctorTopbar
    from "../components/doctors/DoctorTopbar";

import {
    Outlet,
} from "react-router-dom";


const DoctorDashboardLayout = () => {

    const [
        sidebarOpen,
        setSidebarOpen,
    ] = useState(false);


    return (

        <div className="
            min-h-screen
            bg-light
        ">

            {/* =========================
                Sidebar
            ========================== */}

            <DoctorSidebar
                isOpen={sidebarOpen}
                onClose={() =>
                    setSidebarOpen(false)
                }
            />


            {/* =========================
                Main
            ========================== */}

            <div className="
                lg:ml-72
            ">

                {/* Topbar */}

                <DoctorTopbar
                    onMenuClick={() =>
                        setSidebarOpen(true)
                    }
                />


                {/* Page Content */}

                <main className="
                    min-h-[calc(100vh-5rem)]
                    p-4
                    sm:p-6
                    lg:p-8
                ">

                    <Outlet />

                </main>

            </div>

        </div>

    );
};


export default DoctorDashboardLayout;
