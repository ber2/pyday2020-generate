import datetime as dt
from pathlib import Path
import uuid

import numpy as np
import pandas as pd


def generate_voter_ids(length: int) -> pd.Series:
    return pd.Series([str(uuid.uuid1()) for _ in range(length)], dtype="object")


def generate_timestamps(length: int) -> pd.Series:
    if length == 0:
        return pd.Series(data=None, dtype="datetime64[ns]")
    date = dt.date(2020, 12, 10)
    hour_range = range(8, 21)

    hours = [dt.time(h) for h in np.random.choice(hour_range, size=length)]

    data = pd.DataFrame(hours)
    data["date"] = date
    data["hour"] = hours

    data["timestamp"] = data.apply(
        lambda row: pd.Timestamp.combine(row["date"], row["hour"]), axis=1
    )
    return data["timestamp"]


def generate_regions(length: int) -> pd.Series:

    data = pd.read_csv(
        Path(__file__).parent / "../data/region_data.csv", usecols=["region", "percent"]
    )

    values = np.random.choice(
        data.region.values, size=length, p=data.percent.values / data.percent.sum()
    )
    return pd.Series(data=values, dtype="object", name="region")


def generate_votes(length: int) -> pd.Series:

    values = np.random.choice(
        ["yellow", "red", "blue"], size=length, p=[0.01, 0.47, 0.52]
    )

    return pd.Series(data=values, dtype="object", name="vote")
