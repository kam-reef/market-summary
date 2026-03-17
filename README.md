
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
Market signals are mixed. Equities (SPY) remain above their 200‑day moving average, suggesting ongoing bullish breadth, but leadership weakness is evident as QQQ trades below its 100‑day MA and ARKK has posted a notable three‑month decline. Volatility readings are conflicted: VIX sits in the mid‑20s (elevated but not panic), while OVX is very high, implying significant oil‑market stress that can spill into equity sentiment and inflation expectations. Meanwhile, Treasury yields are elevated (TNX > 4%), which increases discount‑rate pressure on growth stocks and may weigh on long‑duration assets. Overall, the environment favors cautious positioning: stay diversified, consider shorter-duration equity exposure or hedges, and monitor energy- and rate-driven event risk.

Market summary (bullets):
- SPY: 669.03, 200‑day MA 659.00 — price above 200MA (bullish breadth signal).
- QQQ: 600.38, 100‑day MA 614.71 — price below 100MA (leadership weakness).
- ARKK: -10.37% over 3 months — meaningful recent drawdown in thematic/growth exposure.
- VIX: 23.51 — elevated volatility (risk elevated but not extreme).
- TNX: 4.23% — higher Treasury yields putting pressure on growth/long-duration assets.
- OVX: 95.92 (regime: high) — very high oil volatility, a notable source of macro/earnings risk.
- Net view: Mixed signals — equity internals supportive at the broad index level, but tech/growth leadership and commodity-driven inflation risk create asymmetric downside risk; maintain risk controls.

Data files referenced:
- /data/SPY_snapshot.json
- /data/QQQ_snapshot.json
- /data/ARKK_snapshot.json
- /data/VIX_snapshot.json
- /data/TNX_snapshot.json
- /data/OVX_snapshot.json

[Audio](https://raw.githubusercontent.com/kam-reef/market-summary/main/audio/latest.mp3)
[RSS](https://kam-reef.github.io/market-summary/feed.xml)

---

## Market Charts

### SPY Trend
![Market Chart](charts/spy.png)

### QQQ Trend
![Market Chart](charts/qqq.png)

### ARKK Drawdown
![ARKK VIX Chart](charts/arkk.png)

### VIX Trend
![Market Chart](charts/vix.png)

### TNX Trend
![Market Chart](charts/tnx.png)

### OVX Trend
![Market Chart](charts/ovx.png)

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
