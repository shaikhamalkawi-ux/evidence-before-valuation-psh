# ECON-CERT P20E5R4-EP2 repository/manuscript synchronization

**Source manuscript:** *Evidence Before Economic Attribution: A Utility-Planning Audit Framework for Hatta and Wivenhoe Pumped Storage* (TESEA author-review draft, 47 pages, dated 22 November 2026).

**Scientific calculation baseline:** R26R3 source and data are retained without modification; mathematical P20 and P20E5R1 audit outputs are published as previously frozen derived verification material, not new field data. The four precision corrections in Table A.1 are archived in `verification/p20/TABLE_A1_CROSS_CASE_CORRECTION.csv` and were already incorporated in the P20E5R1 manuscript.

**Newly published from the independently audited P20E5R1 package:** `verification/p20/48_case_independent_prior_replay.csv`, `P20_response_shape_envelope_48.csv`, `test_service_response_envelope.py`, `P20_response_shape_verification.json`, `FIGURE5_84_CELL_POSITIONAL_AUDIT.csv`, `FIGURE5_POSITIONAL_SUMMARY.json`, and `TABLE_A1_CROSS_CASE_CORRECTION.csv`. Their SHA-256 hashes and versions are recorded in `verification/p20/SHA256SUMS.txt`.

**Reproducibility boundaries:** The 48-case verifier performs 381 deterministic checks under explicitly declared source-conditioned model assumptions. Its output does not substantiate measured resilience-service delivery, a physical availability lower bound, a local counterfactual, E4 economic certification, or full original-source regeneration of OECD and AEMO raw archives.

**Rights and submission:** Only original scripts and derived material are added. Original external photographs are not included. The TESEA manuscript is not yet approved for submission: third-party image rights, all-author sign-off, and APC wording versus the journal's fee policy remain unresolved. No repository or manuscript DOI is asserted. Historical materials remain available at their previous commits.

**Remote-CI metadata correction:** The previous `results/data_sha256.json` described two stale versions of the filtered Wivenhoe CSV files. That descriptor was regenerated from the SHA-256 digests and byte lengths of the unchanged CSV files actually committed to this repository. No operational inputs, event membership, results, or source-derived scientific table were modified.
