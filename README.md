
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
The market picture is mixed and warrants caution. Equities (SPY) remain above the 200-day moving average, signaling underlying bullish breadth, but leadership is uneven — QQQ is below its 100-day MA and ARKK has shown a notable 3‑month decline. Volatility measures are conflicted: VIX sits in the mid-20s (23.51), not in panic territory but elevated versus typical calm regimes, while OVX is extremely high (95.92), indicating outsized oil-market stress that can propagate to equities and inflation expectations. Rising Treasury yields (TNX 4.23%, above 4%) increase discount-rate pressure on growth stocks and corporate financing costs. Overall, upside remains possible, but asymmetric risks from energy shocks and higher rates suggest trimming exposure, favoring quality and duration-aware positioning, and keeping cash or hedges ready.

Market summary (bullet points):
- SPY: Price 669.03 vs 200‑day MA 659.0 — trading above its 200‑day MA, bullish long-term trend.
- QQQ: Price 600.38 vs 100‑day MA 614.71 — below its 100‑day MA, indicating weakness in large-cap tech leadership.
- ARKK: 3‑month change -10.37% — active-tech/innovation ETF showing material recent underperformance.
- VIX: 23.51 — elevated volatility, neither calm (<20) nor extreme (>25+), implying uncertain investor sentiment.
- TNX (10‑yr yield): 4.23% — above 4%, signaling tighter financial conditions and pressure on growth valuations.
- OVX (oil vol): 95.92 — extremely high oil volatility, a significant tail-risk for inflation and corporate margins.
- Regime label: Mixed Signals (🟡) — bullish breadth in broad market but sectoral stress, rising rates, and oil volatility create uneven risk-reward.

Data files:
- /data/SPY_snapshot.json
- /data/QQQ_snapshot.json
- /data/ARKK_snapshot.json
- /data/VIX_snapshot.json
- /data/TNX_snapshot.json
- /data/OVX_snapshot.json

(Use these raw files for verification or to drive automated models.)

[Audio](https://raw.githubusercontent.com/kam-reef/market-summary/main/audio/latest.mp3)
[RSS](https://kam-reef.github.io/market-summary/feed.xml)

---

## Market Charts

### SPY Trend vs VIX
![Market Chart](charts/market_chart.png)

### ARKK Drawdown vs VIX
![ARKK VIX Chart](charts/arkk_vix_chart.png)

---

## Market Snapshot

- SPY: 669.03 (200MA: 659.0)
- QQQ: 600.38 (100MA: 614.71)
- ARKK 3M Change: -10.37%

- VIX: 23.51
- TNX (10Y Yield): 4.23%
- OVX (Oil Volatility): 95.92

## Data

- Snapshot [data/market_snapshot.json](data/market_snapshot.json) 
- Signals: [data/signals.json](data/signals.json)  
- History: [data/history.json](data/history.json)
