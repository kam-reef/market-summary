
# Market Risk Monitor

![Status](https://img.shields.io/badge/Market%20Regime-yellow-yellow)

⚠️ **Disclaimer**

This project is an experimental data pipeline and educational demonstration.
It is **not financial advice**. The signals and AI commentary are generated
automatically from public market data and may be incomplete, delayed, or
incorrect. Do not make investment decisions based solely on this repository.

Last Updated: 2026-03-17

## Market Regime
🟡 Mixed Signals

## AI Risk Commentary

Risk commentary
The market shows mixed technical signals that increase short-term uncertainty. SPY is only slightly above its 200-day moving average (662.29 vs. 658.6), suggesting the large-cap trend is just marginally bullish but vulnerable to a pullback. QQQ trading materially below its 100-day MA (593.72 vs. 614.82) points to relative weakness in large-cap growth/tech, increasing the risk of sector-led volatility. VIX at 23.51 sits between calm and elevated territory—neither low enough to signal complacency nor high enough to indicate panic—so expect sporadic spikes in realized volatility. ARKK’s 3-month decline (-14.39%) highlights continued risk appetite divergence and potential for concentrated, idiosyncratic drawdowns in active/innovation-focused strategies. Overall, positioning should remain cautious: consider trimming risk exposures, keeping liquid buffers, and using disciplined risk controls (stops, position sizing, or hedges) until clearer trend confirmation emerges.

Market summary (bullets)
- SPY: 662.29, slightly above 200‑day MA 658.6 — marginally bullish on the large-cap index but close to a key support level.  
- QQQ: 593.72, below 100‑day MA 614.82 — tech/growth looks weak relative to broader market; potential headwind for risk assets.  
- ARKK: -14.39% over 3 months — continued notable drawdown for innovation-focused active exposure.  
- VIX: 23.51 — intermediate volatility environment (neither low nor extreme), watch for episodic spikes.  
- Regime label: 🟡 Mixed Signals — conflicting breadth/sector technicals warrant cautious positioning and active risk management.

Raw data files
- /data/signals.json
- /data/snapshot.json

## Market Charts

### SPY Trend vs VIX
![Market Chart](charts/market_chart.png)

### ARKK Drawdown vs VIX
![ARKK VIX Chart](charts/arkk_vix_chart.png)

## Market Snapshot
[data/market_snapshot.json](data/market_snapshot.json)

## Raw Signals
[data/signals.json](data/signals.json)

## History
[data/history.json](data/history.json)
