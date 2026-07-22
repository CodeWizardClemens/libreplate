document.addEventListener("DOMContentLoaded", () => {

    const searchInput = document.getElementById("foodSearch");
    const addButton = document.getElementById("addSelectedBtn");
    const sortSelect = document.getElementById("sortSelect");

    //
    // Search filter
    //
    if (searchInput) {
        searchInput.addEventListener("input", function () {
            const query = this.value.trim().toLowerCase();

            document.querySelectorAll(".food-item").forEach(food => {
                const name = (food.dataset.name || "").toLowerCase();
                const description = (food.dataset.description || "").toLowerCase();

                const visible =
                    name.includes(query) ||
                    description.includes(query);

                food.classList.toggle("hidden-food", !visible);
            });
        });
    }

    //
    // Sorting
    //
    if (sortSelect) {
        sortSelect.addEventListener("change", function () {
            const url = new URL(window.location.href);
            url.searchParams.set("sort", this.value);
            window.location.href = url.toString();
        });
    }

    //
    // Add button enable/disable
    //
    function updateAddButton() {
        if (!addButton) return;

        const checked = document.querySelectorAll(".food-checkbox:checked");
        addButton.disabled = checked.length === 0;
    }

    document.querySelectorAll(".food-checkbox").forEach(cb => {
        cb.addEventListener("change", updateAddButton);
    });

    updateAddButton();

});