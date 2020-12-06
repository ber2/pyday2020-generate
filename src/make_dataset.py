import time
from multiprocessing import Pool

import pandas as pd

from generators import (
    generate_votes
)


def generate_one_file(index: int) -> None:
    path = f"../data/votes_{index}.csv"
    tic = time.time()
    generate_votes(2000000).to_csv(path, index=False)
    tac = time.time()
    print(f"Generated 2M rows in file: {index}\t{tac - tic} seconds")


def main() -> None:

    print("Will generate 72 files with 2M rows each")

    with Pool() as pl:
        pl.map(generate_one_file, list(range(72)))
    # for index in range(72):
        # generate_one_file(index, "../data/votes")
    print("All done")


if __name__ == "__main__":
    main()
