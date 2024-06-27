import pandas as pd
import numpy as np
import re
import argparse

def strip_if_str(s): 
    """
    Strip leading/trailing whitespace from a variable if it's a string,
    otherwise return it as is.
    """
    return s.strip() if isinstance(s, str) else s

def remove_whitespace(df, columns=[]):
    """
    Remove leading/trailing whitespace from the elements of all columns with 
    string values
    """
    
    if len(columns) == 0:
        df = df.map(strip_if_str)
    else:
        df[columns] = df[columns].map(strip_if_str)
    
    return df
    
def normalize_column_name(name):
    """
    Convert a single column name into snake case (like_this)
    """
    new_name = name.strip().lower()
    # This regex removes parentheticals completely
    new_name = re.sub(r' \(.*?\)', r'', new_name)
    new_name = new_name.replace(" ", "_")
    new_name = new_name.replace("/", "_or_")

    return new_name

def normalize_columns(df, columns=[]):
    """
    Convert columns names into snake case (like_this)
    """

    col_names = df.columns

    if len(columns) == 0:
        col_names = col_names.map(normalize_column_name)
    else:
        index_names = [normalize_column_name(name) if name in columns else name for name in col_names]
        col_names = pd.Index(index_names)
    
    df.columns = col_names

    return df

def yes_no_to_bool(df, columns=[]):
    """
    Convert 'Yes' and 'No' values to True and False.
    """

    KEY = {"Yes": True, "Yes?": True, "No": False, "No?": False, "unknown": False}

    if len(columns) == 0:
        df = df.replace(KEY).fillna(False)
    else:
        df[columns] = df[columns].replace(KEY).fillna(False)

    return df

def comma_years_to_float(elem):
    if pd.isna(elem) or elem.lower() == "unknown": return np.nan
    if isinstance(elem, float) or isinstance(elem, int): return elem
    
    if "less" in elem.lower():
        # Temporary because this is useless information that shouldn't even exist,
        # either provide months or nothing at all
        #return elem
        return np.nan

    try:
        elem = elem.replace(" ", "").split(",")
        # Comma separation
        if len(elem) == 2:
            span = float(elem[0]) + float(elem[1]) / 12
            return span
        # Comma absent, single integer
        elif len(elem) == 1:
            return float(elem[0])
        else:
            raise Exception("Unexpected format in comma separated years element")
    except Exception as e:
        print(repr(e))
        exit(1)

def convert_years_to_float(df, columns=[]):
    """
    Convert comma separated, numeric year format (years, months) to float
    """

    if len(columns) == 0: columns = df.columns

    df[columns] = df[columns].map(comma_years_to_float)

    return df

def normalize_numeric_elem(elem):
    """
    Normalize an element to be castable as an int or a float
    """

    if pd.isna(elem) or isinstance(elem, int) or isinstance(elem, float): return elem

    key = ['unknown', 'unfinished']
    if elem in key: return np.nan

    # Eliminate leading/trailing whitespace and parentheticals
    # NOTE: Cells with multiple numeric values retain all values. 
    # They need to decide on a single one, but that's how it works for now...
    elem = elem.strip()
    return re.sub(r' \(.*?\)', r'', elem).replace("?", "")

def normalize_numeric_col(df, columns=[]):
    """
    Normalize a column intended to hold numeric values by converting strings 
    to either ints or floats.
    """

    if len(columns) == 0: columns = df.columns

    df[columns] = df[columns].map(normalize_numeric_elem)

    return df


def main():
    description = __doc__
    parser = argparse.ArgumentParser(description=description)

    # Add arguments
    parser.add_argument(
        '-i',
        '--input',
        help="The name of the input file",
        required=True
    )
    parser.add_argument(
        "-o",
        '--output',
        help="The name of the output file",
    )
    parser.add_argument(
        '-w',
        '--removews',
        '--remove-whitespace',
        nargs='*',
        help="Remove whitespace from string elements"
    )
    parser.add_argument(
        '-c',
        '--normcols',
        '--normalize-columns',
        nargs='*',
        help="Normalize column names"
    )
    parser.add_argument(
        '-b',
        '--tobool',
        nargs='*',
        help="Convert Yes/No values to boolean True/False"
    )
    parser.add_argument(
        '-y',
        '--yearstof',
        nargs='*',
        help="Convert comma separated years (years, months) to float"
    )
    parser.add_argument(
        '-n',
        '--normnum',
        nargs='*',
        help='Normalize numeric columns'
    )
    parser.add_argument(
        '-d',
        '--dropblank',
        nargs=1,
        help='Drop blank rows (identified by NA values in the given column)'
    )

    args = parser.parse_args()

    # Read the data into a dataframe
    # Supported file types: csv, json
    intype = args.input.split(".")
    if len(intype) < 2:
        raise Exception("File name missing extension")
    intype = intype[-1].lower()

    if intype == "json":
        df = pd.read_json(args.input)
    elif intype == "csv":
        df = pd.read_csv(args.input)
    else:
        raise Exception("Unsupported input file type or file name missing extension. Supported file types: csv, json")

    # Execute cleanup functions based on command line arguments
    if args.removews != None:
        df = remove_whitespace(df, args.removews)
    if args.tobool != None:
        df = yes_no_to_bool(df, args.tobool)
    if args.yearstof != None:
        df = convert_years_to_float(df, args.yearstof)
    if args.normnum != None:
        df = normalize_numeric_col(df, args.normnum)
    if args.dropblank:
        df = df.dropna(subset=args.dropblank)
    if args.normcols != None:
        df = normalize_columns(df, args.normcols)

    # Export dataset
    # Supported file types: csv, json
    outpath = args.output if args.output else "out.json"
    outtype = outpath.split(".")
    if len(intype) < 2:
        raise Exception("File name missing extension")
    outtype = outtype[-1].lower()

    if outtype == "json":
        df.to_json(outpath, orient="columns", indent=2)
    elif outtype == "csv":
        df.to_csv(outpath, index=False, header=True)
    else:
        raise Exception("Unsupported output file type or file name missing extension. Supported file types: csv, json")

if __name__ == "__main__":
    main()

''' Tests for pytest '''
def test_normcols_default():
    df = pd.DataFrame({'A (or something)': [1, 2, 3], 'B and C/D': [3, 4, 5]})
    desired = pd.Index(['a', 'b_and_c_or_d'])
    assert normalize_columns(df).columns.equals(desired)

def test_normcols_selective():
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [3, 4, 5]})
    desired = pd.Index(['A', 'b'])
    assert normalize_columns(df, ['B']).columns.equals(desired)