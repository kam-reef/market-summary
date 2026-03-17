
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
The market shows mixed signals — equities (SPY) remain above the 200-day moving average, which is constructive for the broad market, but other risk indicators are cautionary. Tech (QQQ) is trading below its 100-day MA, suggesting leadership weakness. Volatility across asset classes is elevated: VIX is in the mid-20s (not extreme but above complacency levels), OVX is extremely high near 96 indicating very large crude-oil volatility, and the 10-year yield (TNX) is firmly above 4%, which increases discount rates and can pressure growth/momentum stocks. Together this suggests a higher-risk environment where headline or commodity-driven shocks could quickly widen market moves. Position sizing, tighter stops or hedges, and selective exposure to lower-duration or value-oriented assets are prudent until clearer regime confirmation.

Market summary (bullets):
- Equities: SPY 669.03 > 200‑day MA 659.0 — broad market still above long-term trend (bullish for market breadth).
- Tech leadership: QQQ 600.38 < 100‑day MA 614.71 — leadership weakening (bearish for growth/tech).
- Thematic/innovation risk: ARKK three-month change -10.37% — meaningful recent drawdown in high-beta/innovation names.
- Volatility: VIX 23.51 — elevated equity volatility (neither calm nor panic), implies caution.
- Rates: TNX yield 4.23% — materially higher rates, upward pressure on discount rates and growth multiples.
- Oil volatility: OVX 95.92 — extreme oil-market volatility, heightened commodity-related risk and potential inflation/real-economy impacts.
- Net read: Mixed regime — underlying trend intact but leadership and cross-asset volatility warrant defensive sizing and selective positioning.

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

## Market Snapshot

- SPY: 669.03 (200MA: 659.0)
- QQQ: 600.38 (100MA: 614.71)
- ARKK 3M Change: -10.37%

- VIX: 23.51
- TNX (10Y Yield): 4.23%
- OVX (Oil Volatility): 95.92

- Snapshot [data/market_snapshot.json](data/market_snapshot.json) 
- Signals: [data/signals.json](data/signals.json)  
- History: [data/history.json](data/history.json)
