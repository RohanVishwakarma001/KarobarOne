"use client";
import React from "react";
import { FaMapMarkerAlt, FaPhoneAlt, FaEnvelope, FaUser } from "react-icons/fa";

function Contact() {
  return (
    <section id="contact" className="w-full py-12 px-4 bg-slate-800">
      
      <div className="max-w-6xl mx-auto bg-white rounded-2xl shadow-lg overflow-hidden">
        
        <div className="grid md:grid-cols-2">
          
          {/* LEFT: MAP */}
          <div className="h-[250px] md:h-[450px]">
            <iframe
              title="map"
              src="https://maps.google.com/maps?q=kolkata&t=&z=13&ie=UTF8&iwloc=&output=embed"
              className="w-full h-full border-0"
              loading="lazy"
            ></iframe>
          </div>

          {/* RIGHT: CONTACT */}
          <div className="p-6 md:p-8 flex flex-col justify-center bg-gray-900 text-white">
            
            <h2 className="text-xl md:text-3xl font-semibold mb-4">
              Get in Touch
            </h2>

            <p className="text-gray-400 mb-6 text-sm">
              Have questions or need assistance? Reach out anytime.
            </p>

            <div className="space-y-4 text-sm">

              <div className="flex items-center gap-3">
                <FaMapMarkerAlt className="text-orange-400" />
                <p>Kolkata, West Bengal, India</p>
              </div>

              <div className="flex items-center gap-3">
                <FaPhoneAlt className="text-green-400" />
                <a href="tel:+919877262321" className="hover:text-green-300 transition">
                  +91 9877262321
                </a>
              </div>

              <div className="flex items-center gap-3">
                <FaEnvelope className="text-blue-400" />
                <a href="mailto:info@xyzcompany.com" className="hover:text-blue-300 transition">
                  info@xyzcompany.com
                </a>
              </div>

              <div className="flex items-center gap-3">
                <FaUser className="text-yellow-400" />
                <p>Kamal Manna</p>
              </div>

            </div>
          </div>

        </div>

      </div>

    </section>
  );
}

export default Contact;