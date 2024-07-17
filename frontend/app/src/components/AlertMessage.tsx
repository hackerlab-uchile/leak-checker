type VariantType = "safe" | "danger";

const messageVariant = {
  safe: "bg-green-hackerlab",
  danger: "bg-red-hackerlab",
};

export default function AlertMessage({
  message,
  variant,
}: {
  message: string;
  variant: VariantType;
}) {
  return (
    <div
      className={`flex px-3 rounded-md justify-center text-white ${messageVariant[variant]} w-[90%]`}
    >
      <p className="text-xl text-center">{message}</p>
    </div>
  );
}
