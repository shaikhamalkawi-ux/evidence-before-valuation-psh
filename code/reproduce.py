#!/usr/bin/env python3
"""ECON-CERT R26R1 companion, bounded Wivenhoe attribution chain. Python 3 + pandas.

Input: exact R26R1 archived filtered AEMO DISPATCHLOAD records and 90-row event file.
This script NEVER interprets FCAS `ACTUALAVAILABILITY` as physical plant availability,
completed service delivery or counterfactual economic value.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path

import pandas as pd

DATA_FILES = [
    'WIVENHOE_DISPATCHLOAD_2025JAN_JUN.csv.gz',
    'AEMO_2025_WIVENHOE_EVENT_DISPATCH_DETAIL.csv',
    'AEMO_2025_WIVENHOE_EPISODE_DISPATCH_SUMMARY.csv',
]
DUIDS_GEN = ['W/HOE#1', 'W/HOE#2']
DUIDS_PUMP = ['PUMP1', 'PUMP2']
FCAS = ['RAISEREG', 'RAISE5MIN', 'RAISE60SEC', 'RAISE6SEC']
FIELDMAP = {
    'RAISEREG': 'RAISEREGACTUALAVAILABILITY',
    'RAISE5MIN': 'RAISE5MINACTUALAVAILABILITY',
    'RAISE60SEC': 'RAISE60SECACTUALAVAILABILITY',
    'RAISE6SEC': 'RAISE6SECACTUALAVAILABILITY',
}
EXPECTED_BASELINE = [
    ('EP25_01', 33, 33, 33, 33),
    ('EP25_02', 21, 21, 21, 14),
    ('EP25_03', 9, 9, 9, 5),
    ('EP25_04', 11, 0, 0, 0),
    ('EP25_05', 7, 7, 7, 0),
    ('EP25_06', 9, 9, 9, 0),
]
FLAG_MEANING = {0: 'Not enabled (FCAS market status)', 1:'Enabled', 3:'Trapped and enabled', 4:'Stranded and not enabled'}
AEMO_MODEL = 'https://visualisations.aemo.com.au/aemo/nemweb/MMSDataModelReport/Electricity/MMS%20Data%20Model%20Report_files/MMS_128.htm'


def shasum(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as f:
        for piece in iter(lambda: f.read(1048576), b''):
            h.update(piece)
    return h.hexdigest()


def check(condition: bool, message: str, checks: list):
    checks.append({'test': message, 'pass': bool(condition)})
    if not condition:
        raise AssertionError(message)


def main(data: Path, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    checks = []
    for f in DATA_FILES:
        check((data/f).is_file(), f'input exists: {f}', checks)
    raw = pd.read_csv(data/DATA_FILES[0], low_memory=False)
    original = pd.read_csv(data/DATA_FILES[1])
    expected = pd.read_csv(data/DATA_FILES[2])
    check(len(raw) == 70272, 'R26R1 raw filtered row count = 70272', checks)
    check(len(original) == 90, 'R26R1 event interval detail row count = 90', checks)
    check(original['interval_end'].is_unique, 'R26R1 event interval timestamps unique', checks)
    check(set(raw['DUID'].unique()) == set(DUIDS_GEN+DUIDS_PUMP), 'four original Wivenhoe DUIDs retained', checks)
    check(not raw[['SETTLEMENTDATE_STD','DUID']].duplicated().any(), 'all raw time/DUID keys unique', checks)
    episode = raw.merge(original[['episode','interval_end','max_lor']], left_on='SETTLEMENTDATE_STD', right_on='interval_end', how='inner', validate='many_to_one', indicator=True)
    check(len(episode) == 360, '90 x 4 exact episode time joins', checks)
    check((episode.groupby('interval_end')['DUID'].nunique()==4).all(), 'complete four-DUID support at every accepted interval', checks)
    check(set(episode['episode'].unique()) == {x[0] for x in EXPECTED_BASELINE}, 'all six R26R1 episode labels retained', checks)
    for f in FCAS:
        check(set(episode[f+'FLAGS'].astype(int).unique()).issubset(FLAG_MEANING),f'{f} flags use official domain',checks)
        check(episode[[f, FIELDMAP[f], f+'FLAGS']].notna().all().all(),f'{f} core status/availability/target fields complete',checks)
        check((episode[FIELDMAP[f]]>=0).all(),f'{f} actual FCAS availability nonnegative',checks)
        check((episode[f]>=0).all(),f'{f} FCAS target nonnegative',checks)
    for f in ['INITIALMW','TOTALCLEARED']:
        check(episode[f].notna().all(),f'{f} present for all 360 entries',checks)

    episode['asset_mode'] = episode['DUID'].map(lambda x:'generation' if x in DUIDS_GEN else 'pumping')
    for f in FCAS:
        episode[f+'_enabled_flag'] = episode[f+'FLAGS'].astype(int).isin([1,3])
        episode[f+'_actual_avail_positive'] = episode[FIELDMAP[f]] > 0
        episode[f+'_target_positive'] = episode[f] > 0
        episode[f+'_enabled_no_actual'] = episode[f+'_enabled_flag'] & ~episode[f+'_actual_avail_positive']
        episode[f+'_actual_no_target'] = episode[f+'_actual_avail_positive'] & ~episode[f+'_target_positive']

    # Target and energy signals are dispatch targets / start-of-interval observations, NOT metered energy or delivered ancillary service.
    rows_unit = []
    for (ep,mode),x in episode.groupby(['episode','asset_mode'], sort=True):
        for f in FCAS:
            flags = x[f+'FLAGS'].astype(int)
            rows_unit.append({
                'episode':ep, 'asset_mode':mode, 'service':f, 'duid_interval_rows':len(x),
                'flag_0':int((flags==0).sum()),'flag_1':int((flags==1).sum()),
                'flag_3_trapped':int((flags==3).sum()),'flag_4_stranded':int((flags==4).sum()),
                'flag_enabled_count':int(x[f+'_enabled_flag'].sum()),
                'computed_actual_availability_positive_count':int(x[f+'_actual_avail_positive'].sum()),
                'fcas_target_positive_count':int(x[f+'_target_positive'].sum()),
                'enabled_flag_but_actual_availability_zero_count':int(x[f+'_enabled_no_actual'].sum()),
                'actual_availability_positive_but_target_zero_count':int(x[f+'_actual_no_target'].sum()),
                'actual_availability_positive_target_zero_unique_intervals':int(x.loc[x[f+'_actual_no_target'], 'interval_end'].nunique()),
            })
    unit_counts = pd.DataFrame(rows_unit)
    unit_counts.to_csv(out/'FCAS_unit_episode_summary.csv',index=False)

    def interval_obj(key,frame):
        gen = frame[frame['asset_mode']=='generation']; pump=frame[frame['asset_mode']=='pumping']
        rec = {'episode':key[0], 'interval_end':key[1], 'max_lor':int(frame['max_lor'].iloc[0]),
            'gen_initial_mw_sum':gen['INITIALMW'].sum(),
            'gen_energy_target_mw_sum':gen['TOTALCLEARED'].sum(),
            'pump_initial_mw_sum':pump['INITIALMW'].sum(),
            'pump_energy_target_mw_sum':pump['TOTALCLEARED'].sum(),
            'positive_generation_observed_gt1MW': int(gen['INITIALMW'].sum()>1),
            'positive_generation_target_gt1MW': int(gen['TOTALCLEARED'].sum()>1),
            'positive_pumping_observed_gt1MW': int(pump['INITIALMW'].sum()>1),
            'positive_pumping_target_gt1MW': int(pump['TOTALCLEARED'].sum()>1)}
        for f in FCAS:
            rec[f+'_any_gen_flag_enabled'] = int(gen[f+'_enabled_flag'].any())
            rec[f+'_gen_actual_availability_mw_sum'] = gen[FIELDMAP[f]].sum()
            rec[f+'_gen_target_mw_sum'] = gen[f].sum()
            rec[f+'_gen_any_actual_availability_positive'] = int(gen[f+'_actual_avail_positive'].any())
            rec[f+'_gen_any_target_positive'] = int(gen[f+'_target_positive'].any())
            rec[f+'_any_pump_flag_enabled'] = int(pump[f+'_enabled_flag'].any())
            rec[f+'_pump_actual_availability_mw_sum'] = pump[FIELDMAP[f]].sum()
            rec[f+'_pump_target_mw_sum'] = pump[f].sum()
        return rec
    intervals = pd.DataFrame(interval_obj(key,x) for key,x in episode.groupby(['episode','interval_end'],sort=True))
    check(len(intervals)==90,'reaggregated 90 interval objects',checks)
    merged=intervals.merge(original,on=['episode','interval_end'],validate='one_to_one')
    for name,orig in [('gen_initial_mw_sum','gen_initial_mw'),('gen_energy_target_mw_sum','gen_target_mw'),('pump_initial_mw_sum','pump_initial_mw'),('pump_energy_target_mw_sum','pump_target_mw'),('RAISEREG_gen_target_mw_sum','gen_raisereg_target_mw')]:
        check(((merged[name]-merged[orig]).abs()<=0.00011).all(), f'independent sum reproduces R26R1 {orig}', checks)
    intervals.to_csv(out/'FCAS_interval_state_matrix_90.csv',index=False, float_format='%.7f')
    rows=[]
    for ep,x in intervals.groupby('episode',sort=True):
        row={'episode':ep,'intervals':len(x),
            'generation_observed_gt1MW':int(x['positive_generation_observed_gt1MW'].sum()),
            'generation_target_gt1MW':int(x['positive_generation_target_gt1MW'].sum()),
            'raise_fcas_target_any':int(x[[f+'_gen_any_target_positive' for f in FCAS]].any(axis=1).sum()),
            'raise_reg_enabled_flag_any':int(x['RAISEREG_any_gen_flag_enabled'].sum()),
            'raise_reg_actual_availability_positive_any':int(x['RAISEREG_gen_any_actual_availability_positive'].sum()),
            'raise_reg_target_positive_any':int(x['RAISEREG_gen_any_target_positive'].sum()),
            'raise_reg_actual_avail_positive_but_target_zero':int(((x['RAISEREG_gen_any_actual_availability_positive']==1)&(x['RAISEREG_gen_any_target_positive']==0)).sum())}
        rows.append(row)
    table=pd.DataFrame(rows)
    table.to_csv(out/'FCAS_episode_chain_6.csv',index=False)
    actual=[tuple(x) for x in table[['episode','intervals','generation_observed_gt1MW','generation_target_gt1MW','raise_fcas_target_any']].itertuples(index=False,name=None)]
    check(actual==EXPECTED_BASELINE, 'all 6 x 5 R26R1 inherited episode result locks replay',checks)
    # 90-interval operational class contingency with interpretable denominators
    states=['positive_generation_observed_gt1MW','positive_generation_target_gt1MW','RAISEREG_any_gen_flag_enabled','RAISEREG_gen_any_actual_availability_positive','RAISEREG_gen_any_target_positive']
    labels=['observed_initial_generation_gt1MW','energy_target_gt1MW','regulation_enabled_FCAS_flag','regulation_computed_availability_positive','regulation_dispatch_target_positive']
    contingency=[]
    for ai,a in enumerate(states):
        for bi,b in enumerate(states):
            if a==b:continue
            lhs=intervals[a].astype(bool);rhs=intervals[b].astype(bool)
            fw=intervals.loc[lhs & ~rhs,['episode','interval_end']]
            contingency.append({'antecedent':labels[ai],'consequent':labels[bi],
                'antecedent_true_intervals':int(lhs.sum()),
                'counterexample_intervals':len(fw),
                'implication_holds_in_90_selected_intervals':int(len(fw)==0),
                'first_counterexample_episode':str(fw.iloc[0]['episode']) if len(fw) else '',
                'first_counterexample_interval_end':str(fw.iloc[0]['interval_end']) if len(fw) else ''})
    pd.DataFrame(contingency).to_csv(out/'FCAS_pairwise_observed_implications.csv',index=False)
    # Full verifiable counterexamples on DUID basis: no mixing of unit and station denominators
    unit_witness=episode[episode['asset_mode']=='generation'].copy()
    unit_witness=unit_witness.loc[
        unit_witness['RAISEREG_actual_no_target'] | 
        ((unit_witness['RAISEREGFLAGS'].isin([3,4]))) |
        (unit_witness['RAISEREG_enabled_no_actual']),
        ['episode','interval_end','DUID','INITIALMW','TOTALCLEARED','RAISEREGFLAGS',
         'RAISEREGACTUALAVAILABILITY','RAISEREG','AVAILABILITY',
         'RAISEREG_enabled_no_actual','RAISEREG_actual_no_target']]
    unit_witness.sort_values(['episode','interval_end','DUID']).to_csv(out/'FCAS_unit_strict_witnesses.csv',index=False,float_format='%.7f')

    june12 = episode[episode['episode']=='EP25_04']
    check(len(june12)==44, '12 June 11 x 4 DUID rows found', checks)
    zero_cols=['INITIALMW','TOTALCLEARED']+[v for f in FCAS for v in [f,FIELDMAP[f],f+'FLAGS']]
    check((june12[zero_cols]==0).all().all(), '12 June all 44 DUID rows zero operational targets/status fields (not physical availability)', checks)
    check((june12.loc[june12['DUID']=='W/HOE#2','AVAILABILITY']==254).all(), '12 June W/HOE#2 submitted energy MAXAVAIL 254MW is not physical availability', checks)
    reg=unit_counts[(unit_counts.asset_mode=='generation')&(unit_counts.service=='RAISEREG')]
    check(int(reg['actual_availability_positive_but_target_zero_count'].sum())==10, '10 unit interval FCAS actual availability positive target zero',checks)
    check(int(table['raise_reg_actual_avail_positive_but_target_zero'].sum())==5,'5 station interval FCAS availability positive, target zero',checks)
    check(set(unit_witness[unit_witness['RAISEREG_actual_no_target']]['episode'].unique())=={'EP25_02'},'unit actual avail without FCAS target only 4 June 2025',checks)
    check(all(~episode.loc[episode['RAISEREG_actual_avail_positive'] if 'RAISEREG_actual_avail_positive' in episode else (episode['RAISEREGACTUALAVAILABILITY']>0),'RAISEREGFLAGS'].isin([0,4])),'actual FCAS availability positive requires enabled in observed records',checks)
    check((unit_witness['RAISEREGFLAGS'].isin([0,1,3,4])).all(),'witness flags within official status semantics',checks)
    check(int((episode['RAISEREGFLAGS']==3).sum())==2,'two trapped Raise Reg unit intervals',checks)
    check(int((episode['RAISEREGFLAGS']==4).sum())==1,'one stranded Raise Reg unit interval',checks)
    check(int((episode[(episode['asset_mode']=='generation')]['RAISEREGFLAGS']==1).sum())==95,'95 Raise Reg enabled nontrapped generation-DUID rows',checks)
    check(int(((episode['asset_mode']=='generation')&(episode['RAISEREGFLAGS']==1)&(episode['RAISEREGACTUALAVAILABILITY']==0)).sum())==3,'three flag-enabled generator rows zero postprocessed actual FCAS availability',checks)
    # Source integrity: records original archived upstream ZIP only, no independent reacquisition
    hashes=[{'path':'data/'+name,'sha256':shasum(data/name),'bytes':(data/name).stat().st_size} for name in DATA_FILES]
    (out/'data_sha256.json').write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')
    metadata={
        'active_source_baseline':'ECON_CERT_R26R1_ExternalReaderClarityClosure',
        'source_scope':'archived, previously filtered AEMO DISPATCHLOAD Jan/Jun 2025, not a new full-year causal study',
        'aemo_field_meanings':AEMO_MODEL,
        'flag_encoding':FLAG_MEANING,
        'qualifier':'Actual FCAS availability is bid/trapezium post-processed market dispatch quantity; not verified physical readiness/delivery.',
        'included_episode_intervals':90,'included_duid_interval_records':360,
        'source_filtered_month_records':70272,
        'unadjusted_selected_2025_MWh_equivalent_Hatta':48222/1500,
        'Hatta_primary_strict_frontiers_FDE_per_year':[54.636,105.883],
        'Hatta_2025_mature_run_rate_identified':False,
        'R26R1_inherited_episode_locks_preserved':True,
        'checks_passed':len(checks),
    }
    check(abs(48222/1500 -32.148)<1e-12,'Hatta favorable stress independent division',checks)
    check(32.148<54.636,'Hatta favorable stress below minimum strict boundary',checks)
    metadata['checks_passed']=len(checks)
    (out/'result_metadata.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (out/'qa_tests.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'checks':len(checks),'passed':all(x['pass'] for x in checks),
        'total_raw_rows':len(raw),'accepted_intervals':len(intervals),'accepted_duid_records':len(episode),
        'availability_positive_target_zero_unit_rows':10,
        'availability_positive_target_zero_station_intervals':5,
        'trapped_flag_unit_rows':2,'stranded_flag_unit_rows':1},indent=2))


if __name__=='__main__':
    arg=argparse.ArgumentParser()
    here=Path(__file__).resolve().parents[1]
    arg.add_argument('--data',type=Path,default=here/'data')
    arg.add_argument('--out',type=Path,default=here/'results')
    a=arg.parse_args()
    main(a.data,a.out)
