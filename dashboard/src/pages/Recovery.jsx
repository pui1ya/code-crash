/*
====================================================
Recovery Page
====================================================

Displays:

- Worker failures
- Recovery events
- Task reassignments
- Recovery metrics
- Failure timeline

====================================================
*/

import { useEffect, useState } from "react";
import FailureEvents from "../components/FailureEvents";
import {
    getRecoveryEvents
} from "../api/coordinatorApi";
import usePolling
from "../hooks/usePolling";

import {
    getWorkers
}
from "../api/coordinatorApi";


function Recovery() {

    const {

    data: events,

    loading

} = usePolling(

    getRecoveryEvents,

    1000
);

    // ==========================================
    // Loading
    // ==========================================

    if (loading) {

        return (

            <div className="page-loading">

                <h2>
                    Loading Recovery Center...
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
    // Metrics
    // ==========================================

    const workerFailures =
        events.filter(
            event =>
            event.event_type ===
            "WORKER_DEAD"
        ).length;

    const taskReassignments =
        events.filter(
            event =>
            event.event_type ===
            "TASK_REASSIGNED"
        ).length;

    const avgRecoveryTime =
        events.length > 0
            ? (
                events.reduce(
                    (
                        total,
                        event
                    ) =>
                        total +
                        (
                            event.recovery_time_seconds ||
                            0
                        ),
                    0
                ) / events.length
            ).toFixed(2)
            : "0.00";


    return (

        <div className="recovery-page">

            {/* ============================
                HEADER
            ============================= */}

            <div className="page-header">

                <h1>
                    Recovery Center
                </h1>

                <p>
                    Monitor worker crashes,
                    task reassignments,
                    and fault-tolerance
                    activity.
                </p>

            </div>


            {/* ============================
                SUMMARY CARDS
            ============================= */}

            <div className="recovery-summary">

                <div className="summary-card">

                    <h3>
                        Recovery Events
                    </h3>

                    <span>
                        {events.length}
                    </span>

                </div>

                <div className="summary-card">

                    <h3>
                        Failed Workers
                    </h3>

                    <span>
                        {workerFailures}
                    </span>

                </div>

                <div className="summary-card">

                    <h3>
                        Reassigned Tasks
                    </h3>

                    <span>
                        {taskReassignments}
                    </span>

                </div>

                <div className="summary-card">

                    <h3>
                        Avg Recovery Time
                    </h3>

                    <span>

                        {avgRecoveryTime}s

                    </span>

                </div>

            </div>


            {/* ============================
                EVENT TIMELINE
            ============================= */}

            <FailureEvents
    events={events}
/>


            {/* ============================
                RECOVERY STATS PANEL
            ============================= */}

            <div className="recovery-stats-panel">

                <div className="stats-card">

                    <h3>
                        Fault Tolerance Status
                    </h3>

                    <div
                        className="status-online"
                    >

                        ● ACTIVE

                    </div>

                    <p>

                        CrashReduce is actively
                        monitoring workers and
                        automatically recovering
                        failed tasks.

                    </p>

                </div>

            </div>

        </div>
    );
}

export default Recovery;