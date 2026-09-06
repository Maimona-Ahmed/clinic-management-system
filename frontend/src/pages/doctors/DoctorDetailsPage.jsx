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
    FaMoneyBillWave,
    FaUserMd,
} from "react-icons/fa";

import api from "../../components/api/axios";

import { DOCTORS_ENDPOINTS } from "../../components/api/endpoints";


const DoctorDetailsPage = () => {

    const { id } = useParams();

    const navigate = useNavigate();


    const [doctor, setDoctor] =
        useState(null);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState("");


    useEffect(() => {

        const fetchDoctor = async () => {

            try {

                setLoading(true);

                setError("");


                const response =
                    await api.get(
                        DOCTORS_ENDPOINTS.detail(id)
                    );


                setDoctor(response.data);


            } catch (error) {

                console.error(
                    "Failed to fetch doctor:",
                    error
                );


                setError(
                    "Unable to load doctor information."
                );

            } finally {

                setLoading(false);

            }

        };


        if (id) {
            fetchDoctor();
        }

    }, [id]);


    /* ================================
       Loading
    ================================= */

    if (loading) {

        return (

            <main
                className="
                    min-h-screen
                    bg-light
                    py-16
                "
            >

                <div
                    className="
                        container-custom
                    "
                >

                    <div
                        className="
                            animate-pulse
                        "
                    >

                        <div
                            className="
                                mb-8
                                h-6
                                w-24
                                rounded
                                bg-gray-200
                            "
                        />


                        <div
                            className="
                                grid
                                grid-cols-1
                                gap-10
                                lg:grid-cols-2
                            "
                        >

                            <div
                                className="
                                    h-125
                                    rounded-2xl
                                    bg-gray-200
                                "
                            />

                            <div
                                className="
                                    space-y-5
                                "
                            >

                                <div
                                    className="
                                        h-10
                                        w-3/4
                                        rounded
                                        bg-gray-200
                                    "
                                />

                                <div
                                    className="
                                        h-6
                                        w-1/2
                                        rounded
                                        bg-gray-200
                                    "
                                />

                                <div
                                    className="
                                        h-24
                                        w-full
                                        rounded
                                        bg-gray-200
                                    "
                                />

                            </div>

                        </div>

                    </div>

                </div>

            </main>

        );

    }


    /* ================================
       Error
    ================================= */

    if (error || !doctor) {

        return (

            <main
                className="
                    flex
                    min-h-screen
                    items-center
                    justify-center
                    bg-light
                    px-4
                "
            >

                <div
                    className="
                        text-center
                    "
                >

                    <p
                        className="
                            mb-6
                            text-red-500
                        "
                    >

                        {error ||
                            "Doctor not found."}

                    </p>


                    <button
                        type="button"
                        onClick={() =>
                            navigate("/doctors")
                        }
                        className="
                            btn-primary
                            inline-flex
                            items-center
                            gap-2
                        "
                    >

                        <FaArrowLeft />

                        Back to Doctors

                    </button>

                </div>

            </main>

        );

    }


    const fullName = [
        doctor.first_name,
        doctor.last_name,
    ]
        .filter(Boolean)
        .join(" ");


    const services =
        doctor.services || [];


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

                {/* ================================
                    Back
                ================================= */}

                <button
                    type="button"
                    onClick={() =>
                        navigate("/doctors")
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

                    Back to Doctors

                </button>


                {/* ================================
                    Doctor Main Information
                ================================= */}

                <section
                    className="
                        grid
                        grid-cols-1
                        gap-8
                        lg:grid-cols-2
                        lg:gap-12
                    "
                >

                    {/* Image */}

                    <div
                        className="
                            flex
                            min-h-100
                            items-center
                            justify-center
                            overflow-hidden
                            rounded-3xl
                            bg-primary/10
                            md:min-h-125
                        "
                    >

                        {doctor.profile_image ? (

                            <img
                                src={
                                    doctor.profile_image
                                }
                                alt={
                                    `Dr. ${fullName}`
                                }
                                className="
                                    h-full
                                    max-h-150
                                    w-full
                                    object-cover
                                "
                            />

                        ) : (

                            <div
                                className="
                                    flex
                                    h-36
                                    w-36
                                    items-center
                                    justify-center
                                    rounded-full
                                    bg-white
                                    text-7xl
                                    text-primary
                                    shadow-lg
                                "
                            >

                                <FaUserMd />

                            </div>

                        )}

                    </div>


                    {/* Information */}

                    <div
                        className="
                            flex
                            flex-col
                            justify-center
                        "
                    >

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

                            Medical Specialist

                        </p>


                        <h1
                            className="
                                text-3xl
                                font-bold
                                text-secondary
                                md:text-5xl
                            "
                        >

                            Dr. {fullName}

                        </h1>


                        <p
                            className="
                                mt-3
                                text-lg
                                font-semibold
                                text-primary
                            "
                        >

                            {doctor.specialization}

                        </p>


                        {/* Bio */}

                        {doctor.bio && (

                            <p
                                className="
                                    mt-6
                                    max-w-xl
                                    leading-7
                                    text-gray-500
                                "
                            >

                                {doctor.bio}

                            </p>

                        )}


                        {/* Fee */}

                        <div
                            className="
                                mt-8
                                flex
                                items-center
                                gap-3
                                rounded-xl
                                bg-white
                                p-5
                                shadow-sm
                            "
                        >

                            <div
                                className="
                                    flex
                                    h-12
                                    w-12
                                    items-center
                                    justify-center
                                    rounded-full
                                    bg-primary/10
                                    text-primary
                                "
                            >

                                <FaMoneyBillWave />

                            </div>


                            <div>

                                <p
                                    className="
                                        text-sm
                                        text-gray-500
                                    "
                                >
                                    Consultation Fee
                                </p>


                                <p
                                    className="
                                        text-xl
                                        font-bold
                                        text-secondary
                                    "
                                >

                                    $
                                    {
                                        doctor.consultation_fee
                                    }

                                </p>

                            </div>

                        </div>


                        {/* Appointment */}

                        <button
                            type="button"
                            onClick={() =>
                                navigate(
                                    `/appointments/create?doctor=${doctor.id}`
                                )
                            }
                            className="
                                btn-primary
                                mt-6
                                inline-flex
                                w-fit
                                items-center
                                gap-2
                            "
                        >

                            Book Appointment

                            <FaArrowRight />

                        </button>

                    </div>

                </section>


                {/* ================================
                    Services
                ================================= */}

                <section
                    className="
                        mt-16
                        md:mt-20
                    "
                >

                    <div
                        className="
                            mb-8
                        "
                    >

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

                            Available Services

                        </p>


                        <h2
                            className="
                                text-3xl
                                font-bold
                                text-secondary
                            "
                        >

                            Services Offered

                        </h2>

                    </div>


                    {services.length > 0 ? (

                        <div
                            className="
                                grid
                                grid-cols-1
                                gap-5
                                sm:grid-cols-2
                                lg:grid-cols-3
                            "
                        >

                            {services.map(
                                (item) => (

                                    <div
                                        key={item.id}
                                        className="
                                            rounded-2xl
                                            bg-white
                                            p-6
                                            shadow-md
                                            transition
                                            duration-300
                                            hover:-translate-y-1
                                            hover:shadow-lg
                                        "
                                    >

                                        <h3
                                            className="
                                                text-lg
                                                font-bold
                                                text-secondary
                                            "
                                        >

                                            {
                                                item.service_name
                                            }

                                        </h3>


                                        <div
                                            className="
                                                mt-4
                                                flex
                                                flex-wrap
                                                gap-4
                                                text-sm
                                                text-gray-500
                                            "
                                        >

                                            {/* Price */}

                                            <div
                                                className="
                                                    flex
                                                    items-center
                                                    gap-2
                                                "
                                            >

                                                <FaMoneyBillWave
                                                    className="
                                                        text-primary
                                                    "
                                                />

                                                $
                                                {
                                                    item.price
                                                }

                                            </div>


                                            {/* Duration */}

                                            <div
                                                className="
                                                    flex
                                                    items-center
                                                    gap-2
                                                "
                                            >

                                                <FaClock
                                                    className="
                                                        text-primary
                                                    "
                                                />

                                                {
                                                    item.duration
                                                }{" "}
                                                min

                                            </div>

                                        </div>

                                    </div>

                                )
                            )}

                        </div>

                    ) : (

                        <div
                            className="
                                rounded-2xl
                                bg-white
                                p-8
                                text-center
                                shadow-sm
                            "
                        >

                            <p
                                className="
                                    text-gray-500
                                "
                            >

                                No services available
                                for this doctor.

                            </p>

                        </div>

                    )}

                </section>

            </div>

        </main>

    );

};


export default DoctorDetailsPage;
