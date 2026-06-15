/*
====================================================
FailureEvents Component
====================================================

Displays:

- Worker crashes
- Task reassignments
- Recovery events
- Cluster incidents

Used By:

- Dashboard
- Recovery Page

====================================================
*/

function FailureEvents({

    events = [],

    maxEvents = 20

}) {

    // ==========================================
    // Event Styling
    // ==========================================

    const getEventMeta = (
        eventType
    ) => {

        switch (eventType) {

            case "WORKER_DEAD":

                return {
                    icon: "🔴",
                    className:
                        "event-critical"
                };

            case "TASK_REASSIGNED":

                return {
                    icon: "🟢",
                    className:
                        "event-success"
                };

            case "RECOVERY_COMPLETE":

                return {
                    icon: "⚡",
                    className:
                        "event-recovery"
                };

            case "JOB_FAILED":

                return {
                    icon: "❌",
                    className:
                        "event-failed"
                };

            case "WORKER_REGISTERED":

                return {
                    icon: "🟩",
                    className:
                        "event-registered"
                };

            default:

                return {
                    icon: "📌",
                    className:
                        "event-default"
                };
        }
    };


    const visibleEvents =
        events.slice(
            0,
            maxEvents
        );


    return (

        <div
            className="failure-events-card"
        >

            {/* ==========================
                HEADER
            =========================== */}

            <div
                className="failure-events-header"
            >

                <h2>
                    Failure Events
                </h2>

                <span
                    className="event-count"
                >

                    {
                        visibleEvents.length
                    }

                </span>

            </div>


            {/* ==========================
                EMPTY STATE
            =========================== */}

            {
                visibleEvents.length === 0 && (

                    <div
                        className="failure-events-empty"
                    >

                        <div
                            className="empty-icon"
                        >

                            ✅

                        </div>

                        <p>

                            No recovery events
                            detected.

                        </p>

                    </div>
                )
            }


            {/* ==========================
                EVENT LIST
            =========================== */}

            {
                visibleEvents.length > 0 && (

                    <div
                        className="failure-events-list"
                    >

                        {
                            visibleEvents.map(
                                (
                                    event,
                                    index
                                ) => {

                                    const meta =
                                        getEventMeta(
                                            event.event_type
                                        );

                                    return (

                                        <div
                                            key={index}
                                            className={`
                                                failure-event-item
                                                ${meta.className}
                                            `}
                                        >

                                            {/* ========
                                                ICON
                                            ========= */}

                                            <div
                                                className="failure-event-icon"
                                            >

                                                {
                                                    meta.icon
                                                }

                                            </div>


                                            {/* ========
                                                BODY
                                            ========= */}

                                            <div
                                                className="failure-event-body"
                                            >

                                                <div
                                                    className="failure-event-type"
                                                >

                                                    {
                                                        event.event_type
                                                    }

                                                </div>

                                                <div
                                                    className="failure-event-message"
                                                >

                                                    {
                                                        event.message
                                                    }

                                                </div>

                                            </div>


                                            {/* ========
                                                TIME
                                            ========= */}

                                            <div
                                                className="failure-event-time"
                                            >

                                                {
                                                    event.timestamp
                                                }

                                            </div>

                                        </div>
                                    );
                                }
                            )
                        }

                    </div>
                )
            }

        </div>
    );
}

export default FailureEvents;