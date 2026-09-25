# tests/test_planner.py
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from scr.restoration_graph import ACTIONS, START, GOAL, available_actions, apply_action
from scr.planner import bfs_search

def is_valid_plan(plan, actions=ACTIONS):
    """A plan is valid if every action's prerequisites are satisfied by
    the actions before it, and every required action appears exactly once."""
    completed = set()
    for action in plan:
        if action in completed:
            return False          # duplicate action
        if not actions[action]["requires"].issubset(completed):
            return False          # prerequisite violated
        completed.add(action)
    return completed == set(actions.keys())


def test_finds_a_valid_plan():
    plan = bfs_search(START, GOAL, available_actions, apply_action)
    assert plan is not None
    assert is_valid_plan(plan)


def test_trivial_already_done():
    # start == goal: the plan should be empty, not None, not a crash
    plan = bfs_search(GOAL, GOAL, available_actions, apply_action)
    assert plan == []


def test_plan_has_no_duplicate_actions():
    plan = bfs_search(START, GOAL, available_actions, apply_action)
    assert len(plan) == len(set(plan))


def test_no_solution_returns_none():
    # TODO: this is your job. Construct a problem where the goal is
    # unreachable — e.g. a goal that includes an action name not in
    # ACTIONS, or an action whose "requires" set can never be satisfied
    # (a circular or impossible prerequisite). Then assert that
    # bfs_search returns None instead of crashing or hanging forever.
    ACTIONS_fake = {
    "skydive": {"requires": {"fly_plane"}, "cost": 3},
    "drive": {"requires": set(), "cost": 2},
    "fly_plane": {"requires": {"pilots license"}, "cost": 1},
    "land": {"requires": {"skydive"}, "cost": 2},}

    def available_actions2(state):
        """Actions whose prerequisites are satisfied and not already done."""
        return [a for a, info in ACTIONS_fake.items()
                if a not in state and info["requires"].issubset(state)]

    def apply_action2(state, action):
        return state | {action}

    GOAL_fake = frozenset(ACTIONS_fake.keys())
    START_fake = frozenset()
    assert bfs_search(START_fake, GOAL_fake, available_actions2, apply_action2) is None
    




def test_large_action_set_terminates():
    # TODO: build a bigger synthetic ACTIONS dict (15-20 actions, chained
    # prerequisites) and assert bfs_search still returns within a couple
    # of seconds. This isn't about speed — it's about proving the search
    # actually terminates instead of looping.
    ACTIONS_fake2 = {
        "test1": {"requires": set(), "cost": 3},
        "test2": {"requires": {"test1"}, "cost": 2},
        "test3": {"requires": {"test2"}, "cost": 1},
        "test4": {"requires": {"test3"}, "cost": 2},
        "test5": {"requires": {"test4"}, "cost": 2},
        "test6": {"requires": {"test5"}, "cost": 2},
        "test7": {"requires": {"test6"}, "cost": 2},
        "test8": {"requires": {"test7", "test1","test2"}, "cost": 2},
        "test9": {"requires": {"test8"}, "cost": 2},
        "test10": {"requires": {"test9"}, "cost": 2},
        "test11": {"requires": {"test10"}, "cost": 2},
        "test12": {"requires": {"test11","test8"}, "cost": 2},
        "test13": {"requires": {"test12"}, "cost": 2},
        "test14": {"requires": {"test13"}, "cost": 2},
        "test15": {"requires": {"test14","test3","test10"}, "cost": 2},
        "test16": {"requires": {"test15"}, "cost": 2},
        "test17": {"requires": {"test16"}, "cost": 2}}

    def available_actions3(state):
        """Actions whose prerequisites are satisfied and not already done."""
        return [a for a, info in ACTIONS_fake2.items()
                if a not in state and info["requires"].issubset(state)]

    def apply_action3(state, action):
        return state | {action}

    GOAL_fake2 = frozenset(ACTIONS_fake2.keys())
    START_fake2 = frozenset()
    assert bfs_search(START_fake2, GOAL_fake2, available_actions3, apply_action3) is not None
    


