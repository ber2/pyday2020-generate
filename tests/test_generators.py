import pytest
from hypothesis import given
import hypothesis.strategies as st

from generators import generate_voter_ids


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
