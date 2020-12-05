import time
from multiprocessing import Pool

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


def generate_one_file(index: int, path_pattern: str) -> None:
    path = path_pattern + f"_{index}.csv"
    tic = time.time()
    make_dataframe(2000000).to_csv(path, index=False)
    tac = time.time()
    print(f"Generated 2M rows in file: {index}\t{tac - tic} seconds")


def main() -> None:

    print("Will generate 72 files with 2M rows each")
    for index in range(72):
        generate_one_file(index, "../data/votes")
    print("All done")


if __name__ == "__main__":
    main()
