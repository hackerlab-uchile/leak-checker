import json
import os
import sys
from datetime import datetime
from hashlib import sha256
from typing import Any

import numpy as np
import pandas as pd
from core.database import get_db
from models.breach import Breach
from models.data_leak import DataLeak
from models.data_type import DataType
from models.password import Password
from repositories.data_type_repository import (
    get_all_data_types,
    get_all_data_types_in_name_list,
    get_only_key_types,
)
from repositories.password_repository import add_or_create_all_passwords
from schemas.breaches import BreachCreate
from sqlalchemy.orm import Session


def valid_file_type() -> bool:
    if len(sys.argv) < 2 or sys.argv[1].lower() not in ["upload", "json", "csv"]:
        return False
    return True


def valid_file_path() -> bool:
    if len(sys.argv) < 3 or not os.path.isfile(sys.argv[2]):
        return False
    return True


def valid_params() -> bool:
    if len(sys.argv) != 3:
        print("Usage:\npython data-uploader.py <file-type> <file-path>")
        return False
    if not valid_file_type() or not valid_file_path():
        return False
    return True


def display_data(data: dict):
    for c in data.keys():
        print(f"{c}: {data[c][:5]}")


def handle_csv_file(f_path: str):
    sep = input("Please enter columns separator: ")
    with open(f_path, "r") as file:
        all_rows = file.read().strip().split("\n")
    sample = all_rows[0].split(sep, maxsplit=1)
    n_cols = len(sample)
    print(f"{n_cols} columns have been detected.")
    print("Please enter the names of the columns in order:")
    columns: list[str] = []
    data = {}
    for i in range(n_cols):
        col_name = input(f"Column number {i+1}: ")
        columns.append(col_name)
        data[col_name] = []
    for row in all_rows:
        values = row.split(sep)
        for i, c in enumerate(columns):
            # value = sha256(values[i].encode("UTF-8")).hexdigest()
            value = values[i]
            # if c == "password":
            #     value = sha256(values[i].encode("UTF-8")).hexdigest()
            data[c].append(value)
    display_data(data)
    return data


def valid_upload_file(data: dict) -> bool:
    breach = data.get("breach")
    error_msg = ""
    if breach is None:
        error_msg += "Invalid Upload File: Must have a 'breach' key\n"

    description = data.get("breach")
    if description is None:
        data["description"] = ""

    data_path = data.get("data_path")
    if data_path is None:
        error_msg += "Invalid Upload File: Must have a 'data_path' key\n"

    file_type = data.get("file_type")
    if file_type is None or file_type not in ["json", "csv"]:
        error_msg += "Invalid Upload File: Must have a 'file_type' key\n"

    if error_msg:
        print(error_msg)
    return error_msg == ""


def handle_upload_file(f_path: str) -> tuple[Any, Any]:
    with open(f_path, "r") as file:
        upload_data = json.load(file)

    if valid_upload_file(upload_data):
        data_leak = handle_csv_file(upload_data["data_path"])
        # display_data(upload_data)
        display_data(data_leak)
        return upload_data, data_leak
    return None, None


def save_passwords(db: Session, pass_list: list[str]):
    hash_list = list(map(lambda x: sha256(x.encode("UTF-8")).hexdigest(), pass_list))
    pass_count = {}
    for p in hash_list:
        if pass_count.get(p):
            pass_count[p] += 1
        else:
            pass_count[p] = 1
    model_list = [Password(hash_password=p, count=c) for p, c in pass_count.items()]
    add_or_create_all_passwords(db, model_list)


def found_or_not_with(x: str | float):
    if not isinstance(x, str):
        print(f"Este dato {x}, no es string. Es {type(x)}")
    return x != np.nan


def data_cleanup(df: pd.DataFrame, session: Session, breach: Breach) -> list[DataLeak]:
    all_types = get_all_data_types(db=session)
    types_by_name: dict[str, DataType] = {
        data_type.name: data_type for data_type in all_types
    }

    all_values_to_add: list[DataLeak] = []
    print("Preparing data...")
    for dtype in get_only_key_types(
        db=session
    ):  # Iteramos por cada 'llave' (email, phone, rut)
        if dtype.name not in df.columns:  # Si la llave NO existe, la saltamos
            continue
        # 1. Hacemos un merge de las filas repetidas que le falten datos
        df.replace("", np.nan, inplace=True)
        tidy_df = df.groupby(dtype.name).agg(aggregate_non_null).reset_index()  # type: ignore

        # 2. Obtenemos todas las columnas, excepto la de la llave
        tidy_df.loc[:, tidy_df.columns != dtype.name] = ~tidy_df.loc[
            :, tidy_df.columns != dtype.name
        ].isnull()

        data_dic_list: list = tidy_df.to_dict("records")
        all_values = map(
            lambda x: get_value_model(dtype, x, types_by_name, breach),
            data_dic_list,
        )
        all_values_to_add += all_values

    return all_values_to_add


def get_value_model(
    key_type: DataType, d: dict, types_by_name: dict, breach: Breach
) -> DataLeak:
    value = d.get(key_type.name)
    hash_value = sha256(value.encode("UTF-8")).hexdigest()  # type: ignore
    # dl = DataLeak(hash_value=d.get(key_type.dtype))
    dl = DataLeak(hash_value=hash_value)
    dl.data_type = key_type
    dl.breach_found = breach
    found_with = []
    for k, v in d.items():
        if v is True:
            found_with.append(types_by_name.get(k))
    dl.found_with = found_with
    return dl


def save_breach_info(
    session: Session, upload_data: dict, data_types_breached: list[str]
) -> Breach:
    """Save all info related to a Breach"""
    # 1. Estructuramos el breach
    breach = {
        "name": upload_data["breach"],
        "description": upload_data["description"],
        "breach_date": datetime.strptime(upload_data["breach_date"], "%Y-%m-%d"),
        "confirmed": True,
        "is_sensitive": True,
    }
    # 2. Se crea el modelo Breach
    breach_scheme_to_create = BreachCreate(**breach)
    breach_to_create = Breach(**breach_scheme_to_create.model_dump())
    # 3. Agregamos al modelo el tipo de datos que se encontraron
    breached_data_types = get_all_data_types_in_name_list(
        db=session, names=list(data_types_breached)
    )
    breach_to_create.data_breached = breached_data_types
    # 4. Guardamos el breach
    session.add(breach_to_create)
    session.flush()
    return breach_to_create


def manage_using_pandas(upload_data, data_leak):
    """Manage a data leak upload using pandas"""
    # Get database session
    session = get_db().__next__()
    # Save Data Breach Info
    breach_created = save_breach_info(session, upload_data, data_leak.keys())
    df = pd.DataFrame(data_leak, columns=data_leak.keys(), dtype="str")
    # Add key values to DataLeak table
    values_to_add = data_cleanup(df, session, breach=breach_created)
    session.add_all(values_to_add)
    # If there are passwords, then we add them to the count
    if "password" in df.columns:
        pass_list = list(df["password"].dropna())
        save_passwords(db=session, pass_list=pass_list)
    # Commit database changes
    session.commit()


# Define custom aggregation function
def aggregate_non_null(series):
    non_null_values = series.dropna()
    if non_null_values.empty:
        return np.nan
    else:
        return non_null_values.iloc[0]


def main():
    if not valid_params():
        return
    f_type = sys.argv[1].lower()
    f_path = sys.argv[2].lower()
    if f_type == "upload":
        upload_data, data_leak = handle_upload_file(f_path)
        if upload_data is None or data_leak is None:
            return 1
        manage_using_pandas(upload_data, data_leak)


if __name__ == "__main__":
    main()
