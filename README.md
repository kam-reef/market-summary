
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

Risk commentary
The market shows mixed signals: large-cap breadth is marginally constructive with SPY trading slightly above its 200‑day moving average, but momentum leadership appears weak (QQQ below its 100‑day MA) and volatility is elevated (VIX > 25). Elevated VIX indicates heightened tail‑risk premium and potential for abrupt downside moves even though the broad index is holding support. Position sizing, tighter risk controls, and preference for higher quality or hedged exposure are prudent until either volatility normalizes or trend leadership reasserts.

Market summary (bullets)
- SPY: 662.29 vs 200‑day MA 658.60 — price is slightly above the 200MA, indicating marginally constructive long‑term bias.
- QQQ: 593.72 vs 100‑day MA 614.82 — trading below the 100MA, signaling weakening momentum among large‑cap growth/tech names.
- ARKK: three‑month change -14.39% — notable recent weakness in innovation/active growth exposure.
- VIX: 27.19 — elevated volatility (>25) implies increased market fear and higher option premia; expect larger intraday moves and wider directional risk.
- Net signal interpretation: Mixed — trend support exists at the index level, but leadership and momentum are inconsistent and risk is elevated; tactical caution recommended.

Raw data files
- /data/SPY_snapshot.json
- /data/QQQ_snapshot.json
- /data/ARKK_snapshot.json
- /data/VIX_snapshot.json
- /data/signals.json

(Use these files for verification or to feed models/algorithms that require the raw inputs.)

## Market Chart

![Market Chart](charts/market_chart.png)

## Market Snapshot
[data/market_snapshot.json](data/market_snapshot.json)

## Raw Signals
[data/signals.json](data/signals.json)
