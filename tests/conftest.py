"""Make the source checkout importable and provide one shared module loader.

Module packages under ``sims/`` start with a digit (``sims/03_engine_cycle``),
so they cannot be imported with a plain ``import`` statement.  Tests load them
through :func:`load_sims_module`, which uses ``importlib.import_module`` so
that each dotted name maps to exactly one module object in ``sys.modules``.
Re-executing a module file under the same (or a stub) name creates a second
copy of every function; ``multiprocessing`` (spawn context in
``sims.common.io.ordered_map``) then refuses to pickle e.g.
``sims.03_engine_cycle.run._task`` because "it's not the same object" as the
one registered in ``sys.modules``.
"""

from pathlib import Path
import importlib
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def load_sims_module(dotted_name):
    """Import a ``sims.*`` module by dotted name via the real package tree."""
    if not dotted_name.startswith("sims."):
        raise ValueError(f"expected a sims.* module, got {dotted_name!r}")
    return importlib.import_module(dotted_name)
