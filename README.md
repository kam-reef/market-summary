
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
The market shows mixed signals — large-cap breadth (SPY) remains slightly above its 200-day average, which supports a constructive backdrop, but leadership in growth/tech (QQQ) is below its 100-day trend and volatility sits in the mid-20s (VIX ≈ 23.5), implying elevated uncertainty. That combination increases the risk of short-term chop and sector rotation: defensive cash management and selective position sizing are prudent until clearer trend confirmation (e.g., QQQ reclaiming its 100MA or a sustained drop in VIX below ~20).

Market summary:
- SPY: 669.03, above 200-day MA (659.0) — bullish long-term bias but not large upside outperformance.
- QQQ: 600.38, below 100-day MA (614.71) — leadership weakness; growth/tech under pressure.
- ARKK: -10.37% over 3 months — thematic/innovation exposure has pulled back meaningfully.
- VIX: 23.51 — volatility elevated, signaling increased market uncertainty (neither calm nor panic).
- Overall regime: Mixed signals — long-term equity trend intact but leadership and volatility suggest caution; expect sideways-to-volatile trading and favor risk management.

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
