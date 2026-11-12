# ECON-CERT reproducibility resources

This repository accompanies the prepared research manuscript **“Evidence Before Valuation in Pumped-Storage Hydropower: A Hatta Economic Application and a Wivenhoe Dispatch Audit”** (**ECON-CERT TESEA P18**, 12 November 2026). P18 is a journal-facing editorial version, **not a new scientific-results version**. As of 12 November 2026, the manuscript had not yet been submitted to TESEA or peer reviewed.

The locked scientific calculations remain based on `ECON_CERT_R26R3`, with the Wivenhoe operational-record analysis and the later 2025 six-episode/90-interval census preserved. This repository contains code, compact derived tables, locked results, and provenance records; it is **not** a complete archive of every upstream raw source.

## Research scope and locked results

- Hatta reported 2025 generation: **48,222 MWh**; nameplate storage energy: **1,500 MWh**; favorable throughput stress: **32.148 full-discharge equivalents (FDE)/year**. Throughput is not a count of qualified resilience events.
- Primary strict Hatta full-investment decision boundary: **54.636–105.883 FDE/year**; required service fraction at 32.148 FDE/year: **q = 1.700–2.815**, outside q in [0,1]. The public-information **No-Certificate** result is not a finding of project failure, lack of value, or actual unprofitability.
- Excluding sunk investment in prospective operations-only accounting gives **five of twelve conditionally positive cases**, each dependent on externally transferred fixed-O&M benchmarks; these are not verified project accounts.
- Wivenhoe 2025 census: **six Queensland Actual-LOR episodes**, **90 complete five-minute intervals**, and **360 four-DUID unit-interval observations**. Five intervals have positive computed Raise Regulation availability with no positive assigned target; the 12 June 2025 episode has 11 intervals with no plant energy or assigned Raise targets.
- Wivenhoe is an **independent operational-market attribution test**, not a second economic valuation or validation of Hatta's economic bridge. The records do not establish mechanical availability, stored-energy sufficiency, delivered reserves, an event-caused response, or avoided economic loss.

## Reproduce and verify

Requirements: Python 3.10 or later and pandas 2.0 or later. From a fresh checkout, run:

```powershell
python -m pip install -r requirements.txt
python code/reproduce.py
python code/independent_csv_audit.py
python code/adversarial_checks.py
python scripts/verify_locked_results.py
```

`reproduce.py` regenerates the retained Wivenhoe tables and 50 checks from the included filtered January/June 2025 DISPATCHLOAD extract and event crosswalk. `independent_csv_audit.py` checks the key joins using the Python standard library. `adversarial_checks.py` tests corrupted inputs. `verify_locked_results.py` checks the manuscript-level Hatta anchors and Wivenhoe summary against the locked scientific baseline.

These commands verify **the included filtered data and derived results**. They do **not** recreate the full analysis from every original OECD or AEMO monthly archive. `SHA256SUMS.txt` records hashes for checked-in payload files at its documented snapshot; metadata-only changes to this repository do not recertify upstream missing archives.

## Provenance and limitations

- `data/source_manifest.csv` records official AEMO retrieval URLs, source sizes, and SHA-256 values for two source months.
- The repository contains project-filtered AEMO rows, not the complete original monthly ZIP archives; the full original OECD ICIO 2016–2022 ZIP was not verified as preserved.
- Hatta tables are derived computations, not DEWA event-time telemetry or financial accounts.
- No undocumented event-specific q, causal avoided-loss value, physical plant failure, or realized project profitability is claimed.
- Source rights and attribution are documented in `DATA_AND_RIGHTS.md`.

## Citation and authors

The manuscript's **approved P18 eight-author order** is:

1. Ghassan Malkawi (corresponding author)
2. Ahmed Elsayed
3. Hussien Alwedyan
4. Rafiq Manna
5. Ashraf AlShalalfeh
6. Abdulwehab A. Ibrahim
7. Mohammed Alhagyan
8. Bakeel Hussein

Current contribution descriptions are in `AUTHORS_AND_CONTRIBUTIONS.md`, and machine-readable citation metadata are in `CITATION.cff`. P18 supersedes older P9/P10 author metadata **for the manuscript**; it does not imply that all eight authors individually wrote repository code.

No public Zenodo DOI or published manuscript DOI is asserted here. Any unpublished Zenodo reviewer-preview link is confidential and must be verified and shared only through the intended editorial channel.

## Rights

`LICENSE` applies to original code only. `DATA_AND_RIGHTS.md` identifies additional rights, source attribution, and upstream gaps; the code license does not grant rights to third-party material.

---
**Metadata synchronization:** 12 November 2026. Editorial/repository metadata change only; locked research data, scripts, numerical outputs and scientific claims unchanged.
