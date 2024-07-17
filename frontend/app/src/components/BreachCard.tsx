import { Breach } from "@/models/Breach";
import { AiOutlineSafety } from "react-icons/ai";

export default function BreachCard({
  breach,
  index,
}: {
  breach: Breach;
  index: number;
}) {
  return (
    <div
      id={`${index}`}
      className={`flex flex-col items-start my-1 p-4 border rounded-lg w-full ${
        breach.is_sensitive ? "border-indigo-600" : ""
      }`}
    >
      {breach.is_sensitive && (
        <p className="text-indigo-600">*Filtración Sensible*</p>
      )}
      <h3 className="font-bold text-xl">
        {`${breach.name} (${breach.breach_date.slice(0, 4)})`}
      </h3>
      <p>{breach.description}</p>
      <p>
        <b>Tipos de datos encontrados: </b>
        {breach.breached_data.join(", ")}
      </p>
      {breach.security_tips.length > 0 && (
        <>
          <p className="font-bold self-center pt-2 underline">
            Consejos de seguridad
          </p>
          <div className="flex flex-col">
            {breach.security_tips.map((tip, index) => (
              <div className="ml-3 flex flex-row items-start gap-1" key={index}>
                {/* <MdOutlineSecurity color="green"></MdOutlineSecurity> */}
                <AiOutlineSafety
                  className="shrink-0 mt-1"
                  color="green"
                ></AiOutlineSafety>
                <>{tip}</>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
