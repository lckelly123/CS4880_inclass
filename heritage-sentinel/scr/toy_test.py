# restoration_graph.py — problem definition only.
# planner.py must not know anything specific to this file.

ACTIONS = {
    "walk": {"requires": set(), "cost": 3},
    "jump": {"requires": {"walk"}, "cost": 2},
    "run": {"requires": {"jump"}, "cost": 1},
    "sprint": {"requires": {"run"}, "cost": 2},
}

GOAL2 = frozenset(ACTIONS.keys())
START2 = frozenset()

def available_actions2(state):
    """Actions whose prerequisites are satisfied and not already done."""
    return [a for a, info in ACTIONS.items()
            if a not in state and info["requires"].issubset(state)]

def apply_action2(state, action):
    return state | {action}