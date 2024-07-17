import re
import sys

import pandas as pd

from tools.csv_analyzer import analyze_data


def get_file_data() -> str:
    with open(sys.argv[1], "r") as f:
        data = f.read()
    return data


def main():
    regex = re.compile(
        r"(insert into )([\w]+)( values\()(\'.*\',\s? )*(\'.*\'\s?)\);", re.IGNORECASE
    )
    data = get_file_data()
    all_found = regex.finditer(data)
    n_cols = 0
    d = {}
    for i, found in enumerate(all_found):
        row = (found.group(4) + found.group(5)).split(",")
        if n_cols == 0 or len(d) == 0:
            n_cols = len(row)
            d = {f"col{c+1}": [] for c in range(n_cols)}
        for i, c in enumerate(row):
            d[f"col{i+1}"].append(c.strip().strip("'"))
    df = pd.DataFrame(d)
    # print(df.head())
    analyze_data(df)


if __name__ == "__main__":
    main()
