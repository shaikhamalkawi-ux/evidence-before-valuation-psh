#!/usr/bin/env python3
"""P20: conditional response-shape envelope audit of the locked ECON-CERT 48-case output.

No simulated service data, probabilities, calibrations, or new physical assumptions.
Only tests implications under an explicitly declared optional bounded-response family.
"""
from __future__ import annotations
import csv, hashlib, json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IN = ROOT / "48_case_independent_prior_replay.csv"
OUT = ROOT / "P20_response_shape_envelope_48.csv"
SUMMARY = ROOT / "P20_response_shape_verification.json"

def as_bool(value):
    assert value in ("True", "False", "true", "false"), value
    return value.lower() == "true"

def close(a,b,tol=5e-12):
    return abs(a-b) < tol

checks=[]
def gate(label,predicate):
    checks.append((label,bool(predicate)))
    if not predicate: raise AssertionError(label)

with IN.open(newline='',encoding='utf-8') as f:
    raw=list(csv.DictReader(f))
gate('48 archived economic rows',len(raw)==48)
gate('unique scope/scenario/anchor/rate',len({(r['decision_perspective'],r['scenario'],r['om_anchor'],r['rate_label']) for r in raw})==48)
gate('two decision perspectives',set(r['decision_perspective'] for r in raw)=={'full-investment','operating-only'})
gate('two rate labels',set(r['rate_label'] for r in raw)=={'primary_r0','nonproject_accounting_r408'})

out=[]
for i,r in enumerate(raw):
    lo=float(r['q0_margin_million_per_year'])
    high=float(r['q1_strict_margin_million_per_year'])
    best=float(r['q1_best_model_B_margin_million_per_year'])
    need=float(r['q_needed_at_source_Bmin'])
    gate(f'R{i+1} finite',all(math.isfinite(x) for x in (lo,high,best,need)))
    gate(f'R{i+1} nonnegative-value envelope order',lo<=high<=best)
    gate(f'R{i+1} locked strict sign',(high>0)==as_bool(r['q1_strict_conditional_positive']))
    gate(f'R{i+1} locked possible sign',(best>0)==as_bool(r['q1_some_model_B_value_positive']))
    gate(f'R{i+1} public information non-certified',not as_bool(r['public_information_certificate']))
    gate(f'R{i+1} lower negative with nonnegative costs',lo < 0)
    if r['decision_perspective']=='full-investment':
        gate(f'R{i+1} full investment upper endpoint negative',high < 0)
        gate(f'R{i+1} full investment highest-source endpoint negative',best < 0)
        gate(f'R{i+1} q_needed over physical max',need>1)
    out.append({
      'scenario':r['scenario'],'om_anchor':r['om_anchor'],
      'scope':r['decision_perspective'],'rate_label':r['rate_label'],
      'lower_annual_margin_if_zero_benefit_millionUSD':f'{lo:.12f}',
      'upper_annual_STRICT_margin_if_full_benefit_millionUSD':f'{high:.12f}',
      'upper_annual_any_state_at_Bmax_millionUSD':f'{best:.12f}',
      'linear_q_required_original_model':f'{need:.12f}',
      'full_scope_reject_all_bounded_responses':str(r['decision_perspective']=='full-investment' and high<0),
      'strict_positive_possible_only_if_response_established':str(high>0),
      'public_information_certifiable':str(as_bool(r['public_information_certificate']))
    })

full=[r for r in out if r['scope']=='full-investment']
op=[r for r in out if r['scope']=='operating-only']
primary_full=[r for r in full if r['rate_label']=='primary_r0']
primary_op=[r for r in op if r['rate_label']=='primary_r0']

# Universal-quantification over source states uses the 2016 minimum B. The conditional
# bound at q=1 upper-envelopes any 0 <= h_s(q) <=1 response model with the same full-event B_s.
assert len(full)==24 and len(op)==24 and len(primary_full)==12 and len(primary_op)==12

gate('24/24 full cases upper endpoint below zero',all(float(r['upper_annual_STRICT_margin_if_full_benefit_millionUSD'])<0 for r in full))
gate('24/24 full cases even Bmax upper below zero',all(float(r['upper_annual_any_state_at_Bmax_millionUSD'])<0 for r in full))
gate('12/12 primary full cases upper endpoint below zero',all(float(r['upper_annual_STRICT_margin_if_full_benefit_millionUSD'])<0 for r in primary_full))
gate('10/24 operating q=1 strict positive',sum(float(r['upper_annual_STRICT_margin_if_full_benefit_millionUSD'])>0 for r in op)==10)
gate('12/24 operating q=1 some-state positive',sum(float(r['upper_annual_any_state_at_Bmax_millionUSD'])>0 for r in op)==12)
gate('5/12 primary operating q=1 strict positive',sum(float(r['upper_annual_STRICT_margin_if_full_benefit_millionUSD'])>0 for r in primary_op)==5)
gate('6/12 primary operating q=1 some-state positive',sum(float(r['upper_annual_any_state_at_Bmax_millionUSD'])>0 for r in primary_op)==6)
gate('all 48 lower endpoint negative',all(float(r['lower_annual_margin_if_zero_benefit_millionUSD'])<0 for r in out))

