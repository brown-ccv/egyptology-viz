import sys
from cleanup_script import *
# Awaiting merge of the package branch before fixing this test script

def test_normcols_default():
    df = pd.DataFrame({'A (or something)': [1, 2, 3], 'B and C/D': [3, 4, 5]})
    desired = pd.Index(['a', 'b_and_c_or_d'])
    assert normalize_columns(df).columns.equals(desired)

def test_normcols_selective():
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [3, 4, 5]})
    desired = pd.Index(['A', 'b'])
    assert normalize_columns(df, ['B']).columns.equals(desired)