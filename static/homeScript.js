var scroller = document.getElementById("scroller");
var scrollerCards = scroller.querySelectorAll(".scroller-card");
var locked = false;

const scrollRight = document.getElementById("right-scroller-arrow");
const scrollLeft = document.getElementById("left-scroller-arrow");


scrollRight.addEventListener("click", function() {
    if (!locked) {
        locked = true;
        setTimeout(() => {locked = false}, 500)
        const cardHeight = scrollerCards[0].clientHeight;

        if (scroller.scrollTop === (scroller.scrollHeight - cardHeight)) {
            scroller.scrollTop = 0;
        } else {
            scroller.scrollTop += cardHeight;
        };
    };
})

scrollLeft.addEventListener("click", function() {
    if (!locked) {
        locked = true;
        setTimeout(() => {locked = false}, 500)
        const cardHeight = scrollerCards[0].clientHeight;

        if (scroller.scrollTop === 0) {
            scroller.scrollTop = scroller.scrollHeight;
        } else {
            scroller.scrollTop -= cardHeight;
        }
    };
})

var titles = document.querySelectorAll(".small-card-title");
titles.forEach((title) => {
    title.innerHTML = title.innerHTML.replace("%3F", "?");
});

var bigTitles = document.querySelectorAll(".big-card-title");
bigTitles.forEach((title) => {
    title.innerHTML = title.innerHTML.replace("%3F", "?");
})

var artists = document.querySelectorAll(".small-card-artist");
artists.forEach((artist) => {
    artist.innerHTML = artist.innerHTML.replace("%3F", "?");
});

var bigArtists = document.querySelectorAll(".big-card-artist");
bigArtists.forEach((title) => {
    title.innerHTML = title.innerHTML.replace("%3F", "?");
})

/*
scrollRight.addEventListener("click", () => {
    if (!locked) {

        let newCardIndex = currentCardIndex + 1;
        if (newCardIndex >= scrollerCards.length) {
            newCardIndex = 0;
        };

        let currentCard = scrollerCards[currentCardIndex];
        let newCard = scrollerCards[newCardIndex];

        currentCard.classList.add("closed");
        currentCard.style.translate = "100px 0px";
        locked = true;
        setTimeout(function() {
            newCard.style.translate = "0px 0px";
            newCard.classList.remove("closed"); 
            locked = false;
        }, 600);

        currentCardIndex = newCardIndex;
    };
});

scrollLeft.addEventListener("click", () => {
    if (!locked) {

        let newCardIndex = currentCardIndex - 1;
        if (newCardIndex < 0) {
            newCardIndex = scrollerCards.length - 1;
        };

        console.log(newCardIndex)

        let currentCard = scrollerCards[currentCardIndex]
        let newCard = scrollerCards[newCardIndex]

        currentCard.classList.add("closed");
        currentCard.style.translate = "-100px 0px";
        locked = true;
        setTimeout(function() {
            newCard.style.translate = "0px 0px";
            newCard.classList.remove("closed"); 
            locked = false;
        }, 600);

        currentCardIndex = newCardIndex;
    };
});
*/
