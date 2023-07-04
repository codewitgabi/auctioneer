const checkoutForm = document.getElementById("checkout-form");
const paymentWrapper = document.querySelector(".payment-wrapper");

checkoutForm.addEventListener("submit", (e) => {
  e.preventDefault();

  checkoutForm.style.display = "none";
  paymentWrapper.style.display = "block";
});

paypal.Buttons({
  createOrder: (data, actions) => {
    return actions.order.create({
      purchase_units: [{
        amount: {
          value: Number(`${ cartTotal }`)
        }
      }]
    });
  },
  onApprove: (data, actions) => {
    return actions.order.capture().then(function(orderData) {
      console.log("Transaction Successful!!");
      window.location.href = "/";
    });
  }
}).render('#paypal-button-container');