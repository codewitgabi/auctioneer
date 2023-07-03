const menuToggler = document.querySelector("#nav-toggler");
const navLinks = document.querySelector("#nav-links");


menuToggler.addEventListener("click", () => {
  if (navLinks.style.right === "" || navLinks.style.right === "-100%") {
    navLinks.style.right = "0";
    menuToggler.classList.remove("bi-list");
    menuToggler.classList.add("bi-x");
  } else {
    navLinks.style.right = "-100%";
    menuToggler.classList.remove("bi-x");
    menuToggler.classList.add("bi-list");
  }
})
