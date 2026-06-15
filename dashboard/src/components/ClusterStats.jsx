/*
====================================================
ClusterStats Component
====================================================

Cluster Overview Panel

Displays:

- Active Workers
- Running Jobs
- Completed Tasks
- Failed Tasks
- Recovery Events

Used By:

- Dashboard Page

====================================================
*/

function ClusterStats({

    activeWorkers = 0,

    runningJobs = 0,

    completedTasks = 0,

    failedTasks = 0,

    recoveryEvents = 0

}) {

    // ==========================================
    // Cluster Health Calculation
    // ==========================================

    const totalTasks =
        completedTasks +
        failedTasks;

    let healthScore = 100;

    if (totalTasks > 0) {

        healthScore = Math.round(

            (
                completedTasks /
                totalTasks
            ) * 100
        );
    }


    // ==========================================
    // Health Status
    // ==========================================

    const getHealthStatus = () => {

        if (healthScore >= 95) {
            return "EXCELLENT";
        }

        if (healthScore >= 80) {
            return "GOOD";
        }

        if (healthScore >= 60) {
            return "WARNING";
        }

        return "CRITICAL";
    };


    const healthStatus =
        getHealthStatus();


    return (

        <div className="cluster-stats">

            {/* ==========================
                HEADER
            =========================== */}

            <div className="cluster-stats-header">

                <div>

                    <h2>
                        Cluster Overview
                    </h2>

                    <p>
                        Real-time distributed
                        system metrics
                    </p>

                </div>

                <div
                    className={`cluster-health-badge ${healthStatus.toLowerCase()}`}
                >

                    ● {healthStatus}

                </div>

            </div>


            {/* ==========================
                STATS GRID
            =========================== */}

            <div className="cluster-stats-grid">

                {/* ACTIVE WORKERS */}

                <div className="cluster-stat-card">

                    <div className="stat-icon">
                        🟢
                    </div>

                    <div className="stat-content">

                        <h3>
                            Active Workers
                        </h3>

                        <span>
                            {activeWorkers}
                        </span>

                    </div>

                </div>


                {/* RUNNING JOBS */}

                <div className="cluster-stat-card">

                    <div className="stat-icon">
                        ⚡
                    </div>

                    <div className="stat-content">

                        <h3>
                            Running Jobs
                        </h3>

                        <span>
                            {runningJobs}
                        </span>

                    </div>

                </div>


                {/* COMPLETED TASKS */}

                <div className="cluster-stat-card">

                    <div className="stat-icon">
                        ✅
                    </div>

                    <div className="stat-content">

                        <h3>
                            Completed Tasks
                        </h3>

                        <span>
                            {completedTasks}
                        </span>

                    </div>

                </div>


                {/* FAILED TASKS */}

                <div className="cluster-stat-card">

                    <div className="stat-icon">
                        🔴
                    </div>

                    <div className="stat-content">

                        <h3>
                            Failed Tasks
                        </h3>

                        <span>
                            {failedTasks}
                        </span>

                    </div>

                </div>


                {/* RECOVERY EVENTS */}

                <div className="cluster-stat-card">

                    <div className="stat-icon">
                        🔄
                    </div>

                    <div className="stat-content">

                        <h3>
                            Recovery Events
                        </h3>

                        <span>
                            {recoveryEvents}
                        </span>

                    </div>

                </div>


                {/* HEALTH SCORE */}

                <div className="cluster-stat-card health-card">

                    <div className="stat-icon">
                        💚
                    </div>

                    <div className="stat-content">

                        <h3>
                            Health Score
                        </h3>

                        <span>

                            {healthScore}%

                        </span>

                    </div>

                </div>

            </div>


            {/* ==========================
                HEALTH BAR
            =========================== */}

            <div className="cluster-health-section">

                <div className="health-label">

                    <span>
                        Cluster Health
                    </span>

                    <span>

                        {healthScore}%

                    </span>

                </div>

                <ProgressBar
    label="Cluster Health"
    value={healthScore}
    max={100}
    color="green"
    size="large"
/>

            </div>

        </div>
    );
}

export default ClusterStats;