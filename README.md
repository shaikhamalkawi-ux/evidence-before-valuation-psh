# ECON-CERT: evidence before economic attribution in pumped-storage hydropower

Companion **public, source-bounded reproducibility repository** for the author-review manuscript:

> **Evidence Before Economic Attribution: A Utility-Planning Audit Framework for Hatta and Wivenhoe Pumped Storage**  
> Manuscript version **ECON-CERT P20E5R4-EP2 (22 November 2026)**, prepared for *Transactions on Energy Systems and Engineering Applications (TESEA)*. The journal manuscript is **not yet submitted or peer-reviewed**; author and image-rights release gates remain open.

The manuscript's **scientific calculations remain locked** to the admitted ECON-CERT R26R3/P20 lineage. The newer P20E5R4-EP2 revision is editorial, production, and manuscript/repository-metadata work; it does not introduce new plant telemetry, a new valuation model, or revised economic results. This repository's content is a bounded reproducibility package, **not** a full original-source data release.

## What the evidence supports

- **Hatta, UAE:** DEWA reports **48,222 MWh** of 2025 generation, equal to **32.148** nameplate full-discharge equivalents (1,500 MWh/FDE), **not** 32.148 qualified resilience events. At hypothetical full delivery (`q = 1`), all **24** tested full-investment cases have nonpositive strict margins; the **12 primary** strict annual-service boundaries span **54.636–105.883 FDE/year**. Five of 12 distinct primary operating-only cost cases are conditionally positive when sunk capital is excluded. No project-level economic certificate follows from the public evidence.
- **Wivenhoe, Australia:** Six Queensland 2025 Actual-LOR episodes provide **90 complete five-minute plant intervals** and **360 matched DUID/interval records**. Positive energy targets appear in **79** intervals, an enabled Raise Regulation flag in **62**, computed-positive availability in **57**, and an assigned-positive Raise Regulation target in **52**. Five computed-positive availability intervals have no positive assigned target. These are market fields, **not** proof of physical reserve delivery or avoided outage losses.
- **Response-shape check:** In the locked 48-case test under an expressly assumed full-event accounting-benefit ceiling, all **24 full-investment** upper-bound cases remain negative. This is not empirical calibration of a nonlinear response or validation of actual avoided damage.

## Files, scope, and exact reproduction

- `data/WIVENHOE_DISPATCHLOAD_2025JAN_JUN.csv.gz`: existing filtered 70,272-row official-source extract for four named Wivenhoe DUIDs; **not** the upstream AEMO monthly source ZIPs.
- `data/AEMO_2025_WIVENHOE_EVENT_DISPATCH_DETAIL.csv`, `data/FCAS_*`, `data/source_manifest.csv`: accepted event/interval crosswalk, recorded dispatch-field classifications, source identifiers, and public source fingerprints.
- `data/hatta_derived/`: seven historical accounting values, 12 primary cost-scope comparisons, 48 sensitivity cases, 84 source-year deletions, and other derived result tables; **not** original OECD ICIO matrices or DEWA SCADA/accounts.
- `verification/`: frozen R26R3 checks. `verification/p20/` adds source-identical 48-case response-shape audit inputs, verified output, exact original Python verifier, archived Figure 5 84-cell check, and four previously corrected Table A.1 comparison rows. These are **derived/audit records**, not new physical evidence.
- `SHA256SUMS.txt`: repository-file SHA-256 inventory for the synchronized metadata and research payload; `verification/p20/SHA256SUMS.txt` additionally covers the retained P20 audit files.

From the repository root using Python **3.10+**:

```bash
python -m pip install -r requirements.txt
python code/reproduce.py
python code/independent_csv_audit.py
python code/adversarial_checks.py
python scripts/verify_locked_results.py
python verification/p20/test_service_response_envelope.py
```

The first four scripts verify **the retained filtered inputs and locked source-derived tables**. The last script performs **381 deterministic checks** on the published 48-case ledger and rewrites its two retained verification outputs. It does not recreate upstream OECD/AEMO raw-source extraction. For manifest checking on a clean checkout: `sha256sum -c SHA256SUMS.txt` (GNU coreutils); re-run the producing scripts first only when intentionally reproducing their outputs.

## Citation and scientific limits

GitHub citation metadata are in [`CITATION.cff`](CITATION.cff); the source-to-claim and licensing limitations are in [`DATA_AND_RIGHTS.md`](DATA_AND_RIGHTS.md), [`data/README.md`](data/README.md), and [`docs/CLAIM_BOUNDARIES.md`](docs/CLAIM_BOUNDARIES.md). Use the repository **commit SHA** to identify the exact material reused. No manuscript DOI or public permanent repository DOI is asserted.

The Hatta accounting values are **conditional model stress values**, not measured lost-load welfare or realized profit. Source-document overlap at Wivenhoe does not by itself demonstrate an event-caused dispatch response, usable stored reservoir energy, service delivery, or economic loss avoided. No original third-party photographs, raw OECD ICIO archive, or complete raw AEMO monthly archives are redistributed here. This update does not clear image permissions, coauthor submission approval, or TESEA article-processing-charge wording.

**Repository synchronization:** 22 November 2026. Newly published P20 audit data/verifier are frozen from the previously verified manuscript package. Historical R26R3 empirical/operational files are not modified.
