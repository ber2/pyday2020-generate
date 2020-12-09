# PyDay 2020: Vote generator

This repository contains the code used to generate an example dataset for my talk at the [Barcelona PyDay
2020](https://pybcn.org/events/pyday_bcn/pyday_bcn_2020/). 

You may find the talk details at the sister repository, available
[here](https://github.com/ber2/pyday2020-counting-votes-with-dask). This includes notebook examples
and links to the talk video and slides.

## Installation

I have used [poetry](https://python-poetry.org/) to specify dependencies. After cloning the
repository, use a fresh python 3.9 virtual environment.  In order to install the dependencies, do:

```bash
poetry install --no-dev
```

## Usage

The main entrypoint is [`src/make_dataset.py`](src/make_dataset.py). You can pass arguments in order
to choose some dataset details. After installing dependencies:

```bash
cd src
python make_dataset.py --help
```

will provide the following description.

```bash
Usage: make_dataset.py [OPTIONS]

  Generate artificial examples of votes

Options:
  -r, --n-rows INTEGER      Number of rows per file
  -f, --n-files INTEGER     Total number of files to generate
  -o, --output-prefix TEXT  Output prefix for the result files
  --help                    Show this message and exit.
```

So, for example, the following call will deliver 5 files containing 200 rows each, written in the
form `"votes_*.csv"`.

```bash
python make_dataset.py -r 200 -f 5 -o "votes_"
```

__Warning__: This code is not optimized and generating the dataset in the talk (60 files having 2M
rows each) is slow. If you decide to generate large amounts of data, you will either need to take
time or parallelize the main loop.


## Testing

You will need to install development dependencies. By using poetry, run:
```bash
poetry install
```

We have used property-based testing in order to ensure that the samples generated match expected
distributions. The framework used is [hypothesis](https://hypothesis.readthedocs.io/en/latest/).
Tests have relaxed timeouts and take long to run. For this reason, there are several testing profiles
available, and we use `pytest-xdist` in order to parallelize the test suite.

So, in order to have a quick test run without running on many CPUs, try:
```bash
pytest -v --hypothesis-profile=debug
```

If you wish to develop code and have a reasonable number of checks, try:
```bash
pytest -v -n 10 --hypothesis-profile=dev
```

Finally, the following will run more extensive examples:
```bash
pytest -v -n 10
```

## Development

If you have any questions or miss any features, feel free to open an issue
[here](https://github.com/ber2/pyday2020-counting-votes-with-dask/issues). 

Similarly, feel free to fork the repository and submit pull requests; I am happy to consider changes
and improvements!

