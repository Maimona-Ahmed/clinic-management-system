import React, { useEffect, useState } from "react";

import api from "../../../components/api/axios";

import { SERVICES_ENDPOINTS } from "../../../components/api/endpoints";

import ServiceCard from "../../../components/services/ServiceCard";


const ServicesPage = () => {

    const [services, setServices] =
        useState([]);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState("");


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


    return (

        <main className="
            min-h-screen
            bg-light
            py-16
            md:py-20
        ">

            <div className="
                container-custom
            ">


                {/* Header */}

                <div className="
                    mb-12
                    text-center
                ">

                    <p className="
                        mb-2
                        text-sm
                        font-semibold
                        uppercase
                        tracking-wider
                        text-primary
                    ">
                        Healthcare Services
                    </p>


                    <h1 className="
                        text-4xl
                        font-bold
                        text-secondary
                        md:text-5xl
                    ">
                        Our Services
                    </h1>


                    <p className="
                        mx-auto
                        mt-4
                        max-w-2xl
                        text-gray-500
                    ">
                        Explore our professional healthcare
                        services and find the care you need.
                    </p>

                </div>


                {/* Loading */}

                {loading && (

                    <div className="
                        grid
                        grid-cols-1
                        gap-6
                        sm:grid-cols-2
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

                )}


                {/* Error */}

                {!loading && error && (

                    <p className="
                        text-center
                        text-red-500
                    ">
                        {error}
                    </p>

                )}


                {/* Services */}

                {!loading &&
                    !error &&
                    services.length > 0 && (

                        <div className="
                            grid
                            grid-cols-1
                            gap-6
                            sm:grid-cols-2
                            lg:grid-cols-3
                        ">

                            {services.map(
                                (service, index) => (

                                    <ServiceCard
                                        key={service.id}
                                        service={service}
                                        index={index}
                                    />

                                )
                            )}

                        </div>

                    )}


                {/* Empty */}

                {!loading &&
                    !error &&
                    services.length === 0 && (

                        <p className="
                            py-10
                            text-center
                            text-gray-500
                        ">
                            No services available.
                        </p>

                    )}

            </div>

        </main>

    );

};


export default ServicesPage;

