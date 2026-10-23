# prob.py — generic probability helpers. No heritage vocabulary allowed here.
from collections import Counter

def fit_categorical(observations, domain, alpha=1.0):
    """P(value) with add-alpha (Laplace) smoothing. Returns {value: prob}.
    Every value in `domain` gets nonzero probability, even if never observed."""
    # TODO: for each value v in `domain`, the probability is
    #       (number of times v appears in observations + alpha)
    #       / (len(observations) + alpha * len(domain))
    # Use collections.Counter to count. Every value in `domain` must appear
    # in the returned dict, including values that were never observed.
    counts = Counter(observations)
    total = len(observations) + alpha * len(domain)
    return {v: (counts[v] + alpha) / total for v in domain}


def fit_conditional(pairs, parent_domain, child_domain, alpha=1.0):
    """P(child | parent) from (parent, child) pairs. Returns {parent: {child: prob}}."""
    by_parent = {p: [] for p in parent_domain}
    for parent, child in pairs:
        by_parent[parent].append(child)
    return {p: fit_categorical(by_parent[p], child_domain, alpha) for p in parent_domain}


def chi_square(observed_counts, expected_probs):
    """Pearson chi-square statistic comparing observed counts to expected probabilities."""
    # TODO: n = total of the observed counts. For each category k with
    #       probability p, expected = n * p, and the statistic gains
    #       (observed - expected)^2 / expected. A category missing from
    #       observed_counts has an observed count of 0.
    n = sum(observed_counts.values())
    statistic = 0.0
    for k, p in expected_probs.items():
        expected = n * p
        observed = observed_counts.get(k, 0)
        statistic += (observed - expected) ** 2 / expected
    return statistic


def percentile(values, q):
    """Nearest-rank style: the value at index floor(q * n) of the sorted list."""
    ordered = sorted(values)
    return ordered[min(int(q * len(ordered)), len(ordered) - 1)]
