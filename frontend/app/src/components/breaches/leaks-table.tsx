import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { LuSearchX } from "react-icons/lu";
import { TbShieldExclamation } from "react-icons/tb";
import { BsShieldExclamation } from "react-icons/bs";
import { IoWarningOutline } from "react-icons/io5";

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
  queried_type: string;
}

export function LeaksTable<TData, TValue>({
  columns,
  data,
  queried_type,
}: DataTableProps<TData, TValue>) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div>
      <h2 className="text-center font-bold">TUS DATOS COMPROMETIDOS</h2>
      <Simbologia />
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead className="text-center" key={header.id}>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                    </TableHead>
                  );
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  data-state={row.getIsSelected() && "selected"}
                >
                  {row.getVisibleCells().map((cell) => (
                    <TableCell
                      // className={cn("border", "[&_td:last-child]:border-0")}
                      // className="border"
                      key={cell.id}
                    >
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      {/* <Simbologia /> */}
    </div>
  );
}

const Simbologia = ({}) => {
  return (
    <div className="py-3 text-sm text-muted-foreground grid grid-cols-2 sm:grid-cols-4 gap-x-1 gap-y-1 justify-items-center">
      <p className="flex flex-row items-center self-start">
        <BsShieldExclamation
          fontSize="1.5em"
          color="red"
          className="shrink-0 text-center self-start"
        ></BsShieldExclamation>
        {/* <TbShieldExclamation
          fontSize="1.5em"
          color="red"
          className="shrink-0 text-center self-start"
        ></TbShieldExclamation> */}
        : Encontrado en la filtración.
      </p>
      <p className="flex flex-row items-center self-start">
        - : Dato no filtrado.
      </p>
      <div className="col-span-2 justify-items-center flex flex-row items-center">
        <p className="flex flex-row self-start">
          {/* <LuSearchX
            className="shrink-0"
            fontSize="1.5em"
            color="gray"
          ></LuSearchX> */}
          <IoWarningOutline
            className="shrink-0"
            fontSize="1.7em"
            color="orange"
          ></IoWarningOutline>
          :
        </p>
        <p className="ml-1 self-start">
          Dato visto en otras cuentas de la misma filtración, pero no detectado
          en esta cuenta.
        </p>
      </div>
    </div>
  );
};
