import pandas as pd

from synthetic_data_experiment import analyze_with_peeking, analyze_without_peeking

# dataset params
SIMULATIONS_NUM = 10000
SAMPLE_SIZE = 320000

# t-Test param (Minimum p-value we need to "accept the test").
ALPHA = 0.05


def get_and_split_users(df: pd.DataFrame, sample_size: int):
    """Randomly pick sample_size * 2 observation from dataframe and equally
    split between groups. Return two numpy arrays."""

    sampled_df = df.sample(n=sample_size * 2, replace=False)
    group_1 = sampled_df.iloc[:sample_size].sort_values(by=['user_id'])
    group_2 = sampled_df.iloc[sample_size:].sort_values(by=['user_id'])

    return group_1['is_buyer'].to_numpy(), group_2['is_buyer'].to_numpy()


if __name__ == "__main__":

    users_data_df = pd.read_csv('some_real_data.tsv', sep='\t')
    peeking_significant_results = 0
    non_peeking_significant_results = 0

    for i in range(SIMULATIONS_NUM):
        control_group, test_group = get_and_split_users(users_data_df, SAMPLE_SIZE)
        p_value_non_peeking = analyze_without_peeking(control_group, test_group)
        p_values_peeking = analyze_with_peeking(control_group, test_group)

        if p_value_non_peeking < ALPHA:
            non_peeking_significant_results += 1

        if any(p < ALPHA for p in p_values_peeking):
            peeking_significant_results += 1

        print(f"Iteration {i} of {SIMULATIONS_NUM}") if i % 100 == 0 else None

    print(
        "-" * 80,
        f"simulations number: {SIMULATIONS_NUM}",
        f"sample_size: {SAMPLE_SIZE}",
        f"alpha: {ALPHA}",
        f"non_peeking_significant_results: {non_peeking_significant_results}",
        f"peeking_significant_results: {peeking_significant_results}",
        sep="\n",
    )
