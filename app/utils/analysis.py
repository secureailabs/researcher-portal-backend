import os
import json
from scipy.stats import ttest_ind
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import plotly.graph_objects as go
import plotly.io as pio


from app.models.cohort import Cohort
from app.utils.cohort_filter import filtered_cohort
from sail_data_layer.csvv1_dataset_serializer import Csvv1DatasetSerializer

# temp code to load the data frame
# file_path_0 = os.path.dirname(os.path.realpath(__file__)) + "/data_frame_0.csv"
# file_path_1 = os.path.dirname(os.path.realpath(__file__)) + "/data_frame_1.csv"
# df1 = pd.read_csv(file_path_0)
# df2 = pd.read_csv(file_path_1)
# df = pd.concat([df1, df2])

serializer_init = Csvv1DatasetSerializer()

# f = open(
#     os.path.dirname(os.path.realpath(__file__)) + "/../../InitializationVector.json",
#     "r",
# )
# iv = json.loads(f.read())

# data_set_id_first = iv["datasets"][0]["id"]
data_set_id_first = "8b54a57a-c186-4a25-b43e-9927ea6ae296"

# read dataset from path ../../data/dataset_id
dataset = serializer_init.read_dataset_for_path(
    os.path.dirname(os.path.realpath(__file__)) + f"/../../data/{data_set_id_first}"
)

df = dataset[0]

sample_cohort_dict = {
    "filter": [
        {"series_name": "gender", "operator": "string", "value": "female"},
        {"series_name": "body_mass_index", "operator": "gt", "value": 30},
    ],
    "filter_operator": ["and"],
}


# Write a function to perform a welch's t-test
def welch_t_test(params):
    """
    Welch's t-test
    Description : Welch's t-test, or unequal variances t-test, is a two-sample location test which is used to test the hypothesis that two populations have equal means.
    """
    cohort = params["cohort"]
    series_name_list = params["series_name_list"]

    #  get the cohort
    filtered_df = filtered_cohort(df, cohort)

    stat, p = ttest_ind(
        filtered_df[series_name_list[0]],
        filtered_df[series_name_list[1]],
        equal_var=False,
    )

    return {"stat": stat, "p": p}


def paired_t_test(params):
    """Paired t-test"""
    cohort = params["cohort"]
    series_name_list = params["series_name_list"]

    print("====================================")
    print("series_name_list: ", series_name_list)

    # print origin length of df
    print("origin length of df: ", len(df))

    #  get the cohort
    filtered_df = filtered_cohort(df, cohort)

    # print length of filtered df
    print("length of filtered df: ", len(filtered_df))

    stat, p = ttest_ind(
        filtered_df[series_name_list[0]], filtered_df[series_name_list[1]]
    )

    data1 = filtered_df[series_name_list[0]]
    data2 = filtered_df[series_name_list[1]]

    # Create histograms for both datasets
    trace1 = go.Histogram(x=data1, name=series_name_list[0], opacity=0.5)
    trace2 = go.Histogram(x=data2, name=series_name_list[1], opacity=0.5)

    # Create the layout
    layout = go.Layout(
        title="Distribution of eGFR Values Before and After Surgery",
        xaxis=dict(title="eGFR Value"),
        yaxis=dict(title="Frequency"),
        barmode="overlay",  # Overlay histograms
    )
    # set width and height
    layout["width"] = 800
    layout["height"] = 600

    # Create the figure using px.histogram
    fig = go.Figure(data=[trace1, trace2], layout=layout)

    fig_json = json.loads(pio.to_json(fig))

    return {"stat": stat, "p": p, "plot": fig_json}


def skew(params):
    """Skew"""
    cohort = params["cohort"]
    series_name = params["series_name"]

    #  get the cohort
    filtered_df = filtered_cohort(df, cohort)
    print("====================================")

    skew = filtered_df[series_name].skew()

    print("skew: ", skew)

    return {"skew": skew}


def chi_square(params):
    """Chi Square"""
    cohort = params["cohort"]
    series_name = params["series_name"]

    #  get the cohort
    filtered_df = filtered_cohort(df, cohort)

    # get the unique values in the series
    unique_values = filtered_df[series_name].unique()

    # get the counts of each unique value
    value_counts = filtered_df[series_name].value_counts()

    # get the total count of the series
    total_count = len(filtered_df[series_name])

    # get the expected value
    expected_value = total_count / len(unique_values)

    # calculate the chi square value
    chi_square = 0
    for value in unique_values:
        chi_square += (value_counts[value] - expected_value) ** 2 / expected_value

    print("chi_square: ", chi_square)

    return {"res": {"chi_square": chi_square}}


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
        "function": paired_t_test,
        "parameterRequired": {
            "series_name_list": ["series_name_1", "series_name_2"],
            "cohort": sample_cohort_dict,
        },
    },
    "anova": {
        "display_name": "ANOVA",
        "description": "ANOVA",
        "function": anova,
        "parameterRequired": {
            "cohort_list": [sample_cohort_dict],
            "series_name": "series_name_1",
        },
    },
    "welch_t_test": {
        "display_name": "Welch's t-test",
        "description": "Welch's t-test",
        "function": welch_t_test,
        "parameterRequired": {
            "series_name_list": ["series_name_1", "series_name_2"],
            "cohort": sample_cohort_dict,
        },
    },
    "skew": {
        "display_name": "Skew",
        "description": "Skew",
        "function": skew,
        "parameterRequired": {
            "series_name": "series_name_1",
            "cohort": sample_cohort_dict,
        },
    },
    "chi_square": {
        "display_name": "Chi Square",
        "description": "Chi Square",
        "function": chi_square,
        "parameterRequired": {
            "series_name": "series_name_1",
            "cohort": sample_cohort_dict,
        },
    },
}


def run_analysis(type, input_params: dict):
    """Run analysis on the cohort"""
    # Run analysis on the cohort
    analysis_function = analysis_function_list[type]
    print("analysis_function: ", analysis_function)
    print("input_params: ", input_params)
    res = analysis_function["function"](input_params)
    return res
