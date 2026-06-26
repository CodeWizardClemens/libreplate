let metricSaveTimer = null;

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

const mealFoodTimers = {};

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
        .then(updateUI);
    }, 300);
}

function saveNote(textarea) {
    const id = textarea.dataset.meal;

    clearTimeout(window.noteTimers?.[id]);

    window.noteTimers = window.noteTimers || {};

    window.noteTimers[id] = setTimeout(() => {
        fetch(`/diary/meal/${id}/note/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRF(),
            },
            body: JSON.stringify({ note: textarea.value })
        });
    }, 400);
}

function updateUI(data) {

    // -----------------------
    // Update edited food row
    // -----------------------
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

    // -----------------------
    // Update meal totals
    // -----------------------
    document.querySelectorAll(".meal-total").forEach(cell => {
        cell.innerText = data.meal[cell.dataset.nutrient] ?? 0;
    });

    // -----------------------
    // Update day totals
    // -----------------------
    document.querySelectorAll(".day-total").forEach(cell => {
        cell.innerText = data.day[cell.dataset.nutrient] ?? 0;
    });

}
function getCSRF() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

document.addEventListener("DOMContentLoaded", () => {
    const dateInput = document.querySelector(".calendar-picker");

    dateInput?.addEventListener("focus", () => dateInput.showPicker?.());
});

