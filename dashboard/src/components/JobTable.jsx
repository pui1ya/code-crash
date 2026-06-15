/*
====================================================
JobTable Component
====================================================

Displays:

- Job ID
- Job Type
- Status
- Progress
- Map Progress
- Reduce Progress
- Runtime

Reusable Across:

- Jobs Page
- Dashboard
- Future Admin Views

====================================================
*/
import ProgressBar
from "./ProgressBar";

function JobTable({ jobs = [] }) {

    // ==========================================
    // Status Styling
    // ==========================================

    const getStatusClass = (
        status
    ) => {

        switch (status) {

            case "RUNNING":
                return "job-status-running";

            case "COMPLETED":
                return "job-status-completed";

            case "FAILED":
                return "job-status-failed";

            case "PENDING":
                return "job-status-pending";

            default:
                return "job-status-unknown";
        }
    };


    // ==========================================
    // Empty State
    // ==========================================

    if (!jobs.length) {

        return (

            <div className="job-table-empty">

                <h3>
                    No Jobs Found
                </h3>

                <p>
                    Submit a MapReduce job
                    to begin processing.
                </p>

            </div>
        );
    }


    // ==========================================
    // Table
    // ==========================================

    return (

        <div className="job-table-wrapper">

            <table className="job-table">

                <thead>

                    <tr>

                        <th>
                            Job ID
                        </th>

                        <th>
                            Job Type
                        </th>

                        <th>
                            Status
                        </th>

                        <th>
                            Progress
                        </th>

                        <th>
                            Map Tasks
                        </th>

                        <th>
                            Reduce Tasks
                        </th>

                        <th>
                            Runtime
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {
                        jobs.map(
                            (job) => (

                            <tr
                                key={
                                    job.job_id
                                }
                            >

                                {/* ===================
                                    JOB ID
                                ==================== */}

                                <td>

                                    <div
                                        className="job-id"
                                    >

                                        {
                                            job.job_id
                                        }

                                    </div>

                                </td>


                                {/* ===================
                                    JOB TYPE
                                ==================== */}

                                <td>

                                    {
                                        job.job_type
                                    }

                                </td>


                                {/* ===================
                                    STATUS
                                ==================== */}

                                <td>

                                    <span
                                        className={
                                            getStatusClass(
                                                job.status
                                            )
                                        }
                                    >

                                        {
                                            job.status
                                        }

                                    </span>

                                </td>


                                {/* ===================
                                    PROGRESS
                                ==================== */}

                                <td>

                                    <div
                                        className="table-progress"
                                    >

                                        <ProgressBar
    value={job.progress_percentage}
    max={100}
    size="small" />

                                        <span>

                                            {
                                                job.progress_percentage || 0
                                            }%

                                        </span>

                                    </div>

                                </td>


                                {/* ===================
                                    MAP TASKS
                                ==================== */}

                                <td>

                                    {
                                        job.completed_maps || 0
                                    }

                                    /

                                    {
                                        job.total_maps || 0
                                    }

                                </td>


                                {/* ===================
                                    REDUCE TASKS
                                ==================== */}

                                <td>

                                    {
                                        job.completed_reduces || 0
                                    }

                                    /

                                    {
                                        job.total_reduces || 0
                                    }

                                </td>


                                {/* ===================
                                    EXECUTION TIME
                                ==================== */}

                                <td>

                                    {
                                        job.execution_time
                                        ||
                                        "-"
                                    }

                                </td>

                            </tr>
                        ))
                    }

                </tbody>

            </table>

        </div>
    );
}

export default JobTable;