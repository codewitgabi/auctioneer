const biddersDisplayBox = document.querySelector("#bidders-display-box");
const bidInput = document.querySelector("#bid-move-amt");
const bidBtn = document.querySelector("#bid-btn");
let interval;
let protocol = "ws:";
if (window.location.protocol === "https:") {
  protocol = "wss:";
}
const socket_url = `${protocol}//${window.location.host}/bid/${lot_id}/`;

lot_has_ended();

const socket = new WebSocket(socket_url);

socket.onopen = function (e) {
  socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const bids = data.bids;

    if (data.type === "bids") {
      let bidders = "";
      for (let index in bids) {
        bidders += `<tr>
        <td class="sn">${Number(index) + 1}.</td>
        <td>${bids[index].bidder}</td>
        <td>$ ${bids[index].bid}</td>
        </tr>`;
      }
      biddersDisplayBox.innerHTML = bidders;
    }
  };
};

bidBtn.addEventListener("click", (e) => {
  fetch(getLotPriceURL)
  .then((response) => response.json())
  .then((data) => {
    let lotPrice = data.lot_price;
    let setBid = bidInput.value;
    let bid = Number(setBid);

    if (bid <= lotPrice && setBid !== "") {
      // do validation here
      alert("Amount too small");
      return;
    }

    if (setBid === "") {
      bid = lotPrice + lotIncrementalValue;
    }

    socket.send(
      JSON.stringify({
        bid: bid,
      })
    );
  });
});

function mark_lot_as_sold(lot_id) {
  fetch(markAsSoldURL);
}

function lot_has_ended() {
  interval = window.setInterval(() => {
    fetch(getLotEndtimeUrl)
    .then((resp) => resp.json())
    .then((data) => {
      if (data.has_ended) {
        window.clearInterval(interval);
        mark_lot_as_sold(lot_id);
        window.location.href = "/";
      }
    });
  }, 1000);
}