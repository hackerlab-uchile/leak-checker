import { DataLeak } from "@/models/Breach";
import { ColumnDef } from "@tanstack/react-table";
import { BsShieldExclamation } from "react-icons/bs";
import { IoWarningOutline } from "react-icons/io5";

export type TypesLeak = {
  filtración: string;
  [key: string]: string;
};

function getDataFoundList(dataLeaks: DataLeak[]): string[] {
  let dataFound: string[] = dataLeaks.reduce(
    (result: string[], current: DataLeak) =>
      [...result].concat(current.breach.breached_data),
    []
  );
  return dataFound.filter(function (elem, index, self) {
    return index === self.indexOf(elem);
  });
}

export function getLeakTableColumns(
  dataLeaks: DataLeak[]
): ColumnDef<TypesLeak>[] {
  const dataFoundUnique: string[] = [
    "filtración",
    ...getDataFoundList(dataLeaks),
  ];
  return dataFoundUnique.map((value) => {
    return {
      accessorKey: value,
      header: value.charAt(0).toUpperCase() + value.slice(1),
      cell: ({ row }) => {
        const index = row.index;
        const rowValue = row.getValue(value);
        if (value == "filtración") {
          if (String(row.getValue("filtración")).indexOf("**") > -1) {
            return (
              <a href={`#${row.index}`} className="text-indigo-600">
                <strong>{row.getValue("filtración")}</strong>
              </a>
            );
          } else {
            return (
              <a href={`#${row.index}`}>
                <strong>{row.getValue("filtración")}</strong>
              </a>
            );
          }
        } else {
          if (rowValue == "no") {
            return (
              <div className="flex justify-center text-center w-full">
                <IoWarningOutline
                  fontSize="2.3em"
                  color="orange"
                ></IoWarningOutline>
              </div>
            );
          } else if (rowValue == "yes") {
            return (
              <div className="flex justify-center text-center w-full">
                <BsShieldExclamation
                  fontSize="2em"
                  color="red"
                  className="text-center"
                ></BsShieldExclamation>
              </div>
            );
          } else {
            // if (rowValue == "-")
            return (
              <div className="flex justify-center text-center w-full">-</div>
            );
          }
        }
      },
    };
  });
}

export function getLeakTableRows(dataLeaks: DataLeak[]): TypesLeak[] {
  const rawColumns: string[] = getDataFoundList(dataLeaks);
  return dataLeaks.map((dl: DataLeak) => {
    let data: TypesLeak = {
      filtración: `${dl.breach.name}${
        dl.breach.is_sensitive ? "**" : ""
      } (${dl.breach.breach_date.slice(0, 4)})`,
    };
    rawColumns.forEach((col) => {
      if ([dl.data_type, ...dl.found_with].includes(col)) {
        data[col] = "yes";
      } else if (dl.breach.breached_data.includes(col)) {
        data[col] = "no";
      } else {
        data[col] = "-";
      }
    });
    return data;
  });
}
