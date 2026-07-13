document.addEventListener("DOMContentLoaded", () => {

    const selected = new Date(window.selectedDate);
    selected.setHours(0, 0, 0, 0);

    let weekStart = getMonday(selected);

    const month = document.getElementById("mdpMonth");
    const days = document.getElementById("mdpDays");

    function getMonday(date) {

        const d = new Date(date);

        const day = (d.getDay() + 6) % 7;

        d.setDate(d.getDate() - day);

        d.setHours(0, 0, 0, 0);

        return d;
    }

    function formatISO(date) {

        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, "0");
        const day = String(date.getDate()).padStart(2, "0");

        return `${year}-${month}-${day}`;
    }

    function render() {

        days.innerHTML = "";

        // Display month (or month range if week crosses months)
        const weekEnd = new Date(weekStart);
        weekEnd.setDate(weekEnd.getDate() + 6);

        if (weekStart.getMonth() === weekEnd.getMonth()) {

            month.textContent = weekStart.toLocaleDateString(undefined, {
                month: "long",
                year: "numeric"
            });

        } else {

            month.textContent =
                weekStart.toLocaleDateString(undefined, {
                    month: "short"
                }) +
                " / " +
                weekEnd.toLocaleDateString(undefined, {
                    month: "short",
                    year: "numeric"
                });

        }

        const today = new Date();
        today.setHours(0, 0, 0, 0);

        for (let i = 0; i < 7; i++) {

            const d = new Date(weekStart);
            d.setDate(d.getDate() + i);
            d.setHours(0, 0, 0, 0);

            const button = document.createElement("button");

            button.className = "mdp-day";
            button.textContent = d.getDate();

            if (d.getTime() === today.getTime()) {
                button.classList.add("today");
            }

            if (formatISO(d) === window.selectedDate) {
                button.classList.add("selected");
            }

            button.addEventListener("click", () => {
                goToDate(formatISO(d));
            });

            days.appendChild(button);
        }

    }

    document.getElementById("prevWeek").addEventListener("click", () => {

        weekStart.setDate(weekStart.getDate() - 7);

        render();

    });

    document.getElementById("nextWeek").addEventListener("click", () => {

        weekStart.setDate(weekStart.getDate() + 7);

        render();

    });

    document.getElementById("todayBtn").addEventListener("click", () => {

        goToDate(formatISO(new Date()));

    });

    document.getElementById("calendarBtn").addEventListener("click", () => {

        const input = document.getElementById("calendarInput");

        if (input.showPicker) {
            input.showPicker();
        } else {
            input.click();
        }

    });

    document.getElementById("calendarInput").addEventListener("change", e => {

        goToDate(e.target.value);

    });

    render();

});