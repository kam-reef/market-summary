# Market Risk Monitor

[![Market Regime](https://img.shields.io/badge/Market%20Regime-Recovery-green)](https://github.com/kam-reef/market-summary)

**🟢 Recovery** | **Score:** Downturn 0/3 | Recovery 3/3 | **Last Updated:** 2026-06-29

---

## Overview
Automated market signal analysis delivering daily risk commentary across equities, bonds, and commodities via GitHub Actions.

## The Problem
Manual market monitoring is inconsistent and time-consuming. Investors need automated, data-driven insights to inform portfolio decisions without daily research overhead.

## The Solution
A Python-based pipeline that:
- Fetches market data (SPY, QQQ, VIX, TNX, ARKK, mortgage rates)
- Generates trend analysis and risk commentary
- Creates visual charts and RSS feed for subscription

## Architecture
```
.
├── app/
│   ├── fetch_data.py      # Market data ingestion
│   ├── signals.py         # Risk calculation logic
│   ├── generate_charts.py # Matplotlib visualizations
│   └── generate_report.py # Report assembly
├── data/                  # JSON snapshots
├── charts/                # Generated PNGs
└── .github/workflows/     # CI/CD automation
```

## Usage
Designed to run as a scheduled GitHub Action. For local testing:
```bash
pip install -r requirements.txt
python app/fetch_data.py
python app/generate_charts.py
python app/generate_report.py
```

## Security
- Read-only market data access (no trading)
- Public data sources only (Yahoo Finance, FRED API)
- No PII or sensitive data collected

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

### Income Spread
![Income Spread](charts/income_spread.png)

---

## Data
- [Market Snapshot](data/market_snapshot.json)
- [Signals](data/signals.json)
- [History](data/history.json)

---

## RSS Feed
https://kam-reef.github.io/market-summary/feed.xml

## License
MIT