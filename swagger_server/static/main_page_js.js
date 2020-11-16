let link = function(link) {
    window.location.href = link;
}

function onStartButtonClicked() {
    setTimeout(() => {link("../choice_page/choice_page.html")}, 500);
}

let animateButton = function(e) {
    e.preventDefault;
    e.target.classList.remove('animate');

    e.target.classList.add('animate');
    setTimeout(function(){
        e.target.classList.remove('animate');
    },700);
};

let bubblyButtons = document.getElementsByClassName("bubbly-button");

for (let i = 0; i < bubblyButtons.length; i++) {
    bubblyButtons[i].addEventListener('click', animateButton, false);
}

let myStartButton = document.querySelector("#startButton");
myStartButton.addEventListener("click", onStartButtonClicked);