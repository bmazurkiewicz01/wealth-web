document.querySelectorAll(".portfolio-nav-item").forEach((link) => {
    if (link.href.replaceAll("/", "") === window.location.href.replaceAll("/", "")) {
        link.classList.add("active");
        link.setAttribute("aria-current", "page");
    }
});

const modal = document.getElementById("myModal");

const btn = document.getElementById("openModal");

const span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
    modal.style.display = "block";
}

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}