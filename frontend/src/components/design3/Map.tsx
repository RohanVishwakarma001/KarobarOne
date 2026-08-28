"use client";
import React from "react";

function Map() {
  return (
    <section className="w-full flex justify-center bg-gray-100">
      <div className="w-full max-w-4xl overflow-hidden shadow-md border border-gray-200">
        <iframe
          title="map"
          src="https://maps.google.com/maps?q=kolkata&t=&z=13&ie=UTF8&iwloc=&output=embed"
          className="w-full h-full border-0"
          loading="lazy"
        ></iframe>
      </div>
    </section>
  );
}

export default Map;
