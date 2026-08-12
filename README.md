
# Market Risk Monitor

![Market Regime](https://img.shields.io/badge/Market%20Regime-Recovery-green)

**🟢 Recovery**  
**Score:** Downturn 0/3 | Recovery 3/3  
**Last Updated:** 2026-08-12

---

⚠️ **Disclaimer**

This is an automated market signal summary for informational purposes only.
It is not financial advice.

A note from the author:
There are hundreds of resources on the Internet in addition to learning resources available through your investment platform.
For example, [this one by Ramit Sethi](https://youtu.be/FF5-FbhaAyc?si=52cXbGUBFqxifu7Q), or [this one by Jaspreet Singh](https://youtu.be/qdqLIjszqy4?si=-R0Sa7C_Q0bCHY08), or [this one by Erin Moriarity](https://youtu.be/FYMfX3Aljow?si=MPQ7nICG0nA1U6vh), or articles like [this one by Fidelity](https://www.fidelity.com/learning-center/smart-money/roth-ira-taxes).
Seek out the information you need for your future self!

---

## AI Risk Commentary

Here's a thinking process:

1.  **Analyze User Request:**
   - **Market regime:** 🟢 Recovery (given)
   - **Input data:** JSON-like snapshot with various metrics
   - **Output requirements:**
     - Short risk commentary
     - Bullet-point market summary
     - Must include explicitly: mortgage rate & condition
     - Must include explicitly: income spread (SP dividend yield vs 10Y)
     - Must explicitly state whether income spread favors bonds or equities
     - Must include VIX, SPY trend, and yield context
     - If conditions unchanged, say they are stable
     - Concise and consistent tone
     - Mention raw data available in /data
   - **Tone:** Professional, concise, consistent

2.  **Extract & Interpret Data:**
   - SPY: price 773.03, ma200 703.48 → Price > MA200, uptrend
   - QQQ: price 720.87, ma100 682.17 → Price > MA100, uptrend
   - ARKK: 3-month change +0.51% → Slight positive momentum
   - VIX: 15.28 → Low volatility
   - TNX: 4.68% → 10Y yield context (though TNX is often Nasdaq 100 yield or similar, but given as yield, I'll treat as relevant yield)
   - OVX: 54.99, regime "low" → Low oil volatility
   - mortgage: rate 6.69%, condition "Neutral"
   - income_spread: sp_div_yield 0.98%, ten_year_yield 4.72%, spread -3.74%, regime "Bond Yield Advantage" → Bonds have advantage (since spread is negative, meaning bond yield > equity yield)

   Key interpretations:
   - SPY above 200-day MA: bullish trend
   - VIX at 15.28: low fear, stable environment
   - Income spread negative (-3.74%): bond yield advantage over equity dividend yield → favors bonds
   - Mortgage rate 6.69%, condition Neutral
   - Regime: Recovery 🟢

3.  **Structure Output:**
   - **Risk Commentary:** Brief paragraph setting the scene, mentioning regime, key themes, stability/unchange.
   - **Bullet-point Market Summary:** Concise bullets covering required elements.
   - Must explicitly state income spread favors bonds or equities → here it's bonds.
   - Include mortgage rate and condition explicitly.
   - Include VIX, SPY trend, yield context.
   - Note raw data in /data.
   - If conditions unchanged → I'll say "conditions are stable" since nothing indicates change.

   Draft - Risk Commentary:
   "Market remains in a 🟢 Recovery regime, characterized by risk-on bias, resilient equity trends, and broadly stable financial conditions. With VIX subdued at 15.28 and SPY holding above its 200-day moving average, the environment favors risk assets, though the negative equity-bond yield spread warrants attention. Mortgage rates are neutral at 6.69%, and overall data points suggest unchanged, stable conditions."

   Draft - Bullets:
   - SPY: $773.03, above 200-DMA (703.48) → bullish trend
   - QQQ: $720.87, above 100-DMA (682.17) → sustained momentum
   - VIX: 15.28 → low volatility, risk-appetite supportive
   - TNX/10Y yield: 4.72% → benchmark yield context
   - Mortgage rate: 6.69% (Neutral) → housing finance conditions stable
   - Income spread: SP dividend yield 0.98% vs 10Y 4.72% → spread -3.74% → **favors bonds** over equities on a yield-capture basis
   - ARKK 3-mo change: +0.51% → modest speculative momentum
   - OVX: 54.99 (low) → stable energy volatility
   - Conditions: stable (unchanged)

   Check requirements:
   - Short risk commentary ✓
   - Bullet-point market summary ✓
   - Mortgage rate and condition explicitly ✓ (6.69%, Neutral)
  

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

### SPY Trailing Dividend Yield (proxy)
![Income Spread](charts/income_spread.png)

---

[View raw data](data/market_snapshot.json)

---

## RSS Feed

https://kam-reef.github.io/market-summary/feed.xml

---

## Data

- Signals: [data/signals.json](data/signals.json)  
- History: [data/history.json](data/history.json)
