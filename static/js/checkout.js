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
      onst lotId = 'uuid4'; // Replace with the actual lot ID
      const apiUrl = '/mark_lot_as_paid/';
      const data = {
        lot_id: lotId,
      };

      fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          if (response.ok) {
            // The lot has been successfully marked as paid
            console.log('Lot marked as paid.');
          } else {
            // Handle the case where the request fails
            console.error('Failed to mark the lot as paid.');
          }
        })
        .catch((error) => {
          console.error('An error occurred while marking the lot as paid:', error);
        });
      window.location.href = "/";
    });
  }
}).render('#paypal-button-container');
