from scipy.stats import ttest_ind
import pandas as pd

def paired_t_test(
        sample_1: pd.DataFrame,
        sample_2: pd.DataFrame,
):
    """Paired t-test"""

    stat, p = ttest_ind(sample_1, sample_2)

    return {
        "stat": stat,
        "p": p
    }


def run_analysis(df, analysis: dict):
    """Run analysis on the cohort"""
    # Run analysis on the cohort
    if analysis["analysis_type"] == "paired_t_test":
        return paired_t_test(df[analysis["parameter"]["series_name_0"]], df[analysis["parameter"]["series_name_1"]])
    else:
        raise Exception("Analysis type not supported")