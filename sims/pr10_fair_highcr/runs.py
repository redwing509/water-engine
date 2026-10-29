# [Grok Bot 2026-10-29 14:25 PDT] PR 10 high-CR fair rerun + factory-CR search (James t282u + 2:15 PM update).
# Wet (humid_evap / liquid) at a w grid and dry DEI (fuel-evap cooling) EACH scanned over CR; best = own knock-limited CR.
# Usage: FUEL=.. REGIME=hot|normal runs.py <points|crn> <n>. Once, never retried. Executed, not validated.
import json, os, sys, time
sys.path.insert(0, "/workspace/self-jobs/coolfrac-step3-sens-ch3oh-cf05-h")
import runs as B
HERE = os.path.dirname(os.path.abspath(__file__))
FUEL, REG = os.environ["FUEL"], os.environ["REGIME"]
TIN, PW = (400.0, 388.15) if REG == "hot" else (360.0, 363.15)
WS = {"CH3OH": (0.15, 0.3, 0.375, 0.5, 0.6), "C2H5OH": (0.15, 0.3, 0.375, 0.5), "PRF91": (0.1, 0.2, 0.3), "E85": (0.1, 0.2, 0.3)}[FUEL]
if REG == "normal": WS = tuple(w for w in WS if w <= 0.375)
CRW, CRD = range(10, 27, 2), range(8, 21, 2)
def tasks():
    t = [dict(grp="dry", cf=0.7, spec=dict(step=4, kind="dry", fuel=FUEL, regime=REG, CR=c, w=0.0, T_intake_K=TIN)) for c in CRD]
    for intake in ("humid_evap", "liquid"):
        for w in WS:
            t += [dict(grp=f"{intake}-w{w}", cf=0.7, spec=dict(step=4, kind="coupled", intake=intake, fuel=FUEL, regime=REG,
                       CR=c, w=w, T_intake_K=TIN, port_wall_K=PW)) for c in CRW]
    return t
B.tasks = tasks; B.HERE = f"{HERE}/{FUEL}-{REG}"; os.makedirs(B.HERE, exist_ok=True)
if __name__ == "__main__":
    mode, n = sys.argv[1], int(sys.argv[2])
    if mode == "points": B.points(n); sys.exit(0)
    outp = f"{B.HERE}/{mode}.jsonl"
    done = {B.K(json.loads(l)) for l in open(outp)} if os.path.exists(outp) else set()
    todo = [r for r in B.allrows() if B.K(r) not in done]
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(n, max_tasks_per_child=1) as ex, open(outp, "a") as fh:
        for x in ex.map(B.one, [(mode, r) for r in todo]): fh.write(json.dumps(x, default=str) + "\n"); fh.flush()
