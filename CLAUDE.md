# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A single-page Streamlit app (`app.py`) that displays the last 30 days of exchange-rate history (USD, EUR, BTC → BRL) using the public AwesomeAPI (`economia.awesomeapi.com.br`). It fetches daily quotes, charts the closing price, shows min/max metrics, and lists the raw data in an expander.

## Running the app

```
streamlit run app.py
```

This starts a local server (default `http://localhost:8501`). `streamlit.log` contains output from the most recent run.

## Dependencies

The app imports `requests`, `pandas`, and `streamlit`. There is no requirements/lock file in the repo — install these three packages directly (e.g., `pip install requests pandas streamlit`) before running.

## Architecture notes

- Everything lives in `app.py`; there is no module structure to navigate.
- `buscar_historico(codigo)` fetches and shapes the API response into a DataFrame; it's wrapped in `@st.cache_data(ttl=600)` so repeated runs within 10 minutes reuse cached results instead of hitting the API again.
- Currency choices are defined in the `MOEDAS` dict (label → API currency code); add entries there to support more currencies.
- API/parsing failures are caught around the `buscar_historico` call and surfaced via `st.error` + `st.stop()` — keep new external calls wrapped similarly so the app fails gracefully rather than throwing a stack trace in the UI.

## GitHub sync

This project is pushed to `https://github.com/MarcosSant0s/moeda-dashboard` (public, remote `origin`, branch `main`).

**After every change you make to tracked files in this repo — no matter how small — commit and push automatically, without asking for confirmation:**

```
git add -A
git commit -m "<descriptive message of what changed and why>"
git push origin main
```

- Do this as the last step of each task, right after the change is verified working.
- Write commit messages that describe the actual change (e.g. "Add EUR/BTC min-max metrics to sidebar"), not generic messages like "update".
- Respect `.gitignore` (e.g. `streamlit.log`, `.claude/`, `__pycache__/`) — don't force-add ignored files.
