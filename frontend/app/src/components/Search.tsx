import { Dispatch, SetStateAction, useEffect, useRef, useState } from "react";
import { FaSearch } from "react-icons/fa";

export default function Search({
  placeholder,
  searchTerm,
  setSearchTerm,
  disabled = false,
  handleFormat = (v: string) => v,
}: {
  placeholder: string;
  searchTerm: string;
  setSearchTerm: Dispatch<SetStateAction<string>>;
  disabled: boolean;
  handleFormat?: (v: string) => string;
}) {
  const [formattedValue, setFormattedValue] = useState<string>(searchTerm);

  useEffect(() => {
    if (formattedValue === "") setFormattedValue(handleFormat(searchTerm));
  }, [searchTerm]);

  function handleSearch(e: React.ChangeEvent<HTMLInputElement>) {
    const term = e.target.value;
    setSearchTerm(term);
    setFormattedValue(handleFormat(term));
  }

  return (
    <div className="relative flex flex-1 flex-shrink-0 w-full">
      <label htmlFor="search" className="sr-only">
        Search
      </label>
      <input
        value={formattedValue}
        className="peer block w-full rounded-md border border-gray-200 py-[9px] pl-10 text-sm outline-2 placeholder:text-gray-500 disabled:pointer-events-none disabled:opacity-50"
        placeholder={placeholder}
        name={"search"}
        onChange={(e) => {
          handleSearch(e);
        }}
        disabled={disabled}
      />
      <FaSearch className="absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900" />
    </div>
  );
}
