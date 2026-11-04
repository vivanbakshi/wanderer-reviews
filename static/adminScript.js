var stat = document.getElementById("stat").innerText;

/*
function sendEdit(value, albumId) {
    $.ajax({
        url: "/admin-stats-edit",
        type: "POST",
        data: {
            column: stat, 
            albumId: albumId,
            value: value
        }
    })
};
*/

function sendToFlask(albumId, value) {
    console.log(albumId, value);
    $.ajax({
        url: "/admin-stats-edit",
        type: "POST",
        data: {
            data: value,
            column: stat,
            albumId: albumId
        }
    });
};

function goToPage(page) {
    window.location.href = (page);
}


const albums = document.querySelectorAll(".admin-stat-album");
albums.forEach((album) => {
    const albumId = album.cells[0];
    const albumstat = album.cells[1];
    console.log(albumId.innerText, albumstat.innerText)

    albumstat.addEventListener("blur", () => {
        sendToFlask(albumId.innerText, albumstat.innerText);
    });
});

