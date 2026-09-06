import React from "react";

import {
    FaUserMd,
    FaStethoscope,
    FaCalendarAlt,
    FaClock,
    FaMoneyBillWave,
    FaArrowRight,
    FaTimes,
} from "react-icons/fa";


const AppointmentCard = ({
    appointment,
    onViewDetails,
    onCancel,
}) => {

    // ==========================================
    // Doctor
    // ==========================================

    const doctor =
        appointment.doctor || {};


    const doctorName =
        doctor.name ||
        "Doctor";


    const specialization =
        doctor.specialization ||
        "Medical Specialist";


    // ==========================================
    // Service
    // ==========================================

    const service =
        appointment.service || {};


    const serviceName =
        service.name ||
        "Medical Service";


    const servicePrice =
        service.price ??
        "0.00";


    const serviceDuration =
        service.duration;


    // ==========================================
    // Status
    // ==========================================

    const status =
        appointment.status ||
        "PENDING";


    const statusConfig = {

        PENDING: {
            label: "Pending",
            className:
                "bg-yellow-50 text-yellow-600",
        },

        CONFIRMED: {
            label: "Confirmed",
            className:
                "bg-green-50 text-green-600",
        },

        COMPLETED: {
            label: "Completed",
            className:
                "bg-blue-50 text-blue-600",
        },

        CANCELLED: {
            label: "Cancelled",
            className:
                "bg-red-50 text-red-600",
        },

    };


    const currentStatus =
        statusConfig[status] ||
        statusConfig.PENDING;


    // ==========================================
    // Cancel
    // ==========================================

    const canCancel =
        status === "PENDING" ||
        status === "CONFIRMED";


    return (

        <article
            className="
                group
                rounded-2xl
                bg-white
                p-5
                shadow-md
                transition
                duration-300
                hover:-translate-y-1
                hover:shadow-xl
            "
        >

            {/* =====================================
                Doctor Header
            ====================================== */}

            <div
                className="
                    flex
                    items-center
                    justify-between
                    gap-4
                "
            >

                {/* Doctor */}

                <div
                    className="
                        flex
                        min-w-0
                        items-center
                        gap-3
                    "
                >

                    {/* Doctor Icon */}

                    <div
                        className="
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
                        "
                    >

                        <FaUserMd />

                    </div>


                    {/* Doctor Info */}

                    <div className="
                        min-w-0
                    ">

                        <h3
                            className="
                                truncate
                                text-lg
                                font-bold
                                text-secondary
                            "
                        >

                            Dr. {doctorName}

                        </h3>


                        <p
                            className="
                                mt-1
                                truncate
                                text-sm
                                text-primary
                            "
                        >

                            {specialization}

                        </p>

                    </div>

                </div>


                {/* Status */}

                <span
                    className={`
                        shrink-0
                        rounded-full
                        px-3
                        py-1.5
                        text-xs
                        font-semibold
                        ${currentStatus.className}
                    `}
                >

                    {currentStatus.label}

                </span>

            </div>


            {/* =====================================
                Divider
            ====================================== */}

            <div
                className="
                    my-5
                    h-px
                    bg-gray-100
                "
            />


            {/* =====================================
                Appointment Information
            ====================================== */}

            <div
                className="
                    space-y-4
                "
            >

                {/* Service */}

                <div
                    className="
                        flex
                        items-center
                        gap-3
                    "
                >

                    <div
                        className="
                            flex
                            h-10
                            w-10
                            shrink-0
                            items-center
                            justify-center
                            rounded-xl
                            bg-primary/10
                            text-primary
                        "
                    >

                        <FaStethoscope />

                    </div>


                    <div>

                        <p
                            className="
                                text-xs
                                text-gray-400
                            "
                        >
                            Service
                        </p>


                        <p
                            className="
                                text-sm
                                font-semibold
                                text-secondary
                            "
                        >

                            {serviceName}

                        </p>

                    </div>

                </div>


                {/* Date + Time */}

                <div
                    className="
                        grid
                        grid-cols-2
                        gap-4
                    "
                >

                    {/* Date */}

                    <div
                        className="
                            flex
                            items-center
                            gap-3
                        "
                    >

                        <div
                            className="
                                flex
                                h-10
                                w-10
                                shrink-0
                                items-center
                                justify-center
                                rounded-xl
                                bg-primary/10
                                text-primary
                            "
                        >

                            <FaCalendarAlt />

                        </div>


                        <div
                            className="
                                min-w-0
                            "
                        >

                            <p
                                className="
                                    text-xs
                                    text-gray-400
                                "
                            >
                                Date
                            </p>


                            <p
                                className="
                                    truncate
                                    text-sm
                                    font-semibold
                                    text-secondary
                                "
                            >

                                {
                                    appointment.appointment_date
                                }

                            </p>

                        </div>

                    </div>


                    {/* Time */}

                    <div
                        className="
                            flex
                            items-center
                            gap-3
                        "
                    >

                        <div
                            className="
                                flex
                                h-10
                                w-10
                                shrink-0
                                items-center
                                justify-center
                                rounded-xl
                                bg-primary/10
                                text-primary
                            "
                        >

                            <FaClock />

                        </div>


                        <div>

                            <p
                                className="
                                    text-xs
                                    text-gray-400
                                "
                            >
                                Time
                            </p>


                            <p
                                className="
                                    text-sm
                                    font-semibold
                                    text-secondary
                                "
                            >

                                {
                                    appointment.appointment_time
                                }

                            </p>

                        </div>

                    </div>

                </div>


                {/* Price + Duration */}

                <div
                    className="
                        flex
                        flex-wrap
                        items-center
                        gap-5
                    "
                >

                    {/* Price */}

                    <div
                        className="
                            flex
                            items-center
                            gap-3
                        "
                    >

                        <div
                            className="
                                flex
                                h-10
                                w-10
                                shrink-0
                                items-center
                                justify-center
                                rounded-xl
                                bg-primary/10
                                text-primary
                            "
                        >

                            <FaMoneyBillWave />

                        </div>


                        <div>

                            <p
                                className="
                                    text-xs
                                    text-gray-400
                                "
                            >
                                Fee
                            </p>


                            <p
                                className="
                                    text-sm
                                    font-bold
                                    text-secondary
                                "
                            >

                                ${servicePrice}

                            </p>

                        </div>

                    </div>


                    {/* Duration */}

                    {serviceDuration && (

                        <div>

                            <p
                                className="
                                    text-xs
                                    text-gray-400
                                "
                            >
                                Duration
                            </p>


                            <p
                                className="
                                    text-sm
                                    font-semibold
                                    text-secondary
                                "
                            >

                                {serviceDuration} min

                            </p>

                        </div>

                    )}

                </div>

            </div>


            {/* =====================================
                Actions
            ====================================== */}

            <div
                className="
                    mt-6
                    flex
                    flex-col
                    gap-3
                    sm:flex-row
                "
            >

                {/* View Details */}

                <button
                    type="button"
                    onClick={() =>
                        onViewDetails?.(
                            appointment
                        )
                    }
                    className="
                        btn-primary
                        inline-flex
                        flex-1
                        items-center
                        justify-center
                        gap-2
                    "
                >

                    View Details

                    <FaArrowRight />

                </button>


                {/* Cancel */}

                {canCancel && (

                    <button
                        type="button"
                        onClick={() =>
                            onCancel?.(
                                appointment
                            )
                        }
                        className="
                            inline-flex
                            items-center
                            justify-center
                            gap-2
                            rounded-xl
                            border
                            border-red-200
                            px-5
                            py-3
                            text-sm
                            font-semibold
                            text-red-500
                            transition
                            hover:bg-red-50
                        "
                    >

                        <FaTimes />

                        Cancel

                    </button>

                )}

            </div>

        </article>

    );

};


export default AppointmentCard;
