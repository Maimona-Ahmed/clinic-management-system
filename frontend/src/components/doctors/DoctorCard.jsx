import React from "react";

import {
    FaUserMd,
    FaArrowRight,
    FaMoneyBillWave,
} from "react-icons/fa";

import { useNavigate } from "react-router-dom";


const DoctorCard = ({ doctor }) => {

    const navigate = useNavigate();


    const fullName = [
        doctor.first_name,
        doctor.last_name,
    ]
        .filter(Boolean)
        .join(" ");


    return (

        <article
            className="
                group
                overflow-hidden
                rounded-2xl
                bg-white
                shadow-lg
                transition-all
                duration-300
                hover:-translate-y-2
                hover:shadow-xl
            "
        >

            {/* ================================
                Doctor Image
            ================================= */}

            <div
                className="
                    relative
                    flex
                    h-64
                    items-center
                    justify-center
                    overflow-hidden
                    bg-primary/10
                "
            >

                {doctor.profile_image ? (

                    <img
                        src={doctor.profile_image}
                        alt={`Dr. ${fullName}`}
                        className="
                            h-full
                            w-full
                            object-cover
                            transition-transform
                            duration-500
                            group-hover:scale-105
                        "
                    />

                ) : (

                    <div
                        className="
                            flex
                            h-28
                            w-28
                            items-center
                            justify-center
                            rounded-full
                            bg-white
                            text-6xl
                            text-primary
                            shadow-md
                        "
                    >

                        <FaUserMd />

                    </div>

                )}

            </div>


            {/* ================================
                Doctor Information
            ================================= */}

            <div className="p-6">


                {/* Name */}

                <h3
                    className="
                        truncate
                        text-xl
                        font-bold
                        text-secondary
                    "
                >

                    Dr. {fullName || "Doctor"}

                </h3>


                {/* Specialization */}

                <p
                    className="
                        mt-1
                        text-sm
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
                            mt-3
                            line-clamp-2
                            min-h-12
                            text-sm
                            leading-6
                            text-gray-500
                        "
                    >

                        {doctor.bio}

                    </p>

                )}


                {/* Fee */}

                <div
                    className="
                        mt-5
                        flex
                        items-center
                        gap-2
                        text-sm
                        text-gray-600
                    "
                >

                    <FaMoneyBillWave
                        className="text-primary"
                    />

                    <span>
                        Consultation:
                    </span>

                    <span
                        className="
                            font-bold
                            text-secondary
                        "
                    >

                        ${doctor.consultation_fee}

                    </span>

                </div>


                {/* View Profile */}

                <button
                    type="button"
                    onClick={() =>
                        navigate(
                            `/doctors/${doctor.id}`
                        )
                    }
                    className="
                        mt-5
                        inline-flex
                        items-center
                        gap-2
                        text-sm
                        font-semibold
                        text-primary
                        transition-all
                        duration-300
                        group-hover:gap-3
                    "
                >

                    View Profile

                    <FaArrowRight />

                </button>

            </div>

        </article>

    );

};


export default DoctorCard;
