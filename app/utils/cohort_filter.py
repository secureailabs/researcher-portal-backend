import pandas as pd


def filtered_cohort(df: pd.DataFrame, cohort: dict) -> pd.DataFrame:
    """Filter cohort based on analysis"""
    # Filter cohort based on analysis
    print("df", df)
    i = 0
    prev_df = pd.DataFrame()
    for item in cohort["filter"]:
        tmp_df = pd.DataFrame()
        if item["operator"] == "eq":
            # filter df where race header is equal to value
            tmp_df = df[df[item["series_name"]] == item["value"]]
            print("tmp_df", tmp_df)
        elif item["operator"] == "gt":
            tmp_df = df[item["series_name"] > item["value"]]
        elif item["operator"] == "lt":
            tmp_df = df[item["series_name"] < item["value"]]
        else:
            raise Exception("Operator not supported")
        if i >= 1:
            if cohort["filter_operator"][i - 1] == "and":
                prev_df = prev_df & tmp_df
            elif cohort["filter_operator"][i - 1] == "or":
                prev_df = prev_df | tmp_df
            else:
                raise Exception("filter operator not supported")
        else:
            prev_df = tmp_df
        i += 1

    return prev_df
