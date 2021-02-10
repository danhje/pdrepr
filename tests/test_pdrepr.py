from pdrepr import pdrepr
import pandas as pd


def test_pdrepr_minimal():
    pdrepr(pd.DataFrame())
    assert True
