/*
====================================================
CrashReduce Dashboard Entry Point
====================================================

Responsibilities

1. Mount React App
2. Load Global Styles
3. Setup Routing
4. Initialize Theme
5. Enable Strict Mode

====================================================
*/

import React from "react";
import ReactDOM from "react-dom/client";

import {
    BrowserRouter
} from "react-router-dom";

import App from "./App";

// Global Styles
import "./styles/index.css";


// ====================================================
// Root Render
// ====================================================

ReactDOM.createRoot(
    document.getElementById("root")
).render(

    <React.StrictMode>

        <BrowserRouter>

            <App />

        </BrowserRouter>

    </React.StrictMode>
);