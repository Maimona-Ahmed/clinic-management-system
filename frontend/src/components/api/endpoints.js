export const AUTH_ENDPOINTS = {
    login: "/auth/login/",
    register: "/auth/register/",
    me: "/auth/me/",
    refresh: "/auth/token/refresh/",
    logout: "/auth/logout/",
    changePassword: "/auth/change-password/",
    forgotPassword: "/auth/forgot-password/",
    resetPassword: "/auth/reset-password/",
};


export const SERVICES_ENDPOINTS = {

    list: "/services/",

    detail: (id) =>
        `/services/${id}/`,

};


export const DOCTORS_ENDPOINTS = {

    list: "/doctors/",

    detail: (id) =>
        `/doctors/${id}/`,

};
export const APPOINTMENTS_ENDPOINTS = {

    list: "/appointments/",

    create: "/appointments/",

    detail: (id) =>
        `/appointments/${id}/`,

    confirm: (id) =>
        `/appointments/${id}/confirm/`,

    cancel: (id) =>
        `/appointments/${id}/cancel/`,

};


export const DOCTOR_DASHBOARD_ENDPOINTS ={
    dashboard:"/doctors/dashboard/",
};
export const DOCTOR_SLOTS_ENDPOINT = (
    doctor,
    service,
    date
) =>
    `/doctor-slots/?doctor=${doctor}&service=${service}&date=${date}`;


    export const CONSULTATIONS_ENDPOINTS = {
    start: "/consultations/start/",

    detail: (id) =>
        `/medical-records/consultations/${id}/`,

    complete: (id) =>
        `/medical-records/consultations/${id}/complete/`,

    diagnoses: (id) =>
        `/medical-records/consultations/${id}/diagnoses/`,

    notes: (id) =>
        `/medical-records/consultations/${id}/notes/`,

    prescription: (id) =>
        `/medical-records/consultations/${id}/prescription/`,

    tests: (id) =>
        `/medical-records/consultations/${id}/tests/`,
};

