//
// Add button enable/disable
//
document.addEventListener("DOMContentLoaded", () => {

    const addButtonMobile = document.getElementById("addSelectedBtnDesktop");
    const addButtonDesktop = document.getElementById("addSelectedBtnMobile");

    if (!addButtonMobile) return;
    if (!addButtonDesktop) return;

    function updateAddButtons() {
        addButtonDesktop.disabled = !document.querySelector(
            ".food-checkbox:checked, .recipe-checkbox:checked"
        );
        addButtonMobile.disabled = !document.querySelector(
            ".food-checkbox:checked, .recipe-checkbox:checked"
        );
    }

    document.addEventListener("change", (e) => {
        if (
            e.target.matches(".recipe-checkbox")
        ) {
            updateAddButtons();
        }
    });

    updateAddButtons();
});