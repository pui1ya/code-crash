/*
====================================================
CrashReduce Coordinator API Client
====================================================

Responsibilities

1. Create Axios instance
2. Centralize API calls
3. Error handling
4. Timeout configuration

====================================================
*/

import axios from "axios";


// ====================================================
// Axios Instance
// ====================================================

const api = axios.create({

    baseURL: "/api",

    timeout: 10000,

    headers: {
        "Content-Type": "application/json"
    }
});


// ====================================================
// Request Interceptor
// ====================================================

api.interceptors.request.use(

    (config) => {

        console.log(
            `[API] ${config.method?.toUpperCase()} ${config.url}`
        );

        return config;
    },

    (error) => {

        return Promise.reject(error);
    }
);


// ====================================================
// Response Interceptor
// ====================================================

api.interceptors.response.use(

    (response) => response,

    (error) => {

        console.error(
            "[API ERROR]",
            error.response?.data || error.message
        );

        return Promise.reject(error);
    }
);


// ====================================================
// Cluster APIs
// ====================================================

export const getClusterStatus = async () => {

    const response =
        await api.get("/cluster");

    return response.data;
};


// ====================================================
// Worker APIs
// ====================================================

export const getWorkers = async () => {

    const response =
        await api.get("/workers");

    return response.data;
};


export const getWorker = async (
    workerId
) => {

    const response =
        await api.get(
            `/workers/${workerId}`
        );

    return response.data;
};


// ====================================================
// Job APIs
// ====================================================

export const getJobs = async () => {

    const response =
        await api.get("/jobs");

    return response.data;
};


export const getJob = async (
    jobId
) => {

    const response =
        await api.get(
            `/jobs/${jobId}`
        );

    return response.data;
};


export const submitJob = async (
    payload
) => {

    const response =
        await api.post(
            "/jobs",
            payload
        );

    return response.data;
};


// ====================================================
// Task APIs
// ====================================================

export const getTasks = async () => {

    const response =
        await api.get("/tasks");

    return response.data;
};


export const getTask = async (
    taskId
) => {

    const response =
        await api.get(
            `/tasks/${taskId}`
        );

    return response.data;
};


// ====================================================
// Recovery APIs
// ====================================================

export const getRecoveryEvents =
    async () => {

        const response =
            await api.get(
                "/recovery"
            );

        return response.data;
    };


// ====================================================
// Metrics APIs
// ====================================================

export const getMetrics =
    async () => {

        const response =
            await api.get(
                "/metrics"
            );

        return response.data;
    };


// ====================================================
// Health Check
// ====================================================

export const getHealth =
    async () => {

        const response =
            await api.get(
                "/health"
            );

        return response.data;
    };


// ====================================================
// Export Instance
// ====================================================

export default api;