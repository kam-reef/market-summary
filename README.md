
# Market Risk Monitor

![Market Regime](https://img.shields.io/badge/Market%20Regime-Mixed-yellow)

**🟡 Mixed Signals**  
**Score:** Downturn 1/3 | Recovery 0/3  
**Last Updated:** 2026-04-04

---

⚠️ **Disclaimer**

This is an automated market signal summary for informational purposes only. It is not financial advice.

---

## AI Risk Commentary

Risk commentary:
Markets are showing mixed signals. Equity internals are slightly defensive with SPY trading below its 200‑day moving average and QQQ below its 100‑day moving average, suggesting limited conviction in the rally. Interest rate risk is elevated: the 10‑yr yield (TNX) is at 4.31%, which keeps financing and discount rate pressure on growth names. Volatility is bifurcated — equity implied volatility (VIX ~23.9) is elevated but not extreme, while oil volatility (OVX) is very high (OVX 93.14), signaling energy market stress that can feed into headline and input‑cost risk. Mortgage conditions are Neutral with a 30‑yr rate near 6.46%, which continues to weigh on housing demand and consumer refinancing activity. Overall, mixed signals imply a cautious stance: manage duration and position sizing, keep stop levels tight, and prefer quality/defensive exposures until clearer directional confirmation.

Market summary (bullets):
- Regime label: 🟡 Mixed Signals — no clear bullish or bearish consensus.
- Signals: SPY_below_200MA = true; SPY_above_200MA = false; QQQ_above_100MA = false; ARKK_3mo_drop = false; VIX_over_25 = false; VIX_under_20 = false; TNX_above_4 = true; TNX_below_3 = false; OVX_high = true (others false).
- Equities: SPY 655.83 vs 200‑day MA 662.58 (below MA); QQQ 584.98 vs 100‑day MA 609.63 (below MA).
- Sector/innovation: ARKK down 3‑month % = -12.45% (not flagged as an extreme signal here but shows recent weakness).
- Volatility: VIX 23.87 (elevated, but under the 25 trigger); OVX 93.14 (high — energy volatility elevated).
- Rates and credit: TNX (10‑yr yield) 4.31% — rate pressure persists; mortgage rate 6.46% with mortgage condition flagged as Neutral.
- Risk posture: Elevated rate and oil volatility risks offset by only moderate equity volatility — favor defensive/quality, limit leverage, watch for

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

### Mortgage Conditions
![Mortgage](charts/mortgage.png)

---

## Market Snapshot

- SPY: 655.83 (200MA: 662.58)
- QQQ: 584.98 (100MA: 609.63)
- ARKK 3M Change: -12.45%

- VIX: 23.87
- TNX (10Y Yield): 4.31%
- OVX (Oil Volatility): 93.14

- Mortgage Rate: 6.46%
- Mortgage Condition: Neutral

[View raw data](data/market_snapshot.json)

---



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

- GitHub Sponsors (Pending)
- Buy Me a Coffee: https://buymeacoffee.com/yourname
