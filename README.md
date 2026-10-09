# Evidence Before Valuation — Pumped-Storage Hydropower

Reproducibility resources for the manuscript:

**Evidence Before Valuation: Project-Level Attribution and Decision Boundaries in Pumped-Storage Hydropower**

## Purpose

This repository supports an evidence-before-valuation analysis for pumped-storage hydropower (PSH). The study asks an upstream question: before assigning economic value to a storage service, does the available evidence identify the event-to-asset-to-service attribution required by that valuation claim?

The current study uses:

- **Hatta (United Arab Emirates)** as the economic decision application; and
- **Wivenhoe (Queensland, Australia)** as an independent operational-data attribution test.

Wivenhoe is **not** a second economic valuation case and does **not** validate the Hatta economic bridge.

## Locked headline results

The current submission-facing baseline preserves the following load-bearing results:

- Reported Hatta 2025 generation: **48,222 MWh**
- Storage energy per full-discharge equivalent: **1,500 MWh**
- Deliberately favorable throughput-equivalent stress: **32.148 FDE/year**
- Primary strict decision boundary: **54.636–105.883 FDE/year**
- Primary required service fraction at 32.148 FDE/year: **q = 1.700–2.815**, outside the physical domain **q ∈ [0,1]**
- Wivenhoe 2025 census: **6 Queensland Actual-LOR episodes, 90/90 accepted five-minute intervals**
- 12 June 2025: **0/11** intervals with generation >1 MW, **0/11** with positive energy target, and **0/11** with any recorded Raise-FCAS target

These statements do **not** imply project failure, physical non-availability, causal non-response, reservoir state, stored-energy sufficiency, delivered reserve service, or avoided economic loss unless the corresponding evidence is available.

## Repository layout

- `scripts/` — reproducibility and verification code
- `data/` — compact derived tables used in the operational-data audit
- `docs/` — data-source, claim-boundary, and reproducibility notes
- `verification/` — machine-readable result locks / QA outputs

Large source archives are not stored here when a stable official source can be reacquired. Source URLs, file sizes, and SHA-256 checksums are recorded so the analysis can be reconstructed independently.

## Data provenance

The Wivenhoe operational analysis uses public Australian Energy Market Operator (AEMO) market data. AEMO permits use of its publicly released material with accurate and appropriate attribution. See AEMO's Copyright Permissions notice.

The Hatta analysis relies on public project and reporting material. No confidential DEWA operational telemetry is included in this repository.

## Reproduction

1. Create a Python environment (Python 3.10+ recommended).
2. Install dependencies listed in `requirements.txt`.
3. Run the verification script in `scripts/`.
4. Compare outputs with the locked values documented in `verification/`.

A release archived in Zenodo is planned after the public repository is checked for publication-safe content and a final license is selected.

## Authors / contributions

- **Ghassan Malkawi** — Writing – original draft
- **Ahmed Elsayed** — Methodology
- **Mohammed Alhagyan** — Visualization
- **Bakeel Hussein** — Writing – review & editing

**Funding:** No specific funding was received for this work.

## Citation

Citation metadata are provided in `CITATION.cff`. A DOI will be added after the first archival release.

## Status

This repository supports a manuscript under preparation/submission. Numerical results and claim boundaries are version-controlled; changes that alter the science will be released as a new tagged version.
