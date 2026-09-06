import React, {
    useEffect,
    useState,
} from "react";

import {
    useNavigate,
    useParams,
} from "react-router-dom";

import {
    FaArrowLeft,
    FaArrowRight,
    FaClock,
    FaUserMd,
    FaMoneyBillWave,
    FaStethoscope,
} from "react-icons/fa";

import api from "../../../components/api/axios";

import { SERVICES_ENDPOINTS } from "../../../components/api/endpoints";


const ServiceDetailsPage = () => {

    const {
        id,
    } = useParams();

    const navigate =
        useNavigate();


    // ==========================================
    // State
    // ==========================================

    const [service, setService] =
        useState(null);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState("");


    // ==========================================
    // Fetch Service Details
    // ==========================================

    useEffect(() => {

        const fetchService = async () => {

            try {

                setLoading(true);

                setError("");


                const response =
                    await api.get(
                        SERVICES_ENDPOINTS.detail(id)
                    );


                setService(
                    response.data
                );


            } catch (error) {

                console.error(
                    "Failed to fetch service:",
                    error
                );

                setError(
                    "Unable to load service details."
                );

            } finally {

                setLoading(false);

            }

        };


        if (id) {

            fetchService();

        }

    }, [id]);


    // ==========================================
    // Loading
    // ==========================================

    if (loading) {

        return (

            <main className="
                min-h-screen
                bg-light
                py-16
            ">

                <div className="
                    container-custom
                    animate-pulse
                ">

                    <div className="
                        h-8
                        w-32
                        rounded
                        bg-gray-200
                    " />

                    <div className="
                        mt-8
                        h-52
                        rounded-3xl
                        bg-gray-200
                    " />

                    <div className="
                        mt-8
                        h-10
                        w-48
                        rounded
                        bg-gray-200
                    " />

                    <div className="
                        mt-6
                        grid
                        grid-cols-1
                        gap-5
                        md:grid-cols-2
                    ">

                        {[1, 2, 3, 4].map(
                            (item) => (

                                <div
                                    key={item}
                                    className="
                                        h-48
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
    // Error / Not Found
    // ==========================================

    if (error || !service) {

        return (

            <main className="
                flex
                min-h-screen
                items-center
                justify-center
                bg-light
                px-4
            ">

                <div className="
                    text-center
                ">

                    <p className="
                        mb-6
                        text-red-500
                    ">

                        {error ||
                            "Service not found."}

                    </p>


                    <button
                        type="button"
                        onClick={() =>
                            navigate("/services")
                        }
                        className="
                            btn-primary
                            inline-flex
                            items-center
                            gap-2
                        "
                    >

                        <FaArrowLeft />

                        Back to Services

                    </button>

                </div>

            </main>

        );

    }


    // ==========================================
    // Data
    // ==========================================

    const doctors =
        service.doctors || [];


    return (

        <main className="
            min-h-screen
            bg-light
            py-12
            md:py-16
        ">

            <div className="
                container-custom
            ">


                {/* =================================
                    Back
                ================================= */}

                <button
                    type="button"
                    onClick={() =>
                        navigate("/services")
                    }
                    className="
                        mb-8
                        inline-flex
                        items-center
                        gap-2
                        text-sm
                        font-semibold
                        text-primary
                        transition
                        hover:gap-3
                    "
                >

                    <FaArrowLeft />

                    Back to Services

                </button>


                {/* =================================
                    Service Header
                ================================= */}

                <section className="
                    rounded-3xl
                    bg-white
                    p-6
                    shadow-md
                    md:p-8
                ">

                    <div className="
                        flex
                        flex-col
                        gap-6
                        md:flex-row
                        md:items-center
                    ">


                        {/* Icon */}

                        <div className="
                            flex
                            h-20
                            w-20
                            shrink-0
                            items-center
                            justify-center
                            rounded-2xl
                            bg-primary/10
                            text-4xl
                            text-primary
                        ">

                            <FaStethoscope />

                        </div>


                        {/* Information */}

                        <div>

                            <p className="
                                mb-2
                                text-sm
                                font-semibold
                                uppercase
                                tracking-wider
                                text-primary
                            ">

                                Medical Service

                            </p>


                            <h1 className="
                                text-3xl
                                font-bold
                                text-secondary
                                md:text-4xl
                            ">

                                {service.name}

                            </h1>


                            <p className="
                                mt-4
                                max-w-3xl
                                leading-7
                                text-gray-500
                            ">

                                {service.description ||
                                    "Professional healthcare service provided by our experienced medical team."
                                }

                            </p>

                        </div>

                    </div>

                </section>


                {/* =================================
                    Doctors Section
                ================================= */}

                <section className="
                    mt-12
                ">


                    <div className="
                        mb-8
                    ">

                        <p className="
                            mb-2
                            text-sm
                            font-semibold
                            uppercase
                            tracking-wider
                            text-primary
                        ">

                            Medical Team

                        </p>


                        <h2 className="
                            text-2xl
                            font-bold
                            text-secondary
                            md:text-3xl
                        ">

                            Doctors Providing This Service

                        </h2>


                        <p className="
                            mt-2
                            text-gray-500
                        ">

                            Choose a doctor and book
                            your appointment.

                        </p>

                    </div>


                    {/* =================================
                        Empty Doctors
                    ================================= */}

                    {doctors.length === 0 ? (

                        <div className="
                            rounded-2xl
                            bg-white
                            p-10
                            text-center
                            shadow-md
                        ">

                            <FaUserMd
                                className="
                                    mx-auto
                                    mb-4
                                    text-4xl
                                    text-gray-300
                                "
                            />

                            <p className="
                                text-gray-500
                            ">

                                No doctors are currently
                                providing this service.

                            </p>

                        </div>

                    ) : (


                        /* =================================
                            Doctors Grid
                        ================================= */

                        <div className="
                            grid
                            grid-cols-1
                            gap-6
                            md:grid-cols-2
                        ">

                            {doctors.map(
                                (doctor) => (

                                    <article
                                        key={
                                            doctor.doctor
                                        }
                                        className="
                                            rounded-2xl
                                            bg-white
                                            p-6
                                            shadow-md
                                            transition
                                            duration-300
                                            hover:-translate-y-1
                                            hover:shadow-xl
                                        "
                                    >

                                        {/* Doctor */}

                                        <div className="
                                            flex
                                            items-center
                                            gap-4
                                        ">

                                            <div className="
                                                flex
                                                h-14
                                                w-14
                                                shrink-0
                                                items-center
                                                justify-center
                                                rounded-full
                                                bg-primary/10
                                                text-2xl
                                                text-primary
                                            ">

                                                <FaUserMd />

                                            </div>


                                            <div className="
                                                min-w-0
                                            ">

                                                <h3 className="
                                                    truncate
                                                    text-lg
                                                    font-bold
                                                    text-secondary
                                                ">

                                                    Dr. {
                                                        doctor.doctor_name
                                                    }

                                                </h3>


                                                <p className="
                                                    mt-1
                                                    text-sm
                                                    text-primary
                                                ">

                                                    Available
                                                    Specialist

                                                </p>

                                            </div>

                                        </div>


                                        {/* Divider */}

                                        <div className="
                                            my-5
                                            h-px
                                            bg-gray-100
                                        " />


                                        {/* Price + Duration */}

                                        <div className="
                                            grid
                                            grid-cols-2
                                            gap-4
                                        ">


                                            {/* Price */}

                                            <div className="
                                                flex
                                                items-center
                                                gap-3
                                            ">

                                                <div className="
                                                    flex
                                                    h-10
                                                    w-10
                                                    items-center
                                                    justify-center
                                                    rounded-xl
                                                    bg-primary/10
                                                    text-primary
                                                ">

                                                    <FaMoneyBillWave />

                                                </div>


                                                <div>

                                                    <p className="
                                                        text-xs
                                                        text-gray-400
                                                    ">

                                                        Fee

                                                    </p>


                                                    <p className="
                                                        text-sm
                                                        font-bold
                                                        text-secondary
                                                    ">

                                                        ${doctor.price}

                                                    </p>

                                                </div>

                                            </div>


                                            {/* Duration */}

                                            <div className="
                                                flex
                                                items-center
                                                gap-3
                                            ">

                                                <div className="
                                                    flex
                                                    h-10
                                                    w-10
                                                    items-center
                                                    justify-center
                                                    rounded-xl
                                                    bg-primary/10
                                                    text-primary
                                                ">

                                                    <FaClock />

                                                </div>


                                                <div>

                                                    <p className="
                                                        text-xs
                                                        text-gray-400
                                                    ">

                                                        Duration

                                                    </p>


                                                    <p className="
                                                        text-sm
                                                        font-semibold
                                                        text-secondary
                                                    ">

                                                        {
                                                            doctor.duration
                                                        }{" "}
                                                        min

                                                    </p>

                                                </div>

                                            </div>

                                        </div>


                                        {/* Book */}

                                        <button
                                            type="button"
                                            onClick={() =>
                                                navigate(
                                                    `/appointments/create?doctor=${doctor.doctor}&service=${service.id}`
                                                )
                                            }
                                            className="
                                                btn-primary
                                                mt-6
                                                inline-flex
                                                w-full
                                                items-center
                                                justify-center
                                                gap-2
                                            "
                                        >

                                            Book Appointment

                                            <FaArrowRight />

                                        </button>

                                    </article>

                                )
                            )}

                        </div>

                    )}

                </section>

            </div>

        </main>

    );

};


export default ServiceDetailsPage;
