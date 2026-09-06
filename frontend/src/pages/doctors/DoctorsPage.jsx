import React, {
    useEffect,
    useState,
} from "react";

import api from "../../components/api/axios";

import { DOCTORS_ENDPOINTS } from "../../components/api/endpoints";

import DoctorCard from "../../components/doctors/DoctorCard";


const DoctorsPage = () => {

    const [doctors, setDoctors] =
        useState([]);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState("");


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


                {/* ==========================
                    Header
                ========================== */}

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
                        Our Medical Team
                    </p>


                    <h1 className="
                        text-4xl
                        font-bold
                        text-secondary
                        md:text-5xl
                    ">
                        Our Doctors
                    </h1>


                    <p className="
                        mx-auto
                        mt-4
                        max-w-2xl
                        text-gray-500
                    ">
                        Meet our experienced doctors and
                        find the right healthcare professional
                        for your needs.
                    </p>

                </div>


                {/* ==========================
                    Loading
                ========================== */}

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
                                        h-117
                                        animate-pulse
                                        rounded-2xl
                                        bg-gray-200
                                    "
                                />

                            )
                        )}

                    </div>

                )}


                {/* ==========================
                    Error
                ========================== */}

                {!loading && error && (

                    <p className="
                        text-center
                        text-red-500
                    ">
                        {error}
                    </p>

                )}


                {/* ==========================
                    Doctors
                ========================== */}

                {!loading &&
                    !error &&
                    doctors.length > 0 && (

                        <div className="
                            grid
                            grid-cols-1
                            gap-6
                            sm:grid-cols-2
                            lg:grid-cols-3
                        ">

                            {doctors.map(
                                (doctor) => (

                                    <DoctorCard
                                        key={doctor.id}
                                        doctor={doctor}
                                    />

                                )
                            )}

                        </div>

                    )}


                {/* ==========================
                    Empty
                ========================== */}

                {!loading &&
                    !error &&
                    doctors.length === 0 && (

                        <p className="
                            py-10
                            text-center
                            text-gray-500
                        ">
                            No doctors available.
                        </p>

                    )}

            </div>

        </main>

    );

};


export default DoctorsPage;
