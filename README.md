
# Market Risk Monitor

![Market Regime](https://img.shields.io/badge/Market%20Regime-Mixed-yellow)

**🟡 Mixed Signals**  
**Score:** Downturn 0/3 | Recovery 1/3  
**Last Updated:** 2026-03-17

---

⚠️ **Disclaimer**

This project is an experimental data pipeline and educational demonstration.
It is **not financial advice**. The signals and AI commentary are generated
automatically from public market data and may be incomplete, delayed, or
incorrect. Do not make investment decisions based solely on this repository.

---

## AI Risk Commentary

Risk commentary:
The market shows mixed signals. SPY trading modestly above its 200‑day moving average suggests underlying breadth and longer-term support, but QQQ below its 100‑day MA and a VIX around 23.5 indicate elevated near‑term uncertainty and rotational weakness in growth/tech. ARKK’s 3‑month decline (-10.37%) reinforces that risk appetite for high‑beta or concentrated innovation names is softer. Keep position sizes and leverage conservative, watch for momentum confirmation (QQQ reclaiming its 100‑day MA or VIX settling below 20) before adding exposure, and use clear stops or hedges given the potential for short‑term volatility.

Market summary (bullets):
- SPY: 669.03, 200‑day MA = 659.00 — trading above 200MA (bullish longer term).
- QQQ: 600.38, 100‑day MA = 614.71 — below 100MA (shorter‑term weakness in tech).
- ARKK: three‑month change = -10.37% — meaningful recent drawdown in innovation/concentrated ETF.
- VIX: 23.51 — elevated implied volatility, between calm (<20) and stressed (>25) regimes.
- Regime label: 🟡 Mixed Signals — longer‑term support with near‑term rotational risk and higher volatility.
- Tactical implication: consider reducing concentration in high‑beta names, use hedges or tighter risk controls, and wait for clearer confirmation from QQQ/VIX before materially increasing exposure.

Raw data files:
- /data/SPY.json
- /data/QQQ.json
- /data/ARKK.json
- /data/VIX.json

---

## Market Charts

### SPY Trend vs VIX
![Market Chart](charts/market_chart.png)

### ARKK Drawdown vs VIX
![ARKK VIX Chart](charts/arkk_vix_chart.png)

---

## Data

- Snapshot: [data/market_snapshot.json](data/market_snapshot.json)  
- Signals: [data/signals.json](data/signals.json)  
- History: [data/history.json](data/history.json)
