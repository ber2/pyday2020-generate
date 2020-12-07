import datetime as dt
from pathlib import Path
import uuid
from typing import Dict, Any, List, Callable

import numpy as np
import pandas as pd


Row = Dict[str, Any]


def generate_timestamp(color: str) -> str:

    if color == "red":
        weights = np.ones(12)
    else:
        weights = np.concatenate([np.ones(9), 3 * np.ones(3)])

    weights_normalized = weights / weights.sum()

    date = dt.date(2020, 12, 10)
    hour = np.random.choice(range(8, 20), size=1, p=weights_normalized)[0]
    return pd.Timestamp.combine(date, dt.time(hour))


def generate_vote(color: str) -> str:

    if color == "red":
        weights = [0.01, 0.54, 0.45]
    else:
        weights = [0.01, 0.47, 0.52]

    return np.random.choice(["yellow", "red", "blue"], size=1, p=weights)[0]


def row_maker() -> Callable:

    data = pd.read_csv(
        Path(__file__).parent / "../data/region_data.csv",
        usecols=["region", "percent", "color"],
    )

    regions = data.region.values
    colors = data.set_index("region").color.to_dict()

    def generate() -> Row:
        region = np.random.choice(
            regions, size=1, p=data.percent.values / data.percent.sum()
        )[0]

        color = colors[region]
        return {
            "timestamp": generate_timestamp(color),
            "id": str(uuid.uuid1()),
            "region": region,
            "vote": generate_vote(color),
        }

    return generate


def generate_votes(length: int) -> pd.DataFrame:
    voting_machine = row_maker()
    return pd.DataFrame([voting_machine() for _ in range(length)])
