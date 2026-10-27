# Profiling (py-spy + scalene)

`profile.sh` profiles any Python command with two free, pip-installable profilers:

| Tool | What it gives | Files |
| --- | --- | --- |
| [py-spy](https://github.com/benfred/py-spy) | sampling flamegraph across worker subprocesses, including native (Cantera/NumPy) frames when available | `pyspy.svg`, `pyspy.speedscope.json` (open at https://www.speedscope.app) |
| [scalene](https://github.com/plasma-umass/scalene) | line-level CPU (Python vs native) and memory | `scalene.json`, `scalene.txt`, `scalene-profile.html` |

```bash
pip install py-spy scalene
# once sim modules exist (SPEC.md: python -m sims.NN_name.run [--quick] [--workers N])
tools/profiling/profile.sh -o /tmp/prof -- python -m sims.01_equilibrium.run --quick --workers 1
tools/profiling/profile.sh -t pyspy -o /tmp/prof -- python some_script.py
```

Notes
- The command must start with `python`/`python3`; `-m module` is supported.
- Profile with `--quick` and `--workers 1` first; py-spy follows subprocesses (`--subprocesses`) if you need the parallel view.
- Cantera/SciPy time is mostly native: read the py-spy flamegraph first, scalene for memory and the Python-vs-native split.
- Profiling repeats the run (py-spy twice, scalene once). Keep `--full` runs off the shared VPS unless the owner approved the compute.
- No C/C++ code exists in this repo yet, so there is no ASan/UBSan workflow. If native extensions are added, copy `.github/workflows/sanitizers.yml` from redwing509/solid-state-fan-project.
