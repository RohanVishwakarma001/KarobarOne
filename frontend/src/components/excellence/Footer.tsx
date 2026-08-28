"use client";

import { useState } from "react";
import { FaFacebook, FaTwitter, FaLinkedin, FaYoutube } from "react-icons/fa";
import { MapPin, Phone, Mail } from 'lucide-react';
import PrivacyPolicyModal from "./Footer-modals/Privacy&Policy";
import TermsConditionsModal from "./Footer-modals/Terms&Conditions";
import ShippingPolicyModal from "./Footer-modals/ShippingPolicy";
import ReturnPolicyModal from "./Footer-modals/ReturnPolicy";
import CookiePolicyModal from "./Footer-modals/CookiePolicy";

type ActiveModal = "privacy" | "terms" | "shipping" | "return" | "cookie" | null;

export default function Footer() {
  const [activeModal, setActiveModal] = useState<ActiveModal>(null);

  return (
    <footer className="bg-gray-900 text-white py-12 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div>
            <h3 className="text-2xl mb-4">Excellence Corp</h3>
            <p className="text-gray-400">
              Delivering innovative solutions since 2015
            </p>
            <div className="mt-6 space-y-4">
              <div className="flex items-center gap-3">
                <MapPin className="text-blue-600" size={24} />
                <span>123 Business Street, New York, NY 10001</span>
              </div>

              <div className="flex items-center gap-3">
                <Phone className="text-blue-600" size={24} />
                <span>+1 (555) 123-4567</span>
              </div>

              <div className="flex items-center gap-3">
                <Mail className="text-blue-600" size={24} />
                <span>contact@company.com</span>
              </div>
            </div>

          </div>

          <div>
            <h4 className="mb-4">Quick Links</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Products</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Services</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
            </ul>
          </div>

          <div>
            <h4 className="mb-4">Legal</h4>
            <ul className="space-y-2 text-gray-400">
              <li>
                <button
                  onClick={() => setActiveModal("privacy")}
                  className="hover:text-white transition-colors text-left"
                >
                  Privacy Policy
                </button>
              </li>
              <li>
                <button
                  onClick={() => setActiveModal("terms")}
                  className="hover:text-white transition-colors text-left"
                >
                  Terms &amp; Conditions
                </button>
              </li>
              <li>
                <button
                  onClick={() => setActiveModal("cookie")}
                  className="hover:text-white transition-colors text-left"
                >
                  Cookie Policy
                </button>
              </li>
              <li>
                <button
                  onClick={() => setActiveModal("shipping")}
                  className="hover:text-white transition-colors text-left"
                >
                  Shipping Policy
                </button>
              </li>
              <li>
                <button
                  onClick={() => setActiveModal("return")}
                  className="hover:text-white transition-colors text-left"
                >
                  Return Policy
                </button>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="mb-4">Follow Us</h4>
            <div className="flex gap-4">
              <a href="#" className="bg-white/10 p-3 rounded-full hover:bg-white/20 transition-colors">
                <FaFacebook className="w-5 h-5" />
              </a>
              <a href="#" className="bg-white/10 p-3 rounded-full hover:bg-white/20 transition-colors">
                <FaTwitter className="w-5 h-5" />
              </a>
              <a href="#" className="bg-white/10 p-3 rounded-full hover:bg-white/20 transition-colors">
                <FaLinkedin className="w-5 h-5" />
              </a>
              <a href="#" className="bg-white/10 p-3 rounded-full hover:bg-white/20 transition-colors">
                <FaYoutube className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 pt-8 text-center text-gray-400">
          <p>&copy; 2016 - {new Date().getFullYear()} Excellence Corporation Ltd. All rights reserved.</p>
          <p>Disclaimer: Excellence Corp does not endorse seller claims or information. Please verify all details independently before proceeding.
          </p>
        </div>
      </div>

      {activeModal === "privacy" && <PrivacyPolicyModal onClose={() => setActiveModal(null)} />}
      {activeModal === "terms" && <TermsConditionsModal onClose={() => setActiveModal(null)} />}
      {activeModal === "shipping" && <ShippingPolicyModal onClose={() => setActiveModal(null)} />}
      {activeModal === "return" && <ReturnPolicyModal onClose={() => setActiveModal(null)} />}
      {activeModal === "cookie" && <CookiePolicyModal onClose={() => setActiveModal(null)} />}
    </footer>
  );
}