import React, {
    useEffect,
    useState,
} from "react";

import {
    useNavigate,
    useSearchParams,
} from "react-router-dom";

import {
    FaArrowLeft,
    FaArrowRight,
    FaCalendarAlt,
    FaClock,
    FaMoneyBillWave,
    FaStethoscope,
    FaUserMd,
} from "react-icons/fa";

import api from "../../components/api/axios";

import {
    DOCTORS_ENDPOINTS,
    APPOINTMENTS_ENDPOINTS,
    DOCTOR_SLOTS_ENDPOINT,
} from "../../components/api/endpoints";


const AppointmentCreatePage = () => {

    const navigate = useNavigate();

    const [searchParams] =
        useSearchParams();


    // ==========================================
    // Doctor ID from URL
    // ==========================================

    const doctorIdFromUrl =
        searchParams.get("doctor");


    // ==========================================
    // State
    // ==========================================

    const [doctors, setDoctors] =
        useState([]);

    const [doctor, setDoctor] =
        useState(null);

    const [selectedDoctor, setSelectedDoctor] =
        useState(
            doctorIdFromUrl || ""
        );

    const [selectedService, setSelectedService] =
        useState("");

    const [selectedDate, setSelectedDate] =
        useState("");

    const [selectedTime, setSelectedTime] =
        useState("");

    const [notes, setNotes] =
        useState("");


    const [slots, setSlots] =
        useState([]);


    const [loadingDoctors, setLoadingDoctors] =
        useState(false);

    const [loadingDoctor, setLoadingDoctor] =
        useState(
            Boolean(doctorIdFromUrl)
        );

    const [loadingSlots, setLoadingSlots] =
        useState(false);

    const [booking, setBooking] =
        useState(false);


    const [error, setError] =
        useState("");

    const [success, setSuccess] =
        useState("");


    // ==========================================
    // Fetch Doctors
    // ==========================================

    useEffect(() => {

        const fetchDoctors = async () => {

            try {

                setLoadingDoctors(true);

                setError("");


                const response =
                    await api.get(
                        DOCTORS_ENDPOINTS.list
                    );


                setDoctors(
                    response.data.results ||
                    response.data
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

                setLoadingDoctors(false);

            }

        };


        /*
         * We only need the doctor list
         * when no doctor was provided
         * in the URL.
         */

        if (!doctorIdFromUrl) {

            fetchDoctors();

        }

    }, [doctorIdFromUrl]);


    // ==========================================
    // Fetch Selected Doctor
    // ==========================================

    useEffect(() => {

        const fetchDoctor = async () => {

            if (!selectedDoctor) {

                setDoctor(null);

                setSelectedService("");

                setSelectedTime("");

                setSlots([]);

                return;

            }


            try {

                setLoadingDoctor(true);

                setError("");


                const response =
                    await api.get(
                        DOCTORS_ENDPOINTS.detail(
                            selectedDoctor
                        )
                    );


                setDoctor(
                    response.data
                );


            } catch (error) {

                console.error(
                    "Failed to fetch doctor:",
                    error
                );

                setDoctor(null);

                setError(
                    "Unable to load doctor information."
                );

            } finally {

                setLoadingDoctor(false);

            }

        };


        fetchDoctor();

    }, [selectedDoctor]);


    // ==========================================
    // Doctor Change
    // ==========================================

    const handleDoctorChange = (event) => {

        const doctorId =
            event.target.value;


        setSelectedDoctor(
            doctorId
        );

        setSelectedService("");

        setSelectedDate("");

        setSelectedTime("");

        setSlots([]);

        setError("");

    };


    // ==========================================
    // Fetch Slots
    // ==========================================

    useEffect(() => {

        const fetchSlots = async () => {

            if (
                !selectedDoctor ||
                !selectedService ||
                !selectedDate
            ) {

                setSlots([]);

                setSelectedTime("");

                return;

            }


            try {

                setLoadingSlots(true);

                setError("");

                setSelectedTime("");


                const response =
                    await api.get(
                        DOCTOR_SLOTS_ENDPOINT(
                            selectedDoctor,
                            selectedService,
                            selectedDate
                        )
                    );


                setSlots(
                    response.data.slots || []
                );


            } catch (error) {

                console.error(
                    "Failed to fetch slots:",
                    error
                );

                setSlots([]);

                setError(
                    "Unable to load available time slots."
                );

            } finally {

                setLoadingSlots(false);

            }

        };


        fetchSlots();

    }, [
        selectedDoctor,
        selectedService,
        selectedDate,
    ]);


    // ==========================================
    // Doctor Data
    // ==========================================

    const fullName = doctor
        ? [
            doctor.first_name,
            doctor.last_name,
        ]
            .filter(Boolean)
            .join(" ")
        : "";


    const services =
        doctor?.services || [];


    const selectedServiceObject =
        services.find(
            (service) =>
                String(service.id) ===
                String(selectedService)
        );


    // ==========================================
    // Submit
    // ==========================================

    const handleSubmit = async (event) => {

        event.preventDefault();


        setError("");

        setSuccess("");


        if (
            !selectedDoctor ||
            !selectedService ||
            !selectedDate ||
            !selectedTime
        ) {

            setError(
                "Please select doctor, service, date and time."
            );

            return;

        }


        try {

            setBooking(true);


            await api.post(
                APPOINTMENTS_ENDPOINTS.create,
                {

                    doctor_service:
                        selectedService,

                    appointment_date:
                        selectedDate,

                    appointment_time:
                        selectedTime,

                    notes,

                }
            );


            setSuccess(
                "Appointment booked successfully."
            );


            setTimeout(() => {

                navigate(
                    "/appointments"
                );

            }, 1200);


        } catch (error) {

            console.error(
                "Failed to create appointment:",
                error
            );


            setError(
                error.response?.data?.detail ||
                "Unable to book appointment."
            );

        } finally {

            setBooking(false);

        }

    };


    // ==========================================
    // Loading Doctor
    // ==========================================

    if (
        loadingDoctor &&
        doctorIdFromUrl &&
        !doctor
    ) {

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
                        h-10
                        w-64
                        rounded
                        bg-gray-200
                    " />

                    <div className="
                        mt-8
                        h-125
                        rounded-3xl
                        bg-gray-200
                    " />

                </div>

            </main>

        );

    }


    // ==========================================
    // Doctor Error
    // ==========================================

    if (
        selectedDoctor &&
        !doctor &&
        !loadingDoctor
    ) {

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
                            "Doctor not found."}

                    </p>


                    <button
                        type="button"
                        onClick={() =>
                            navigate(
                                "/doctors"
                            )
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
                        navigate(
                            selectedDoctor
                                ? `/doctors/${selectedDoctor}`
                                : "/doctors"
                        )
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

                    Back

                </button>


                {/* =================================
                    Header
                ================================= */}

                <div className="
                    mb-10
                ">

                    <p className="
                        mb-2
                        text-sm
                        font-semibold
                        uppercase
                        tracking-wider
                        text-primary
                    ">

                        Appointment

                    </p>


                    <h1 className="
                        text-3xl
                        font-bold
                        text-secondary
                        md:text-5xl
                    ">

                        Book an Appointment

                    </h1>


                    <p className="
                        mt-3
                        max-w-2xl
                        text-sm
                        text-gray-500
                    ">

                        Choose a doctor, service,
                        date and available time.

                    </p>

                </div>


                <div className="
                    grid
                    grid-cols-1
                    gap-8
                    lg:grid-cols-3
                ">


                    {/* =================================
                        Doctor Summary
                    ================================= */}

                    <div className="
                        rounded-3xl
                        bg-white
                        p-6
                        shadow-md
                        lg:col-span-1
                    ">


                        {/* =================================
                            Doctor Selection
                        ================================= */}

                        {!doctorIdFromUrl && (

                            <div className="
                                mb-8
                            ">

                                <label className="
                                    mb-2
                                    block
                                    text-sm
                                    font-semibold
                                    text-secondary
                                ">

                                    Choose Doctor

                                </label>


                                <div className="
                                    relative
                                ">

                                    <FaUserMd
                                        className="
                                            absolute
                                            left-4
                                            top-1/2
                                            -translate-y-1/2
                                            text-primary
                                        "
                                    />


                                    <select
                                        value={
                                            selectedDoctor
                                        }
                                        onChange={
                                            handleDoctorChange
                                        }
                                        disabled={
                                            loadingDoctors
                                        }
                                        className="
                                            w-full
                                            rounded-xl
                                            border
                                            border-gray-200
                                            bg-white
                                            py-3
                                            pl-11
                                            pr-4
                                            text-sm
                                            outline-none
                                            transition
                                            focus:border-primary
                                            focus:ring-2
                                            focus:ring-primary/20
                                            disabled:cursor-not-allowed
                                            disabled:bg-gray-50
                                        "
                                    >

                                        <option value="">
                                            {
                                                loadingDoctors
                                                    ? "Loading doctors..."
                                                    : "Select a doctor"
                                            }
                                        </option>


                                        {doctors.map(
                                            (item) => {

                                                const name = [
                                                    item.first_name,
                                                    item.last_name,
                                                ]
                                                    .filter(Boolean)
                                                    .join(" ");


                                                return (

                                                    <option
                                                        key={
                                                            item.id
                                                        }
                                                        value={
                                                            item.id
                                                        }
                                                    >

                                                        Dr. {name}

                                                    </option>

                                                );

                                            }
                                        )}

                                    </select>

                                </div>

                            </div>

                        )}


                        {/* =================================
                            Selected Doctor
                        ================================= */}

                        {doctor ? (

                            <div>

                                <div className="
                                    flex
                                    items-center
                                    gap-4
                                ">

                                    {doctor.profile_image ? (

                                        <img
                                            src={
                                                doctor.profile_image
                                            }
                                            alt={
                                                `Dr. ${fullName}`
                                            }
                                            className="
                                                h-20
                                                w-20
                                                rounded-full
                                                object-cover
                                            "
                                        />

                                    ) : (

                                        <div className="
                                            flex
                                            h-20
                                            w-20
                                            items-center
                                            justify-center
                                            rounded-full
                                            bg-primary/10
                                            text-3xl
                                            text-primary
                                        ">

                                            <FaUserMd />

                                        </div>

                                    )}


                                    <div className="
                                        min-w-0
                                    ">

                                        <h2 className="
                                            truncate
                                            text-xl
                                            font-bold
                                            text-secondary
                                        ">

                                            Dr. {fullName}

                                        </h2>


                                        <p className="
                                            mt-1
                                            truncate
                                            text-sm
                                            text-primary
                                        ">

                                            {
                                                doctor.specialization
                                            }

                                        </p>

                                    </div>

                                </div>


                                {/* =================================
                                    Service Info
                                ================================= */}

                                {selectedServiceObject && (

                                    <div className="
                                        mt-8
                                        rounded-2xl
                                        bg-light
                                        p-4
                                    ">

                                        <div className="
                                            flex
                                            items-center
                                            gap-3
                                        ">

                                            <FaMoneyBillWave
                                                className="
                                                    text-primary
                                                "
                                            />

                                            <div>

                                                <p className="
                                                    text-xs
                                                    text-gray-500
                                                ">

                                                    Consultation Fee

                                                </p>

                                                <p className="
                                                    font-bold
                                                    text-secondary
                                                ">

                                                    $
                                                    {
                                                        selectedServiceObject.price
                                                    }

                                                </p>

                                            </div>

                                        </div>

                                    </div>

                                )}

                            </div>

                        ) : (

                            <div className="
                                flex
                                min-h-45
                                flex-col
                                items-center
                                justify-center
                                rounded-2xl
                                bg-light
                                p-6
                                text-center
                            ">

                                <FaUserMd
                                    className="
                                        mb-3
                                        text-4xl
                                        text-primary
                                    "
                                />

                                <p className="
                                    text-sm
                                    font-medium
                                    text-secondary
                                ">

                                    Select a doctor

                                </p>


                                <p className="
                                    mt-1
                                    text-xs
                                    text-gray-400
                                ">

                                    Doctor information
                                    will appear here.

                                </p>

                            </div>

                        )}

                    </div>


                    {/* =================================
                        Booking Form
                    ================================= */}

                    <form
                        onSubmit={
                            handleSubmit
                        }
                        className="
                            rounded-3xl
                            bg-white
                            p-6
                            shadow-md
                            lg:col-span-2
                            md:p-8
                        "
                    >


                        {/* =================================
                            Error
                        ================================= */}

                        {error && (

                            <div className="
                                mb-6
                                rounded-xl
                                bg-red-50
                                p-4
                                text-sm
                                text-red-600
                            ">

                                {error}

                            </div>

                        )}


                        {/* =================================
                            Success
                        ================================= */}

                        {success && (

                            <div className="
                                mb-6
                                rounded-xl
                                bg-green-50
                                p-4
                                text-sm
                                text-green-600
                            ">

                                {success}

                            </div>

                        )}


                        {/* =================================
                            Service
                        ================================= */}

                        <div className="
                            mb-6
                        ">

                            <label className="
                                mb-2
                                block
                                text-sm
                                font-semibold
                                text-secondary
                            ">

                                Choose Service

                            </label>


                            <div className="
                                relative
                            ">

                                <FaStethoscope
                                    className="
                                        absolute
                                        left-4
                                        top-1/2
                                        -translate-y-1/2
                                        text-primary
                                    "
                                />


                                <select
                                    value={
                                        selectedService
                                    }
                                    onChange={(
                                        event
                                    ) =>
                                        setSelectedService(
                                            event.target.value
                                        )
                                    }
                                    disabled={
                                        !doctor
                                    }
                                    className="
                                        w-full
                                        rounded-xl
                                        border
                                        border-gray-200
                                        bg-white
                                        py-3
                                        pl-11
                                        pr-4
                                        text-sm
                                        outline-none
                                        transition
                                        focus:border-primary
                                        focus:ring-2
                                        focus:ring-primary/20
                                        disabled:cursor-not-allowed
                                        disabled:bg-gray-50
                                    "
                                >

                                    <option value="">
                                        {
                                            doctor
                                                ? "Select a service"
                                                : "Select doctor first"
                                        }
                                    </option>


                                    {services.map(
                                        (service) => (

                                            <option
                                                key={
                                                    service.id
                                                }
                                                value={
                                                    service.id
                                                }
                                            >

                                                {
                                                    service.service_name
                                                }

                                            </option>

                                        )
                                    )}

                                </select>

                            </div>

                        </div>


                        {/* =================================
                            Date
                        ================================= */}

                        <div className="
                            mb-6
                        ">

                            <label className="
                                mb-2
                                block
                                text-sm
                                font-semibold
                                text-secondary
                            ">

                                Choose Date

                            </label>


                            <div className="
                                relative
                            ">

                                <FaCalendarAlt
                                    className="
                                        absolute
                                        left-4
                                        top-1/2
                                        -translate-y-1/2
                                        text-primary
                                    "
                                />


                                <input
                                    type="date"
                                    value={
                                        selectedDate
                                    }
                                    min={
                                        new Date()
                                            .toISOString()
                                            .split("T")[0]
                                    }
                                    disabled={
                                        !selectedService
                                    }
                                    onChange={(
                                        event
                                    ) =>
                                        setSelectedDate(
                                            event.target.value
                                        )
                                    }
                                    className="
                                        w-full
                                        rounded-xl
                                        border
                                        border-gray-200
                                        bg-white
                                        py-3
                                        pl-11
                                        pr-4
                                        text-sm
                                        outline-none
                                        transition
                                        focus:border-primary
                                        focus:ring-2
                                        focus:ring-primary/20
                                        disabled:cursor-not-allowed
                                        disabled:bg-gray-50
                                    "
                                />

                            </div>

                        </div>


                        {/* =================================
                            Slots
                        ================================= */}

                        {selectedDoctor &&
                            selectedService &&
                            selectedDate && (

                                <div className="
                                    mb-6
                                ">

                                    <label className="
                                        mb-3
                                        block
                                        text-sm
                                        font-semibold
                                        text-secondary
                                    ">

                                        Available Time

                                    </label>


                                    {loadingSlots ? (

                                        <div className="
                                            grid
                                            grid-cols-2
                                            gap-3
                                            sm:grid-cols-3
                                            md:grid-cols-4
                                        ">

                                            {[1, 2, 3, 4].map(
                                                (item) => (

                                                    <div
                                                        key={
                                                            item
                                                        }
                                                        className="
                                                            h-12
                                                            animate-pulse
                                                            rounded-xl
                                                            bg-gray-200
                                                        "
                                                    />

                                                )
                                            )}

                                        </div>

                                    ) : slots.length > 0 ? (

                                        <div className="
                                            grid
                                            grid-cols-2
                                            gap-3
                                            sm:grid-cols-3
                                            md:grid-cols-4
                                        ">

                                            {slots.map(
                                                (time) => (

                                                    <button
                                                        key={
                                                            time
                                                        }
                                                        type="button"
                                                        onClick={() =>
                                                            setSelectedTime(
                                                                time
                                                            )
                                                        }
                                                        className={`
                                                            inline-flex
                                                            items-center
                                                            justify-center
                                                            gap-2
                                                            rounded-xl
                                                            border
                                                            py-3
                                                            text-sm
                                                            font-semibold
                                                            transition

                                                            ${
                                                                selectedTime === time
                                                                    ? "border-primary bg-primary text-white"
                                                                    : "border-gray-200 bg-white text-secondary hover:border-primary hover:text-primary"
                                                            }
                                                        `}
                                                    >

                                                        <FaClock />

                                                        {time}

                                                    </button>

                                                )
                                            )}

                                        </div>

                                    ) : (

                                        <div className="
                                            rounded-xl
                                            bg-gray-50
                                            p-5
                                            text-center
                                            text-sm
                                            text-gray-500
                                        ">

                                            No available
                                            appointments
                                            for this date.

                                        </div>

                                    )}

                                </div>

                            )}


                        {/* =================================
                            Notes
                        ================================= */}

                        <div className="
                            mb-8
                        ">

                            <label className="
                                mb-2
                                block
                                text-sm
                                font-semibold
                                text-secondary
                            ">

                                Notes

                                <span className="
                                    ml-1
                                    font-normal
                                    text-gray-400
                                ">

                                    (Optional)

                                </span>

                            </label>


                            <textarea
                                value={
                                    notes
                                }
                                onChange={(
                                    event
                                ) =>
                                    setNotes(
                                        event.target.value
                                    )
                                }
                                rows={4}
                                placeholder="
                                    Write any additional notes...
                                "
                                className="
                                    w-full
                                    resize-none
                                    rounded-xl
                                    border
                                    border-gray-200
                                    px-4
                                    py-3
                                    text-sm
                                    outline-none
                                    transition
                                    focus:border-primary
                                    focus:ring-2
                                    focus:ring-primary/20
                                "
                            />

                        </div>


                        {/* =================================
                            Submit
                        ================================= */}

                        <button
                            type="submit"
                            disabled={
                                booking ||
                                !selectedDoctor ||
                                !selectedService ||
                                !selectedDate ||
                                !selectedTime
                            }
                            className="
                                btn-primary
                                inline-flex
                                w-full
                                items-center
                                justify-center
                                gap-2
                                disabled:cursor-not-allowed
                                disabled:opacity-50
                            "
                        >

                            {booking
                                ? "Booking..."
                                : "Book Appointment"
                            }


                            {!booking && (

                                <FaArrowRight />

                            )}

                        </button>

                    </form>

                </div>

            </div>

        </main>

    );

};


export default AppointmentCreatePage;
