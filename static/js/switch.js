const sliders = document.querySelectorAll(".slider");
sliders.forEach((slider) => {
  slider.addEventListener("click", () => {
    slider.classList.toggle("on");
    if (slider.classList.contains("on")) {
      slider.nextElementSibling.textContent = "ON";
    } else {
      slider.nextElementSibling.textContent = "OFF";
    }
  });
});