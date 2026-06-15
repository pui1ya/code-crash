/*
====================================================
CrashReduce Dashboard Page
====================================================

Cluster Overview

Shows:

- Active Workers
- Running Jobs
- Completed Tasks
- Recovery Events

- Cluster Health
- Throughput Metrics
- Recovery Feed

====================================================
*/

import { useEffect, useState } from "react";

import {
    getClusterStatus,
    getMetrics,
    getRecoveryEvents
} from "../api/coordinatorApi";

import StatCard from "../components/StatCard";
import ThroughputChart from "../components/ThroughputChart";
import ClusterHealth from "../components/ClusterHealth";
import RecoveryFeed from "../components/RecoveryFeed";
import ClusterStats from "../components/ClusterStats";



function Dashboard() {

    const [cluster, setCluster] =
        useState(null);

    const [metrics, setMetrics] =
        useState(null);

    const [recoveryEvents, setRecoveryEvents] =
        useState([]);

    const [loading, setLoading] =
        useState(true);


    // ==================================================
    // Load Dashboard Data
    // ==================================================

    useEffect(() => {

        const fetchData = async () => {

            try {

                const [
                    clusterData,
                    metricsData,
                    recoveryData
                ] = await Promise.all([

                    getClusterStatus(),

                    getMetrics(),

                    getRecoveryEvents()
                ]);

                setCluster(
                    clusterData
                );

                setMetrics(
                    metricsData
                );

                setRecoveryEvents(
                    recoveryData
                );

            } catch (error) {

                console.error(
                    "Dashboard Load Error",
                    error
                );

            } finally {

                setLoading(false);
            }
        };

        fetchData();

    }, []);


    // ==================================================
    // Loading Screen
    // ==================================================

    if (loading) {

        return (

            <div className="dashboard-loading">

                <div className="loading-spinner" />

                <h2>
                    Initializing Cluster...
                </h2>

            </div>
        );
    }


    return (

        <div className="dashboard-page">

            {/* ====================================
                HEADER
            ===================================== */}

            <div className="dashboard-header">

                <h1>
                    CrashReduce Cluster
                </h1>

                <p>
                    Distributed MapReduce
                    Monitoring Console
                </p>

            </div>


            {/* ====================================
                STATS GRID
            ===================================== */}

            <div className="stats-grid">

                <StatCard
                    title="Active Workers"
                    value={
                        cluster?.active_workers || 0
                    }
                    icon="🟢"
                />

                <StatCard
                    title="Running Jobs"
                    value={
                        cluster?.running_jobs || 0
                    }
                    icon="⚡"
                />

                <StatCard
                    title="Completed Tasks"
                    value={
                        metrics?.completed_tasks || 0
                    }
                    icon="✅"
                />

                <StatCard
                    title="Recovery Events"
                    value={
                        recoveryEvents.length
                    }
                    icon="🔄"
                />

            </div>


            {/* ====================================
                HEALTH SECTION
            ===================================== */}

            <div className="dashboard-section">

                <ClusterHealth
                    cluster={cluster}
                />

            </div>


            {/* ====================================
                THROUGHPUT GRAPH
            ===================================== */}

            <div className="dashboard-section">

                <ThroughputChart
                    metrics={metrics}
                />

            </div>


            {/* ====================================
                RECOVERY EVENTS
            ===================================== */}

            <div className="dashboard-section">

                <RecoveryFeed
                    events={
                        recoveryEvents
                    }
                />

            </div>

            <ClusterStats

    activeWorkers={
        cluster?.active_workers || 0
    }

    runningJobs={
        cluster?.running_jobs || 0
    }

    completedTasks={
        metrics?.completed_tasks || 0
    }

    failedTasks={
        metrics?.failed_tasks || 0
    }

    recoveryEvents={
        recoveryEvents.length
    }
/>

        </div>
    );
}

export default Dashboard;