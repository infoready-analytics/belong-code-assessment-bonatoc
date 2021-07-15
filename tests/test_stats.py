from pathlib import Path

from belong_code_assessment import stats, utils

this_dir = Path(__file__).parent.absolute()


def test_read_dataframe():
    df = utils.load_dataframe(this_dir.joinpath("test_stats.json"))
    assert len(df) == 1000


def test_top_n_by_day():
    df = utils.load_dataframe(this_dir.joinpath("test_stats.json"))

    # this data contains only values for Friday, Saturday, and Sunday
    top_all, top_n = stats.get_top_n_by_time(df, "day", top_n=5)

    # check the 5th result for Friday
    top_n_test_1 = top_n.loc[(top_n["day"] == "Friday") & (top_n["rank"] == 5)].iloc[0]
    assert top_n_test_1["sensor_name"] == "Flinders Street Station Underpass"

    # check the 2nd result for Sunday
    top_n_test_2 = top_n.loc[(top_n["day"] == "Sunday") & (top_n["rank"] == 2)].iloc[0]
    assert top_n_test_2["sensor_name"] == "New Quay"

    # check the 1st result for Saturday
    top_n_test_3 = top_n.loc[(top_n["day"] == "Saturday") & (top_n["rank"] == 1)].iloc[0]
    assert top_n_test_3["sensor_name"] == "Flinders St-Elizabeth St (East)"

    # check the 55th result for Saturday
    top_all_test_1 = top_all.loc[(top_all["day"] == "Saturday") & (top_all["rank"] == 55)].iloc[0]
    assert top_all_test_1["sensor_name"] == "Waterfront City"


def test_top_n_by_month():
    df = utils.load_dataframe(this_dir.joinpath("test_stats.json"))

    # this data contains only values for September and November
    top_all, top_n = stats.get_top_n_by_time(df, "month", top_n=5)

    # check the 1st result for September
    top_n_test_1 = top_n.loc[(top_n["month"] == "September") & (top_n["rank"] == 1)].iloc[0]
    assert top_n_test_1["sensor_name"] == "Birrarung Marr"

    # check the 5th result for November
    top_n_test_2 = top_n.loc[(top_n["month"] == "November") & (top_n["rank"] == 5)].iloc[0]
    assert top_n_test_2["sensor_name"] == "Princes Bridge"

    # check the 32nd result for November
    top_all_test_2 = top_all.loc[(top_all["month"] == "November") & (top_all["rank"] == 32)].iloc[0]
    assert top_all_test_2["sensor_name"] == "Lonsdale St-Spring St (West)"


def test_high_top_n():
    df = utils.load_dataframe(this_dir.joinpath("test_stats.json"))
    _, top_n = stats.get_top_n_by_time(df, "day", top_n=50)
    assert top_n is None
