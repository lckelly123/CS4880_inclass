# restoration_csp.py — problem definition only.
from restoration_graph import ACTIONS      # reuse the Lab 1 data

VARIABLES = list(ACTIONS.keys())           # a list, not a set. Remember this.
DOMAINS = {a: list(range(1, len(VARIABLES) + 1)) for a in VARIABLES}

def build_constraints(actions=ACTIONS, tranche_cap=4):
    constraints = []

    # 1. all-different
    for i, a in enumerate(VARIABLES):
        for b in VARIABLES[i + 1:]:
            constraints.append(((a, b), lambda x, y: x != y))

    # 2. TODO: prerequisites. For each action and each action it requires,
    #    add a constraint on the pair (required, action) saying the
    #    required action's slot is smaller.

    for action, info in actions.items():
        for required in info["requires"]:
            constraints.append((
                (required, action),
                lambda required_slot, action_slot: required_slot < action_slot))

    # 3. TODO: tranche rule. One constraint over ALL variables: the summed
    #    cost of every action whose slot is <= 2 must be <= tranche_cap.
    #    Hint: scope = tuple(VARIABLES); the check function receives one
    #    slot per variable, in that same order.

    scope = tuple(VARIABLES)

    constraints.append((
        scope,
        lambda *slots: sum(
            ACTIONS[action]["cost"]
            for action, slot in zip(scope, slots)
            if slot <= 2
        ) <= tranche_cap))

    return constraints
