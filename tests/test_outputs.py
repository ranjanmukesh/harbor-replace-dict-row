import numpy as np
import pytest
from pandas import (
    DataFrame,
    Series,
    Timestamp,
)
import pandas._testing as tm
from pandas.tests.copy_view.util import get_array



@pytest.mark.parametrize(
    "to_replace, value",
    [
        # matching pair before a no-op pair
        ([2, 200], [20, 10]),
        # every pair matches
        ([2, 3], [20, 30]),
        # more than two pairs
        ([2, 200, 201], [20, 10, 10]),
    ],
)
def test_replace_listlike_inplace_keeps_tracking_copies(to_replace, value):
    # GH#58966 replace_list dropped the block's self-reference once it had
    #  copied, so views taken afterwards were no longer copy-on-write protected
    df = DataFrame({"a": [1, 2, 3], "b": [1, 2, 3]})
    view = df[:]
    df.replace(to_replace, value, inplace=True)
    # the copy triggered by ``view`` must not have leaked the original values
    tm.assert_frame_equal(view, DataFrame({"a": [1, 2, 3], "b": [1, 2, 3]}))

    df_orig = df.copy()
    view2 = df[:]
    df.iloc[0, 0] = 999
    assert not np.shares_memory(get_array(df, "a"), get_array(view2, "a"))
    tm.assert_frame_equal(view2, df_orig)
