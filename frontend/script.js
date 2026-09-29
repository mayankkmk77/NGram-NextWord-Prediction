const input = document.getElementById("text-input");
const button = document.getElementById("predict-btn");

const results = document.getElementById("results");
const predictionList = document.getElementById("prediction-list");
const modelInfo = document.getElementById("model-info");


/* =====================================================
   HIDE PREVIOUS RESULTS WHEN USER STARTS A NEW TEST
   ===================================================== */

input.addEventListener("input", function () {
    results.style.display = "none";
});


/* =====================================================
   PREDICT BUTTON
   ===================================================== */

button.addEventListener("click", function () {

    const text = input.value.trim().toLowerCase();

    /* Check for empty input */

    if (text === "") {
        alert("Please enter some text.");
        return;
    }


    const words = text.split(/\s+/);

    let predictions = [];
    let model = "";


    /* =================================================
       BIGRAM PREDICTION
       ================================================= */

    if (words.length === 1) {

        model = "Bigram";


        /* Input: is */

        if (words[0] === "is") {

            predictions = [
                ["learning", "0.0440"],
                ["studying", "0.0330"],
                ["preparing", "0.0330"]
            ];

        }


        /* Input: studying */

        else if (words[0] === "studying") {

            predictions = [
                ["computer", "0.0282"],
                ["machine", "0.0282"]
            ];

        }


        /* Input not available in dataset */

        else {

            predictions = [
                [
                    "This input is not currently available in the dataset. More data coming soon!",
                    "--"
                ]
            ];
        }
    }


    /* =================================================
       TRIGRAM PREDICTION
       ================================================= */

    else {

        model = "Trigram";


        /*
           Take the last two words as the
           Trigram context.
        */

        const word1 = words[words.length - 2];
        const word2 = words[words.length - 1];


        /* Input: student is */

        if (word1 === "student" && word2 === "is") {

            predictions = [
                ["studying", "0.0385"],
                ["learning", "0.0385"],
                ["preparing", "0.0385"]
            ];

        }


        /* Input not available in dataset */

        else {

            predictions = [
                [
                    "This input is not currently available in the dataset. More data coming soon!",
                    "--"
                ]
            ];
        }
    }


    /* =================================================
       UPDATE MODEL INFORMATION
       ================================================= */

    modelInfo.textContent = model;


    /* =================================================
       CLEAR PREVIOUS RESULTS
       ================================================= */

    predictionList.innerHTML = "";


    /* =================================================
       DISPLAY RESULTS
       ================================================= */

    predictions.forEach(function (prediction, index) {

        const row = document.createElement("div");

        row.className = "prediction-row";


        /*
           Special layout for unavailable inputs.
        */

        if (prediction[1] === "--") {

            row.classList.add("not-found");

            row.innerHTML = `
                <div class="prediction-message">
                    ${prediction[0]}
                </div>
            `;

        }


        /*
           Normal prediction layout.
        */

        else {

            row.innerHTML = `
                <div class="rank">
                    ${String(index + 1).padStart(2, "0")}
                </div>

                <div class="prediction-word">
                    ${prediction[0]}
                </div>

                <div class="probability">
                    ${prediction[1]}
                </div>
            `;
        }


        predictionList.appendChild(row);
    });


    /* =================================================
       SHOW RESULTS
       ================================================= */

    results.style.display = "block";

});


/* =====================================================
   ENTER KEY SUPPORT
   ===================================================== */

input.addEventListener("keydown", function (event) {

    if (event.key === "Enter") {
        button.click();
    }

});