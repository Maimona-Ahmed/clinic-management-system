import React, {
    useEffect,
    useState,
} from "react";

import api from "../../../components/api/axios";
import { DOCTORS_ENDPOINTS } from "../../../components/api/endpoints";

import DoctorCard from "../../../components/doctors/DoctorCard";
import {
    FaArrowRight,
} from "react-icons/fa";

import {
    useNavigate,
} from "react-router-dom";


const DoctorsSection = () => {
    const [doctors, setDoctors] =
        useState([]);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState("");


    const navigate = useNavigate();
    


    useEffect(() => {

        const fetchDoctors = async () => {

            try {

                setLoading(true);

                const response =
                    await api.get(
                        DOCTORS_ENDPOINTS.list
                    );


                const data =
                    response.data;


                setDoctors(
                    Array.isArray(data)
                        ? data
                        : data.results || []
                );


            } catch (error) {

                console.error(
                    "Failed to fetch doctors:",
                    error
                );

                setError(
                    "Unable to load doctors."
                );

            } finally {

                setLoading(false);

            }

        };


        fetchDoctors();

    }, []);


    // ==============================
    // Loading
    // ==============================

    if (loading) {

        return (

            <section
                id="doctors"
                className="
                    bg-white
                    py-16
                    md:py-20
                "
            >

                <div className="
                    container-custom
                ">


                    {/* Header Skeleton */}

                    <div className="
                        mb-10
                        text-center
                    ">

                        <div className="
                            mx-auto
                            mb-3
                            h-4
                            w-28
                            animate-pulse
                            rounded
                            bg-gray-200
                        " />

                        <div className="
                            mx-auto
                            h-10
                            w-64
                            animate-pulse
                            rounded
                            bg-gray-200
                        " />

                    </div>


                    {/* Cards Skeleton */}

                    <div className="
                        grid
                        grid-cols-1
                        gap-6
                        sm:grid-cols-2
                        lg:grid-cols-3
                    ">

                        {[1, 2, 3].map(
                            (item) => (

                                <div
                                    key={item}
                                    className="
                                        h-117
                                        animate-pulse
                                        rounded-2xl
                                        bg-gray-200
                                    "
                                />

                            )
                        )}

                    </div>

                </div>

            </section>

        );

    }


    // ==============================
    // Error
    // ==============================

    if (error) {

        return (

            <section
                id="doctors"
                className="
                    bg-white
                    py-16
                    md:py-20
                "
            >

                <div className="
                    container-custom
                    text-center
                ">

                    <p className="
                        text-red-500
                    ">
                        {error}
                    </p>

                </div>

            </section>

        );

    }


    // ==============================
    // Display 3 doctors
    // ==============================

    const displayedDoctors =
        doctors.slice(0, 3);
    


    return (

        <section
            id="doctors"
            className="
                bg-white
                py-16
                md:py-20
            "
        >

            <div className="
                container-custom
            ">


                {/* ==========================
                    Section Header
                ========================== */}

                <div className="
                    mb-10
                    text-center
                    md:mb-12
                ">

                    <p className="
                        mb-2
                        text-sm
                        font-semibold
                        uppercase
                        tracking-wider
                        text-primary
                    ">
                        Our Medical Team
                    </p>


                    <h2 className="
                        section-title
                        text-secondary
                    ">
                        Meet Our Doctors
                    </h2>


                    <p className="
                        section-description
                        mx-auto
                        max-w-2xl
                    ">
                        Meet our experienced doctors and
                        healthcare professionals who are
                        dedicated to your health.
                    </p>

                </div>


                {/* ==========================
                    Doctors Grid
                ========================== */}

                {displayedDoctors.length > 0 ? (

                    <div className="
                        grid
                        grid-cols-1
                        gap-6
                        sm:grid-cols-2
                        lg:grid-cols-3
                    ">

                        {displayedDoctors.map(
                            (doctor) => (

                                <DoctorCard
                                    key={doctor.id}
                                    doctor={doctor}
                                />

                            )
                        )}

                    </div>

                ) : (

                    <p className="
                        py-10
                        text-center
                        text-gray-500
                    ">
                        No doctors available.
                    </p>

                )}


                {/* ==========================
                    View All
                ========================== */}

                {doctors.length > 3 && (

                    <div className="
                        mt-10
                        flex
                        justify-center
                    ">

                        <button
                            type="button"
                            onClick={() =>
                                navigate("/doctors")
                            }
                            className="
                                btn-outline
                                inline-flex
                                items-center
                                gap-2
                            "
                        >

                            View All Doctors

                            <FaArrowRight />

                        </button>

                    </div>

                )}

            </div>

        </section>

    );

};


export default DoctorsSection;

