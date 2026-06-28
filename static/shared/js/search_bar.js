document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".search-bar-form").forEach(function (form) {

        const sort = form.querySelector("select");

        if (sort) {
            sort.addEventListener("change", function () {
                form.submit();
            });
        }

    });

});