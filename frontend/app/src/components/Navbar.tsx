import React from "react";

import Link from "next/link";
import { Button } from "./ui/button";
import { useAuth } from "@/contexts/AuthContext";
import SessionInfoButton from "./SessionInfoButton";

interface NavbarItem {
  title: string;
  href: string;
}

const NAVBAR_ITEMS: NavbarItem[] = [
  // { title: "Acerca de", href: "/about" },
  // { title: "Filtraciones sensibles", href: "/verification" },
  // {title: "Estadísticas", href: "/stats"},
  // {title: "¿Qué hacer si mis datos han sido filtrados?", href: "/what-now"},
  // {title: "¿Cómo funciona?", href: "/how-it-works"},
  // {title: "¡Notifícame!", href: "/notifications"},
];

const Navbar = () => {
  const { user, logout } = useAuth();
  return (
    <>
      <nav className="w-full relative top-0 z-40">
        <div className="container mx-auto">
          <div className="flex items-center justify-between py-2">
            <div className="flex w-full sm:w-2/4 items-center justify-between">
              {/* <div className="flex w-full items-center justify-between"> */}
              {/* Logo Sitio */}
              <Link href="/" className="block">
                <h1 className="text-lg font-bold">Data-Leak-Checker</h1>
              </Link>
            </div>
            {/* <div className="flex w-3/4 flex-wrap items-center justify-between"> */}
            <div className="flex sm:w-2/4 gap-x-5 flex-wrap items-center justify-center">
              {/* <div className="flex flex-row sm:w-3/4 gap-x-5 flex-wrap "> */}
              {NAVBAR_ITEMS.map((item) => (
                <Button
                  key={item.title}
                  className="self-center"
                  variant="outline"
                  asChild
                >
                  <Link href={item.href} className="block">
                    <h3 className="font-bold">{item.title}</h3>
                  </Link>
                </Button>
              ))}
            </div>
            <SessionInfoButton />
          </div>
        </div>
      </nav>
    </>
  );
};

export default Navbar;
