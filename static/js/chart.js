let chart;

function loadChart(type = "1") {
    const container = document.getElementById("tradingview_chart");
    if (!container || typeof TradingView === "undefined") return;

    container.innerHTML = "";

    chart = new TradingView.widget({
        width: "100%",
        height: 320,
        symbol: "BINANCE:BTCUSDT",
        interval: "1",
        timezone: "Etc/UTC",
        theme: "dark",
        style: type,
        locale: "en",
        toolbar_bg: "#0d0f17",
        enable_publishing: false,
        allow_symbol_change: true,
        container_id: "tradingview_chart"
    });
}

document.addEventListener("DOMContentLoaded", () => {
    loadChart();

    const typeSelect = document.getElementById("chartType");
    if (typeSelect) {
        typeSelect.addEventListener("change", () => {
            loadChart(typeSelect.value);
        });
    }
});

