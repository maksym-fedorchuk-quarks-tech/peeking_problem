import numpy as np
from scipy import stats

# dataset params
SIMULATIONS_NUM = 10000
SAMPLE_SIZE = 320000
AVG_BUYERS_PERCENTAGE = 0.02

# t-Test param (Minimum p-value we need to "accept the test").
ALPHA = 0.05
# Every 'PEEKING_STEP_SIZE' observations we going to check the p-value
PEEKING_STEP_SIZE = 50000


def generate_synthetic_data(user_num: int, buyers_percentage: float):
    """Generate two datasets representing user simulations. Each element in the
    arrays indicates whether a user is a buyer (1) or not (0).

    Parameters:
        user_num (int): Number of users (simulations) in each dataset.
        buyers_percentage (float): Probability that a user is a buyer (1).

    Returns:
        tuple: Two numpy arrays of size N."""

    group1 = np.random.choice([0, 1], size=user_num, p=[1 - buyers_percentage, buyers_percentage])
    group2 = np.random.choice([0, 1], size=user_num, p=[1 - buyers_percentage, buyers_percentage])

    return group1, group2


def analyze_without_peeking(group1: np.ndarray, group2: np.ndarray) -> int:
    """Return p-value for whole test data samples"""
    t_stat, p_value = stats.ttest_ind(group1, group2)

    return p_value


def analyze_with_peeking(group1: np.ndarray, group2: np.ndarray, step_size=None) -> list:
    """Return list of all observed p-values, representing the results of peeking
    at the data after every 'step_size' number of samples.
    Default moments we going to 'peek' our test results are 100k, 150k and 200k observations."""

    if step_size is None:
        peeking_group_size = [100000 + 50000 * n for n in range(3)]
    else:
        peeking_group_size = range(step_size, len(group1) + 1, step_size)

    p_values = []
    for n in peeking_group_size:
        t_stat, p_value = stats.ttest_ind(group1[:n], group2[:n])
        p_values.append(p_value)

    return p_values


if __name__ == "__main__":
    peeking_significant_results = 0
    non_peeking_significant_results = 0

    for i in range(SIMULATIONS_NUM):
        control_group, test_group = generate_synthetic_data(SAMPLE_SIZE, AVG_BUYERS_PERCENTAGE)
        p_value_non_peeking = analyze_without_peeking(control_group, test_group)
        p_values_peeking = analyze_with_peeking(control_group, test_group)

        if p_value_non_peeking < ALPHA:
            non_peeking_significant_results += 1

        if any(p < ALPHA for p in p_values_peeking):
            peeking_significant_results += 1

        print(f"Iteration {i} of {SIMULATIONS_NUM}") if i % 1000 == 0 else None

    print(
        "-" * 80,
        f"simulations number: {SIMULATIONS_NUM}",
        f"sample_size: {SAMPLE_SIZE}",
        f"alpha: {ALPHA}",
        f"peeking every N observations: {PEEKING_STEP_SIZE}",
        f"non_peeking_significant_results: {non_peeking_significant_results}",
        f"peeking_significant_results: {peeking_significant_results}",
        sep="\n",
    )
