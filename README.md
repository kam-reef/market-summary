
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
The market shows mixed signals — broad U.S. equities (SPY) are trading modestly above their 200‑day moving average, which is constructive, but leadership and risk appetite are uneven. Tech (QQQ) sits below its 100‑day MA, long yields (TNX) are elevated above 4%, and oil volatility (OVX) is extremely high. VIX is in the mid‑20s (neither calm nor panic). Elevated rates and very high oil volatility increase macro and sectoral risk, while SPY’s above‑200MA status tempers but does not eliminate the potential for rotation or volatility spikes. Position sizes should be conservative, hedges reviewed (especially energy and rate-sensitive exposures), and stop/loss discipline maintained.

Market summary (bullets):
- SPY: 669.03 vs 200‑day MA 659.00 — trading above 200MA (bullish signal).
- QQQ: 600.38 vs 100‑day MA 614.71 — trading below 100MA (weakness in large‑cap tech).
- ARKK: three‑month change −10.37% — no flagged 3‑month collapse but notable drawdown.
- VIX: 23.51 — elevated volatility environment (neither low nor extreme).
- TNX: 4.23% — yields above 4% (tightening/market sensitivity to rates).
- OVX: 95.92 — extremely high oil volatility (major oil market stress or event risk).
- Overall regime: Mixed signals — cautious stance warranted; monitor rates and energy volatility for near‑term directional risk.

Raw data files (available):
- /data/SPY.json
- /data/QQQ.json
- /data/ARKK.json
- /data/VIX.json
- /data/TNX.json
- /data/OVX.json

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
