import { getSensitiveDataLeaks, getSensitiveDataLeaksDemo } from "@/api/api";
import Navbar from "@/components/Navbar";
import { useRouter } from "next/navigation";
import { DataLeak } from "@/models/Breach";
import { useEffect, useState } from "react";
import BreachCard from "@/components/BreachCard";
import { IconContext } from "react-icons";
import { PiShieldWarningFill } from "react-icons/pi";
import { ColumnDef } from "@tanstack/react-table";
import {
  TypesLeak,
  getLeakTableColumns,
  getLeakTableRows,
} from "@/components/breaches/columns";
import { FaCheckCircle } from "react-icons/fa";
import { FcIdea } from "react-icons/fc";
import { Loader2 } from "lucide-react";
import { AiOutlineSafety } from "react-icons/ai";
import AlertMessage from "@/components/AlertMessage";
import { LeaksTable } from "@/components/breaches/leaks-table";
import { safetyTips } from "@/utils/webSafetyTips";

const redColor = "#ED342F";

export default function SensitiveBreach() {
  const [dataLeaks, setDataLeaks] = useState<DataLeak[]>([]);
  const [columns, setColumns] = useState<ColumnDef<TypesLeak>[]>([]);
  const [tableData, setTableData] = useState<TypesLeak[]>([]);
  const [waitingResponse, setWaitingResponse] = useState(false);
  const [responseReceived, setResponseReceived] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const { push } = useRouter();

  async function getBreaches() {
    setWaitingResponse(true);
    const [dataLeakList, errorMsg] = await getSensitiveDataLeaksDemo();
    setDataLeaks(dataLeakList);
    setErrorMsg(errorMsg.message);
    setWaitingResponse(false);
    setResponseReceived(true);
  }

  useEffect(() => {
    if (dataLeaks.length > 0) {
      setColumns(getLeakTableColumns(dataLeaks));
      setTableData(getLeakTableRows(dataLeaks));
    }
  }, [dataLeaks]);

  useEffect(() => {
    if (!waitingResponse && !responseReceived) {
      getBreaches();
    }
    return () => {
      setDataLeaks([]);
      setResponseReceived(true);
    };
  }, []);

  if (responseReceived && errorMsg.length !== 0) {
    push("/verification");
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-start md:px-24 pt-2 pb-20">
      <Navbar />
      <div className="flex flex-col mt-20 w-full items-center justify-start">
        <div className="flex flex-col self-start w-full items-center gap-x-5">
          <h2 className="text-xl font-bold">Verificación Completada</h2>
          <p>
            A continuación se muestran los resultados sobre tus filtraciones
            sensibles:
          </p>
        </div>
        {responseReceived ? (
          <>
            {errorMsg === "" ? (
              <div className="flex flex-col mt-5 w-full items-center justify-start">
                <div className="flex flex-col w-full self-start justifiy-start items-center">
                  {dataLeaks.length > 0 ? (
                    <>
                      <IconContext.Provider value={{ color: `${redColor}` }}>
                        <PiShieldWarningFill
                          fontSize="3.5em"
                          className="self-center"
                        />
                        <AlertMessage
                          variant="danger"
                          message={`¡Esta cuenta ha sido visto en ${dataLeaks.length} filtraciones de nuestro conocimiento!`}
                        />
                      </IconContext.Provider>
                      <div className="w-full mx-auto py-5">
                        <LeaksTable
                          columns={columns}
                          data={tableData}
                          queried_type={dataLeaks[0].data_type}
                        />
                      </div>
                    </>
                  ) : (
                    <>
                      <FaCheckCircle
                        fontSize="3.5em"
                        className="self-center text-green-hackerlab"
                      />
                      <AlertMessage
                        variant="safe"
                        message={`¡Esta cuenta no ha sido encontrado en filtraciones de nuestro conocimiento!`}
                      />
                      <div className="p-3 my-5 flex flex-col justify-center w-full sm:w-[90%] border rounded-md border-cyan-400">
                        <h3 className="flex flex-row text-lg font-bold underline">
                          <FcIdea className="mt-1"></FcIdea>
                          Recomendaciones de seguridad
                        </h3>
                        {safetyTips.map((tip, index) => (
                          <div
                            className="ml-3 items-start flex flex-row gap-1 text-lg"
                            key={index}
                          >
                            <AiOutlineSafety
                              className="mt-1.5 shrink-0"
                              color="green"
                            ></AiOutlineSafety>
                            <p className="font-thin m-0">
                              <b>{tip.title}: </b>
                              {tip.value}
                            </p>
                          </div>
                        ))}
                        <p></p>
                      </div>
                    </>
                  )}
                </div>
                {dataLeaks.map((dLeak, index) => (
                  <BreachCard key={index} breach={dLeak.breach} index={index} />
                ))}
              </div>
            ) : (
              <div className="my-5 w-full text-center">
                <p className="text-lg text-red-hackerlab">
                  Error: por favor, inténtelo de nuevo más tarde
                </p>
              </div>
            )}
          </>
        ) : (
          <>
            {waitingResponse && (
              <div className="mt-10 flex w-full justify-center">
                <Loader2 size={"3em"} className="animate-spin"></Loader2>
              </div>
            )}
          </>
        )}
        <div className="flex flex-col">
          <div className="ml-3 flex flex-row items-start gap-1"></div>
        </div>
      </div>

      <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-4 lg:text-left"></div>
    </main>
  );
}
