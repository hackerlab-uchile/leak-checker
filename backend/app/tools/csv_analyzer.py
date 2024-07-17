import re
import sys

import pandas as pd

from tools.data_checker import DataChecker, DataType

data_checkers = [
    DataChecker(DataType.EMAIL, regex_list=[r"^[\w\-\.]+\@([\w\-]+\.)+[\w\-]{2,4}$"]),
    DataChecker(
        DataType.PHONE,
        regex_list=[
            r"^(\+?56)?(\s*)9(\s*)?[98765432](\d{3})(\s*)?(\d{4})$",
            r"^(\+?56)?(\s*)?(2|\d{2})(\s*)?[98765432](\d{3})(\s*)(\d{4})$",
        ],
    ),
    DataChecker(DataType.RUT, regex_list=[r"^([1-9]{1,3})(\.?\d{3})*[\-\s]?([\dkK])$"]),
    DataChecker(
        DataType.HASH,
        regex_list=[r"^([0-9a-f]{128})|([0-9a-f]{64})|([0-9a-f]{40})|([0-9a-f]{32})$"],
    ),
    DataChecker(
        DataType.IP_ADDR,
        regex_list=[r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$"],
    ),
    DataChecker(
        DataType.CREDIT_CARD,
        regex_list=[
            r"^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$"
        ],
        sanitize_func=lambda x: re.sub(r"\D", "", x),
    ),
    DataChecker(
        DataType.DATE,
        regex_list=[
            r"^(\d){4}[^\n](\d){2}(\d){2}$",
            r"^(\d){2}[^\n]{1}(\d){2}[^\n]{1}(\d){4}$",
        ],
    ),
    DataChecker(
        DataType.NUMERIC,
        regex_list=[r"^\d+$"],
    ),
]


def identify_data_type(sample: pd.Series) -> tuple[DataType, dict[DataType, list]]:
    sorted_data: dict[DataType, list[str]] = {dc.dtype: [] for dc in data_checkers}
    results = {dc.dtype: 0 for dc in data_checkers}

    sorted_data[DataType.STRING] = []
    results[DataType.STRING] = 0
    for value in sample:
        try:
            has_match = False
            for dc in data_checkers:
                if dc.match(value):
                    has_match = True
                    sorted_data[dc.dtype].append(value)
                    results[dc.dtype] += 1
            if not has_match:
                sorted_data[DataType.STRING] += [value]
                results[DataType.STRING] += 1
        except TypeError:  # nan values
            # print(f"ERROR: {value} of type: {type(value)} is not string")
            continue
    return max(results, key=results.get), sorted_data  # type: ignore


def get_file_info(delimiter=":") -> pd.DataFrame:
    with open(sys.argv[1], "r") as f:
        all_lines = f.read().strip().split("\n")
    n_cols = len(all_lines[0].split(delimiter))
    d: dict[str, list] = {f"col{i+1}": [] for i in range(n_cols)}
    for line in all_lines:
        for i, data in enumerate(line.split(delimiter, maxsplit=n_cols - 1)):
            d[f"col{i+1}"].append(data.strip())
    return pd.DataFrame(data=d)


def analyze_data(df: pd.DataFrame):
    total_rows = len(df)
    for col in range(len(df.columns)):
        data_type, results = identify_data_type(df.iloc[:, col])
        print(f"\nColumn {col} -> {data_type}")
        for dtype in DataType:
            n_r = len(results[dtype])
            if n_r > 0:
                print(f"{dtype} : {n_r} ({'{:.2f}'.format(100 * n_r / total_rows)}%)")
        # if col == 0:
        #     print(f"{DataType.RUT}: {results[DataType.RUT][:5]}")
        # if col == 1:
        #     print(f"{DataType.CREDIT_CARD}: {results[DataType.CREDIT_CARD][:15]}")


def main():
    df = get_file_info()
    analyze_data(df)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:\n\tpython -m tools.csv-analyzer.py <data-file>")
    else:
        main()
