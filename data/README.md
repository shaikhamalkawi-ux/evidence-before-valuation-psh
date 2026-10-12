# Data contents

This directory contains compact derived and filtered records used by the Wivenhoe operational-data attribution checks, plus selected Hatta calculation outputs. It does not contain the complete original OECD ICIO or AEMO monthly archives.

## Wivenhoe source and derived data

- `WIVENHOE_DISPATCHLOAD_2025JAN_JUN.csv.gz`: the previously filtered 70,272-row January/June 2025 DISPATCHLOAD extract used in the locked analysis.
- `AEMO_2025_WIVENHOE_EVENT_DISPATCH_DETAIL.csv` and `AEMO_2025_WIVENHOE_EPISODE_DISPATCH_SUMMARY.csv`: the six-episode, 90-interval event crosswalk and summary.
- `FCAS_unit_episode_summary.csv`, `FCAS_unit_strict_witnesses.csv`, `FCAS_pairwise_observed_implications.csv`, `FCAS_episode_chain_6.csv`, and `FCAS_interval_state_matrix_90.csv`: generated result tables.
- `source_manifest.csv`: the two official source URLs, expected archive sizes and SHA-256 values, plus the actual filtered row counts.

Data were filtered to four Wivenhoe DUIDs: `W/HOE#1`, `W/HOE#2`, `PUMP1`, and `PUMP2`. Generation and pumping are aggregated separately. Market dispatch availability and targets are not measurements of physical readiness or delivered service.

The original January and June source ZIP files are not included; the hashes in the manifest document the expected upstream versions, not a claim that those complete ZIPs are preserved here. AEMO publicly released materials are used with attribution under AEMO’s [copyright permissions](https://www.aemo.com.au/privacy-and-legal-notices/copyright-permissions). Field semantics are linked to the official [AEMO MMS data model](https://visualisations.aemo.com.au/aemo/nemweb/MMSDataModelReport/Electricity/MMS%20Data%20Model%20Report_files/MMS_128.htm).

## Hatta derived outputs

`hatta_derived/` contains selected R26R3 derived tables for the seven annual states, 84 leave-one-source-year-out cases, the 12 primary scope comparisons, 48 sensitivity comparisons, five positive operating-scope witnesses, and 24 archived-case regression comparisons. These are calculation outputs, not the original OECD input archive or raw DEWA records. Their summary lock and independent replay records are in `../verification/`.
