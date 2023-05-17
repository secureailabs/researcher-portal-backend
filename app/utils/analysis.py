import os
from scipy.stats import ttest_ind
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

from app.models.cohort import Cohort
from app.utils.cohort_filter import filtered_cohort

# temp code to load the data frame
file_path_0 = os.path.dirname(os.path.realpath(__file__)) + "/data_frame_0.csv"
file_path_1 = os.path.dirname(os.path.realpath(__file__)) + "/data_frame_1.csv"
df1 = pd.read_csv(file_path_0)
df2 = pd.read_csv(file_path_1)
df = pd.concat([df1, df2])

sample_cohort_dict = {
    "filter": [
        {"series_name": "gender", "operator": "string", "value": "female"},
        {"series_name": "body_mass_index", "operator": "gt", "value": 30},
    ],
    "filter_operator": ["and"],
}


def paired_t_test(params):
    """Paired t-test"""
    cohort = params["cohort"]
    series_name_list = params["series_name_list"]

    #  get the cohort
    filtered_df = filtered_cohort(df, cohort)

    stat, p = ttest_ind(
        filtered_df[series_name_list[0]], filtered_df[series_name_list[1]]
    )

    return {"stat": stat, "p": p}


def anova(params):
    """ANOVA"""
    cohort_list = params["cohort_list"]
    series_name = params["series_name"]

    filtered_df_list = []
    for cohort in cohort_list:
        filtered_df_list.append(filtered_cohort(df, cohort))

    # extract values for series-name from each cohort
    series_list = []
    for filtered_df in filtered_df_list:
        series_list.append(filtered_df[series_name])

    # Create a dictionary to hold the series data
    data = {f"Cohort {i+1}": series for i, series in enumerate(series_list)}

    # Convert the dictionary to a pandas DataFrame
    df_anova = pd.DataFrame(data)

    # Reshape the DataFrame for ANOVA
    df_melt = pd.melt(
        df_anova, value_vars=df_anova.columns, var_name="Cohort", value_name=series_name
    )

    # Create the ANOVA model
    model = ols(f"{series_name} ~ C(Cohort)", data=df_melt).fit()

    # Perform ANOVA and obtain the table
    anova_table = sm.stats.anova_lm(model, typ=2)

    return anova_table


analysis_funcion_map = {
    "paired_t_test": paired_t_test,
    "anova": anova,
}

analysis_function_list = {
    "paired_t_test": {
        "display_name": "Paired t-test",
        "description": "Paired t-test",
        "function": "paired_t_test",
        "parameter": {
            "series_name_list": ["series_name_1", "series_name_2"],
            "cohort": sample_cohort_dict,
        },
    },
    "anova": {
        "display_name": "ANOVA",
        "description": "ANOVA",
        "function": "anova",
        "parameter": {
            "cohort_list": [sample_cohort_dict],
            "series_name": "series_name_1",
        },
    },
}


def run_analysis(type, input_params: dict):
    """Run analysis on the cohort"""
    # Run analysis on the cohort
    analysis_function = analysis_funcion_map[analysis_function_list[type]["function"]]
    return analysis_function(input_params)
