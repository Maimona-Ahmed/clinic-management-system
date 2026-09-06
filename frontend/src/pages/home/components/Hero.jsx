import { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    FaCalendarCheck,
    FaUserMd,
    FaClock,
    FaCheckCircle,
} from "react-icons/fa";

import { useAuth } from "../../../context/AuthContext";

import LoginModal from "../../../components/auth/LoginModal";
import RegisterModal from "../../../components/auth/RegisterModal";


export default function Hero() {

    const {
        isAuthenticated,
    } = useAuth();

    const navigate = useNavigate();


    const [showLogin, setShowLogin] =
        useState(false);

    const [showRegister, setShowRegister] =
        useState(false);


    // =========================================
    // BOOK APPOINTMENT
    // =========================================

    const handleAppointment = () => {

        if (isAuthenticated) {

            navigate("/appointments/create");

        } else {

            setShowLogin(true);

        }

    };


    // =========================================
    // OPEN REGISTER
    // =========================================

    const handleOpenRegister = () => {

        setShowLogin(false);
        setShowRegister(true);

    };


    // =========================================
    // OPEN LOGIN
    // =========================================

    const handleOpenLogin = () => {

        setShowRegister(false);
        setShowLogin(true);

    };


    return (

        <>

            {/* =====================================
                HERO
            ===================================== */}

            <section className="
                relative
                overflow-hidden
                bg-light
            ">

                <div className="
                    container-custom
                    grid
                    min-h-[calc(100vh-4rem)]
                    items-center
                    gap-12
                    py-12
                    lg:grid-cols-2
                    lg:py-0
                ">


                    {/* =================================
                        LEFT CONTENT
                    ================================= */}

                    <div className="
                        order-2
                        max-w-2xl
                        lg:order-1
                    ">


                        {/* Small Badge */}

                        <div className="
                            mb-5
                            inline-flex
                            items-center
                            gap-2
                            rounded-full
                            px-4
                            py-2
                            text-sm
                            font-medium
                            text-primary
                        ">

                            <FaUserMd />

                            Trusted Healthcare

                        </div>


                        {/* Heading */}

                        <h1 className="
                            text-4xl
                            font-bold
                            leading-tight
                            text-secondary
                            sm:text-5xl
                            lg:text-6xl
                        ">

                            Your Health,

                            <span className="
                                block
                                text-primary
                            ">
                                Our Priority
                            </span>

                        </h1>


                        {/* Description */}

                        <p className="
                            mt-6
                            max-w-xl
                            text-base
                            leading-7
                            text-gray-500
                            sm:text-lg
                        ">

                            Professional healthcare made
                            simple, accessible, and convenient.
                            Book appointments with trusted doctors
                            and receive the care you deserve.

                        </p>


                        {/* Buttons */}

                        <div className="
                            mt-8
                            flex
                            flex-col
                            gap-3
                            sm:flex-row
                        ">


                            {/* Appointment */}

                            <button
                                type="button"
                                onClick={
                                    handleAppointment
                                }
                                className="
                                    btn-primary
                                    inline-flex
                                    items-center
                                    justify-center
                                    gap-2
                                "
                            >

                                <FaCalendarCheck />

                                Book an Appointment

                            </button>


                            {/* Learn More */}

                            <a
                                href="#about"
                                className="
                                    btn-outline
                                    inline-flex
                                    items-center
                                    justify-center
                                "
                            >
                                Learn More
                            </a>

                        </div>


                        {/* =================================
                            FEATURES
                        ================================= */}

                        <div className="
                            mt-10
                            grid
                            grid-cols-1
                            gap-4
                            sm:grid-cols-3
                        ">


                            {/* Feature 1 */}

                            <div className="
                                flex
                                items-center
                                gap-3
                            ">

                                <FaCheckCircle
                                    className="
                                        shrink-0
                                        text-primary
                                    "
                                />

                                <span className="
                                    text-sm
                                    text-gray-600
                                ">
                                    Experienced Doctors
                                </span>

                            </div>


                            {/* Feature 2 */}

                            <div className="
                                flex
                                items-center
                                gap-3
                            ">

                                <FaCalendarCheck
                                    className="
                                        shrink-0
                                        text-primary
                                    "
                                />

                                <span className="
                                    text-sm
                                    text-gray-600
                                ">
                                    Easy Booking
                                </span>

                            </div>


                            {/* Feature 3 */}

                            <div className="
                                flex
                                items-center
                                gap-3
                            ">

                                <FaClock
                                    className="
                                        shrink-0
                                        text-primary
                                    "
                                />

                                <span className="
                                    text-sm
                                    text-gray-600
                                ">
                                    Quality Care
                                </span>

                            </div>

                        </div>

                    </div>


                    {/* =================================
                        RIGHT IMAGE
                    ================================= */}

                    <div className="
                        order-1
                        flex
                        h-full
                        items-center
                        justify-center
                        lg:order-2
                    ">

                        <div className="
                            relative
                            w-full
                            max-w-xl
                        ">


                            {/* Background Shape */}

                            {/* <div className="
                                absolute
                                inset-x-4
                                bottom-0
                                top-10
                                rounded-[3rem]
                                bg-primary/10
                            " /> */}


                            {/* Doctor Image */}

                            <div
                                className="
                                    relative
                                    mx-auto
                                    h-130
                                    w-130
                                    overflow-hidden
                                    sm:h-110
                                    lg:h-130
                                    rounded-[3rem]
                                "
                                style={{
                                    clipPath:
                                        "polygon(0 0, 100% 0, 100% 90%, 0 100%)",
                                }}
                            >

                                <img
                                    src="/images/doctor-hero.jpg"
                                    alt="Doctor"
                                    className="
                                        h-full
                                        w-full
                                        object-top
                                    "
                                />

                            </div>


                            {/* Floating Card */}

                            <div className="
                                absolute
                                bottom-8
                                left-4
                                flex
                                items-center
                                gap-3
                                rounded-2xl
                                bg-white
                                px-4
                                py-3
                                shadow-xl
                                sm:bottom-12
                                sm:left-0
                            ">

                                <div className="
                                    flex
                                    h-11
                                    w-11
                                    items-center
                                    justify-center
                                    rounded-full
                                    bg-primary/10
                                    text-primary
                                ">

                                    <FaUserMd />

                                </div>


                                <div>

                                    <p className="
                                        text-sm
                                        font-semibold
                                        text-secondary
                                    ">
                                        Professional Care
                                    </p>

                                    <p className="
                                        text-xs
                                        text-gray-500
                                    ">
                                        Your health matters
                                    </p>

                                </div>

                            </div>

                        </div>

                    </div>

                </div>

            </section>


            {/* =====================================
                LOGIN MODAL
            ===================================== */}

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


            {/* =====================================
                REGISTER MODAL
            ===================================== */}

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
