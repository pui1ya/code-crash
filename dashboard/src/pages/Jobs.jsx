/*
====================================================
Jobs Page
====================================================

Displays:

- Submitted Jobs
- Job Progress
- Map Progress
- Reduce Progress
- Job Status
- Execution Time

====================================================
*/

import { useEffect, useState } from "react";
import JobTable from "../components/JobTable";
import {
    getJobs
} from "../api/coordinatorApi";
import usePolling
from "../hooks/usePolling";

import {
    getWorkers
}
from "../api/coordinatorApi";


function Jobs() {
    // ==========================================
    // Fetch Jobs
    // ==========================================

    const {

    data: jobs,

    loading

} = usePolling(

    getJobs,

    2000
);


    // ==========================================
    // Loading
    // ==========================================

    if (loading) {

        return (

            <div className="page-loading">

                <h2>
                    Loading Jobs...
                </h2>

            </div>
        );
    }


    // ==========================================
    // Error
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
    // Status Styling
    // ==========================================

    const getStatusClass =
        (status) => {

            switch (status) {

                case "RUNNING":
                    return "job-running";

                case "COMPLETED":
                    return "job-completed";

                case "FAILED":
                    return "job-failed";

                case "PENDING":
                    return "job-pending";

                default:
                    return "job-unknown";
            }
        };


    return (

        <div className="jobs-page">

            {/* ==================================
                HEADER
            =================================== */}

            <div className="page-header">

                <h1>
                    MapReduce Jobs
                </h1>

                <p>
                    Monitor submitted jobs,
                    execution progress,
                    and cluster workload.
                </p>

            </div>


            {/* ==================================
                JOB SUMMARY
            =================================== */}

            <div className="job-summary">

                <div className="summary-card">

                    <h3>
                        Total Jobs
                    </h3>

                    <span>
                        {jobs.length}
                    </span>

                </div>

                <div className="summary-card">

                    <h3>
                        Running
                    </h3>

                    <span>

                        {
                            jobs.filter(
                                job =>
                                job.status ===
                                "RUNNING"
                            ).length
                        }

                    </span>

                </div>

                <div className="summary-card">

                    <h3>
                        Completed
                    </h3>

                    <span>

                        {
                            jobs.filter(
                                job =>
                                job.status ===
                                "COMPLETED"
                            ).length
                        }

                    </span>

                </div>

                <div className="summary-card">

                    <h3>
                        Failed
                    </h3>

                    <span>

                        {
                            jobs.filter(
                                job =>
                                job.status ===
                                "FAILED"
                            ).length
                        }

                    </span>

                </div>

            </div>


            {/* ==================================
                JOB CARDS
            =================================== */}

            <JobTable
    jobs={jobs}
/>

        </div>
    );
}

export default Jobs;