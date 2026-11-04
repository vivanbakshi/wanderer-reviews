var formBackgroundOverlay = document.getElementById("form-background-overlay");
var spotlightId = document.getElementById("title").innerText.replaceAll(" ", "-");


function openForm(formID) {
    const form = document.getElementById(formID);
    form.classList.remove("closed");
    formBackgroundOverlay.classList.remove("closed");
};

function closeForms() {
    const forms = document.querySelectorAll(".popout-form")
    forms.forEach((form) => {
        form.classList.add("closed");
    });
    formBackgroundOverlay.classList.add("closed");
};

function goToPage(page) {
    window.location.href = (page);
}

function deletePost() {
    $.ajax({
        url: "/delete-post",
        type: "POST",
        data: {
            postId: spotlightId,
            type: "spotlight"
        }
    })
    goToPage("/")
};

function sendEdit(value, column) {
    $.ajax({
        url: "/edit-post",
        type: "POST",
        data: {
            data: value,
            column: column,
            type: "spotlight",
            postId: spotlightId
        }
    })
};


const summary = document.getElementById("summary");
summary.addEventListener("blur", function() {
    sendEdit(summary.innerText, "summary")
});

const imageHref = document.getElementById("image");
if (imageHref) {
    imageHref.addEventListener("blur", function() {
        sendEdit(imageHref.innerText, "leadImage")
    })
};

const content = document.getElementById("content");
content.addEventListener("blur", function() {
    sendEdit(content.innerHTML, "content")
});