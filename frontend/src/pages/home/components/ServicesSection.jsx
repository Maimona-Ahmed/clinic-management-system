import React, { useEffect, useState } from "react";

import api from "../../../components/api/axios";

import { SERVICES_ENDPOINTS } from "../../../components/api/endpoints";
    

import ServiceCard from "../../../components/services/ServiceCard";

import {
    FaArrowRight,
} from "react-icons/fa";

import { useNavigate } from "react-router-dom";


const ServicesSection = () => {

    const [services, setServices] =
        useState([]);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState("");


    const navigate = useNavigate();


    useEffect(() => {

        const fetchServices = async () => {

            try {

                setLoading(true);

                const response =
                    await api.get(
                        SERVICES_ENDPOINTS.list
                    );


                const data =
                    response.data;


                setServices(
                    Array.isArray(data)
                        ? data
                        : data.results || []
                );


            } catch (error) {

                console.error(
                    "Failed to fetch services:",
                    error
                );

                setError(
                    "Unable to load services."
                );

            } finally {

                setLoading(false);

            }

        };


        fetchServices();

    }, []);


    // ==============================
    // Loading
    // ==============================

    if (loading) {

        return (

            <section
                id="services"
                className="
                    section
                    bg-light
                    py-16
                    md:py-20
                "
            >

                <div className="
                    container-custom
                ">

                    <div className="
                        grid
                        grid-cols-1
                        gap-6
                        md:grid-cols-2
                        lg:grid-cols-3
                    ">

                        {[1, 2, 3, 4, 5, 6].map(
                            (item) => (

                                <div
                                    key={item}
                                    className="
                                        h-64
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
                id="services"
                className="
                    bg-light
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
    // Display 6 services
    // ==============================

    const displayedServices =
        services.slice(0, 6);


    return (

        <section
            id="services"
            className="
                bg-light
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
                        What We Offer
                    </p>


                    <h2 className="
                        section-title
                        text-secondary
                    ">
                        Our Services
                    </h2>


                    <p className="
                        section-description
                        mx-auto
                        max-w-2xl
                    ">
                        Professional healthcare services
                        designed to meet your needs.
                    </p>

                </div>


                {/* ==========================
                    Services Grid
                ========================== */}

                {displayedServices.length > 0 ? (

                    <div className="
                        grid
                        grid-cols-1
                        gap-6
                        sm:grid-cols-2
                        lg:grid-cols-3
                    ">

                        {displayedServices.map(
                            (service, index) => (

                                <ServiceCard
                                    key={service.id}
                                    service={service}
                                    index={index}
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
                        No services available.
                    </p>

                )}


                {/* ==========================
                    View All
                ========================== */}

                {services.length > 6 && (

                    <div className="
                        mt-10
                        flex
                        justify-center
                    ">

                        <button
                            type="button"
                            onClick={() =>
                                navigate("/services")
                            }
                            className="
                                btn-outline
                                inline-flex
                                items-center
                                gap-2
                            "
                        >

                            View All

                            <FaArrowRight />

                        </button>

                    </div>

                )}

            </div>

        </section>

    );

};


export default ServicesSection;
