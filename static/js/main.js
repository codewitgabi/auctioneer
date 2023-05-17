const closeMenu = document.getElementById("close-menu");
const openMenu = document.getElementById("open-menu");
const navLinks = document.getElementById("nav-links");

/* Close nav menu */
closeMenu.addEventListener("click", () => {
  navLinks.style.right = "-220px";
})

/* Open nav menu */
openMenu.addEventListener("click", () => {
  navLinks.style.right = "0";
})