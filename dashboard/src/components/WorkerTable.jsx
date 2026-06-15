/*
====================================================
WorkerTable Component
====================================================

Displays:

- Worker ID
- Status
- Current Task
- Tasks Completed
- Tasks Failed
- Last Heartbeat

Reusable across:

- Workers Page
- Dashboard Page
- Future Admin Views

====================================================
*/

function WorkerTable({ workers = [] }) {

    // ==========================================
    // Status Badge Styling
    // ==========================================

    const getStatusClass = (
        status
    ) => {

        switch (status) {

            case "IDLE":
                return "worker-status-idle";

            case "BUSY":
                return "worker-status-busy";

            case "DEAD":
                return "worker-status-dead";

            default:
                return "worker-status-unknown";
        }
    };


    // ==========================================
    // Empty State
    // ==========================================

    if (!workers.length) {

        return (

            <div
                className="worker-table-empty"
            >

                <h3>
                    No Workers Registered
                </h3>

                <p>
                    Waiting for workers to
                    connect to the coordinator.
                </p>

            </div>
        );
    }


    // ==========================================
    // Table
    // ==========================================

    return (

        <div
            className="worker-table-wrapper"
        >

            <table
                className="worker-table"
            >

                <thead>

                    <tr>

                        <th>
                            Worker ID
                        </th>

                        <th>
                            Status
                        </th>

                        <th>
                            Current Task
                        </th>

                        <th>
                            Completed
                        </th>

                        <th>
                            Failed
                        </th>

                        <th>
                            Last Heartbeat
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {
                        workers.map(
                            (worker) => (

                            <tr
                                key={
                                    worker.worker_id
                                }
                            >

                                {/* =====================
                                    WORKER ID
                                ====================== */}

                                <td>

                                    <div
                                        className="worker-id"
                                    >

                                        {
                                            worker.worker_id
                                        }

                                    </div>

                                </td>


                                {/* =====================
                                    STATUS
                                ====================== */}

                                <td>

                                    <span
                                        className={
                                            getStatusClass(
                                                worker.status
                                            )
                                        }
                                    >

                                        {
                                            worker.status
                                        }

                                    </span>

                                </td>


                                {/* =====================
                                    CURRENT TASK
                                ====================== */}

                                <td>

                                    {
                                        worker.current_task
                                        ||
                                        "-"
                                    }

                                </td>


                                {/* =====================
                                    COMPLETED TASKS
                                ====================== */}

                                <td>

                                    {
                                        worker.tasks_completed
                                        ?? 0
                                    }

                                </td>


                                {/* =====================
                                    FAILED TASKS
                                ====================== */}

                                <td>

                                    {
                                        worker.tasks_failed
                                        ?? 0
                                    }

                                </td>


                                {/* =====================
                                    HEARTBEAT
                                ====================== */}

                                <td>

                                    {
                                        worker.last_heartbeat
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

export default WorkerTable;