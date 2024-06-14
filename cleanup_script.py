import pandas as pd
import re

# Read the json data into a dataframe
df = pd.DataFrame(pd.read_json("assets/pyramid_data.json"))

# Remove leading/trailing whitespace from the elements of all columns with string values
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

# Convert the column names into snake case
def normalize_labels(name):
    new_name = name.strip()
    new_name = new_name.lower()
    new_name = re.sub(r' \(.*\)', r'', new_name)
    new_name = new_name.replace(" ", "_")
    new_name = new_name.replace("/", "_or_")
    return new_name
df.columns = df.columns.map(lambda x: normalize_labels(x))

# Export dataset to json
df.to_json("assets/normalized_pyramid_data.json", orient="columns", indent=2)