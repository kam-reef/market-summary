
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
Markets show mixed technical signals — SPY remains modestly above its 200-day MA (supportive) while QQQ sits below its 100-day MA (cautionary). VIX around 23.5 is elevated versus low-volatility regimes but not in panic territory, implying that investors are somewhat uncertain but not fearful. The modest 3-month decline in ARKK (-10.37%) adds a hint of risk-off in growth/alpha-sensitive names. Overall, position sizing and stop discipline remain important; favor selective exposure, keep cash or hedges handy, and avoid over-leveraging into areas lacking clear trend confirmation.

Market summary (bullets):
- SPY: price 669.03 vs 200MA 659.00 — trading above long-term average (bullish bias).
- QQQ: price 600.38 vs 100MA 614.71 — trading below shorter-term average (bearish/caution for tech).
- ARKK: 3-month change -10.37% — notable drawdown in high-growth/active basket.
- VIX: 23.51 — elevated/uncertain volatility environment (neither calm nor extreme).
- Regime label: Mixed Signals — some indices showing strength while others signal caution; expect choppy trading and rotation between sectors.
- Tactical implication: prefer diversified exposure, trim concentration in momentum names underperforming their MAs, use hedges or smaller position sizes.

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
