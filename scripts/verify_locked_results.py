from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / "verification" / "LOCKED_RESULTS.json").read_text(encoding="utf-8"))
SUMMARY = pd.read_csv(ROOT / "data" / "AEMO_2025_WIVENHOE_EPISODE_DISPATCH_SUMMARY.csv")

checks: list[tuple[str, bool]] = []

def check(name: str, condition: bool) -> None:
    checks.append((name, bool(condition)))
    if not condition:
        raise AssertionError(f"FAIL: {name}")
    print(f"PASS: {name}")

# Hatta headline arithmetic
h = LOCK["hatta"]
check("hatta_48222_div_1500", abs(h["reported_2025_generation_mwh"] / h["storage_energy_mwh"] - 32.148) < 1e-12)
check("hatta_below_primary_strict_floor", h["favorable_throughput_fde_per_year"] < h["primary_strict_boundary_fde_per_year"][0])
check("hatta_required_q_above_physical_domain", h["primary_required_q_at_32_148"][0] > h["q_domain"][1])

# Wivenhoe census
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

# 12 June bounded result
j = SUMMARY.loc[SUMMARY["episode"] == w["june_12_episode"]["episode"]].iloc[0]
check("june12_11_intervals", int(j["complete_intervals"]) == 11)
check("june12_generation_zero", int(j["initial_gt_1mw_intervals"]) == 0)
check("june12_energy_target_zero", int(j["target_gt_1mw_intervals"]) == 0)
check("june12_raise_target_zero", int(j["intervals_with_any_raise_target"]) == 0)
check("june12_diagnostic", j["energy_target_diagnostic"] == "ZERO_OUTPUT_ZERO_ENERGY_TARGET_ALL_INTERVALS")

print(f"ALL PASS {len(checks)}/{len(checks)}")
