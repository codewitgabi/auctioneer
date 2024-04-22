let slidePosition = 1;
SlideShow(slidePosition);

// forward/Back controls
function plusSlides(n) {
  slidePosition += n;
  SlideShow(slidePosition);
}

//  images controls
function currentSlide(n) {
  slidePosition = n;
  SlideShow(slidePosition);
}

function SlideShow(n) {
  let i;
  let slides = document.getElementsByClassName("slide");
  let circles = document.getElementsByClassName("dots");
  if (n > slides.length) {
    slidePosition = 1;
  }
  if (n < 1) {
    slidePosition = slides.length;
  }
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < circles.length; i++) {
    circles[i].className = circles[i].className.replace(" enable", "");
  }
  slides[slidePosition - 1].style.display = "block";
  circles[slidePosition - 1].className += " enable";
}
