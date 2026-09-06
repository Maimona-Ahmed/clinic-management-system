import React from "react";

import {
    FaTachometerAlt,
    FaCalendarAlt,
    FaUsers,
    FaFileMedical,
    FaStethoscope,
    FaMoneyBillWave,
    FaCog,
    FaSignOutAlt,
    FaTimes,
} from "react-icons/fa";

import { NavLink } from "react-router-dom";


const DoctorSidebar = ({
    isOpen,
    onClose,
}) => {

    const navigationItems = [
        {
            label: "Dashboard",
            path: "/doctor/dashboard",
            icon: FaTachometerAlt,
        },
        {
            label: "Appointments",
            path: "/doctor/appointments",
            icon: FaCalendarAlt,
        },
        {
            label: "Patients",
            path: "/doctor/patients",
            icon: FaUsers,
        },
        {
            label: "Medical Records",
            path: "/doctor/medical-records",
            icon: FaFileMedical,
        },
        {
            label: "Services",
            path: "/doctor/services",
            icon: FaStethoscope,
        },
        {
            label: "Payments",
            path: "/doctor/payments",
            icon: FaMoneyBillWave,
        },
        {
            label: "Settings",
            path: "/doctor/settings",
            icon: FaCog,
        },
    ];


    return (
        <>
            {/* Mobile Overlay */}

            {isOpen && (
                <div
                    onClick={onClose}
                    className="
                        fixed
                        inset-0
                        z-40
                        bg-black/40
                        lg:hidden
                    "
                />
            )}


            <aside
                className={`
                    fixed
                    left-0
                    top-0
                    z-50
                    flex
                    h-screen
                    w-72
                    flex-col
                    bg-secondary
                    shadow-xl
                    transition-transform
                    duration-300
                    lg:translate-x-0
                    ${
                        isOpen
                            ? "translate-x-0"
                            : "-translate-x-full"
                    }
                `}
            >

                {/* =========================
                    Logo
                ========================== */}

                <div className="
                    flex
                    h-20
                    items-center
                    justify-between
                    border-b
                    border-white/10
                    px-6
                ">

                    <div>

                        <h1 className="
                            text-xl
                            font-bold
                            text-white
                        ">
                            MediCare
                        </h1>

                        <p className="
                            mt-1
                            text-xs
                            text-white/50
                        ">
                            Doctor Portal
                        </p>

                    </div>


                    {/* Mobile Close */}

                    <button
                        type="button"
                        onClick={onClose}
                        className="
                            rounded-lg
                            p-2
                            text-white/70
                            transition
                            hover:bg-white/10
                            hover:text-white
                            lg:hidden
                        "
                    >
                        <FaTimes />
                    </button>

                </div>


                {/* =========================
                    Navigation
                ========================== */}

                <nav className="
                    flex-1
                    space-y-1
                    overflow-y-auto
                    px-4
                    py-6
                ">

                    {navigationItems.map(
                        (item) => {

                            const Icon =
                                item.icon;

                            return (

                                <NavLink
                                    key={
                                        item.path
                                    }
                                    to={
                                        item.path
                                    }
                                    onClick={
                                        onClose
                                    }
                                    className={({
                                        isActive,
                                    }) => `
                                        flex
                                        items-center
                                        gap-3
                                        rounded-xl
                                        px-4
                                        py-3
                                        text-sm
                                        font-medium
                                        transition
                                        ${
                                            isActive
                                                ? "bg-primary text-white shadow-md"
                                                : "text-white/70 hover:bg-white/10 hover:text-white"
                                        }
                                    `}
                                >

                                    <Icon className="
                                        text-lg
                                    " />

                                    <span>
                                        {item.label}
                                    </span>

                                </NavLink>

                            );
                        }
                    )}

                </nav>


                {/* =========================
                    Logout
                ========================== */}

                <div className="
                    border-t
                    border-white/10
                    p-4
                ">

                    <button
                        type="button"
                        className="
                            flex
                            w-full
                            items-center
                            gap-3
                            rounded-xl
                            px-4
                            py-3
                            text-sm
                            font-medium
                            text-white/70
                            transition
                            hover:bg-red-500/10
                            hover:text-red-400
                        "
                    >

                        <FaSignOutAlt />

                        <span>
                            Logout
                        </span>

                    </button>

                </div>

            </aside>
        </>
    );
};


export default DoctorSidebar;
