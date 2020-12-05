from hypothesis import given
import hypothesis.strategies as st

from make_dataset import make_dataframe


@given(st.integers(min_value=0, max_value=1000))
def test_dataframe_shape(length):
    assert make_dataframe(length).shape == (length, 4)


@given(st.integers(min_value=0, max_value=1000))
def test_dataframe_columns(length):
    assert list(make_dataframe(length).columns) == ["timestamp", "id", "region", "vote"]
