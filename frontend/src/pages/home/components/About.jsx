import {
    FaCheck,
    FaUserMd,
    FaArrowRight,
} from "react-icons/fa";


export default function About() {

    return (

        <section
            id="about"
            className="
                w-full
                overflow-hidden
                bg-white
                py-16
                sm:py-20
                lg:py-24
            "
        >

            <div className="
                container-custom
                grid
                grid-cols-1
                items-center
                gap-12
                lg:grid-cols-2
                lg:gap-16
            ">


                {/* =================================
                    LEFT - OVERLAPPING IMAGES
                ================================= */}

                <div className="
                    relative
                    min-h-100
                    w-full
                    sm:min-h-125
                ">


                    {/* Background Image */}

                    <div className="
                        absolute
                        left-0
                        top-0
                        h-70
                        w-[72%]
                        overflow-hidden
                        rounded-2xl
                        shadow-lg
                        sm:h-90
                    ">

                        <img
                            src="/images/clinic.jpeg"
                            alt="Modern medical clinic"
                            className="
                                h-full
                                w-full
                                object-cover
                            "
                        />

                    </div>


                    {/* Front Image */}

                    <div className="
                        absolute
                        -bottom-10
                        right-0
                        h-70
                        w-[60%]
                        overflow-hidden
                        rounded-2xl
                        border-4
                        border-white
                        shadow-2xl
                        sm:h-90
                    ">

                        <img
                            src="/images/doctor-about.png"
                            alt="Professional doctor"
                            className="
                                h-full
                                w-full
                                object-cover
                            "
                        />

                    </div>



                </div>


                {/* =================================
                    RIGHT - CONTENT
                ================================= */}

                <div className="
                    flex
                    flex-col
                    items-start
                ">


                    {/* Small Label */}

                    <span className="
                        mb-4
                        text-sm
                        font-semibold
                        uppercase
                        tracking-wider
                        text-primary
                    ">

                        About Us

                    </span>


                    {/* Heading */}

                    <h2 className="
                        text-3xl
                        font-bold
                        leading-tight
                        text-secondary
                        sm:text-4xl
                        lg:text-5xl
                    ">

                        Healthcare You Can
                        
                        <span className="
                            block
                            text-primary
                        ">
                            Trust and Rely On
                        </span>

                    </h2>


                    {/* Description */}

                    <div className="
                        mt-6
                        space-y-4
                        text-sm
                        leading-7
                        text-gray-500
                        sm:text-base
                    ">

                        <p>
                            We are committed to providing high-quality
                            healthcare that is simple, accessible, and
                            centered around your needs.
                        </p>

                        <p>
                            Our team of experienced doctors and healthcare
                            professionals works together to provide reliable
                            medical care in a safe and comfortable environment.
                        </p>

                    </div>


                    {/* =================================
                        FEATURES
                    ================================= */}

                    <div className="
                        mt-7
                        space-y-4
                    ">


                        {/* Feature 1 */}

                        <div className="
                            flex
                            items-center
                            gap-3
                        ">

                            <span className="
                                flex
                                h-6
                                w-6
                                shrink-0
                                items-center
                                justify-center
                                rounded-full
                                bg-primary/10
                                text-xs
                                text-primary
                            ">

                                <FaCheck />

                            </span>

                            <span className="
                                text-sm
                                font-medium
                                text-secondary
                                sm:text-base
                            ">
                                Experienced and trusted doctors
                            </span>

                        </div>


                        {/* Feature 2 */}

                        <div className="
                            flex
                            items-center
                            gap-3
                        ">

                            <span className="
                                flex
                                h-6
                                w-6
                                shrink-0
                                items-center
                                justify-center
                                rounded-full
                                bg-primary/10
                                text-xs
                                text-primary
                            ">

                                <FaCheck />

                            </span>

                            <span className="
                                text-sm
                                font-medium
                                text-secondary
                                sm:text-base
                            ">
                                Easy and convenient appointment booking
                            </span>

                        </div>


                        {/* Feature 3 */}

                        <div className="
                            flex
                            items-center
                            gap-3
                        ">

                            <span className="
                                flex
                                h-6
                                w-6
                                shrink-0
                                items-center
                                justify-center
                                rounded-full
                                bg-primary/10
                                text-xs
                                text-primary
                            ">

                                <FaCheck />

                            </span>

                            <span className="
                                text-sm
                                font-medium
                                text-secondary
                                sm:text-base
                            ">
                                Patient-centered quality care
                            </span>

                        </div>

                    </div>


                    {/* =================================
                        BOTTOM
                    ================================= */}

                    <div className="
                        mt-8
                        flex
                        w-full
                        flex-col
                        gap-5
                        sm:flex-row
                        sm:items-center
                    ">


                        {/* Button */}

                        <a
                            href="#doctors"
                            className="
                                btn-primary
                                inline-flex
                                items-center
                                justify-center
                                gap-2
                            "
                        >

                            Learn More

                            <FaArrowRight />

                        </a>


                        {/* Doctor Info */}

                        <div className="
                            flex
                            items-center
                            gap-3
                            border-t
                            border-gray-100
                            pt-4
                            sm:border-l
                            sm:border-t-0
                            sm:pl-5
                            sm:pt-0
                        ">

                            <div className="
                                flex
                                h-11
                                w-11
                                items-center
                                justify-center
                                rounded-full
                                bg-primary/10
                                text-lg
                                text-primary
                            ">

                                <FaUserMd />

                            </div>


                            <div>

                                <p className="
                                    text-sm
                                    font-semibold
                                    text-secondary
                                ">
                                    Professional Care
                                </p>

                                <p className="
                                    text-xs
                                    text-gray-500
                                ">
                                    Your health matters
                                </p>

                            </div>

                        </div>

                    </div>

                </div>

            </div>

        </section>

    );
}
