"""V-C second half (ACCEPTANCE.md): integrated Wiebe heat vs Q_avail at every comparison row. Not run by verify.py."""
import warnings,sys;warnings.filterwarnings('ignore')
sys.path.insert(0,'.')
from multiprocessing import Pool
from engines.m03_cantera import engine as E, points as P
def f(k):
    d=P.load_rows(); reg=k.split('|')[0]
    out=[]
    for ht in ('woschni','hohenberg'):
        r=E.run_case(P.case_from_row(d['rows'][k],reg,heat_transfer=ht))
        out.append(abs(r['wiebe_integral_error']))
    return k,max(out)
if __name__=='__main__':
    ks=list(P.load_rows()['rows'])
    with Pool(6) as p: res=p.map(f,ks)
    import json, pathlib
    o = dict(criterion="V-C Wiebe integral |err| <= 1e-6 relative (rtol 1e-9, woschni + hohenberg, all 18 rows)", max_rel_err=float(max(x[1] for x in res)), per_row={k: float(v) for k, v in res})
    o["pass_"] = o["max_rel_err"] <= 1e-6
    pathlib.Path("results/engines/m03_cantera/wiebe_integral.json").write_text(json.dumps(o, indent=1))
    print(o["max_rel_err"], o["pass_"])
