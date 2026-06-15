/*
====================================================
usePolling Hook
====================================================

Reusable polling hook for:

- Cluster Status
- Workers
- Jobs
- Recovery Events
- Metrics

Features

✓ Auto polling
✓ Cleanup on unmount
✓ Error handling
✓ Pause / Resume

====================================================
*/

import {
    useEffect,
    useRef,
    useState
} from "react";


export default function usePolling(

    asyncFunction,

    interval = 5000,

    enabled = true
) {

    const [data, setData] =
        useState(null);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState(null);

    const intervalRef =
        useRef(null);


    // ==========================================
    // Fetch Function
    // ==========================================

    const fetchData =
        async () => {

            try {

                setError(null);

                const result =
                    await asyncFunction();

                setData(result);

            } catch (err) {

                console.error(
                    "Polling Error:",
                    err
                );

                setError(err);

            } finally {

                setLoading(false);
            }
        };


    // ==========================================
    // Polling Lifecycle
    // ==========================================

    useEffect(() => {

        if (!enabled) {

            return;
        }

        // Initial fetch

        fetchData();

        // Start polling

        intervalRef.current =
            setInterval(
                fetchData,
                interval
            );

        // Cleanup

        return () => {

            if (
                intervalRef.current
            ) {

                clearInterval(
                    intervalRef.current
                );
            }
        };

    }, [
        interval,
        enabled
    ]);


    // ==========================================
    // Manual Refresh
    // ==========================================

    const refresh =
        async () => {

            await fetchData();
        };


    // ==========================================
    // Stop Polling
    // ==========================================

    const stopPolling =
        () => {

            if (
                intervalRef.current
            ) {

                clearInterval(
                    intervalRef.current
                );
            }
        };


    return {

        data,

        loading,

        error,

        refresh,

        stopPolling
    };
}