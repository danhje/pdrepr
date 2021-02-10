from pdrepr import pdrepr
import pandas as pd


def test_pdrepr_minimal():
    original_df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["num1", "num2", "num3"]})
    string_representation = pdrepr(original_df)
    recreated_df = eval(string_representation)
    pd.testing.assert_frame_equal(original_df, recreated_df)
