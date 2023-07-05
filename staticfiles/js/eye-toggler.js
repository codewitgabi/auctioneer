const eye = document.querySelector("#eye");
const password = document.querySelector("#password");
let count = 0;


eye.addEventListener("click", () => {
  if (count % 2 === 0) {
    eye.classList.remove("bi-eye-slash");
    eye.classList.add("bi-eye");
    password.type = "text";
  } else {
    eye.classList.remove("bi-eye");
    eye.classList.add("bi-eye-slash");
    password.type = "password";
  }

  count++;
})