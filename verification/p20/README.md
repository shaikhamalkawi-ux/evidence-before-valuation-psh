# Locked P20/P20E5R1 quantitative audit supplement

All files in this folder are copied from, or deterministically reproduced from, the **already verified** `ECON_CERT_P20E5R1_Independent_Numerical_Audit_COMPLETE.zip` manuscript audit package. They are public **derived scenario/audit records**, not upstream raw AEMO/DEWA/OECD data or independently measured project economic benefits.

- `48_case_independent_prior_replay.csv` — 48 previously replayed cost/scope cases; complete 48-case prior input ledger.
- `P20_response_shape_envelope_48.csv` — lower/upper conditional annual-margin endpoints in **million 2025 USD/year**, under the stated full-event accounting-value ceiling. The two operating scopes and two rate labels remain distinct.
- `test_service_response_envelope.py` — unchanged original self-contained verifier. Run `python verification/p20/test_service_response_envelope.py` from the repository root (Python 3.10+). Prints/serializes **381/381 deterministic checks**; rewrites the output CSV/JSON from the input CSV; no random data or new empirical calibration.
- `P20_response_shape_verification.json` — stored verification summary from the original program, confirming the bounded interpretation; not a field-validation report.
- `FIGURE5_84_CELL_POSITIONAL_AUDIT.csv` and `FIGURE5_POSITIONAL_SUMMARY.json` — 84-cell source-coordinate audit for the archived **P20** Figure 5. Current manuscript figure renumbering may differ after inserting the photographic site-orientation figure; the underlying heatmap values did not change.
- `TABLE_A1_CROSS_CASE_CORRECTION.csv` — four earlier charging-precision display corrections already adopted in P20E5R1; not fresh calculations or alternative scientific results.

Scientific limits: Hatta public records still admit service lower bound `q = 0`; the 48-case bounded nonlinear check does not establish event-time delivery, observed avoided unserved energy, or a project-specific profitability measure. `SHA256SUMS.txt` covers the payloads excluding this README and itself.
