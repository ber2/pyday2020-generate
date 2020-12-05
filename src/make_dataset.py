import pandas as pd

from generators import (
    generate_voter_ids,
    generate_timestamps,
    generate_regions,
    generate_votes,
)


def make_dataframe(length: int) -> pd.DataFrame:

    result = pd.DataFrame()
    result["timestamp"] = generate_timestamps(length)
    result["id"] = generate_voter_ids(length)
    result["region"] = generate_regions(length)
    result["vote"] = generate_votes(length)

    return result
