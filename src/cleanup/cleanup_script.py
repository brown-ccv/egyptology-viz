import pandas as pd
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
    new_name = re.sub(r' \(.*\)', r'', new_name)
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
        '-n',
        '--normcols',
        '--normalize-columns',
        nargs='*',
        help="Normalize column names"
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
        df.to_csv(outpath)
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