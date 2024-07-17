import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

import Search from "@/components/Search";
import Navbar from "@/components/Navbar";
import { useEffect, useState } from "react";
import { DataLeak } from "@/models/Breach";
import { getDataLeaksByValueAndTypeDemo, QueryType } from "@/api/api";
import { FaCheckCircle } from "react-icons/fa";
import { FaIdCard } from "react-icons/fa";
import { FcIdea } from "react-icons/fc";
import { FaUnlock } from "react-icons/fa6";
import { AiOutlineSafety } from "react-icons/ai";
import { useRouter } from "next/router";
import { IconContext } from "react-icons";
import { PiShieldWarningFill } from "react-icons/pi";
import { LeaksTable } from "@/components/breaches/leaks-table";
import { ColumnDef } from "@tanstack/react-table";
import {
  TypesLeak,
  getLeakTableColumns,
  getLeakTableRows,
} from "@/components/breaches/columns";
import { LuMailWarning } from "react-icons/lu";
import { Loader2 } from "lucide-react";
import BreachCard from "@/components/BreachCard";
import AlertMessage from "@/components/AlertMessage";
import { safetyTips } from "@/utils/webSafetyTips";
import { useAuth } from "@/contexts/AuthContext";
import Turnstile from "@/components/Turnstile";
import { SearchQuery } from "@/models/SearchQuery";
import MobileNumberInput from "@/components/MobileNumberInput";
import { AuthButton } from "@/components/SessionInfoButton";

const redColor = "#ED342F";
const CLOUDFLARE_ENABLED = process.env.NEXT_PUBLIC_CLOUDFLARE_ENABLED;
const CLOUDFLARE_SITE_KEY = process.env.NEXT_PUBLIC_CLOUDFLARE_SITE_KEY
  ? process.env.NEXT_PUBLIC_CLOUDFLARE_SITE_KEY
  : "";
const MUST_VERIFY_SEARCH_KEYS = process.env.NEXT_PUBLIC_MUST_VERIFY_SEARCH_KEYS
  ? process.env.NEXT_PUBLIC_MUST_VERIFY_SEARCH_KEYS.split(",")
  : [];
const ENABLED_SEARCH_KEYS = ["email", "phone", "rut"];

