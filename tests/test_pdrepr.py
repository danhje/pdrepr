import pytest
from pdrepr import pdrepr
import datetime
import pandas as pd
import numpy as np
from contextlib import contextmanager
import mock


@contextmanager
def rename_pd():
    global pd
    orig = pd
    del pd
    yield orig
    pd = orig


def test_pdrepr_minimal():
    original = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    string_representation = pdrepr(original)
    recreated = eval(string_representation)
    pd.testing.assert_frame_equal(original, recreated)


def test_pdrepr_strings():
    original = pd.DataFrame({"col1": ["1", "2", "3"], "col2": ["4", "5", "6"]})
    string_representation = pdrepr(original)
    recreated = eval(string_representation)
    pd.testing.assert_frame_equal(original, recreated)


def test_pdrepr_floats():
    original = pd.DataFrame({"col1": [1., 2., 3.], "col2": [42., 0.00, 3.14159265359]})
    string_representation = pdrepr(original)
    recreated = eval(string_representation)
    pd.testing.assert_frame_equal(original, recreated)


@pytest.mark.xfail
def test_pdrepr_datetimes():
    first_date = datetime.datetime.now()
    date_range = [first_date + datetime.timedelta(days=5-d) for d in range(5)]
    original = pd.DataFrame({"col1": date_range, "col2": date_range})
    string_representation = pdrepr(original)
    recreated = eval(string_representation)
    pd.testing.assert_frame_equal(original, recreated)


def test_pdrepr_other():
    class MyClass:
        def __init__(self, attr):
            self._attr = attr
        def __repr__(self):
            return f"MyClass({self._attr})"
        def __eq__(self, other):
            return repr(self) == repr(other)
    objects = [MyClass(d) for d in range(5)]
    original = pd.DataFrame({"col1": objects, "col2": objects})
    string_representation = pdrepr(original)
    recreated = eval(string_representation)
    pd.testing.assert_frame_equal(original, recreated)


@pytest.mark.xfail
def test_pdrepr_nans():
    original = pd.DataFrame({"col1": [1, 2, pd.NA], "col2": [pd.NA, pd.NA, pd.NA]})
    string_representation = pdrepr(original)
    recreated = eval(string_representation)
    pd.testing.assert_frame_equal(original, recreated)


def test_pdrepr_custom_row_index():
    original = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]}).set_index("col1")
    string_representation = pdrepr(original)
    recreated = eval(string_representation)
    pd.testing.assert_frame_equal(original, recreated)


def test_pdrepr_multiindex_rows():
    original = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6], "col3": [7, 8, 9]})
    original.set_index(["col1", "col2"], inplace=True)
    string_representation = pdrepr(original)
    recreated = eval(string_representation)
    pd.testing.assert_frame_equal(original, recreated)


def test_pdrepr_multiindex_columns():
    original = pd.Series(np.random.rand(3), index=["a", "b", "c"]).to_frame().T
    original.columns = pd.MultiIndex.from_product([["top"], original.columns])
    string_representation = pdrepr(original)
    recreated = eval(string_representation)
    pd.testing.assert_frame_equal(original, recreated)


@pytest.mark.xfail
def test_pdrepr_atypical_import_alias():
    with rename_pd() as pand:
        with pytest.raises(NameError):  # "pd" is now not a valid alias for pandas, only "pand" is.
            pd.NA
        original = pand.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
        string_representation = pdrepr(original)
        recreated = eval(string_representation)
        pand.testing.assert_frame_equal(original, recreated)
    pd.NA  # Verifies that the "pd" alias is restored
