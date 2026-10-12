#!/usr/bin/env python3
"""Independent standard-library-only cross-check of all central Wivenhoe findings.
No pandas and no calls to reproduce.py; use gzip/csv/Counter only.
"""
import csv, gzip, json, sys
from collections import Counter, defaultdict
from pathlib import Path

root = Path(__file__).resolve().parents[1]
with (root/'data/AEMO_2025_WIVENHOE_EVENT_DISPATCH_DETAIL.csv').open(newline='', encoding='utf-8-sig') as f:
    d = list(csv.DictReader(f))
selected={r['interval_end']:r['episode'] for r in d}
assert len(selected)==90
rows=[]; total=0
with gzip.open(root/'data/WIVENHOE_DISPATCHLOAD_2025JAN_JUN.csv.gz','rt',newline='') as f:
    for r in csv.DictReader(f):
        total+=1
        if r['SETTLEMENTDATE_STD'] in selected:
            r['episode']=selected[r['SETTLEMENTDATE_STD']]
            rows.append(r)
assert total==70272 and len(rows)==360
assert len(set((r['SETTLEMENTDATE_STD'],r['DUID']) for r in rows))==360
assert set(r['DUID'] for r in rows)=={'W/HOE#1','W/HOE#2','PUMP1','PUMP2'}

def num(r,field): return float(r[field])
gen=[r for r in rows if r['DUID'].startswith('W/HOE')]
reg=[r for r in gen if num(r,'RAISEREGACTUALAVAILABILITY')>0 and num(r,'RAISEREG')==0]
assert len(reg)==10 and set(r['episode'] for r in reg)=={'EP25_02'}
assert set(r['DUID'] for r in reg)=={'W/HOE#2'}
assert len(set(r['SETTLEMENTDATE_STD'] for r in reg))==10

by_interval=defaultdict(list)
for r in gen:by_interval[r['SETTLEMENTDATE_STD']].append(r)
station=[(ts,selected[ts]) for ts,x in by_interval.items() if any(num(y,'RAISEREGACTUALAVAILABILITY')>0 for y in x) and all(num(y,'RAISEREG')==0 for y in x)]
assert len(station)==5 and set(ep for ts,ep in station)=={'EP25_02'}
assert Counter(int(float(r['RAISEREGFLAGS'])) for r in gen)==Counter({1:95,0:82,3:2,4:1})
assert sum(num(r,'RAISEREGACTUALAVAILABILITY')>0 for r in gen)==92
assert sum(num(r,'RAISEREG')>0 for r in gen)==82
assert sum(int(float(r['RAISEREGFLAGS'])) in (1,3) for r in gen)==97

jun12=[r for r in rows if r['episode']=='EP25_04']
assert len(jun12)==44
fields=['INITIALMW','TOTALCLEARED']
for f in ['RAISEREG','RAISE5MIN','RAISE60SEC','RAISE6SEC']:
    fields.extend([f,f+'FLAGS',f+'ACTUALAVAILABILITY'])
assert all(num(r,f)==0 for f in fields for r in jun12)
assert all(num(r,'AVAILABILITY')==254 for r in jun12 if r['DUID']=='W/HOE#2')

obs={'raw_rows':total,'joined_rows':len(rows),'intervals':len(selected),'gen_duid_counts':len(gen),
'RaiseReg_market_flag_enabled_gen_duid_rows':97,'RaiseReg_computed_availability_positive_gen_duid_rows':92,
'RaiseReg_target_positive_gen_duid_rows':82,
'positive_avail_no_target_gen_duid_rows':len(reg),'positive_avail_no_target_station_intervals':len(station),
'Jun12_all_operational_fields_zero_across_44_DUID_intervals':True,'PASS':True}
(root/'qa/INDEPENDENT_CSV_AUDIT.json').write_text(json.dumps(obs,indent=2)+'\n')
print(json.dumps(obs,indent=2))
