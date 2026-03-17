
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
The market shows mixed signals: broad large-cap strength (SPY above its 200‑day MA) contrasts with sector/tech softness (QQQ below its 100‑day MA). Elevated oil volatility (OVX ~96) and a meaningful rise in the 10‑year yield (TNX ~4.23%) increase uncertainty for equity and inflation-sensitive sectors. VIX around 23.5 sits between calm and stressed regimes, implying above-normal equity volatility risk without outright panic. Together, higher rates and very high oil volatility create a two-headed risk profile — earnings and growth pressure for rate-sensitive tech and consumer names, plus margin and input-cost risk for energy‑exposed and cyclical companies. Position sizing and stop discipline remain important until directional clarity returns.

Market summary (bullets):
- Equities: SPY 669.03 > 200‑day MA 659.0 — broad-market trend still technically bullish.
- Tech/mega-cap: QQQ 600.38 < 100‑day MA 614.71 — short- to medium-term weakness in growth/tech leadership.
- Thematic/active: ARKK three‑month change −10.37% — concentrated/innovation exposure underperforming.
- Volatility: VIX 23.51 — elevated equity volatility, between normal and stressed.
- Rates: TNX yield 4.23% — materially higher yields, tightening financial conditions for rate-sensitive sectors.
- Energy market risk: OVX 95.92 — extreme oil volatility, signaling large price swings and supply/geo-political risk to commodities and related equities.
- Regime label: 🟡 Mixed Signals — some trend-following indicators bullish (SPY), other risk and leadership indicators cautionary (QQQ, OVX, TNX).

Data files:
- Referenced raw data files are in /data (e.g., /data/SPY.json, /data/QQQ.json, /data/ARKK.json, /data/VIX.json, /data/TNX.json, /data/OVX.json).

[Audio](https://raw.githubusercontent.com/kam-reef/market-summary/main/audio/latest.mp3)
[RSS](https://kam-reef.github.io/market-summary/feed.xml)

---

## Market Charts

### SPY Trend vs VIX
![Market Chart](charts/market_chart.png)

### ARKK Drawdown vs VIX
![ARKK VIX Chart](charts/arkk_vix_chart.png)

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
