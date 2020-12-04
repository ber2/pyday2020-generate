import pytest
from hypothesis import given
import hypothesis.strategies as st

import pandas as pd

from generators import generate_voter_ids, generate_timestamps


@given(st.integers(min_value=0, max_value=2000))
def test_generated_as_many_ids_as_requested(length):
    assert generate_voter_ids(length).shape == (length,)


@given(st.integers(min_value=0, max_value=1200))
def test_generated_ids_have_proper_length(length):
    string_lengths = generate_voter_ids(length).apply(lambda x: len(x))
    assert all(uid_len == 36 for uid_len in string_lengths)


@given(st.integers(min_value=0, max_value=2000))
def test_generated_ids_have_no_repetitions(length):
    assert len(generate_voter_ids(length).drop_duplicates()) == length


@given(st.integers(min_value=0, max_value=2000))
def test_generated_as_many_timestamps_as_requested(length):
    assert generate_timestamps(length).shape == (length,)


@given(st.integers(min_value=0, max_value=2000))
def test_generated_timestamps_all_have_constant_date(length):
    dates = list(generate_timestamps(length).dt.date.unique())
    assert not dates or dates == [pd.Timestamp("2020-12-10")]


@given(st.integers(min_value=0, max_value=2000))
def test_generated_timestamps_all_have_hours_within_range(length):
    hours = generate_timestamps(length).dt.hour.unique()
    assert all(hour in range(8, 21) for hour in hours)
