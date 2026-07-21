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

function toggleFilter(name) {
    const form = document.getElementById("filterForm");
    const input = form.querySelector(`[name="${name}"]`);

    if (!input) {
        console.error(`Missing filter input: ${name}`);
        return;
    }

    input.value = input.value === "1" ? "0" : "1";
}

document.addEventListener("htmx:configRequest", function (event) {
    const modal = document.getElementById("tagsModal");

    if (modal && modal.classList.contains("show")) {
        event.detail.headers["X-Tags-Modal-Open"] = "true";
    }
});


document.body.addEventListener("htmx:afterSettle", function () {
    const modalElement = document.getElementById("tagsModal");

    if (!modalElement) {
        return;
    }

    if (modalElement.dataset.keepOpen !== "true") {
        return;
    }

    const oldModal = bootstrap.Modal.getInstance(modalElement);

    if (oldModal) {
        oldModal.dispose();
    }

    document.querySelectorAll(".modal-backdrop").forEach((backdrop) => {
        backdrop.remove();
    });

    document.body.classList.remove("modal-open");
    document.body.style.removeProperty("padding-right");

    const modal = new bootstrap.Modal(modalElement, {
        backdrop: true,
        focus: true,
    });

    modal.show();

    delete modalElement.dataset.keepOpen;
});