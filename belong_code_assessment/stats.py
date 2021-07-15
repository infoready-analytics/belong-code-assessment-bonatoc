def get_top_n_by_time(df, time_col, count_col="hourly_counts", query_col="sensor_name", top_n=10):

    """Determine which sensors report the most pedestrian traffic for a specified unit of time. The
    unit of time must exist as a column within the DataFrame. The resulting DataFrame will contain
    the column specified by time_col in addition to sensor_name, hourly_counts, and rank.

    Args:
        df (pd.DataFrame): DataFrame containing pedestrian data.
        time_col (str): Column name to determine stats against, e.g. day, month, year.
        count_col (str, optional): Column name with pedestrian counts. Defaults to "hourly_counts".
        query_col (str, optional): Column name with sensor locations. Defaults to "sensor_name".
        top_n (int, optional): Number of top results per unique value in time_col to return.
        Defaults to 10.

    Returns:
        (pd.DataFrame, pd.DataFrame): Two DataFrames - one with all sensors ranked and the other
        with only the top_n ranked sensor names per unique value in time_col.
    """

    # test columns are in DataFrame
    if not all(col in df.columns for col in [time_col, count_col, query_col]) or len(df) == 0:
        return None, None

    # test at least top_n examples are available for each unique time value
    for _, time_df in df.groupby(time_col):
        if len(time_df) < top_n:
            return None, None

    # sum pedestrian counts for each sensor per unique value in time_col
    df = df.groupby([time_col, query_col])[count_col].sum().reset_index(name=count_col)

    # rank hourly counts by time_col
    df["rank"] = df.groupby(time_col)[count_col].rank(ascending=False).astype(int)

    # sort DataFrame by rank to grab top_n rows
    df = df.sort_values(by=["rank"]).reset_index(drop=True)

    # make assumption data in time_col is clean
    return df, df.head(df[time_col].nunique() * top_n)


def aggregate(df):
    """Utility function for applying the get_top_n_by_time() function to a DataFrame and returning
    the outputs in a dictionary format.

    Args:
        df (pd.DataFrame): DataFrame containing pedestrian counts.

    Returns:
        dict: Dictionary with keys as what was calculated and values as the respective DataFrame.
    """

    daily_all, daily_10 = get_top_n_by_time(df, "day")
    monthly_all, monthly_10 = get_top_n_by_time(df, "month")

    return {
        "top_all_daily": daily_all,
        "top_10_daily": daily_10,
        "monthly_all_daily": monthly_all,
        "monthly_10_daily": monthly_10,
    }
