"use client";

import React, { useState } from "react";
const Logo = "/assets/design4/logo.png";
import { FaBars, FaTimes } from "react-icons/fa";

function Navbar() {
  const [navOpen, setNavOpen] = useState(false);
  const menuItems = [
    { name: "Home", link: "#home" },
    { name: "Services", link: "#services" },
    { name: "About", link: "#about" },
    { name: "Contact", link: "#contact" },
  ];
  const toggleNav = () => setNavOpen((prev) => !prev);
  const closeNav = () => setNavOpen(false);

  return (
    <>
      <nav className="fixed top-0 w-full z-50 backdrop-blur-xl bg-white/40 border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto flex justify-between items-center px-2 py-1">
          {/* Logo + Name */}
          <div className="flex items-center gap-2">
            <img src={Logo} alt="Logo" className="h-10 w-auto" />
            <h1 className="text-slate-900 text-xl md:text-2xl font-bold">
              Creyo<span className="text-blue-700">tech</span>
            </h1>
          </div>

          {/* Desktop Menu */}
          <ul className="hidden md:flex gap-6 text-sm font-medium text-gray-700">
            {menuItems.map((item) => (
              <li key={item.name}>
                <a
                  href={item.link}
                  className="hover:text-blue-600 transition-colors duration-200"
                >
                  {item.name}
                </a>
              </li>
            ))}
          </ul>

          {/* Hamburger */}
          <button
            className="md:hidden text-2xl text-gray-800"
            onClick={toggleNav}
            aria-label="Toggle navigation"
          >
            {navOpen ? <FaTimes /> : <FaBars />}
          </button>
        </div>

        {/* Mobile Menu */}
        <div
          className={`md:hidden overflow-hidden transition-all duration-300 ${
            navOpen ? "max-h-60 py-4" : "max-h-0"
          } backdrop-blur-lg bg-white/90 border-t border-gray-200`}
        >
          <ul className="flex flex-col items-center gap-4 text-sm font-medium text-gray-700">
            {menuItems.map((item) => (
              <li key={item.name}>
                <a
                  href={item.link}
                  onClick={closeNav}
                  className="hover:text-blue-600 transition"
                >
                  {item.name}
                </a>
              </li>
            ))}
          </ul>
        </div>
      </nav>
      <div className="h-12" />
    </>
  );
}

export default Navbar;
