/*
====================================================
ProgressBar Component
====================================================

Reusable progress bar component.

Features:

✓ Animated Fill
✓ Percentage Display
✓ Custom Colors
✓ Labels
✓ Status-Based Styling

Used By:

- Jobs
- Dashboard
- Recovery
- Metrics

====================================================
*/

function ProgressBar({

    value = 0,

    max = 100,

    label = "",

    showPercentage = true,

    size = "medium",

    color = "green"
}) {

    // ==========================================
    // Calculate Percentage
    // ==========================================

    const percentage = Math.min(
        Math.max(
            (value / max) * 100,
            0
        ),
        100
    );


    // ==========================================
    // CSS Classes
    // ==========================================

    const sizeClass =
        `progress-${size}`;

    const colorClass =
        `progress-${color}`;


    return (

        <div className="progress-container">

            {/* ==========================
                LABEL
            =========================== */}

            {
                label && (

                    <div
                        className="progress-header"
                    >

                        <span>

                            {label}

                        </span>

                        {
                            showPercentage && (

                                <span>

                                    {
                                        percentage.toFixed(
                                            0
                                        )
                                    }%

                                </span>
                            )
                        }

                    </div>
                )
            }


            {/* ==========================
                BAR
            =========================== */}

            <div
                className={
                    `progress-track ${sizeClass}`
                }
            >

                <div
                    className={`
                        progress-fill
                        ${colorClass}
                    `}
                    style={{
                        width:
                        `${percentage}%`
                    }}
                />

            </div>


            {/* ==========================
                NO LABEL MODE
            =========================== */}

            {
                !label &&
                showPercentage && (

                    <div
                        className="progress-footer"
                    >

                        {
                            percentage.toFixed(
                                0
                            )
                        }%

                    </div>
                )
            }

        </div>
    );
}

export default ProgressBar;