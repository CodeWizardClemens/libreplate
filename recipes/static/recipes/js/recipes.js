//
// Add button enable/disable
//
document.addEventListener("DOMContentLoaded", () => {

    const addButton = document.getElementById("addSelectedBtn");

    function updateAddButton() {
        if (!addButton) return;

        const checked = document.querySelectorAll(
            ".food-checkbox:checked, .recipe-checkbox:checked"
        );

        addButton.disabled = checked.length === 0;
    }

    document
        .querySelectorAll(".food-checkbox, .recipe-checkbox")
        .forEach(cb => cb.addEventListener("change", updateAddButton));

    updateAddButton();

});