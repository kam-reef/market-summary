
# Market Risk Monitor

⚠️ **Disclaimer**

This project is an experimental data pipeline and educational demonstration.
It is **not financial advice**. The signals and AI commentary are generated
automatically from public market data and may be incomplete, delayed, or
incorrect. Do not make investment decisions based upon any data, display, words or summary in this repository.

Last Updated: 2026-03-17

## Market Regime
🟡 Mixed Signals

## AI Risk Commentary

Risk commentary:
Market signals are mixed. SPY is trading slightly above its 200‑day MA, which supports a constructive bias for broad large-cap equities, but QQQ sits well below its 100‑day MA and ARKK has shown a material 3‑month decline, indicating underlying weakness in growth/innovation names. Elevated VIX at 27.19 signals meaningful near‑term volatility and a higher risk of short‑term drawdowns. Overall, position sizing should reflect uncertainty — prefer defensive tilts, tighter stops, or reduced exposure until clearer regime confirmation.

Market summary (bullets):
- SPY: 662.29 vs 200‑day MA 658.60 — price slightly above long‑term trend (bullish signal).
- QQQ: 593.72 vs 100‑day MA 614.82 — trading below shorter-term trend (bearish for tech/growth).
- ARKK: -14.39% over 3 months — significant recent decline in innovation-focused equities.
- VIX: 27.19 (over 25) — volatility elevated; higher tail‑risk and risk premia.
- Regime label: 🟡 Mixed Signals — breadth between large caps and growth is divergent; expect choppy, higher‑volatility action.
- Suggested tactical posture: defensive or diversified, smaller position sizes, and use options/hedges if downside protection is required.

Data files referenced:
- /data/SPY_snapshot.json
- /data/QQQ_snapshot.json
- /data/ARKK_snapshot.json
- /data/VIX_snapshot.json
- /data/signals.json

## Market Charts

### SPY Trend vs VIX
![Market Chart](charts/market_chart.png)

### ARKK Drawdown vs VIX
![ARKK VIX Chart](charts/arkk_vix_chart.png)

## Market Snapshot
[data/market_snapshot.json](data/market_snapshot.json)

## Raw Signals
[data/signals.json](data/signals.json)
