// LIVE PRICE TICKER (Animated)
const tickerContainer = document.getElementById("live-ticker");

async function fetchPrices() {
    try {
        const response = await fetch("/api/prices");
        const data = await response.json();

        tickerContainer.innerHTML = ""; // Clear old prices

        data.forEach(item => {
            const span = document.createElement("span");
            span.className = "ticker-item";
            span.innerHTML = `${item.symbol}: <strong>${item.price}</strong>`;
            tickerContainer.appendChild(span);
        });

    } catch (err) {
        console.error("Ticker error:", err);
    }
}

// Update every 3 seconds
setInterval(fetchPrices, 3000);
fetchPrices();

