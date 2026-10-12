# ECON-CERT reproducibility resources

This repository accompanies **“From Generation Records to Economic Claims: Evidence Boundaries for Pumped-Storage Hydropower”** (ECON-CERT TESEA P10). It preserves the scientific baseline `ECON_CERT_R26R3` and the supporting Wivenhoe field-attribution records from R26R2. It contains code, compact derived tables, locked results, and provenance records; it is not a complete archive of every upstream raw source.

## Research scope and locked results

- Hatta reported 2025 generation: 48,222 MWh; storage energy per full-discharge equivalent: 1,500 MWh; favorable throughput stress: 32.148 FDE/year.
- Primary strict Hatta decision boundary: 54.636–105.883 FDE/year; required service fraction at 32.148 FDE/year: q = 1.700–2.815, outside q ∈ [0,1]. The result is a public-information No-Certificate, not a finding of project failure or negative value.
- Wivenhoe 2025 census: six Queensland Actual-LOR episodes and 90 accepted five-minute intervals. The records establish observed dispatch and market fields only; they do not establish physical availability, delivered reserve service, causal response, reservoir state, or avoided loss.
- Wivenhoe is an operational-data attribution test, not a second economic valuation case and not validation of Hatta’s economic bridge.

The machine-readable locks and derived Hatta tables are in `verification/` and `data/hatta_derived/`. Compact Wivenhoe derived inputs, source manifests, and outputs are in `data/`, `results/`, and `verification/`.

## Reproduce and verify

Requirements: Python 3.10 or later and pandas 2.0 or later. From a fresh checkout, run:

```powershell
python -m pip install -r requirements.txt
python code/reproduce.py
python code/independent_csv_audit.py
python code/adversarial_checks.py
python scripts/verify_locked_results.py
```

`reproduce.py` regenerates the Wivenhoe result tables and 50 result checks from the included filtered January/June 2025 DISPATCHLOAD extract and event crosswalk. `independent_csv_audit.py` independently checks the key joins and findings using only Python’s standard library. `adversarial_checks.py` confirms four deliberately corrupted inputs are rejected. `verify_locked_results.py` checks the manuscript-level Hatta anchors and the Wivenhoe summary against the locked scientific baseline.

These commands verify the included filtered data and derived results. They do not recreate the full analysis from every original OECD or AEMO monthly archive. `SHA256SUMS.txt` records hashes for the checked-in payload at this commit; the manifest excludes itself.

## Provenance and limits

- `data/source_manifest.csv` records the official AEMO retrieval URLs, source sizes and SHA-256 values for the two source months.
- The repository includes the previously filtered AEMO rows used by the Wivenhoe analysis, not the complete original January and June monthly ZIP archives. The full original OECD ICIO 2016–2022 ZIP is also not verified as preserved. These gaps are not filled with substitute or fabricated data.
- Hatta derived tables are calculation outputs, not raw DEWA telemetry or a full copy of OECD input data. No confidential project correspondence, credentials, or local working archives are included.
- AEMO publicly available material is attributed in the data documentation. Upstream sources and field definitions are linked in `data/README.md` and `data/source_manifest.csv`.

## Citation and contributors

Citation metadata are in `CITATION.cff`. The four-author order is Ghassan Malkawi, Ahmed Elsayed, Mohammed Alhagyan, and Bakeel Hussein. The approved CRediT roles are recorded in `AUTHORS_AND_CONTRIBUTIONS.md`. Bakeel Hussein’s ORCID was not independently verified and is intentionally omitted.

## Rights

`LICENSE` applies only to original code. Data and derived-table rights, attribution, and upstream gaps are described separately in `DATA_AND_RIGHTS.md`; the code license does not grant rights to third-party source material. No Zenodo record or DOI is claimed in this repository. The companion Zenodo reviewer record is planned as an unpublished draft; public release is not authorized before documented journal acceptance.
