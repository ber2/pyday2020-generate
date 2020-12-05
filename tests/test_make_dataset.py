import os
from unittest import mock

from hypothesis import given
import hypothesis.strategies as st

import pandas as pd

from make_dataset import make_dataframe, generate_one_file, main


@given(st.integers(min_value=0, max_value=1000))
def test_dataframe_shape(length):
    assert make_dataframe(length).shape == (length, 4)


@given(st.integers(min_value=0, max_value=1000))
def test_dataframe_columns(length):
    assert list(make_dataframe(length).columns) == ["timestamp", "id", "region", "vote"]


def test_make_one_file():
    if os.path.exists("tests/test_file_3.csv"):
        os.remove("tests/test_file_3.csv")

    generate_one_file(3, "tests/test_file")

    assert os.path.exists("tests/test_file_3.csv")

    result = pd.read_csv("tests/test_file_3.csv")
    assert result.shape == (2000000, 4)
    assert list(result.columns) == ["timestamp", "id", "region", "vote"]

    os.remove("tests/test_file_3.csv")


def test_main():

    with mock.patch("make_dataset.generate_one_file") as gen:
        main()
        assert gen.call_count == 72
