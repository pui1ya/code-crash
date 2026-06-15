/*
====================================================
CrashReduce Dashboard Root Application
====================================================

Responsibilities

1. Application Layout
2. Route Definitions
3. Sidebar Navigation
4. Top Navigation
5. Page Rendering

====================================================
*/

import {
    Routes,
    Route,
    Navigate
} from "react-router-dom";


// Pages
import Dashboard from "./pages/Dashboard";
import Workers from "./pages/Workers";
import Jobs from "./pages/Jobs";
import Recovery from "./pages/Recovery";
import Metrics from "./pages/Metrics";


// Components
import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";


// ====================================================
// Root App
// ====================================================

function App() {

    return (

        <div className="app-container">

            {/* ================================
                SIDEBAR
            ================================= */}

            <Sidebar />


            {/* ================================
                MAIN CONTENT
            ================================= */}

            <div className="main-layout">

                <Navbar />

                <main className="page-content">

                    <Routes>

                        <Route
                            path="/"
                            element={<Dashboard />}
                        />

                        <Route
                            path="/workers"
                            element={<Workers />}
                        />

                        <Route
                            path="/jobs"
                            element={<Jobs />}
                        />

                        <Route
                            path="/recovery"
                            element={<Recovery />}
                        />

                        <Route
                            path="/metrics"
                            element={<Metrics />}
                        />

                        {/* Unknown Route */}

                        <Route
                            path="*"
                            element={
                                <Navigate
                                    to="/"
                                    replace
                                />
                            }
                        />

                    </Routes>

                </main>

            </div>

        </div>
    );
}

export default App;