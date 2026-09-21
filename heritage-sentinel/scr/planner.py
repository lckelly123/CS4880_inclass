# planner.py — search algorithm only. No mention of statues, cracks, or pigment allowed here.
from collections import deque

def bfs_search(start, goal, available_actions, apply_action):
    frontier = deque([(start, [])])
    visited = {start}
    while frontier:
        state, path = frontier.popleft()
        if state == goal:
            return path
        else:
            action = available_actions(state)
            if action==[]:
                break
            for i in range(len(action)):
                next_state = apply_action(state, action[i])
                if next_state not in visited:
                    visited.add(next_state)
                    frontier.append((next_state, path + [action[i]]))
        # TODO: for each action available from `state`, compute the next
        # state, and if it hasn't been visited, add it to the frontier
        # with the updated path.
        ...
    return None  # no valid sequence exists