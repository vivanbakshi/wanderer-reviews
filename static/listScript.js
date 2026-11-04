var formBackgroundOverlay = document.getElementById("form-background-overlay");
var listId = document.getElementById("title").innerText.replaceAll(" ", "-");


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
            postId: listId,
            type: "list"
        }
    })
    goToPage("/")
};

function addItem() {
    $.ajax({
        url: "/add-list-item",
        type: "POST",
        data: {
            postId: listId,
        }
    })
    window.location.reload()
};

function sendEdit(value, column) {
    $.ajax({
        url: "/edit-post",
        type: "POST",
        data: {
            data: value,
            column: column,
            type: "list",
            postId: listId
        }
    })
};

function sendItemEdit(itemNumber, value, column) {
    $.ajax({
        url: "/edit-list-item",
        type: "POST",
        data: {
            itemNumber: itemNumber,
            data: value,
            column: column,
            postId: listId
        }
    })
};

function deleteListItem() {
    $.ajax({
        url: "/delete-list-item",
        type: "POST",
        data: {
            postId: listId
        }
    });
    window.location.reload();
};

const image = document.getElementById("image");
if (image) {
    console.log("image");
    image.addEventListener("blur", function() {
        sendEdit(image.innerText, "leadImage");
    })
};

const summary = document.getElementById("summary");
summary.addEventListener("blur", function() {
    sendEdit(summary.innerText, "summary");
});

const date = document.getElementById("date");
date.addEventListener("blur", function() {
    sendEdit(date.innerText, "dateCreated");
});

const ordered = document.getElementById("ordered");
ordered.addEventListener("blur", function() {
    sendEdit(ordered.innerText, "ordered");
});

const introParagraph = document.getElementById("intro-paragraph");
introParagraph.addEventListener("blur", function() {
    sendEdit(introParagraph.innerHTML, "introParagraph");
});


const allListItems = document.querySelectorAll(".list-item-container");
allListItems.forEach((listItem) => {
    const itemNumber = listItem.querySelector(".list-item-number").innerText;

    const itemTitle = listItem.querySelector(".list-item-title");
    itemTitle.addEventListener("blur", function() {
        sendItemEdit(itemNumber, itemTitle.innerText, "title");
    });

    const itemArtist = listItem.querySelector(".list-item-artist");
    itemArtist.addEventListener("blur", function() {
        sendItemEdit(itemNumber, itemArtist.innerText, "artist");
    });

    const itemContent = listItem.querySelector(".list-item-content");
    itemContent.addEventListener("blur", function() {
        sendItemEdit(itemNumber, itemContent.innerHTML, "content");
    });

    const itemImageHref = listItem.querySelector(".list-item-image-href");
    itemImageHref.addEventListener("blur", function() {
        sendItemEdit(itemNumber, itemImageHref.innerText, "image");
    });
})
