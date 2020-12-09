import time
from multiprocessing import Pool

import click

from generators import (
    generate_votes
)


def generate_one_file(index: int, n_rows: int, path_prefix: str) -> None:
    path = f"{path_prefix}_{index}.csv"
    tic = time.time()
    generate_votes(n_rows).to_csv(path, index=False)
    tac = time.time()
    print(f"Generated {n_rows} rows in file: {path}\t{tac - tic} seconds")


@click.command(help="Generate artificial examples of votes")
@click.option(
    "--n-rows",
    "-r",
    default=2000000,
    help="Number of rows per file"
)
@click.option(
    "--n-files",
    "-f",
    default=60,
    help="Total number of files to generate"
)
@click.option(
    "--output-prefix",
    "-o",
    default="../data/votes",
    help="Output prefix for the result files"
)
def main(n_rows: int, n_files: int, output_prefix: str) -> None:

    print(f"Will generate {n_files} files with {n_rows} rows each")

    for index in range(n_files):
        generate_one_file(index, n_rows, output_prefix)

    print("All done")


if __name__ == "__main__":
    main()
