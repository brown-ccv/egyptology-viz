import pandas as pd
import re
import argparse

def remove_whitespace(df, columns=[]):
    """
    Remove leading/trailing whitespace from the elements of all columns with 
    string values
    """
    
    if len(columns) == 0:
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    else:
        df[columns].map(lambda x: x.strip() if isinstance(x, str) else x)
    
    return df
    
def normalize_column_name(name):
    """
    Convert a single column name into snake case (like_this)
    """
    new_name = name.strip()
    new_name = new_name.lower()
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
        col_names = col_names.map(lambda x: normalize_column_name(x))
    else:
        #col_names = col_names[col_names.index(name)] = normalize_column_name(name)
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
        '--in',
        '--inname',
        help="The name of the input file",
        required=True
    )
    parser.add_argument(
        "-o",
        '--out',
        '--outname',
        help="The name of the output file",
    )
    parser.add_argument(
        '-rw',
        '--removews',
        '--remove_whitespace',
        nargs='*'
    )
    parser.add_argument(
        '-nc',
        '--normcols',
        '--normalize_columns',
        nargs='*'
    )

    args = parser.parse_args()

    # Read the json data into a dataframe
    #df = pd.DataFrame(pd.read_excel("../assets/Condensed Pyramid Data copy (6-14-2024).xlsx"))
    df = pd.DataFrame(pd.read_json("assets/raw_pyramid_data.json"))

    # Execute cleanup functions based on command line arguments
    if args.removews != None:
        df = remove_whitespace(df, args.removews)
    if args.normcols != None:
        df = normalize_columns(df, args.normcols)

    # Export dataset to json
    outpath = args.out if args.out != None else "out.json"
    df.to_json(outpath, orient="columns", indent=2)

if __name__ == "__main__":
    main()