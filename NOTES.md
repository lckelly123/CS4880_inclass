Commit 1:
I tested main.py with restoration_graph and toy_test in parallel. Both worked fully and neither affected the other. This is because planner.py does not care about the other files as long as it has START,GOAL, and the appropriate setup with available_actions and apply_action.

Commit 2:
I was surprised that `test_no_solution_returns_none` initially passed even though `available_actions` was still using the original actions, so it was not actually testing my fake problem's missing prerequisite.

Commit 3:
I tested the set version in separate runs and got different plans with the same seed. This is because Python randomizes string hashes between runs, which can change the set's order. The seed only controls the solver's shuffling.

I also saw that my old is_valid_plan still accepted a plan over budget. It checked the Lab 2 rules but not the new tranche rule, so tests need to change when the requirements change.

Commit 4:
The forward chaining loop ends because `known` only grows after a new symbol is added; and it is bounded by the starting facts and the non-infinite number of rule conclusions. Once a full pass adds nothing, `changed` stays false and the loop stops.

The premises are sorted so that the same proof prints in a consistent order. Without this, set iteration might rearrange the explanation between runs, like the set version in Lab 3.

I shuffled the rules for a scratch report with more than one damage type and got the same conclusions, however different rejection proofs. This is because `why` keeps the first rule that derives a symbol, so rule order matters when comparing rejection logs during a audit.

I checked the starter reports and got 4 accepted and 7 rejected, which matched the lab's self-check. r9 had both violations, while r10 and r11 failed at the schema stage.

I cannot directly write a rule for major severity with no damage using the current Horn clauses because they only check for facts that are present. I could add a `no_damage` fact during conversion when the damage list is empty, then combine it with `severity_major`. This assumes the damage list is complete, and the fact must be removed and the conclusions recomputed if damage is added later.

Commit 5:
Accepted quarentined or rejected guesses from incoming a:
1: quarentined
2: rejected
3: quarentined
4: rejected
5: rejected

Incoming B passes the individual report checks because each report obeys the logical rules and has a plausible combination of material, damage, and severity. Its problem is the changed material proportions across the batch. A check of one report cannot measure those proportions; the batch-level chi-square check compares the material counts with the reference distribution and detects the shift.

The held-out quarantine rate uses a range of 0.5% to 4% because new random samples can have different proportions of low-likelihood reports. Calibrating the threshold near 2% on the reference data does not guarantee exactly 2% on fresh data.

1. Predictions: I only disagreed on a-odd2 because my extra ceramic-corrosion rule predicted rejection. With that rule disabled, quarantine is correct: the report is valid but improbable.

2. Independence: A crack can loosen an object's base, so crack and loose_base can be related even for the same material.

3. Parameters: The scoring model has 4 material + 25 damage + 6 severity = 35 free parameters. Part E adds 2 separately. Four hundred reports are reasonable, although rare cases remain uncertain, 40 would leave sparse counts and unreliable estimates.

4. Smoothing: A new import could contain stone with corrosion, which never appeared in the reference data. Without smoothing, its zero probability causes log(0) to raise ValueError.

5. Calibration: A small gap is expected because both datasets use the same distribution and the model is small and smoothed. Fewer reports, a more complex model, or a changed incoming distribution could increase the gap.

6. Quarantine versus reject: Rare true reports are delayed for human review. I would lower the threshold (make it more negative) to quarantine fewer rare finds, at the cost of accepting more typos.
