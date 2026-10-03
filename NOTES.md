Commit 1:
I tested main.py with restoration_graph and toy_test in parallel. Both worked fully and neither affected the other. This is because planner.py does not care about the other files as long as it has START,GOAL, and the appropriate setup with available_actions and apply_action.

Commit 2:
I was surprised that `test_no_solution_returns_none` initially passed even though `available_actions` was still using the original actions, so it was not actually testing my fake problem's missing prerequisite.

Commit 3:
I tested the set version in separate runs and got different plans with the same seed. This is because Python randomizes string hashes between runs, which can change the set's order. The seed only controls the solver's shuffling.

I also saw that my old is_valid_plan still accepted a plan over budget. It checked the Lab 2 rules but not the new tranche rule, so tests need to change when the requirements change.
