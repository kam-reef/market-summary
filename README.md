
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
Mixed signals dominate the tape. Equity breadth is holding up (SPY above its 200‑day), but momentum in growth names is soft (QQQ below its 100‑day) and oil volatility is extreme (OVX >100), which raises tail‑risk for energy and commodities-sensitive sectors. Elevated Treasury yields (TNX 4.23%) increase discounting pressure on long‑duration growth names, while VIX in the low‑20s signals caution without panic. Net: posture should be guarded — favor diversified, quality exposure and keep position sizing tight until clearer directional confirmation.

Market summary (bullets):
- Equities: SPY 669.03 > 200‑day MA 659.0 — constructive for broad market; QQQ 600.38 < 100‑day MA 614.71 — leadership rotation / growth softness.
- Volatility: VIX 23.51 — above 20 but below panic levels (mixed volatility environment).
- Rates: TNX (10‑yr yield) 4.23% — materially elevated, a headwind for long-duration assets.
- Commodities/energy risk: OVX 101.97 — very high oil volatility, potential for sharp moves in energy names and related sectors.
- Thematic/active risk: ARKK three‑month change −10.37% — recent drawdown in high‑beta/tech innovation exposure.
- Overall read: Mixed signals — offensive positions should be selective; use hedges or reduced sizing where sensitivity to rates or oil is high.

Raw data files:
- /data/SPY.json
- /data/QQQ.json
- /data/ARKK.json
- /data/VIX.json
- /data/TNX.json
- /data/OVX.json

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
