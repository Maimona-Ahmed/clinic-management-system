import { useState } from "react";

import {
    Link,
    NavLink,
} from "react-router-dom";

import {
    FaUserCircle,
    FaBars,
    FaTimes,
} from "react-icons/fa";

import { useAuth } from "../../context/AuthContext";

import LoginModal from "../auth/LoginModal";
import RegisterModal from "../auth/RegisterModal";


export default function Navbar() {

    const {
        user,
        isAuthenticated,
    } = useAuth();


    const [showLogin, setShowLogin] =
        useState(false);

    const [showRegister, setShowRegister] =
        useState(false);

    const [mobileMenuOpen, setMobileMenuOpen] =
        useState(false);


    // =========================================
    // OPEN LOGIN
    // =========================================

    const handleOpenLogin = () => {

        setMobileMenuOpen(false);
        setShowRegister(false);
        setShowLogin(true);

    };


    // =========================================
    // OPEN REGISTER
    // =========================================

    const handleOpenRegister = () => {

        setMobileMenuOpen(false);
        setShowLogin(false);
        setShowRegister(true);

    };


    // =========================================
    // CLOSE MOBILE MENU
    // =========================================

    const closeMobileMenu = () => {

        setMobileMenuOpen(false);

    };


    // =========================================
    // NAV LINK STYLE
    // =========================================

    const navLinkClass = ({ isActive }) =>
        isActive
            ? "font-medium text-primary"
            : "nav-link";


    return (

        <>

            {/* =====================================
                NAVBAR
            ===================================== */}

            <nav className="
                sticky
                top-0
                z-40
                border-b
                border-gray-100
                bg-white
            ">

                <div className="container-custom">

                    <div className="
                        flex
                        min-h-20
                        items-center
                        justify-between
                    ">


                        {/* =================================
                            LOGO + DESKTOP NAV
                        ================================= */}

                        <div className="
                            flex
                            items-center
                            gap-8
                        ">


                            {/* Logo */}

                            <Link
                                to="/"
                                onClick={closeMobileMenu}
                                className="
                                    shrink-0
                                    text-xl
                                    font-bold
                                    text-primary
                                "
                            >
                                Clinic
                            </Link>


                            {/* Desktop Navigation */}

                            <div className="
                                hidden
                                items-center
                                gap-6
                                md:flex
                            ">

                                <NavLink
                                    to="/"
                                    className={
                                        navLinkClass
                                    }
                                >
                                    Home
                                </NavLink>
                                <NavLink
                                    to="/services"
                                    className={
                                        navLinkClass
                                    }
                                >
                                    Services
                                </NavLink>
                                <NavLink
                                    to="/doctors"
                                    className={
                                        navLinkClass
                                    }
                                >
                                    Doctors
                                </NavLink>


                                <a
                                    href="/#about"
                                    className="nav-link"
                                >
                                    About Us
                                </a>


                                <a
                                    href="/#contact"
                                    className="nav-link"
                                >
                                    Contact Us
                                </a>

                            </div>

                        </div>


                        {/* =================================
                            DESKTOP RIGHT SIDE
                        ================================= */}

                        <div className="
                            hidden
                            items-center
                            gap-3
                            md:flex
                        ">


                            {isAuthenticated ? (

                                <>

                                    {/* Appointment */}

                                    <Link
                                        to="/appointments"
                                        className="btn-primary"
                                    >
                                        Appointment
                                    </Link>


                                    {/* Profile */}

                                    <Link
                                        to="/profile"
                                        title="Profile"
                                        className="
                                            flex
                                            items-center
                                            justify-center
                                            rounded-full
                                            p-1
                                            text-2xl
                                            text-gray-600
                                            transition
                                            hover:text-primary
                                        "
                                    >

                                        <FaUserCircle />

                                    </Link>

                                </>

                            ) : (

                                <button
                                    type="button"
                                    onClick={handleOpenLogin}
                                    className="btn-primary"
                                >
                                    Login
                                </button>

                            )}

                        </div>


                        {/* =================================
                            MOBILE MENU BUTTON
                        ================================= */}

                        <button
                            type="button"
                            onClick={() =>
                                setMobileMenuOpen(
                                    !mobileMenuOpen
                                )
                            }
                            className="
                                rounded-lg
                                p-2
                                text-xl
                                text-gray-700
                                hover:bg-gray-100
                                md:hidden
                            "
                            aria-label={
                                mobileMenuOpen
                                    ? "Close menu"
                                    : "Open menu"
                            }
                        >

                            {mobileMenuOpen ? (
                                <FaTimes />
                            ) : (
                                <FaBars />
                            )}

                        </button>

                    </div>


                    {/* =================================
                        MOBILE MENU
                    ================================= */}

                    {mobileMenuOpen && (

                        <div className="
                            border-t
                            border-gray-100
                            py-4
                            md:hidden
                        ">

                            <div className="
                                flex
                                flex-col
                                gap-2
                            ">


                                {/* Home */}

                                <NavLink
                                    to="/"
                                    onClick={
                                        closeMobileMenu
                                    }
                                    className={({
                                        isActive,
                                    }) =>
                                        `
                                        rounded-lg
                                        px-3
                                        py-2
                                        ${
                                            isActive
                                                ? "bg-primary/10 text-primary"
                                                : "text-gray-700 hover:bg-gray-50"
                                        }
                                        `
                                    }
                                >
                                    Home
                                </NavLink>


                                {/* About */}

                                <a
                                    href="/#about"
                                    onClick={
                                        closeMobileMenu
                                    }
                                    className="
                                        rounded-lg
                                        px-3
                                        py-2
                                        text-gray-700
                                        hover:bg-gray-50
                                    "
                                >
                                    About Us
                                </a>


                                {/* Contact */}

                                <a
                                    href="/#contact"
                                    onClick={
                                        closeMobileMenu
                                    }
                                    className="
                                        rounded-lg
                                        px-3
                                        py-2
                                        text-gray-700
                                        hover:bg-gray-50
                                    "
                                >
                                    Contact Us
                                </a>


                                {/* =================================
                                    AUTHENTICATED MOBILE
                                ================================= */}

                                {isAuthenticated ? (

                                    <>

                                        {/* Appointment */}

                                        <Link
                                            to="/appointments"
                                            onClick={
                                                closeMobileMenu
                                            }
                                            className="
                                                btn-primary
                                                mt-2
                                                text-center
                                            "
                                        >
                                            Appointment
                                        </Link>


                                        {/* Profile */}

                                        <Link
                                            to="/profile"
                                            onClick={
                                                closeMobileMenu
                                            }
                                            className="
                                                flex
                                                items-center
                                                gap-3
                                                rounded-lg
                                                px-3
                                                py-2
                                                text-gray-700
                                                hover:bg-gray-50
                                            "
                                        >

                                            <FaUserCircle
                                                className="text-xl"
                                            />

                                            <span>
                                                Profile
                                            </span>

                                        </Link>

                                    </>

                                ) : (

                                    /* =================================
                                        NOT AUTHENTICATED MOBILE
                                    ================================= */

                                    <button
                                        type="button"
                                        onClick={
                                            handleOpenLogin
                                        }
                                        className="
                                            btn-primary
                                            mt-2
                                            w-full
                                        "
                                    >
                                        Login
                                    </button>

                                )}

                            </div>

                        </div>

                    )}

                </div>

            </nav>


            {/* =========================================
                LOGIN MODAL
            ========================================= */}

            {showLogin && (

                <LoginModal

                    onClose={() =>
                        setShowLogin(false)
                    }

                    onRegister={
                        handleOpenRegister
                    }

                />

            )}


            {/* =========================================
                REGISTER MODAL
            ========================================= */}

            {showRegister && (

                <RegisterModal

                    onClose={() =>
                        setShowRegister(false)
                    }

                    onLogin={
                        handleOpenLogin
                    }

                />

            )}

        </>

    );
}
