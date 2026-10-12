#!/usr/bin/env python3
"""Non-destructive negative controls: corrupt four evidence fields in temporary copies.
Every corrupted case must be rejected by the executable evidence gates.
"""
import copy, gzip, json, shutil, subprocess, sys, tempfile
from pathlib import Path
import pandas as pd

r=Path(__file__).resolve().parents[1]
data=r/'data';runner=r/'code/reproduce.py'
base=pd.read_csv(data/'WIVENHOE_DISPATCHLOAD_2025JAN_JUN.csv.gz',low_memory=False)
events=pd.read_csv(data/'AEMO_2025_WIVENHOE_EVENT_DISPATCH_DETAIL.csv')
def witness_index():
    m=(base['SETTLEMENTDATE_STD']=='2025-06-04 18:05:00')&(base['DUID']=='W/HOE#2')
    assert m.sum()==1
    return base.index[m][0]

def june_index():
    m=(base['SETTLEMENTDATE_STD']=='2025-06-12 06:35:00')&(base['DUID']=='W/HOE#1')
    assert m.sum()==1
    return base.index[m][0]

out=[]
with tempfile.TemporaryDirectory(prefix='econ_fcas_negative_') as t:
    root=Path(t)
    for label in ['erase_positive_availability_witness','add_unsupported_june12_service','inject_nonofficial_flag','break_interval_join']:
        here=root/label;here.mkdir()
        x=base.copy(deep=True)
        ev=events.copy(deep=True)
        if label=='erase_positive_availability_witness': x.at[witness_index(),'RAISEREGACTUALAVAILABILITY']=0
        if label=='add_unsupported_june12_service': x.at[june_index(),'RAISEREG']=1
        if label=='inject_nonofficial_flag':x.at[witness_index(),'RAISEREGFLAGS']=2
        if label=='break_interval_join':ev.at[0,'interval_end']='2025-01-22 17:35:01'
        x.to_csv(here/'WIVENHOE_DISPATCHLOAD_2025JAN_JUN.csv.gz',index=False,compression='gzip')
        ev.to_csv(here/'AEMO_2025_WIVENHOE_EVENT_DISPATCH_DETAIL.csv',index=False)
        shutil.copy2(data/'AEMO_2025_WIVENHOE_EPISODE_DISPATCH_SUMMARY.csv',here/'AEMO_2025_WIVENHOE_EPISODE_DISPATCH_SUMMARY.csv')
        p=subprocess.run([sys.executable,str(runner),'--data',str(here),'--out',str(here/'results')],capture_output=True,text=True,timeout=30)
        accepted=p.returncode==0
        out.append({'corruption':label,'rejected':not accepted,'exit_code':p.returncode,'error_tail':p.stderr.strip().splitlines()[-1] if p.stderr else ''})
assert all(x['rejected'] for x in out),out
(r/'qa/ADVERSARIAL_MUTATION_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'expected_rejections':len(out),'actual_rejections':sum(x['rejected'] for x in out),'PASS':True},indent=2))
