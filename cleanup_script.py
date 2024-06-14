import pandas as pd
import re
import argparse

def remove_whitespace(df, columns=[]):
    """
    Remove leading/trailing whitespace from the elements of all columns with 
    string values
    """
    
    if len(columns) != 0:
        df = df[columns]    
    
    return df.map(lambda x: x.strip() if isinstance(x, str) else x)

    
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
        col_names.map(lambda x: normalize_column_name(x))
    else:
        for name in columns:
            col_names[col_names.index(name)] = normalize_column_name(name)

    return col_names

def main():
    description = __doc__
    parser = argparse.ArgumentParser(description=description)

    # Read the json data into a dataframe
    #df = pd.DataFrame(pd.read_excel("../assets/Condensed Pyramid Data copy (6-14-2024).xlsx"))
    df = pd.DataFrame(pd.read_json("assets/raw_pyramid_data.json"))

    # Figure out which functions to execute based on the arguments
    # These function calls are here to reserve the functionality of the 
    # previous version for now.
    remove_whitespace(df)
    normalize_columns(df)

    # Export dataset to json
    df.to_json("assets/normalized_pyramid_data.json", orient="columns", indent=2)

if __name__ == "__main__":
    main()