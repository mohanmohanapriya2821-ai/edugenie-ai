// ============================================
// ELEMENTS
// ============================================

const task =
    document.getElementById("task");

const input =
    document.getElementById("inputText");

const button =
    document.getElementById("submitBtn");

const result =
    document.getElementById("result");

const status =
    document.getElementById("status");

const copyBtn =
    document.getElementById("copyBtn");


// ============================================
// PLACEHOLDERS
// ============================================

const placeholders = {

    qa:
        "Example: What is the difference between a stack and a queue?",

    explain:
        "Example: Explain binary search trees to a beginner.",

    quiz:
        "Paste a lesson, paragraph, or topic here to generate 3 MCQs.",

    summarize:
        "Paste the educational passage you want to summarize.",

    learn:
        "Example: Learn SQL from beginner to advanced."
};


// ============================================
// CHANGE PLACEHOLDER
// ============================================

task.addEventListener(
    "change",
    () => {

        input.placeholder =
            placeholders[
                task.value
            ];

    }
);


// ============================================
// HTML ESCAPE
// ============================================

function escapeHtml(value) {

    return String(value)

        .replaceAll(
            "&",
            "&amp;"
        )

        .replaceAll(
            "<",
            "&lt;"
        )

        .replaceAll(
            ">",
            "&gt;"
        )

        .replaceAll(
            '"',
            "&quot;"
        )

        .replaceAll(
            "'",
            "&#039;"
        );
}


// ============================================
// RENDER RESPONSE
// ============================================

function render(data) {

    if (!data || typeof data !== "object") {

        result.textContent =
            typeof data === "string"
                ? data
                : "Received an unexpected response from the server.";

        result.classList.remove("muted");
        copyBtn.disabled = false;
        return;

    }


    // Q&A

    if (data.answer) {

        result.innerHTML =
            escapeHtml(
                data.answer
            );

    }


    // EXPLANATION

    else if (data.explanation) {

        result.innerHTML =
            escapeHtml(
                data.explanation
            );

    }


    // SUMMARY

    else if (data.summary) {

        result.innerHTML =
            escapeHtml(
                data.summary
            );

    }


    // QUIZ

    else if (Array.isArray(data.questions) && data.questions.length) {

        result.innerHTML =
            data.questions
                .map(
                    (q, index) => `

                    <div class="quiz-question">

                        <h3>
                            ${index + 1}.
                            ${escapeHtml(q.question || "")}
                        </h3>

                        ${
                            Array.isArray(q.options)
                                ? q.options
                                    .map(
                                        option => `
                                        <div class="option">
                                            ○
                                            ${escapeHtml(option ?? "")}
                                        </div>
                                        `
                                    )
                                    .join("")
                                : ""
                        }

                        <p>

                            <strong>
                                Correct Answer:
                            </strong>

                            ${escapeHtml(
                                q.correct_answer || ""
                            )}

                        </p>

                        <p>

                            ${escapeHtml(
                                q.explanation || ""
                            )}

                        </p>

                    </div>

                `
                )
                .join("");

    }


    // LEARNING PATH

    else if (Array.isArray(data.steps) && data.steps.length) {

        result.innerHTML = `

            <h3>
                ${escapeHtml(data.topic || "")}
            </h3>

            <p>
                ${escapeHtml(data.overview || "")}
            </p>

            ${
                data.steps
                    .map(
                        (step, index) => `

                        <div class="path-step">

                            <strong>

                                ${index + 1}.

                                ${escapeHtml(
                                    step.level || ""
                                )}

                                —

                                ${escapeHtml(
                                    step.topic || ""
                                )}

                            </strong>


                            <p>

                                <strong>
                                    Duration:
                                </strong>

                                ${escapeHtml(
                                    step.duration || ""
                                )}

                            </p>


                            <p>

                                <strong>
                                    Goals:
                                </strong>

                                ${
                                    Array.isArray(step.goals)
                                        ? step.goals
                                            .map(
                                                item => escapeHtml(item ?? "")
                                            )
                                            .join(" • ")
                                        : ""
                                }

                            </p>


                            <p>

                                <strong>
                                    Resources:
                                </strong>

                                ${
                                    Array.isArray(step.resources)
                                        ? step.resources
                                            .map(
                                                item => escapeHtml(item ?? "")
                                            )
                                            .join(" • ")
                                        : ""
                                }

                            </p>

                        </div>

                    `
                    )
                    .join("")
            }

        `;

    }


    // FALLBACK

    else {

        result.textContent =
            JSON.stringify(
                data,
                null,
                2
            );

    }


    result.classList.remove(
        "muted"
    );

    copyBtn.disabled = false;
}


// ============================================
// SUBMIT
// ============================================

async function submit() {

    const text =
        input.value.trim();


    if (!text) {

        result.innerHTML =
            `
            <div class="error">
                Please enter some text first.
            </div>
            `;

        return;
    }


    const endpoints = {

        qa:
            "/qa",

        explain:
            "/explain",

        quiz:
            "/quiz",

        summarize:
            "/summarize",

        learn:
            "/learn/recommendations"

    };


    button.disabled = true;

    copyBtn.disabled = true;

    status.textContent =
        "Thinking...";


    result.textContent =
        "Generating your learning result...";


    result.classList.remove(
        "muted"
    );


    try {

        const response =
            await fetch(
                endpoints[
                    task.value
                ],
                {

                    method:
                        "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify({
                            text: text
                        })

                }
            );


        let data;

        const responseText =
            await response.text();

        if (responseText) {

            try {

                data =
                    JSON.parse(
                        responseText
                    );

            }

            catch {

                data = {
                    message:
                        responseText
                };

            }

        }


        if (!response.ok) {

            const message =
                data?.detail ||
                data?.message ||
                "The server returned an error.";

            throw new Error(
                Array.isArray(message)
                    ? message
                        .map(
                            item => item.msg || item
                        )
                        .join("; ")
                    : message
            );

        }


        render(data);


        status.textContent =
            "Ready";


    }

    catch (error) {

        const message =
            error instanceof Error
                ? error.message
                : String(error);

        result.innerHTML = `

            <div class="error">

                ${escapeHtml(
                    message
                )}

            </div>

        `;

        status.textContent =
            "Error";

    }

    finally {

        button.disabled =
            false;

    }

}


// ============================================
// GENERATE BUTTON
// ============================================

button.addEventListener(
    "click",
    submit
);


// ============================================
// COPY BUTTON
// ============================================

copyBtn.addEventListener(
    "click",
    async () => {

        await navigator.clipboard.writeText(
            result.innerText
        );


        status.textContent =
            "Copied";


        setTimeout(
            () => {

                status.textContent =
                    "Ready";

            },
            1200
        );

    }
);


// ============================================
// CTRL + ENTER
// ============================================

input.addEventListener(
    "keydown",
    event => {

        if (
            (event.ctrlKey ||
             event.metaKey)
            &&
            event.key === "Enter"
        ) {

            submit();

        }

    }
);