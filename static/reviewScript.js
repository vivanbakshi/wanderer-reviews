// SENDS MAIN BODY EDITS TO FLASK
function sendToFlask(value, column, albumId) {
    $.ajax({
        url: '/getedit',
        type: 'POST',
        data: {
            data: value, 
            column: column,
            albumId: albumId
        }
    });
}

// SENDS TRACK BY TRACK EDITS TO FLASK
function tbtToFlask(songId, data, column) {
    $.ajax({
        url: '/update-tbt',
        type: 'POST',
        data: {
            data: data,
            column: column,
            songId: songId,
            albumId: albumId
        }
    })
}

function deleteAlbum(albumId) {
    $.ajax({
        url: "/delete-album",
        type: "POST",
        data: {
            albumId: albumId
        }
    })
    goToPage("/")
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

function showTBT() {
    tbtTable = document.querySelector(".tbt-container");
    tbtButton = document.querySelector(".tbt-button h3.tbt-header");
    if (tbtTable.classList.contains("closed")) {
        console.log("displaying")
        tbtTable.classList.remove('closed')
        tbtButton.innerHTML = "Track by track (Click to hide)"
    } else {
        console.log("removing")
        tbtTable.classList.add('closed')
        tbtButton.innerHTML = "Track by track (Click to show)"
    }
}

function showRanking() {
    ranking = document.querySelector(".ranking-container");
    rankingButton = document.querySelector(".tbt-button h3.ranking-header");
    if (ranking.classList.contains("closed")) {
        console.log("displaying")
        ranking.classList.remove("closed");
        rankingButton.innerHTML = "Track ranking (Click to hide)";
    } else {
        console.log("removing")
        ranking.classList.add("closed");
        rankingButton.innerHTML = "Track ranking (Click to show)";
    }
}

var title = document.getElementById("title");
var artist = document.getElementById("artist");
var albumId = (title.innerText.replaceAll("?", "%3F") + "_" + artist.innerText.replaceAll("?", "%3F")).replaceAll(" ", "-");
console.log(albumId);


function addTbt(songIndex) {
    songId = albumId + "_" + songIndex;
    $.ajax({
        url: "/add-tbt",
        type: "POST", 
        data: {
            songId: songId,
            albumId: albumId
        }
    });
    location.reload();
};

function deleteTbt(songIndex) {
    const songId = albumId + "_" + (+songIndex - 1);
    $.ajax({
        url: "/delete-tbt",
        type: "POST",
        data: {
            songId: songId
        }
    });
    location.reload();
}

function updateTrackQuality() {
    $.ajax({
        url: "/update-review-track-quality",
        type: "POST",
        data: {
            albumId: albumId
        }
    });
    location.reload();
}




const genre = document.getElementById("genre");
genre.addEventListener("blur", function() {
    sendToFlask(genre.innerText, "genre", albumId)
})

const spotifyLink = document.getElementById("spotify-link");
spotifyLink.addEventListener("blur", function() {
    sendToFlask(spotifyLink.innerText, "spotifyLink", albumId) 
})

const imageHref = document.getElementById("image");
imageHref.addEventListener("blur", function() {
    sendToFlask(imageHref.innerText, "image", albumId)
})

const releaseDate = document.getElementById("release-date");
releaseDate.addEventListener("blur", function () {
    sendToFlask(releaseDate.innerText, "releaseDate", albumId)
})

const introParagraph = document.getElementById("intro-paragraph");
if (introParagraph) {
    introParagraph.addEventListener("blur", function() {
        sendToFlask(introParagraph.innerHTML, "introParagraph", albumId)
    })
}

const summaryParagraph = document.getElementById("summary-paragraph");
summaryParagraph.addEventListener("blur", function() {
    sendToFlask(summaryParagraph.innerHTML, "summaryParagraph", albumId)
})

const opinionParagraph = document.getElementById("opinion-paragraph");
opinionParagraph.addEventListener("blur", function() {
    sendToFlask(opinionParagraph.innerHTML, "opinionParagraph", albumId)
})

const rating = document.getElementById("rating");
rating.addEventListener("blur", function() {
    sendToFlask(rating.innerText, "rating", albumId)
})

const cohesiveness = document.getElementById("cohesiveness");
cohesiveness.addEventListener("blur", function() {
    sendToFlask(cohesiveness.innerText, "cohesiveness", albumId)
})

const trackQuality = document.getElementById("track-quality");
trackQuality.addEventListener("blur", function() {
    sendToFlask(trackQuality.innerText, "trackQuality", albumId)
})

const tags = document.getElementById("tags");
tags.addEventListener("blur", function() {
    sendToFlask(tags.innerText, "tags", albumId)
})

const beginnerFriendly = document.getElementById("beginner-friendly");
beginnerFriendly.addEventListener("blur", function() {
    sendToFlask(beginnerFriendly.innerText, "beginnerFriendly", albumId)
})

const imageCopyright = document.getElementById("image-copyright");
imageCopyright.addEventListener("blur", function() {
    sendToFlask(imageCopyright.innerText, "imageCopyright", albumId)
})

const date = document.getElementById("date");
date.addEventListener("blur", function() {
    sendToFlask(date.innerText, "date", albumId)
})


const tbt = document.querySelectorAll(".tbt-track-container");
tbt.forEach((track, index) => {
    const trackName = track.querySelector(".tbt-track-name");
    const trackSuperlative = track.querySelector(".tbt-track-superlative");
    const trackComments = track.querySelector(".tbt-track-comments");
    const trackCollabs = track.querySelector(".tbt-track-collabs");
    const trackRating = track.querySelector(".tbt-track-rating");

    trackName.addEventListener("blur", function() {
        tbtToFlask(albumId + "_" + index, trackName.innerText, "name");
    });

    trackSuperlative.addEventListener("blur", function() {
        tbtToFlask(albumId + "_" + index, trackSuperlative.innerText, "superlative");
    });

    trackComments.addEventListener("blur", function() {
        tbtToFlask(albumId + "_" + index, trackComments.innerText, "comments");
    });

    trackCollabs.addEventListener("blur", function() {
        tbtToFlask(albumId + "_" + index, trackCollabs.innerText, "collabs");
    });

    trackRating.addEventListener("blur", function() {
        tbtToFlask(albumId + "_" + index, trackRating.innerText, "rating");
    });
})

/*const tableBody = document.querySelector("tbody");  // gets the tbt table
const rows = tableBody.querySelectorAll("tr");  // gets all the rows from the table
rows.forEach((row, index) => {  // for each row
    const trackId = index;  // gets index of track (index auto increments per iteration)
    const name = row.cells[0];  
    const comments = row.cells[1];
    const superlative = row.cells[2];

    name.addEventListener("blur", function() {  // add event listener to name
        tbtToFlask(albumId + "_" + trackId, name.innerText, "name");
    });
    
    comments.addEventListener("blur", function() {  // and to comments
        tbtToFlask(albumId + "_" + trackId, comments.innerText, "comments");
    });

    superlative.addEventListener("blur", function() {  // and to superlative
        tbtToFlask(albumId + "_" + trackId, superlative.innerText, "superlative");
    });
});
*/ 


const ol = document.querySelector("ol");  // gets the ordered list for ranking
const tracks = ol.querySelectorAll("li");  // gets each list item (track) in the list
tracks.forEach((track) => {  // for each list item (track) in the list
    const name = track.querySelector("span.ranking-name").innerText;  // gets id of track 
    const collabs = track.querySelector("span.ranking-collabs");
    const rating = track.querySelector("span.ranking-rating");

    if (collabs) {
        collabs.addEventListener("blur", function() {  // add event listener to collabs
            tbtToFlask(name, collabs.innerText, "collabs");
        });
    }

    rating.addEventListener("blur", function() {  // and to rating
        tbtToFlask(name, rating.innerText, "rating");
    });
});
