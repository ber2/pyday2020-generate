import uuid

import pandas as pd


def generate_voter_ids(length: int) -> pd.Series:
    return pd.Series([str(uuid.uuid1()) for _ in range(length)], dtype="object")
