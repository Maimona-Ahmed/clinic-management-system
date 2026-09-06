import React from "react";

import {
    FaBars,
    FaBell,
    FaUserMd,
} from "react-icons/fa";


const DoctorTopbar = ({
    onMenuClick,
}) => {

    return (

        <header
            className="
                sticky
                top-0
                z-30
                flex
                h-20
                items-center
                justify-between
                border-b
                border-gray-100
                bg-white
                px-4
                shadow-sm
                sm:px-6
                lg:px-8
            "
        >

            {/* Left */}

            <div
                className="
                    flex
                    items-center
                    gap-4
                "
            >

                {/* Mobile Menu */}

                <button
                    type="button"
                    onClick={onMenuClick}
                    className="
                        rounded-xl
                        p-2.5
                        text-secondary
                        transition
                        hover:bg-gray-100
                        lg:hidden
                    "
                >

                    <FaBars />

                </button>


                <div>

                    <p
                        className="
                            text-xs
                            text-gray-400
                        "
                    >
                        Welcome back
                    </p>

                    <h2
                        className="
                            text-lg
                            font-bold
                            text-secondary
                        "
                    >
                        Doctor Dashboard
                    </h2>

                </div>

            </div>


            {/* Right */}

            <div
                className="
                    flex
                    items-center
                    gap-3
                "
            >

                {/* Notifications */}

                <button
                    type="button"
                    className="
                        relative
                        rounded-xl
                        p-3
                        text-gray-500
                        transition
                        hover:bg-gray-100
                        hover:text-primary
                    "
                >

                    <FaBell />

                    <span
                        className="
                            absolute
                            right-2
                            top-2
                            h-2
                            w-2
                            rounded-full
                            bg-red-500
                        "
                    />

                </button>


                {/* Doctor Profile */}

                <button
                    type="button"
                    className="
                        flex
                        items-center
                        gap-3
                        rounded-xl
                        p-1.5
                        transition
                        hover:bg-gray-50
                    "
                >

                    <div
                        className="
                            flex
                            h-10
                            w-10
                            items-center
                            justify-center
                            rounded-full
                            bg-primary/10
                            text-primary
                        "
                    >

                        <FaUserMd />

                    </div>


                    <div
                        className="
                            hidden
                            text-left
                            sm:block
                        "
                    >

                        <p
                            className="
                                text-sm
                                font-semibold
                                text-secondary
                            "
                        >
                            Doctor
                        </p>

                        <p
                            className="
                                text-xs
                                text-gray-400
                            "
                        >
                            Medical Specialist
                        </p>

                    </div>

                </button>

            </div>

        </header>

    );
};


export default DoctorTopbar;

