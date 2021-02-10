# pdrepr

pdrepr takes a pandas DataFrame as input, and *attempts* to output a string that, when passed to Python's built-in `eval()`, will reproduce the original DataFrame.

![Testing and linting](https://github.com/danhje/pdrepr/workflows/Test%20And%20Lint/badge.svg)
[![codecov](https://codecov.io/gh/danhje/pdrepr/branch/master/graph/badge.svg)](https://codecov.io/gh/danhje/pdrepr)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/danhje/pdrepr?include_prereleases)
![PyPI](https://img.shields.io/pypi/v/pdrepr)

## Motivation

I was tired of having to manually construct DataFrames to be used in testing, especially the reference object to be compared with the resulting DF. With this package, such a code snipped can be created from the resulting DF.


## Installation

Using poetry:

```shell
poetry add pdrepr
```

Using pipenv:

```shell
pipenv install pdrepr
```

Using pip:

```shell
pip install pdrepr
```
