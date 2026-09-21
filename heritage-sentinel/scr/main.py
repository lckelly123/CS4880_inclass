from restoration_graph import START, GOAL, available_actions, apply_action
from toy_test import START2, GOAL2, available_actions2, apply_action2
from planner import bfs_search

if __name__ == "__main__":
    plan = bfs_search(START, GOAL, available_actions, apply_action)
    print("Restoration plan:", plan)

    plan2 = bfs_search(START2, GOAL2, available_actions2, apply_action2)
    print("Toy test plan:", plan2)
