# Architecture

Pipeline:

1. Fetch market data (Massive + CBOE)
2. Compute signals (Python)
3. Classify market regime
4. Generate AI summary (OpenAI)
5. Generate charts (matplotlib)
6. Update README
7. Commit to repository

Design principles:

- Deterministic signals
- AI used only for narrative
- Fully auditable via repo data