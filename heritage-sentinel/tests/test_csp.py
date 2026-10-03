# TODO: set up the CSP tests and helpers from the handout.
import subprocess
import sys
from pathlib import Path

import pytest

from csp import backtracking_search
from restoration_csp import VARIABLES, DOMAINS, build_constraints
from test_planner import is_valid_plan


def solve(seed=0, cap=4, all_solutions=False):
    return backtracking_search(VARIABLES, DOMAINS, build_constraints(tranche_cap=cap),
                               seed=seed, all_solutions=all_solutions)


def to_plan(assignment):
    return sorted(assignment, key=assignment.get)


# TODO: check that the solver returns a valid plan.
def test_solution_is_valid():
    plan = to_plan(solve()[0])
    assert is_valid_plan(plan, tranche_cap=4)


# TODO: check that the same seed produces the same solution.
def test_same_seed_same_plan():
    assert solve(seed=7) == solve(seed=7)


# TODO: parametrize over the table in the self-check:
# cap 4 -> 5 plans, cap 3 -> 1 plan, cap 2 -> 0 plans.
@pytest.mark.parametrize("cap, expected", [(4, 5), (3, 1), (2, 0)])
def test_solution_counts(cap, expected):
    assert len(solve(cap=cap, all_solutions=True)) == expected


def test_old_oracle_gap_is_closed():
    bad = ["stabilize_base", "seal_crack", "clean_surface", "restore_pigment"]
    # TODO: assert your extended is_valid_plan rejects this plan at cap 4.
    assert not is_valid_plan(bad, tranche_cap=4)


def test_reproducible_across_processes():
    # TODO: run main_csp.py in a subprocess twice and compare the outputs.
    # Use this repository's heritage-sentinel/scr layout.
    repo_root = Path(__file__).resolve().parents[2]
    command = [sys.executable, str(repo_root / "heritage-sentinel" / "scr" / "main_csp.py")]
    first = subprocess.run(command, cwd=repo_root, capture_output=True,
                           text=True, check=True).stdout
    second = subprocess.run(command, cwd=repo_root, capture_output=True,
                            text=True, check=True).stdout
    assert first == second
