import { Dispatch, SetStateAction } from "react";

export default function MobileNumberInput({
  placeholder,
  searchTerm,
  setSearchTerm,
  prefix = "+56",
}: {
  placeholder: string;
  searchTerm: string;
  setSearchTerm: Dispatch<SetStateAction<string>>;
  prefix?: string;
}) {
  function handleSearch(term: string) {
    setSearchTerm(term);
  }

  return (
    <div className="relative flex flex-1 flex-shrink-0 w-full">
      <label htmlFor="search" className="sr-only">
        Search
      </label>
      <input
        value={searchTerm}
        className="peer block w-full rounded-md border border-gray-200 py-[9px] pl-20 text-sm outline-2 placeholder:text-gray-500"
        placeholder={placeholder}
        name={"search"}
        onChange={(e) => {
          handleSearch(e.target.value);
        }}
      />
      <div className="absolute left-3 top-1/2 h-[20px] w-[60px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900">
        <p>{prefix} |</p>
      </div>
    </div>
  );
}
