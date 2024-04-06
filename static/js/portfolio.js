document.querySelectorAll(".portfolio-nav-item").forEach((link) => {
    console.log(link.href.replaceAll("/", ""));
    console.log(window.location.href.replaceAll("/", ""));
    if (link.href.replaceAll("/", "") === window.location.href.replaceAll("/", "")) {
        link.classList.add("active");
        link.setAttribute("aria-current", "page");
    }
});