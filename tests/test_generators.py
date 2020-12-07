import pytest
from hypothesis import given, settings
import hypothesis.strategies as st

import numpy as np
import pandas as pd

from generators import (
    generate_votes,
    row_maker,
)


def test_row_keys():
    voting_machine = row_maker()
    row = voting_machine()
    assert list(row.keys()) == ["timestamp", "id", "region", "vote"]


@settings(deadline=None)
@given(st.integers(min_value=0, max_value=200))
def test_generated_as_many_votes_as_requested(length):
    votes = generate_votes(length)
    assert (length == 0 and votes.empty) or generate_votes(length).shape == (length, 4)


@settings(deadline=None)
@given(st.integers(min_value=0, max_value=200))
def test_votes_columns(length):

    data = generate_votes(length)
    assert (length == 0 and data.empty) or list(data.columns) == [
        "timestamp",
        "id",
        "region",
        "vote",
    ]


@settings(deadline=None)
@given(st.integers(min_value=1, max_value=200))
def test_id_lengths(length):
    string_lengths = generate_votes(length)["id"].apply(lambda x: len(x))
    assert all(uid_len == 36 for uid_len in string_lengths)


@settings(deadline=None)
@given(st.integers(min_value=1, max_value=200))
def test_ids_have_no_repetitions(length):
    assert generate_votes(length)["id"].drop_duplicates().shape[0] == length


@settings(deadline=None)
@given(st.integers(min_value=1, max_value=200))
def test_timestamps_have_constant_date(length):
    dates = list(generate_votes(length)["timestamp"].dt.date.unique())
    assert (length == 0 and not dates) or dates == [pd.Timestamp("2020-12-10")]


@settings(deadline=None)
@given(st.integers(min_value=1, max_value=200))
def test_timestamps_have_hours_within_range(length):
    hours = generate_votes(length)["timestamp"].dt.hour.unique()
    assert all(hour in range(8, 21) for hour in hours)


@settings(deadline=None)
@given(st.integers(min_value=1000, max_value=1400))
def test_all_regions_appear(length):
    expected_regions = set(pd.read_csv("data/region_data.csv").region)
    actual_regions = set(generate_votes(length)["region"].unique())
    assert expected_regions == actual_regions


@settings(deadline=None)
@given(st.integers(min_value=1000, max_value=1800))
def test_regions_distribution(length):
    expected = pd.read_csv("data/region_data.csv", usecols=["region", "percent"])
    regions = pd.DataFrame(generate_votes(length)["region"])
    regions["cnt"] = 1
    actual = (regions.groupby("region").agg("count") / length).reset_index()

    joined = pd.merge(expected, actual, on="region")
    assert joined.shape == (51, 3)

    joined["diff"] = np.abs(joined["percent"] - joined["cnt"])
    assert joined["diff"].max() < 0.05


@settings(deadline=None)
@given(st.integers(min_value=1000, max_value=1500))
def test_votes_have_three_colours(length):
    expected = {"yellow", "blue", "red"}
    actual = set(generate_votes(length)["vote"].unique())
    assert expected == actual


@settings(deadline=None)
@given(st.integers(min_value=1000, max_value=1500))
def test_timestamp_distribution_blue(length):
    colors = (
        pd.read_csv("data/region_data.csv", usecols=["region", "color"])
        .set_index("region")
        .color.to_dict()
    )

    votes = generate_votes(length)
    votes["color"] = votes["region"].apply(lambda x: colors[x])
    blue_votes = votes[votes["color"] == "blue"].copy()
    blue_votes["cnt"] = 1
    blue_votes["hour"] = blue_votes["timestamp"].dt.hour

    expected = pd.DataFrame(
        {
            "hour": list(range(8, 20)),
            "weight": np.concatenate([np.ones(9), 3 * np.ones(3)]) / 18,
        }
    )
    actual = (
        blue_votes.groupby("hour").cnt.agg("count") / blue_votes.shape[0]
    ).reset_index()

    joined = pd.merge(expected, actual, on="hour")
    joined["diff"] = np.abs(joined["weight"] - joined["cnt"])

    assert joined["diff"].max() < 0.05


@settings(deadline=None)
@given(st.integers(min_value=1000, max_value=1500))
def test_timestamp_distribution_red(length):
    colors = (
        pd.read_csv("data/region_data.csv", usecols=["region", "color"])
        .set_index("region")
        .color.to_dict()
    )

    votes = generate_votes(length)
    votes["color"] = votes["region"].apply(lambda x: colors[x])
    red_votes = votes[votes["color"] == "red"].copy()
    red_votes["cnt"] = 1
    red_votes["hour"] = red_votes["timestamp"].dt.hour

    expected = pd.DataFrame({"hour": list(range(8, 20)), "weight": np.ones(12) / 12})
    actual = (
        red_votes.groupby("hour").cnt.agg("count") / red_votes.shape[0]
    ).reset_index()

    joined = pd.merge(expected, actual, on="hour")
    joined["diff"] = np.abs(joined["weight"] - joined["cnt"])

    assert joined["diff"].max() < 0.05


@settings(deadline=None)
@given(st.integers(min_value=1000, max_value=1500))
def test_vote_distribution_blue(length):

    colors = (
        pd.read_csv("data/region_data.csv", usecols=["region", "color"])
        .set_index("region")
        .color.to_dict()
    )
    votes = generate_votes(length)
    votes["color"] = votes["region"].apply(lambda x: colors[x])
    blue_votes = votes[votes["color"] == "blue"].copy()
    blue_votes["cnt"] = 1

    expected = pd.DataFrame(
        {"vote": ["yellow", "red", "blue"], "weight": [0.01, 0.47, 0.52]}
    )
    actual = (
        blue_votes.groupby("vote").cnt.agg("count") / blue_votes.shape[0]
    ).reset_index()

    joined = pd.merge(expected, actual, on="vote")
    joined["diff"] = np.abs(joined["weight"] - joined["cnt"])

    assert joined["diff"].max() < 0.05


@settings(deadline=None)
@given(st.integers(min_value=1000, max_value=1500))
def test_vote_distribution_red(length):

    colors = (
        pd.read_csv("data/region_data.csv", usecols=["region", "color"])
        .set_index("region")
        .color.to_dict()
    )

    votes = generate_votes(length)
    votes["color"] = votes["region"].apply(lambda x: colors[x])
    red_votes = votes[votes["color"] == "red"].copy()
    red_votes["cnt"] = 1

    expected = pd.DataFrame(
        {"vote": ["yellow", "red", "blue"], "weight": [0.01, 0.54, 0.45]}
    )
    actual = (
        red_votes.groupby("vote").cnt.agg("count") / red_votes.shape[0]
    ).reset_index()

    joined = pd.merge(expected, actual, on="vote")
    joined["diff"] = np.abs(joined["weight"] - joined["cnt"])

    assert joined["diff"].max() < 0.05
