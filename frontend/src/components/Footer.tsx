"use client";

import Link from "next/link";
import Image from "next/image";
import { Mail, Phone, MapPin } from "lucide-react";
import { FaFacebook, FaTwitter, FaLinkedin, FaInstagram } from "react-icons/fa";
export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-white py-16">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-12 mb-12">
          <div>
            <div className="flex items-center gap-3 mb-6">
              <div>
                <Image
                  src="/Logo.jpeg"
                  alt="Karobar Logo"
                  width={50}
                  height={50}
                  className="rounded-md object-contain"
                />
              </div>
              <span className="text-xl font-semibold">KarobarOne</span>
            </div>
            <p className="text-gray-400 mb-6">
              Empowering Indian entrepreneurs to grow their businesses profitably with our all-in-one e-commerce platform.
            </p>
            <div className="space-y-3">
              <div className="flex items-center gap-3 text-gray-400">
                <Mail className="w-4 h-4 flex-shrink-0" />
                <span>support@karobarone.com</span>
              </div>
              <div className="flex items-center gap-3 text-gray-400">
                <Phone className="w-4 h-4 flex-shrink-0" />
                <span>+91 98765 43210</span>
              </div>
              <div className="flex items-center gap-2 text-gray-400">
                <MapPin className="w-4 h-4 flex-shrink-0" />
                <span>Kolkata, India</span>
              </div>
              <div className="flex items-center gap-2 text-gray-400">
                <MapPin className="w-4 h-4 flex-shrink-0" />
                <span>Pune / Mumbai, India</span>
              </div>
              <div className="flex items-center gap-2 text-gray-400">
                <MapPin className="w-4 h-4 flex-shrink-0" />
                <span>Ahmedabad, India</span>
              </div>
              <div className="flex items-center gap-2 text-gray-400">
                <MapPin className="w-4 h-4 flex-shrink-0" />
                <span>Reno, USA</span>
              </div>
            </div>
          </div>

          <div>
            <h3 className="font-semibold text-lg mb-6">Information</h3>
            <ul className="space-y-3">
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  Media/News
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  Merchant Agreement
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  PCI-DSS Certificate
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  ISO Certificate
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  SOC Certificate
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  API Reference
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  Sitemap
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-lg mb-6">Explore</h3>
            <ul className="space-y-3">
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  Help Center
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  Book a Demo
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  Blog
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  Case Studies & Examples
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  White Papers
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  Industries
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  Marketing
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  Technology
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  Themes
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  Topics
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  Use Cases
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-lg mb-6">Resources</h3>
            <ul className="space-y-3">
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  Help Center
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  Documentation
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  API Reference
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  Terms of Service
                </a>
              </li>
              <li>
                <a href="/under-maintenance" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  Refund Policy
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="pt-8">
          {/* Top Row - Badges & Social Icons */}
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">

            {/* Certification Badges */}
            <div className="flex items-center gap-4 flex-wrap justify-center md:justify-start">
              <div className="bg-white rounded-md p-1.5 w-[70px] h-[44px] flex items-center justify-center overflow-hidden">
                <Image
                  src="/badges/MakeInIndia.webp"
                  alt="Make In India"
                  width={70}
                  height={44}
                  className="object-contain w-full h-full"
                />
              </div>

              <div className="bg-white rounded-md p-1.5 w-[70px] h-[44px] flex items-center justify-center overflow-hidden">
                <Image
                  src="/badges/Nasscom.webp"
                  alt="Nasscom Startups"
                  width={70}
                  height={44}
                  className="object-contain w-full h-full"
                />
              </div>

              <div className="bg-white rounded-md p-1.5 w-[70px] h-[44px] flex items-center justify-center overflow-hidden">
                <Image
                  src="/badges/NSDC.webp"
                  alt="NSDC"
                  width={70}
                  height={44}
                  className="object-contain w-full h-full"
                />
              </div>

              <div className="bg-white rounded-md p-1.5 w-[70px] h-[44px] flex items-center justify-center overflow-hidden">
                <Image
                  src="/badges/StartUpIndia.webp"
                  alt="Startup India"
                  width={70}
                  height={44}
                  className="object-contain w-full h-full"
                />
              </div>
            </div>

            {/* Social Icons */}
            <div className="flex gap-4">
              <a
                href="https://facebook.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-[#5b4ef9] transition-colors"
              >
                <FaFacebook className="w-5 h-5" />
              </a>

              <a
                href="https://twitter.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-[#5b4ef9] transition-colors"
              >
                <FaTwitter className="w-5 h-5" />
              </a>

              <a
                href="https://linkedin.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-[#5b4ef9] transition-colors"
              >
                <FaLinkedin className="w-5 h-5" />
              </a>

              <a
                href="https://instagram.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-[#5b4ef9] transition-colors"
              >
                <FaInstagram className="w-5 h-5" />
              </a>
            </div>
          </div>

          {/* Divider */}
          <div className="border-t border-gray-800 mt-8"></div>

          {/* Copyright */}
          <div className="py-2 flex justify-center">
            <p className="text-gray-400 text-sm">
              © 2016 - {currentYear} KarobarOne. All rights reserved.
            </p>
          </div>

        </div>
      </div>
    </footer>
  );
}