export default function Home() {
  const { user } = useAuth();
  const router = useRouter();
  const searchedValue = router.query.search ? String(router.query.search) : "";
  const searchedType = router.query.type ? String(router.query.type) : "";
  const [queryLoaded, setQueryLoaded] = useState(false);
  const [searchEmail, setSearchEmail] = useState("");
  const [responseReceived, setResponseReceived] = useState(false);
  const [error, setError] = useState<string>("");
  const [waitingResponse, setWaitingResponse] = useState(false);
  const [searchRut, setSearchRut] = useState("");
  const [searchPhone, setSearchPhone] = useState("");
  const [dataLeaks, setDataLeaks] = useState<Array<DataLeak>>([]);
  const [columns, setColumns] = useState<ColumnDef<TypesLeak>[]>([]);
  const [tableData, setTableData] = useState<TypesLeak[]>([]);
  const [tabValue, setTabValue] = useState<string>(ENABLED_SEARCH_KEYS[0]);
  const [turnstileToken, setTurnstileToken] = useState<string | null>(null);
  const [turnstileNeedReset, setTurnstileNeedReset] = useState<boolean>(false);
  const totalNumberTabs = ENABLED_SEARCH_KEYS.length;

  async function handleSearch(query: string, queryType: QueryType) {
    const searchQuery: SearchQuery = { value: query, dtype: queryType };
    if (CLOUDFLARE_ENABLED?.toLowerCase() === "true") {
      if (turnstileToken == null) {
        setError("Por favor, complete el CAPTCHA");
        return;
      }
      searchQuery.turnstile_response = turnstileToken;
    }
    setResponseReceived(false);
    setWaitingResponse(true);
    const [dataLeaksList, gotError]: [DataLeak[], boolean] =
      // await getDataLeaksByValueAndType(query, QueryType.Email);
      await getDataLeaksByValueAndTypeDemo(searchQuery);
    if (gotError) {
      setError(
        "Ha ocurrido un error innesperado, inténtelo de nuevo más tarde."
      );
    } else {
      setError("");
    }
    setTurnstileNeedReset(true);
    setDataLeaks(dataLeaksList);
    setResponseReceived(true);
    setWaitingResponse(false);
  }

  async function handleEmailSubmit() {
    const emailQuery = searchEmail.trim().toLowerCase();
    if (emailQuery) {
      handleSearch(emailQuery, QueryType.Email);
    }
  }

  async function handleRutSubmit() {
    const rutQuery = searchRut
      .trim()
      .replace(/\s/g, "")
      .replace(/\./g, "")
      .replace("-", "");
    if (rutQuery) {
      handleSearch(rutQuery, QueryType.Rut);
    }
  }

  async function handlePhoneSubmit() {
    const phoneQuery = searchPhone.trim();
    if (phoneQuery) {
      handleSearch(phoneQuery, QueryType.Phone);
    }
  }

  useEffect(() => {
    if (dataLeaks.length > 0) {
      setColumns(getLeakTableColumns(dataLeaks));
      setTableData(getLeakTableRows(dataLeaks));
    }
  }, [dataLeaks]);

  function getEnabledSearchKeys() {
    const availableSearchKeys = [
      {
        title: "Email",
        value: "email",
        description:
          "Ingrese el correo electrónico que desea consultar. Se revisará si dicho correo fue encontrado en alguna filtración de datos que tengamos conocimiento.",
        submitFunc: handleEmailSubmit,
        inputFormatting: (val: string) => val,
        search: searchEmail,
        setSearch: setSearchEmail,
        inputHint: "Consulte un email...",
        name: "correo",
        needsAuth: MUST_VERIFY_SEARCH_KEYS.includes("email"),
      },
      {
        title: "RUT",
        value: "rut",
        description:
          "Ingrese el RUT que desea consultar. Se revisará si dicho RUT fue encontrado en alguna filtración de datos que tengamos conocimiento.",
        submitFunc: handleRutSubmit,
        inputFormatting: (val: string) => {
          let lastChar = val.charAt(val.length - 1).toLowerCase();
          let onlyNums = val.replace(/\D+/g, (c) => "");
          console.log("Last char value", lastChar);
          console.log("Only nums", onlyNums);
          if (lastChar === "k") {
            onlyNums += "K";
          }
          if (onlyNums.length > 9) onlyNums = onlyNums.slice(0, 9);
          console.log("Last char after", lastChar);
          const rutBody = onlyNums.slice(0, -1);
          const dv = onlyNums.slice(onlyNums.length - 1);
          console.log("Rut Body", rutBody);
          return onlyNums.length ? rutBody + "-" + dv : "";
        },
        search: searchRut,
        setSearch: setSearchRut,
        inputHint: "Consulte un RUT...",
        name: "RUT",
        needsAuth: MUST_VERIFY_SEARCH_KEYS.includes("rut"),
      },
      {
        title: "Número telefónico",
        value: "phone",
        description:
          "Ingrese el número telefónico que desea consultar. Se revisará si dicho número fue encontrado en alguna filtración de datos que tengamos conocimiento." +
          "\nRecuerde que un número celular tiene el siguiente formato 9 XXXX XXXX, mientras que uno particular tiene la forma 2 XXXX XXXX (Región Metropolitana)" +
          " o YY XXXX XXX (siendo YY el prefijo correspondiente según la región).",
        submitFunc: handlePhoneSubmit,
        inputFormatting: (val: string) => val,
        search: searchPhone,
        setSearch: setSearchPhone,
        inputHint: "Consulte un número telefónico...",
        name: "número telefónico",
        needsAuth: MUST_VERIFY_SEARCH_KEYS.includes("phone"),
      },
    ];
    let enabledKeys = [];
    for (let i = 0; i < availableSearchKeys.length; i++) {
      if (ENABLED_SEARCH_KEYS.includes(availableSearchKeys[i].value))
        enabledKeys.push(availableSearchKeys[i]);
    }
    return enabledKeys;
  }

  const searchKeys = getEnabledSearchKeys();

  useEffect(() => {
    if (searchedValue) {
      for (let i = 0; i < searchKeys.length; i++) {
        if (searchKeys[i]["value"] === searchedType) {
          setTabValue(searchedType);
          searchKeys[i].setSearch(searchedValue);
          setQueryLoaded(true);
        }
      }
    }
  }, [searchedValue, searchedType]);

  useEffect(() => {
    if (queryLoaded) {
      setResponseReceived(false);
      setQueryLoaded(false);
    }
  }, [queryLoaded]);

  useEffect(() => {
    let keyType = searchKeys.filter((obj) => obj.value == tabValue)[0];
    if (keyType.needsAuth && user?.dtype == keyType.value) {
      keyType.setSearch(user.value);
    }
  }, [tabValue]);

  function clearSearchIput() {
    // setSearchEmail("");
    // setSearchPhone("");
    // setSearchRut("");
    setError("");
    router.replace("/", undefined, { shallow: true });
    setResponseReceived(false);
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-start md:px-24 pt-2 pb-20">
      <Navbar />
      <div className="flex flex-col mt-5 w-full items-center justify-start">
        <div className="flex flex-col w-full items-center text-center py-3">
          <h2 className="font-black text-2xl text-cyan-500">
            ¡Bienvenid@ a Data Leak Checker!
          </h2>
          <p className="text-lg w-[90%]">
            ¡En esta plataforma podrás enterarte qué datos privados tuyos han
            sido encontrados en filtraciones de datos!
          </p>
        </div>
        {/*<POCMessage></POCMessage>*/}
        <Tabs
          value={tabValue}
          onValueChange={(value) => setTabValue(value)}
          className="w-[90%] md:w-[80%] max-w-[1280px]"
        >
          {/* <TabsList className={`grid w-full grid-cols-${totalNumberTabs}`}> */}
          <TabsList className={`flex w-full flex-row justify-around`}>
            {searchKeys.map((item) => (
              <TabsTrigger
                onClick={clearSearchIput}
                key={item.value}
                value={item.value}
                className="w-full"
              >
                {item.title}
              </TabsTrigger>
            ))}
          </TabsList>
          {searchKeys.map((item) => (
            <TabsContent key={item.value} value={item.value}>
              <Card>
                <CardHeader>
                  {item.needsAuth ? (
                    <>
                      <CardTitle>
                        {item.title} (Requiere Verificación)
                      </CardTitle>
                      <CardDescription>
                        Para consultar por este tipo de dato, es necesario
                        verificar que seas dueño de la cuenta.
                      </CardDescription>
                    </>
                  ) : (
                    <>
                      <CardTitle>{item.title}</CardTitle>
                      <CardDescription>{item.description}</CardDescription>
                    </>
                  )}
                </CardHeader>
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    item.submitFunc();
                  }}
                  autoComplete="off"
                  className="w-full"
                >
                  <CardContent className="space-y-2">
                    <div className="z-10 max-w-5xl w-full items-center self-center justify-self-center justify-between font-mono text-sm lg:flex">
                      {item.needsAuth ? (
                        <>
                          {!(user?.dtype == item.value) ? (
                            <div className="flex w-full justify-center">
                              <AuthButton />
                            </div>
                          ) : (
                            // <SessionInfoButton></SessionInfoButton>
                            <div className="flex w-full justify-center">
                              <div className="w-fit px-3 rounded-md border border-gray-200 py-[9px] text-sm outline-2 placeholder:text-gray-500 disabled:pointer-events-none">
                                {item.search}
                              </div>
                              {/* <Button
                                type="button"
                                variant={"outline"}
                                className="justify-self-center"
                              >
                                {item.search}
                              </Button> */}
                            </div>
                            // <div>Buscar: {item.search}</div>
                          )}
                        </>
                      ) : (
                        <>
                          {item.value == "phone" ? (
                            <MobileNumberInput
                              placeholder={item.inputHint}
                              searchTerm={item.search}
                              setSearchTerm={item.setSearch}
                            />
                          ) : (
                            <Search
                              placeholder={item.inputHint}
                              searchTerm={
                                item.needsAuth
                                  ? user?.value
                                    ? user.value
                                    : ""
                                  : item.search
                              }
                              setSearchTerm={item.setSearch}
                              handleFormat={item.inputFormatting}
                            />
                          )}
                        </>
                      )}
                    </div>
                  </CardContent>
                  <CardFooter className="flex flex-col gap-y-5 items-center justify-center">
                    {CLOUDFLARE_ENABLED?.toLowerCase() === "true" &&
                      ((item.needsAuth && user?.dtype == item.value) ||
                        !item.needsAuth) && (
                        <Turnstile
                          siteKey={CLOUDFLARE_SITE_KEY}
                          onTokenChange={setTurnstileToken}
                          needReset={turnstileNeedReset}
                          setNeedReset={setTurnstileNeedReset}
                        ></Turnstile>
                      )}
                    {(!item.needsAuth ||
                      (item.needsAuth && user?.dtype == item.value)) && (
                      <Button type="submit">Buscar</Button>
                    )}
                  </CardFooter>
                </form>
              </Card>
              {user === null && (
                <div className="flex flex-col w-full items-center">
                  <p className="text-indigo-600">
                    <b>Nota:</b> Para ver TODAS las filtraciones de una cuenta
                    debes autenticarte
                  </p>
                </div>
              )}
              {error && (
                <div className="my-5 w-full text-center">
                  <p className="text-lg text-red-hackerlab">{error}</p>
                </div>
              )}
              {responseReceived && !error ? (
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
                            message={`¡Este ${item.name} ha sido visto en ${dataLeaks.length} filtraciones de nuestro conocimiento!`}
                          />
                        </IconContext.Provider>
                        {/* <div className="container mx-auto py-10"> */}
                        <div className="w-full mx-auto py-5">
                          <LeaksTable
                            columns={columns}
                            data={tableData}
                            queried_type={item.name}
                          />
                        </div>
                      </>
                    ) : (
                      <>
                        <FaCheckCircle
                          // color="green"
                          fontSize="3.5em"
                          className="self-center text-green-hackerlab"
                        />
                        <AlertMessage
                          variant="safe"
                          message={`¡Este ${item.name} no ha sido encontrado en filtraciones de nuestro conocimiento!`}
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
                    <BreachCard
                      key={index}
                      breach={dLeak.breach}
                      index={index}
                    />
                  ))}
                </div>
              ) : (
                <>
                  {waitingResponse ? (
                    <div className="mt-10 flex w-full justify-center">
                      <Loader2 size={"3em"} className="animate-spin"></Loader2>
                    </div>
                  ) : (
                    <LandingPage></LandingPage>
                  )}
                </>
              )}
            </TabsContent>
          ))}
        </Tabs>
        {/* </div> */}
      </div>

      <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-4 lg:text-left"></div>
    </main>
  );
}