def minh_out(row,col): return min(float(x[col]) for x in row)
def maxh_out(row,col): return max(float(x[col]) for x in row)
gate('published best strict margin full primary', close(maxh_out(primary_full,'upper_annual_STRICT_margin_if_full_benefit_millionUSD'), -3.4202020854377126))
gate('published best Bmax margin full primary', close(maxh_out(primary_full,'upper_annual_any_state_at_Bmax_millionUSD'), -2.4454425774377127))
gate('published best strict margin full rate stress',close(maxh_out([r for r in full if r['rate_label']=='nonproject_accounting_r408'],'upper_annual_STRICT_margin_if_full_benefit_millionUSD'), -15.041744745885472))

# The interval endpoints are SHARP for any interior q with unrestricted monotone
# response functions h_s:[0,1] -> [0,1] s.t. h_s(0)=0, h_s(1)=1.
# h_lo(z)=1(z==1), h_hi(z)=1(z>0): both monotone and boundary-compatible;
# we test endpoints, ordering, and their presence at an interior q, not measured h.
for q in [0.25,0.5,0.75]:
    h_lo=(1 if q==1 else 0)
    h_hi=(1 if q>0 else 0)
    gate(f'sharp witnesses at q={q}',h_lo==0 and h_hi==1)
    gate(f'linear q strictly between admissible witness extremes at q={q}',h_lo<q<h_hi)

with OUT.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
summary={
 'version':'P20 source-conditioned service-response-shape diagnostic',
 'scope':'No new event observation or calibrated service-value shape. Full benefit B_s remains an ICIO accounting proxy, not E4. The input 48-case ledger is a previously independently replayed set of P19 locked results.',
 'assumption':'0 <= h_s(z) <=1, nondecreasing, h_s(0)=0,h_s(1)=1, B_s fixed full-FDE ceiling for the same declared event and valuation scope; q is joint delivered service fraction lower bound; study retains only source year and cost case envelope.',
 'conditional_model_boundary':'For any 0<q<1, without a numerical lower response-function bound, the strict conditional annual margin range is [existing q0 lower endpoint, existing q1 upper endpoint]. For q=1 the upper endpoint is exact; the original qB_s assumption corresponds to the special h_s(z)=z, NOT a universal guarantee.',
 'n_cases':len(raw), 'n_full_investment':len(full), 'n_operating':len(op),
 'n_full_investment_upper_negative':sum(float(r['upper_annual_STRICT_margin_if_full_benefit_millionUSD'])<0 for r in full),
 'n_full_investment_even_Bmax_negative':sum(float(r['upper_annual_any_state_at_Bmax_millionUSD'])<0 for r in full),
 'n_operating_strict_positive_only_at_full_assumed_benefit':sum(float(r['upper_annual_STRICT_margin_if_full_benefit_millionUSD'])>0 for r in op),
 'n_operating_any_state_positive_at_full_assumed_benefit':sum(float(r['upper_annual_any_state_at_Bmax_millionUSD'])>0 for r in op),
 'max_primary_full_strict_margin_million_USD_per_year':maxh_out(primary_full,'upper_annual_STRICT_margin_if_full_benefit_millionUSD'),
 'max_primary_full_Bmax_margin_million_USD_per_year':maxh_out(primary_full,'upper_annual_any_state_at_Bmax_millionUSD'),
 'n_checks':len(checks),'n_pass':sum(ok for _,ok in checks),
 'source_file':str(IN.name),'source_sha256':hashlib.sha256(IN.read_bytes()).hexdigest(),
 'cautions':['This is not independent external empirical validation of ECON-CERT.','No new numerical event value is inferred.','The full-event benefit cap is an explicit conditional assumption, not physical law or observed welfare.','The original q-dependent thresholds are valid under the original linear response assumption; they do not carry over unchanged to arbitrary shapes.','The Hatta public-information No-Certificate remains separate from the source-conditioned negative q=1 full-investment stress.']}
SUMMARY.write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(summary,indent=2))
