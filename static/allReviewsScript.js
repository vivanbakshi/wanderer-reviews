const albumsContainer = document.getElementById("albums-container");
var albums = albumsContainer.querySelectorAll(".album-container");

function displayAllAlbums() {
    albums.forEach((album) => {
        album.classList.remove("closed")
    });
};

function filterAlbums(key) {
    if (key === "none") {
        displayAllAlbums();
    } else {
        albums.forEach((album) => {
            if ((album.dataset.tags.includes(key))) {
                album.classList.remove("closed");
            } else {
                album.classList.add("closed");
            };
        });
    };
};

function sortAlbums(key) {
    let albumsToSort = Array.from(albums);

    albumsToSort.sort(function(a, b) {
        if (key === "rating") {
            if (isNaN(a.dataset.rating)) return 1;
            if (isNaN(b.dataset.rating)) return -1;
            return (parseFloat(b.dataset.rating) > parseFloat(a.dataset.rating)) ? 1:-1;

        } else if (key === "date") {
            if (!(a.dataset.date)) return -1;
            if (!(b.dataset.date)) return 1;
            return (b.dataset.date > a.dataset.date) ? 1:-1;

        } else if (key === "alphabetical") {
            return ((b.dataset.name.toUpperCase()) > a.dataset.name.toUpperCase()) ? -1:1;
        };
    });

    return albumsToSort;
};

function searchAlbums(searchBy, searchTerm) {
    if (searchBy === "name") {
        albums.forEach(album => {
            if (album.dataset.name.toUpperCase().includes(searchTerm.toUpperCase())) {
                album.classList.remove("closed");
            } else {
                album.classList.add("closed");
            };
        });

    } else if (searchBy === "artist") {
        albums.forEach(album => {
            if (album.dataset.artist.toUpperCase().includes(searchTerm.toUpperCase())) {
                album.classList.remove("closed");
            } else {
                album.classList.add("closed");
            };
        });

    } else if (searchBy === "genre") {
        albums.forEach(album => {
            if (album.dataset.genre.toUpperCase().includes(searchTerm.toUpperCase())) {
                album.classList.remove("closed");
            } else {
                album.classList.add("closed");
            };
        });
    };
};

function resetTools() {
    displayAllAlbums();
    const sortedAlbums = sortAlbums("date");
    sortedAlbums.forEach(album => albumsContainer.append(album));

    const filterSelect = document.getElementById("filter-select");
    filterSelect.value = "none";

    const sortSelect = document.getElementById("sort-select");
    sortSelect.value = "date";

    const searchBy = document.getElementById("search-by");
    searchBy.value = "name";

    const searchTerm = document.getElementById("search-term");
    searchTerm.value = "";
};

const params = new URLSearchParams(window.location.search);
const filterParam = params.get("filter");
const sortParam = params.get("sort");
const searchByParam = params.get("search-by");
const searchParam = params.get("search");
const hofParam = params.get("hof");

if (filterParam) {
    document.getElementById("filter-select").value = filterParam;
    filterAlbums(filterParam);
};

if (sortParam) {
    document.getElementById("sort-select").value = sortParam;
    const sortedAlbums = sortAlbums(sortParam);
    sortedAlbums.forEach(album => albumsContainer.append(album));
};

if (searchByParam && searchParam) {
    document.getElementById("search-by").value = searchByParam;
    document.getElementById("search-term").value = searchParam;
    searchAlbums(searchByParam, searchParam);
};

if (hofParam) {
    if (hofParam === "true"){
        albums.forEach(album => {
            if (+(album.dataset.rating) >= 82.5) {
                album.classList.remove("closed");
            } else {
                album.classList.add("closed");
            };
            const sortedHofAlbums = sortAlbums("rating");
            sortedHofAlbums.forEach(album => albumsContainer.append(album));
        });
    };
};


const filterForm = document.getElementById("toolbar-filter-form");

filterForm.addEventListener("submit", function() {
    const filterSelect = document.getElementById("filter-select").value;
    filterAlbums(filterSelect);
});


const sortForm = document.getElementById("toolbar-sort-form");

sortForm.addEventListener("submit", function() {
    const sortSelect = document.getElementById("sort-select").value;
    const sortedAlbums = sortAlbums(sortSelect);

    sortedAlbums.forEach(album => albumsContainer.append(album));
});

const toolbarSearchForm = document.getElementById("toolbar-search-form");

toolbarSearchForm.addEventListener("submit", function() {
    console.log("submitted")
    const searchBy = document.getElementById("search-by").value;
    const searchTerm = document.getElementById("search-term").value;
    searchAlbums(searchBy, searchTerm);
});


var titles = document.querySelectorAll(".small-card-title");
titles.forEach((title) => {
    title.innerHTML = title.innerHTML.replace("%3F", "?");
});

var artists = document.querySelectorAll(".small-card-artist");
artists.forEach((artist) => {
    artist.innerHTML = artist.innerHTML.replace("%3F", "?");
});
