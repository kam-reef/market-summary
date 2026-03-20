
# Market Risk Monitor

![Market Regime](https://img.shields.io/badge/Market%20Regime-Mixed-yellow)

**🟡 Mixed Signals**  
**Score:** Downturn 1/3 | Recovery 0/3  
**Last Updated:** 2026-03-20

---

⚠️ **Disclaimer**

This is an automated market signal summary for informational purposes only. It is not financial advice.

---

## AI Risk Commentary

Risk commentary:
Markets show mixed signals and elevated tail-risk: equities are hovering just below key long-term support (SPY slightly under its 200‑day MA) while tech (QQQ) remains clearly below its 100‑day trend. Interest rates are notably higher (TNX ~4.25%), and oil volatility is extreme (OVX ~92.7), implying elevated commodity/energy risk and potential event-driven shocks. VIX around 24 indicates elevated equity volatility but not panic. Because several indicators (SPY vs 200MA, QQQ vs 100MA, TNX above 4, OVX high) are unchanged from the previous read, conditions are stable for now — mixed but skewed toward caution.

Market summary:
- Equities:
  - SPY: 659.80 vs 200‑day MA 660.10 — trading marginally below long‑term support.
  - QQQ: 593.02 vs 100‑day MA 614.35 — clearly below shorter‑term trend; tech underperformance persists.
  - ARKK: three‑month change -8.53% — not a dramatic collapse but negative momentum for high-beta/innovation names.
- Volatility:
  - VIX: 24.06 — elevated equity volatility, implying higher option costs and investor caution.
  - OVX: 92.68 (regime: high) — extreme oil volatility; watch energy-related risk and supply/geo-political events.
- Rates:
  - TNX (10‑yr yield): 4.25% — yields above 4% increase discounting pressure on equities and risk assets.
- Regime flags (current):
  - SPY_below_200MA: true (SPY_above_200MA: false)
  - QQQ_above_100MA: false
  - ARKK_3mo_drop: false
  - VIX_over_25: false, VIX_under_20: false (VIX in elevated mid-range)
  - TNX_above_4: true (TNX_below_3: false)
  - OVX_high: true (OVX_low/mid: false)

Operational notes:
- Conditions are stable relative to the last signal set (no signal changes).
- Raw data files used for these signals are available in /data.

---

## Charts

### SPY Trend
![SPY](charts/spy.png)

### QQQ Trend
![QQQ](charts/qqq.png)

### ARKK Drawdown
![ARKK](charts/arkk.png)

### VIX
![VIX](charts/vix.png)

### 10Y Yield
![TNX](charts/tnx.png)

### Oil Volatility
![OVX](charts/ovx.png)

---

## Market Snapshot

- SPY: 659.8 (200MA: 660.1)
- QQQ: 593.02 (100MA: 614.35)
- ARKK 3M Change: -8.53%

- VIX: 24.06
- TNX (10Y Yield): 4.25%
- OVX (Oil Volatility): 92.68

[View raw data](data/market_snapshot.json)

---

## Latest Audio Update

[Listen to today's update](https://raw.githubusercontent.com/kam-reef/market-summary/main/audio/2026-03-20.mp3)

---

## RSS Feed

Subscribe to daily updates:

https://kam-reef.github.io/market-summary/feed.xml

---

## Data

- Signals: [data/signals.json](data/signals.json)  
- History: [data/history.json](data/history.json)

---

## Support

This is an automated, continuously running project built to answer practical questions about market conditions and retirement risk.

No content, no predictions—just data, rules, and outputs.

If you find it useful, you can support the project here:

- GitHub Sponsors
- Buy Me a Coffee: https://buymeacoffee.com/yourname
