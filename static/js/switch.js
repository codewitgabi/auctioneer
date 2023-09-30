const sliders = document.querySelectorAll(".slider");
const switchUserRole = `${window.location.origin}/toggle-user-as-marketer`;
const userHasRole = JSON.parse(document.getElementById("perm").textContent);


sliders.forEach((slider) => {
  if (userHasRole) {
    slider.classList.add("on");
    slider.nextElementSibling.textContent = "ON";
  }
  slider.addEventListener("click", () => {
    slider.classList.toggle("on");
    window.location.href = switchUserRole;
    if (slider.classList.contains("on")) {
      slider.nextElementSibling.textContent = "ON";
    } else {
      slider.nextElementSibling.textContent = "OFF";
    }
  });
});