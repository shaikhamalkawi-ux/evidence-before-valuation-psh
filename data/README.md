# Data

This directory contains compact, publication-safe tables and metadata used to reproduce the Wivenhoe operational-data attribution analysis.

## Source

The underlying operational-market data are public files released by the Australian Energy Market Operator (AEMO) through NEMWeb.

AEMO's Copyright Permissions notice states that AEMO material made publicly available by AEMO may be used for any purpose with accurate and appropriate attribution.

## Raw source archives

The raw monthly archives are not stored in this repository. They can be reacquired from the official URLs listed in `source_manifest.csv`.

January 2025 DISPATCHLOAD:
- bytes: 108,998,184
- SHA-256: `c4e0d64682294f827db7bdbc3887031d01f6fca1e31ae567ddfd7784490b2282`

June 2025 DISPATCHLOAD:
- bytes: 108,587,365
- SHA-256: `1c93f2a76c8a07125aed5b532d27abc56f4b33e01f0396084b053743e72593da`

## Wivenhoe DUIDs

Generation:
- `W/HOE#1`
- `W/HOE#2`

Pumping/load:
- `PUMP1`
- `PUMP2`

Generation and pumping are aggregated separately; no generation-minus-pumping netting is used.

## Locked interval-selection rule

Accepted five-minute dispatch endpoints satisfy:

`event_start < t <= event_end`

across the complete six-episode 2025 Queensland Actual-LOR census used in the analysis.
