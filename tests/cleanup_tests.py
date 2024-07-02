from cleanup.cleanup_script import *

def test_normcols_default():
    """
    Test column name normalization with the default settings (ie operate on all column names)
    """
    df = pd.DataFrame({'A (or something)': [1, 2, 3], 'B and C/D': [3, 4, 5]})
    desired = pd.Index(['a', 'b_and_c_or_d'])
    assert normalize_columns(df).columns.equals(desired)

def test_normcols_selective():
    """
    Test column name normalization on specific columns
    """
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [3, 4, 5]})
    desired = pd.Index(['A', 'b'])
    assert normalize_columns(df, ['B']).columns.equals(desired)

def test_remove_whitespace_default():
    """
    Test leading/trailing whitespace removal on values across all columns
    """
    df = pd.DataFrame({'A': ['  one', 'two  ', ' three  '],
                       'B': ['four', ' five five ', 'six']})
    desired = pd.DataFrame({'A': ['one', 'two', 'three'],
                            'B': ['four', 'five five', 'six']})
    assert remove_whitespace(df).equals(desired)

def test_remove_whitespace_selective():
    """
    Test leading/trailing whitespace removal on the values of specific columns
    """
    df = pd.DataFrame({'A': ['  one', 'two  ', ' three  '],
                       'B': ['four', ' five five ', 'six']})
    desired = pd.DataFrame({'A': ['one', 'two', 'three'],
                            'B': ['four', ' five five ', 'six']})
    assert remove_whitespace(df, ['A']).equals(desired)

def test_yes_no_bool_default():
    """
    Test the conversion of Yes/No values to True/False across all columns
    """
    df = pd.DataFrame({'A': ['Yes', 'Yes?', 'yes', 'yes?', 'Unknown'],
                       'B': ['No', 'No?', 'no', 'no?', 'unknown']})
    desired = pd.DataFrame({'A': [True, True, True, True, False],
                            'B': [False, False, False, False, False]})
    assert yes_no_to_bool(df).equals(desired)

def test_yes_no_bool_selective():
    """
    Test the conversion of Yes/No values to True/False on specific columns
    """
    df = pd.DataFrame({'A': ['Yes', 'Yes?', 'yes', 'yes?', 'Unknown'],
                       'B': ['No', 'No?', 'no', 'no?', 'unknown']})
    desired = pd.DataFrame({'A': [True, True, True, True, False],
                            'B': ['No', 'No?', 'no', 'no?', 'unknown']})
    assert yes_no_to_bool(df, ['A']).equals(desired)