# Data contents and source boundaries

This directory contains compact, filtered Wivenhoe operational-market records and Hatta **derived accounting** tables. It does not contain the complete original OECD ICIO 2016–2022 archive, the full AEMO monthly source ZIPs, DEWA telemetry, or measured economic counterfactuals.

## Wivenhoe (previously locked files; unchanged in the 2026-11-22 sync)

- `WIVENHOE_DISPATCHLOAD_2025JAN_JUN.csv.gz`: 70,272 previously filtered January/June 2025 DISPATCHLOAD rows for `W/HOE#1`, `W/HOE#2`, `PUMP1`, and `PUMP2`.
- `AEMO_2025_WIVENHOE_EVENT_DISPATCH_DETAIL.csv`, `AEMO_2025_WIVENHOE_EPISODE_DISPATCH_SUMMARY.csv`: six-source-episode, 90-interval crosswalk and summary.
- `FCAS_unit_episode_summary.csv`, `FCAS_unit_strict_witnesses.csv`, `FCAS_pairwise_observed_implications.csv`, `FCAS_episode_chain_6.csv`, and `FCAS_interval_state_matrix_90.csv`: source-derived market-signal tables.
- `source_manifest.csv`: official AEMO retrieval URLs, expected upstream archive sizes and hashes, with retained filtered-row counts.

The market's `RAISEREGACTUALAVAILABILITY` is a computed offer/dispatch field; it does **not** measure mechanical plant availability, event-time stored energy, physical FCAS delivery or avoided economic losses. The two full original AEMO monthly ZIPs are **not** redistributed. See [AEMO copyright permissions](https://www.aemo.com.au/privacy-and-legal-notices/copyright-permissions).

## Hatta (previously locked files; unchanged in the 2026-11-22 sync)

`hatta_derived/` retains the seven UAE accounting-source-year values, 12 distinct primary cost-scope comparisons, 48 cost/rate stress cases, 84 leave-one-year-out comparisons and five positive operating-only witnesses, as source-scoped **derived calculation outputs**. None is a measured Hatta qualified-event count, usable SOC, O&M account or avoided-unserved-energy value. The original OECD ICIO archive is **not** redistributed.

## New P20 verification supplements (no raw upstream data)

`../verification/p20/` publishes the **previously calculation-locked** 48-case input ledger, response-shape upper/lower margin audit, exact deterministic verification script and 381-check summary, plus the Figure 5 84-cell positional audit and the four corrected Table A.1 source-row witnesses. These records do **not** replace the R26R3 empirical/operational baseline or add measured project benefits.