function POCMessage({}) {
  return (
    <div className="w-[90%] md:w-[80%] max-w-[1280px] rounded-md border-2 px-3 mb-4 border-red-600 bg-red-300">
      <p className="font-bold">Leer antes de usar:</p>
      <p>
        Los datos de filtraciones presentes son <b>100% falsos</b>. Los datos
        entregados son totalmente al azar, y no corresponden a ninguna
        filtración de datos del mundo real. Este sitio es solamente una prueba
        de concepto con el fin de averiguar si la información presentada es
        comprensible para un futuro usuario.
      </p>
    </div>
  );
}

const LandingPage = ({}) => {
  return (
    <div className="flex flex-col divide-y pt-7 text-center justify-center w-full">
      <div className="py-3">
        <h2 className="font-bold text-xl">¿Qué es una filtración de datos?</h2>
        <p className="italic text-muted-foreground">
          &ldquo;Una filtración de datos corresponde a cualquier incidente de
          seguridad en que{" "}
          <b>
            terceros no autorizadas ganan acceso a datos sensibles o información
            confidencial
          </b>
          &rdquo;
        </p>
      </div>
      <div className="py-3">
        <h2 className="font-bold text-xl">
          ¿De qué me sirve esta información?
        </h2>
        <p className="text-muted-foreground">
          Es sumamente importante mantenerse informado y consciente de qué datos
          personales han caído en manos de terceros no autorizados. Agentes
          malintencionados pueden hacer uso de esta información para
          <b> obtener acceso a tus cuentas</b>, <b>suplantar tu identidad</b> e{" "}
          <b>incluso crear estafas más convincentes</b>.
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 text-center py-5 justify-items-center">
          <div className="flex flex-col items-center">
            <FaUnlock fontSize={"5em"} className="my-3"></FaUnlock>
            <p className="text-muted-foreground">
              <b>Prevenir accesos a tus cuentas</b> por terceros, cambiando tu
              contraseñas/credenciales filtradas oportunamente
            </p>
          </div>
          <div className="flex flex-col items-center">
            <FaIdCard fontSize={"5em"} className="my-3"></FaIdCard>
            <p className="text-muted-foreground">
              <b>Evitar una suplantación de identidad</b>, conociendo qué datos
              personales o credenciales se han visto comprometidas
            </p>
          </div>
          <div className="flex flex-col items-center">
            <LuMailWarning fontSize={"5em"} className="my-3"></LuMailWarning>
            <p className="text-muted-foreground">
              <b>Estar atento/a frente a intentos de estafas</b>, relacionadas a
              la información filtrada
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
