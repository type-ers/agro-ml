const nav = document.getElementById("navbar");
const mobileNav = document.querySelector(".mobile-navigation");
const loginBtn = document.querySelector(".login");
//navbar
mobileNav.addEventListener('click', () => {
    if (nav.getAttribute("data-visible") === "false") {
        nav.style.transform = "translateX(0%)";
        nav.setAttribute("data-visible", true);
    } else {
        nav.style.transform = "translateX(100%)";
        nav.setAttribute("data-visible", false);
    }
});

loginBtn.addEventListener('click', () => {
    window.open("./login.html","_blank")
})