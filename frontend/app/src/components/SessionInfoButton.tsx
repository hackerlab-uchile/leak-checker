import { useAuth } from "@/contexts/AuthContext";
import { Button } from "./ui/button";
import Link from "next/link";
import { useRouter } from "next/router";
import { RiArrowDropDownLine } from "react-icons/ri";

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { FaCircleUser } from "react-icons/fa6";
import { useEffect, useState } from "react";
import { Separator } from "./ui/separator";
import { IoLogOutOutline, IoSearch } from "react-icons/io5";
import useWindowSize, { SizeType } from "@/hooks/useWindowSize";

const buttonVariant = "info";

export default function SessionInfoButton() {
  const { user, login, logout, ready } = useAuth();
  const [timeLeft, setTimeLeft] = useState<number>(0);
  const { width } = useWindowSize();

  function startTimer(dateString: string) {
    let timeDifference = new Date(dateString).getTime() - Date.now();
    setTimeLeft(timeDifference);
    const timer = setInterval(() => {
      setTimeLeft((time) => {
        if (time <= 1) {
          clearInterval(timer);
          logout();
          return 0;
        } else {
          return time - 1000;
        }
      });
    }, 1000);
    return timer;
  }

  function timeLeftCustomFormatting(timestamp: number): string {
    let date = new Date(timestamp);
    let minutes = date.getUTCMinutes();
    let seconds = date.getUTCSeconds();
    return `${
      Math.floor(minutes / 10) > 0 ? minutes : "0" + minutes.toString()
    }:${Math.floor(seconds / 10) > 0 ? seconds : "0" + seconds.toString()}`;
  }

  useEffect(() => {
    if (ready && user) {
      let timer = startTimer(user.exp);
      return () => clearInterval(timer);
    }
  }, [ready]);

  return (
    <div className="flex flex-1 flex-shrink-0 w-full justify-center">
      {user && timeLeft > 0 ? (
        <Button type="button" className="self-end justify-self-end" asChild>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              {width && width >= SizeType.SM ? (
                <Button variant={buttonVariant}>
                  <DropdownMenuLabel>{user.value}</DropdownMenuLabel>
                  <Separator orientation="vertical" />
                  <p className="ml-1.5">{timeLeftCustomFormatting(timeLeft)}</p>
                  <RiArrowDropDownLine size={"2em"} />
                </Button>
              ) : (
                <Button variant={buttonVariant}>
                  <p>{timeLeftCustomFormatting(timeLeft)}</p>
                  <Separator className="mx-1" orientation="vertical" />
                  <FaCircleUser className="mr-1" size={"2em"} />
                  <RiArrowDropDownLine size={"2em"} />
                </Button>
              )}
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              {width && width >= SizeType.SM ? (
                <>
                  <DropdownMenuItem asChild>
                    <Link href={`/?search=${user.value}&type=${user.dtype}`}>
                      <IoSearch className="mr-1" size={"1.2em"}></IoSearch>
                      Ver filtraciones
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={(e) => logout()}>
                    <IoLogOutOutline className="mr-1" size={"1.2em"} />
                    Cerrar Sesión
                  </DropdownMenuItem>
                </>
              ) : (
                <>
                  <DropdownMenuLabel>{user.value}</DropdownMenuLabel>
                  <DropdownMenuItem disabled>
                    <p className="mr-1">
                      Tiempo restante: {timeLeftCustomFormatting(timeLeft)}
                    </p>
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem asChild>
                    <Link href={`/?search=${user.value}&type=${user.dtype}`}>
                      <IoSearch className="mr-1" size={"1em"}></IoSearch>
                      Ver filtraciones
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={(e) => logout()}>
                    <IoLogOutOutline className="mr-1" size={"1.2em"} />
                    Cerrar Sesión
                  </DropdownMenuItem>
                </>
              )}
            </DropdownMenuContent>
          </DropdownMenu>
        </Button>
      ) : (
        <AuthButton></AuthButton>
        // <Button
        //   className="self-end justify-self-end"
        //   variant={buttonVariant}
        //   asChild
        // >
        //   <Link href={"/verification"} className="block">
        //     <h3 className="font-bold">Autenticarse</h3>
        //   </Link>
        // </Button>
      )}
    </div>
  );
}

export function AuthButton() {
  return (
    <Button
      className="self-center justify-self-center"
      variant={buttonVariant}
      asChild
    >
      <Link href={"/verification"} className="block">
        <h3 className="font-bold">Autenticarse</h3>
      </Link>
    </Button>
  );
}
