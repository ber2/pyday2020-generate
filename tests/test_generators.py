import pytest
from hypothesis import given
import hypothesis.strategies as st

import numpy as np
import pandas as pd

from generators import (
    generate_voter_ids,
    generate_timestamps,
    generate_regions,
    generate_votes,
)


@given(st.integers(min_value=0, max_value=2000))
def test_generated_as_many_ids_as_requested(length):
    assert generate_voter_ids(length).shape == (length,)


@given(st.integers(min_value=0, max_value=1200))
def test_ids_have_proper_length(length):
    string_lengths = generate_voter_ids(length).apply(lambda x: len(x))
    assert all(uid_len == 36 for uid_len in string_lengths)


@given(st.integers(min_value=0, max_value=2000))
def test_ids_have_no_repetitions(length):
    assert len(generate_voter_ids(length).drop_duplicates()) == length


@given(st.integers(min_value=0, max_value=2000))
def test_generated_as_many_timestamps_as_requested(length):
    assert generate_timestamps(length).shape == (length,)


@given(st.integers(min_value=0, max_value=2000))
def test_timestamps_have_constant_date(length):
    dates = list(generate_timestamps(length).dt.date.unique())
    assert not dates or dates == [pd.Timestamp("2020-12-10")]


@given(st.integers(min_value=0, max_value=2000))
def test_timestamps_have_hours_within_range(length):
    hours = generate_timestamps(length).dt.hour.unique()
    assert all(hour in range(8, 21) for hour in hours)


@given(st.integers(min_value=0, max_value=2000))
def test_generated_as_many_regions_as_requested(length):
    assert generate_regions(length).shape == (length,)


@given(st.integers(min_value=1000, max_value=4000))
def test_all_regions_appear(length):
    expected_regions = set(pd.read_csv("data/region_data.csv").region)
    actual_regions = set(generate_regions(length).unique())
    assert expected_regions == actual_regions


@given(st.integers(min_value=40000, max_value=80000))
def test_regions_distribution(length):
    expected = pd.read_csv("data/region_data.csv", usecols=["region", "percent"])
    regions = pd.DataFrame(generate_regions(length))
    regions["cnt"] = 1
    actual = (regions.groupby("region").agg("count") / length).reset_index()

    joined = pd.merge(expected, actual, on="region")
    assert joined.shape == (51, 3)

    joined["diff"] = np.abs(joined["percent"] - joined["cnt"])
    assert joined["diff"].max() < 0.006


@given(st.integers(min_value=0, max_value=1000))
def test_generated_as_many_votes_as_requested(length):
    assert generate_votes(length).shape == (length,)


@given(st.integers(min_value=1000, max_value=2000))
def test_votes_have_three_colours(length):
    expected = {"yellow", "blue", "red"}
    actual = set(generate_votes(length).unique())
    assert expected == actual


@given(st.integers(min_value=40000, max_value=80000))
def test_votes_distribution(length):
    expected = pd.DataFrame(
        {"vote": ["yellow", "red", "blue"], "ratio": [0.01, 0.47, 0.52]}
    )

    votes = pd.DataFrame(generate_votes(length))
    votes["cnt"] = 1
    actual = (votes.groupby("vote").agg("count") / length).reset_index()

    joined = pd.merge(expected, actual, on="vote")
    assert joined.shape == (3, 3)

    joined["diff"] = np.abs(joined["ratio"] - joined["cnt"])
    assert joined["diff"].max() < 0.005
