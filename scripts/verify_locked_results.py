from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / "verification" / "LOCKED_RESULTS.json").read_text(encoding="utf-8"))
SUMMARY = pd.read_csv(ROOT / "data" / "AEMO_2025_WIVENHOE_EPISODE_DISPATCH_SUMMARY.csv")
FCAS = pd.read_csv(ROOT / "data" / "FCAS_episode_chain_6.csv")
R26R3 = json.loads((ROOT / "verification" / "R26R3_STUDY_SUMMARY.json").read_text(encoding="utf-8"))

checks: list[tuple[str, bool]] = []


def check(name: str, condition: bool) -> None:
    checks.append((name, bool(condition)))
    if not condition:
        raise AssertionError(f"FAIL: {name}")
    print(f"PASS: {name}")


check("scientific_baseline_R26R3", LOCK["baseline"] == "ECON_CERT_R26R3")

# Hatta headline arithmetic and decision boundary
h = LOCK["hatta"]
check("hatta_48222_div_1500", abs(h["reported_2025_generation_mwh"] / h["storage_energy_mwh"] - 32.148) < 1e-12)
check("hatta_below_primary_strict_floor", h["favorable_throughput_fde_per_year"] < h["primary_strict_boundary_fde_per_year"][0])
check("hatta_required_q_above_physical_domain", h["primary_required_q_at_32_148"][0] > h["q_domain"][1])
check("r26r3_display_checks_120", R26R3["pass_display_checks"] == 120)
check("r26r3_scope_cases_24_and_48", R26R3["n_full_cases"] == 24 and R26R3["n_scope_comparisons"] == 48)
check("r26r3_leave_year_out_cases_84", R26R3["leave_year_out_cases"] == 84)
check("r26r3_no_unconditional_certificate", R26R3["unconditional_economic_certificate"].startswith("NOT_ESTABLISHED"))

# Wivenhoe interval census and episode summary
w = LOCK["wivenhoe_2025"]
check("six_episodes", len(SUMMARY) == w["episodes"])
check("ninety_intervals", int(SUMMARY["complete_intervals"].sum()) == w["accepted_five_minute_intervals"])
check("zero_missing", int(SUMMARY["missing"].sum()) == w["missing_generation_intervals"])
check("generation_gt_1mw_79", int(SUMMARY["initial_gt_1mw_intervals"].sum()) == w["generation_gt_1mw_intervals"])
check(
    "five_episodes_positive_generation_throughout",
    int((SUMMARY["initial_gt_1mw_intervals"] == SUMMARY["complete_intervals"]).sum())
    == w["episodes_with_positive_generation_throughout"],
)

# FCAS interval-chain result table
check("six_FCAS_episodes", len(FCAS) == 6)
check("FCAS_interval_count_90", int(FCAS["intervals"].sum()) == w["accepted_five_minute_intervals"])
check("FCAS_positive_energy_targets_79", int(FCAS["generation_target_gt1MW"].sum()) == w["positive_energy_targets"])
check("FCAS_RaiseReg_enabled_62", int(FCAS["raise_reg_enabled_flag_any"].sum()) == w["raise_reg_enabled_intervals"])
check("FCAS_RaiseReg_availability_57", int(FCAS["raise_reg_actual_availability_positive_any"].sum()) == w["positive_computed_raise_reg_availability_intervals"])
check("FCAS_RaiseReg_targets_52", int(FCAS["raise_reg_target_positive_any"].sum()) == w["positive_raise_reg_targets"])
check("FCAS_availability_without_target_5", int(FCAS["raise_reg_actual_avail_positive_but_target_zero"].sum()) == w["positive_availability_zero_target_intervals"])

# Bounded 12 June result
j = SUMMARY.loc[SUMMARY["episode"] == w["june_12_episode"]["episode"]].iloc[0]
check("june12_11_intervals", int(j["complete_intervals"]) == 11)
check("june12_generation_zero", int(j["initial_gt_1mw_intervals"]) == 0)
check("june12_energy_target_zero", int(j["target_gt_1mw_intervals"]) == 0)
check("june12_raise_target_zero", int(j["intervals_with_any_raise_target"]) == 0)
check("june12_diagnostic", j["energy_target_diagnostic"] == w["june_12_episode"]["diagnostic"])

print(f"ALL PASS {len(checks)}/{len(checks)}")
