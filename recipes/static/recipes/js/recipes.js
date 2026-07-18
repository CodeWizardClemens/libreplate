//
// Add button enable/disable
//
document.addEventListener("DOMContentLoaded", () => {
    const addButton = document.getElementById("addSelectedBtn");

    if (!addButton) return;

    function updateAddButton() {
        addButton.disabled = !document.querySelector(
            ".food-checkbox:checked, .recipe-checkbox:checked"
        );
    }

    document.addEventListener("change", (e) => {
        if (
            e.target.matches(".food-checkbox, .recipe-checkbox")
        ) {
            updateAddButton();
        }
    });

    updateAddButton();
});