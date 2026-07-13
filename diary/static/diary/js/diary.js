let metricSaveTimer = null;
const mealFoodTimers = {};
window.noteTimers = window.noteTimers || {};

/* -----------------------
   METRICS
----------------------- */

function saveMetric(input) {
    clearTimeout(metricSaveTimer);
    metricSaveTimer = setTimeout(() => {
        fetch("/diary/body-metrics/save/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRF(),
            },
            body: JSON.stringify({
                metric_id: input.dataset.metricId,
                amount: input.value,
                date: window.selectedDate
            })
        });
    }, 400);
}

/* -----------------------
   MEAL FOOD ROWS
----------------------- */
function saveMealFood(input) {
    const row = input.closest("tr");
    const id = input.dataset.mealFood;

    clearTimeout(mealFoodTimers[id]);

    mealFoodTimers[id] = setTimeout(() => {
        fetch("/diary/meal-food/update/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRF(),
            },
            body: JSON.stringify({
                meal_food_id: id,
                serving_size: row.querySelector(".serving-size").value,
                number_of_servings: row.querySelector(".servings").value
            })
        })
        .then(r => r.json())
        .then(updateUI)
        .catch(err => console.error("Meal food update failed:", err));
    }, 300);
}

/* -----------------------
   NOTE AUTOSAVE (FIXED)
----------------------- */
function saveNote(textarea) {
    const id = textarea.dataset.meal;

    clearTimeout(window.noteTimers[id]);

    window.noteTimers[id] = setTimeout(() => {
        fetch(`/diary/meal/${id}/note/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRF(),
            },
            body: JSON.stringify({
                note: textarea.value
            })
        })
        .catch(err => console.error("Note save failed:", err));
    }, 400);
}

/* -----------------------
   UI UPDATE
----------------------- */
function updateUI(data) {

    if (data.meal_food) {
        const mealFoodId = Object.keys(data.meal_food)[0];
        const nutrients = data.meal_food[mealFoodId];

        const input = document.querySelector(
            `.serving-size[data-meal-food="${mealFoodId}"]`
        );

        if (input) {
            const row = input.closest("tr");

            row.querySelectorAll(".nutrient-cell").forEach(cell => {
                cell.innerText = nutrients[cell.dataset.nutrient] ?? 0;
            });
        }
    }

    document.querySelectorAll(".meal-total").forEach(cell => {
        cell.innerText = data.meal[cell.dataset.nutrient] ?? 0;
    });

    document.querySelectorAll(".day-total").forEach(cell => {
        cell.innerText = data.day[cell.dataset.nutrient] ?? 0;
    });
}

/* -----------------------
   CSRF
----------------------- */
function getCSRF() {
    const el = document.querySelector("[name=csrfmiddlewaretoken]");
    return el ? el.value : "";
}

/* -----------------------
   INIT
----------------------- */
document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".meal-card textarea").forEach(textarea => {

        autoResize(textarea);

        textarea.addEventListener("input", () => {
            autoResize(textarea);
            saveNote(textarea);
        });
    });

    const dateInput = document.querySelector(".calendar-picker");
    dateInput?.addEventListener("focus", () => dateInput.showPicker?.());
});

/* -----------------------
   AUTO RESIZE
----------------------- */
function autoResize(textarea) {
    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";
}

function goToDate(dateString) {
    window.location.href = `/diary/${dateString}/`;
}