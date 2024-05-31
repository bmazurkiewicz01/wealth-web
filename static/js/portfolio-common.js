document.querySelectorAll(".portfolio-nav-item").forEach((link) => {
    if (link.href.replaceAll("/", "") === window.location.href.replaceAll("/", "")) {
        link.classList.add("active");
        link.setAttribute("aria-current", "page");
    }
});