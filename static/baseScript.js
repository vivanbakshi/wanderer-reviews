function openForm(formId) {
    const form = document.getElementById(formId);
    const overlay = document.getElementById("form-background-overlay");

    form.classList.remove("closed");
    overlay.classList.remove("closed");
};

function closeForms() {
    const forms = document.querySelectorAll(".popout-form");
    forms.forEach((form) => {
        form.classList.add("closed");
    });

    const overlay = document.getElementById("form-background-overlay");
    overlay.classList.add("closed");
}

const searchForm = document.getElementById("homepage-search-form");
searchForm.addEventListener("submit", function() {
    const searchTerm = document.getElementById("search").value;
    window.location.href = "/reviews?search-by=name&search=" + searchTerm;
});