import React from "react";

import {
    FaStethoscope,
    FaHeartbeat,
    FaTooth,
    FaEye,
    FaChild,
    FaFlask,
    FaArrowRight,
} from "react-icons/fa";
import { useNavigate } from "react-router-dom";


const serviceIcons = [
    FaStethoscope,
    FaHeartbeat,
    FaTooth,
    FaEye,
    FaChild,
    FaFlask,
];


const ServiceCard = ({ service, index = 0 }) => {

    const Icon =
        serviceIcons[index % serviceIcons.length];
    const navigate = useNavigate();


    return (

        <div className="
            group
            h-full
            rounded-2xl
            bg-white
            p-6
            shadow-lg
            transition
            duration-300
            hover:-translate-y-2
            hover:shadow-xl
        ">

            {/* Icon */}

            <div className="
                mb-5
                flex
                h-14
                w-14
                items-center
                justify-center
                rounded-2xl
                bg-primary/10
                text-2xl
                text-primary
                transition
                duration-300
                group-hover:bg-primary
                group-hover:text-white
            ">

                <Icon />

            </div>


            {/* Title */}

            <h3 className="
                text-xl
                font-bold
                text-secondary
            ">

                {service.name}

            </h3>


            {/* Description */}

            <p className="
                mt-3
                line-clamp-3
                text-sm
                leading-6
                text-gray-500
            ">

                {service.description ||
                    "Professional healthcare service provided by our experienced medical team."
                }

            </p>


            {/* Learn More */}

            <button
                type="button"
                onClick={()=>
                    navigate(`/services/${service.id}`)
                }
                className="
                    mt-5
                    inline-flex
                    items-center
                    gap-2
                    text-sm
                    font-semibold
                    text-primary
                    transition
                    group-hover:gap-3
                "
            >

                Learn More

                <FaArrowRight />

            </button>

        </div>

    );
};


export default ServiceCard;

