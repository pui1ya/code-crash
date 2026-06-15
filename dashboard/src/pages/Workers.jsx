/*
====================================================
Workers Page
====================================================

Displays:

- All registered workers
- Worker status
- Current task
- Heartbeats
- Task statistics

====================================================
*/

import { useEffect, useState } from "react";
import WorkerTable from "../components/WorkerTable";

import {
    getWorkers
} from "../api/coordinatorApi";

import usePolling
from "../hooks/usePolling";

import {
    getWorkers
}
from "../api/coordinatorApi";



function Workers() {

    // const [workers, setWorkers] =
    //     useState([]);

    // const [loading, setLoading] =
    //     useState(true);

    // const [error, setError] =
    //     useState(null);


    // ==========================================
    // Fetch Workers
    // ==========================================

    const { data: workers, loading, error } = usePolling(

    getWorkers,

    3000
);

    // ==========================================
    // Loading State
    // ==========================================

    if (loading) {

        return (

            <div className="page-loading">

                <h2>
                    Loading Workers...
                </h2>

            </div>
        );
    }


    // ==========================================
    // Error State
    // ==========================================

    if (error) {

        return (

            <div className="page-error">

                <h2>
                    {error}
                </h2>

            </div>
        );
    }


    // ==========================================
    // Status Badge
    // ==========================================

    const getStatusClass =
        (status) => {

            switch (status) {

                case "IDLE":
                    return "status-idle";

                case "BUSY":
                    return "status-busy";

                case "DEAD":
                    return "status-dead";

                default:
                    return "status-unknown";
            }
        };


    return (

        <div className="workers-page">

            {/* ==================================
                PAGE HEADER
            =================================== */}

            <div className="page-header">

                <h1>
                    Worker Nodes
                </h1>

                <p>
                    Monitor worker health,
                    execution status,
                    and heartbeat activity.
                </p>

            </div>


            {/* ==================================
                SUMMARY BAR
            =================================== */}

            <div className="worker-summary">

                <div className="summary-card">

                    <h3>
                        Total Workers
                    </h3>

                    <span>
                        {workers.length}
                    </span>

                </div>

                <div className="summary-card">

                    <h3>
                        Active
                    </h3>

                    <span>

                        {
                            workers.filter(
                                worker =>
                                worker.status !==
                                "DEAD"
                            ).length
                        }

                    </span>

                </div>

                <div className="summary-card">

                    <h3>
                        Dead
                    </h3>

                    <span>

                        {
                            workers.filter(
                                worker =>
                                worker.status ===
                                "DEAD"
                            ).length
                        }

                    </span>

                </div>

            </div>


            {/* ==================================
                WORKER TABLE
            =================================== */}

            <div className="worker-table-container">

<WorkerTable workers={workers} />

            </div>

        </div>
    );
}

export default Workers;