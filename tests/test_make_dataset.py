import os

import pytest
from hypothesis import given
import hypothesis.strategies as st

import pandas as pd

from make_dataset import generate_one_file, main


def test_make_one_file():
    if os.path.exists("tests/test_file_3.csv"):
        os.remove("tests/test_file_3.csv")

    generate_one_file(3, 200, "tests/test_file")

    assert os.path.exists("tests/test_file_3.csv")

    result = pd.read_csv("tests/test_file_3.csv")
    assert result.shape == (200, 4)
    assert list(result.columns) == ["timestamp", "id", "region", "vote"]

    os.remove("tests/test_file_3.csv")

