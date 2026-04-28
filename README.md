# ΩMEGA PRIME Δ — OPD

**Version:** v14.2.1 Priority Agent Baseline  
**Status:** Priority-agent logic implemented as a supervised/paper baseline. Audit and backtest validation required before any production or live-trading claim.

## What this repo contains

This repository seeds the ΩMEGA PRIME Δ agent layer with six priority strategy agents:

- `GAP` — gap-fill strategy
- `REV` — RSI/Bollinger mean-reversion strategy
- `SENTI` — sentiment-extreme strategy using injectable sentiment data
- `TWIN` — pair-spread/z-score strategy using explicit pair input
- `MAKER` — market-making quote-intent strategy
- `HARVEST` — yield/harvest opportunity intent strategy

The baseline also includes a canonical normalizer that maps strategy-specific outputs into safer contract shapes for downstream risk review.

## Safety boundary

This repo is **not live-trading-ready**. It is a supervised/paper baseline. All strategy outputs must pass a risk-authoritative service before any order is generated. No broker integration is included here.

## Lovable prototype

Dashboard prototype:

https://lovable.dev/projects/55b44a43-fb0c-4830-b676-41cc609002ac

## Current audit stance

The original v14.2.1 agent draft had several defects:

- `MAKER` was cut off mid-function.
- `HARVEST` was not supplied.
- Agent fields used mixed names such as `direction`, `entry`, `size`, and `agent` instead of canonical signal fields.
- `SENTI` simulated random sentiment, which is not acceptable for production claims.
- `TWIN` and `MAKER` require special intent contracts rather than ordinary one-leg directional signals.
- ATR helpers needed NaN protection.

This seeded version addresses those issues at the agent-contract layer, but still requires full integration tests, backtests, risk-service validation, and execution-service integration.

## Structure

```txt
apps/agent-service/
  normalizer.py
  strategies/
    __init__.py
    common.py
    gap.py
    rev.py
    senti.py
    twin.py
    maker.py
    harvest.py

docs/
  AUDIT_FINDINGS.md
  PRIORITY_AGENTS_V14_2_1.md
```

## Next verification checklist

```bash
python -m compileall apps/agent-service
pytest tests/unit
```

Planned next release:

```txt
v14.2.2 — canonical tests, pair/quote/yield intent risk handling, backtest fixtures, and verify_10_of_10.sh
```
