const ws = new WebSocket("ws://localhost:8000/ws");
const form = document.getElementById("orderForm");

form.addEventListener("submit", (e) => {
    e.preventDefault();
    const order = {
        symbol: document.getElementById("symbol").value,
        price: parseFloat(document.getElementById("price").value),
        quantity: parseInt(document.getElementById("quantity").value),
        side: document.getElementById("side").value
    };
    ws.send(JSON.stringify(order));
});

ws.onmessage = (event) => {
    const response = JSON.parse(event.data);
    document.getElementById("response").innerHTML = 
        `Order #${response.order_id}: ${response.status}`;
};