const title = document.getElementById("title");
const artist = document.getElementById("artist");
var albumId = (title.innerText + "_" + artist.innerText).replaceAll(" ", "-");

function addTrack(last_track_index) {
    $.ajax({
        url: '/add-rc-song',
        type: 'POST',
        data: {
            albumId: albumId,
            index: +last_track_index + 1
        }
    });
    location.reload();
}
    
function deleteAlbum() {
    $.ajax({
        url: "/delete-rc",
        type: "POST",
        data: {
            albumId: albumId
        }
    })
    goToPage("/")
}

function sendToFlask(data, column) {
    $.ajax({
        url: "/update-rc",
        type: "POST",
        data: {
            data: data,
            column: column,
            albumId: albumId
        }
    })
}

function trackToFlask(data, column, index) {
    const trackId = albumId + "_" + index
    $.ajax({
        url: "/update-rc-track",
        type: "POST",
        data: {
            data: data,
            column: column,
            trackId: trackId,
            albumId: albumId
        }
    });
}

function updateTrackQuality() {
    $.ajax({
        url: '/update-rc-track-quality',
        type: "POST",
        data: {
            albumId: albumId
        }
    });
    location.reload();
}

function deleteTrack(songIndex) {
    const songId = albumId + "_" + songIndex;
    $.ajax({
        url: "/delete-rc-track",
        type: "POST",
        data: {
            songId: songId
        }
    });
    location.reload();
}

function openDelete() {
    let deleteForm = document.getElementById("delete-form");
    let overlay = document.getElementById("form-background-overlay");

    deleteForm.classList.remove("closed");
    overlay.classList.remove("closed");
}

function closeDelete() {
    let deleteForm = document.getElementById("delete-form");
    let overlay = document.getElementById("form-background-overlay");

    deleteForm.classList.add("closed");
    overlay.classList.add("closed");
}

function goToPage(page) {
    window.location.href = (page);
}

const spotifyLink = document.getElementById("spotify-link");
spotifyLink.addEventListener("blur", function() {
    sendToFlask(spotifyLink.innerText, "spotifyLink")
});

const image = document.getElementById("image");
image.addEventListener("blur", function() {
    sendToFlask(image.innerText, "image")
});

const notes = document.getElementById("notes");
notes.addEventListener("blur", function() {
    sendToFlask(notes.innerText, "notes")
});

const imageCredit = document.getElementById("image-copyright");
imageCredit.addEventListener("blur", function() {
    sendToFlask(imageCredit.innerText, "imageCopyright")
});

const date = document.getElementById("date");
date.addEventListener("blur", function() {
    sendToFlask(date.innerText, "date");
});

const table = document.getElementById("admin-table");
if (table) {
    const rows = table.querySelectorAll("tr");
    rows.forEach((track, index) => {
        const name = track.cells[0];
        const comments = track.cells[1];
        const rating = track.cells[2];

        name.addEventListener("blur", function() {
            trackToFlask(name.innerText, "name", index)
        })

        comments.addEventListener("blur", function() {
            trackToFlask(comments.innerText, "comments", index)
        })

        rating.addEventListener("blur", function() {
            trackToFlask(rating.innerText, "rating", index)
        })
    })
}