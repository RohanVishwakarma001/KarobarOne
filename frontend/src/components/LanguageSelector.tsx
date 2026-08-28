"use client";

import { useEffect, useState } from "react";
import { Globe, ChevronDown } from "lucide-react";

declare global {
  interface Window {
    google: any;
    googleTranslateElementInit: () => void;
  }
}

const LANGUAGES = [
  { code: "en", label: "English" },
  { code: "hi", label: "हिन्दी" },
  { code: "mr", label: "मराठी" },
  { code: "gu", label: "ગુજરાતી" },
  { code: "ta", label: "தமிழ்" },
  { code: "te", label: "తెలుగు" },
  { code: "bn", label: "বাংলা" },
  { code: "kn", label: "ಕನ್ನಡ" },
  { code: "ml", label: "മലയാളം" },
  { code: "pa", label: "ਪੰਜਾਬੀ" },
  { code: "ur", label: "اردو" },
];

function getCookieLang(): string {
  const match = document.cookie.match(/googtrans=\/[a-zA-Z-]*\/([a-zA-Z-]+)/);
  return match?.[1] || "en";
}

function setCookieForAllPaths(name: string, value: string) {
  const hostname = window.location.hostname;
  document.cookie = `${name}=${value}; path=/`;
  document.cookie = `${name}=${value}; path=/; domain=${hostname}`;
  document.cookie = `${name}=${value}; path=/; domain=.${hostname}`;
}

export function LanguageSelector() {
  const [open, setOpen] = useState(false);
  const [current, setCurrent] = useState("en");

  useEffect(() => {
    setCurrent(getCookieLang());

    // Load fonts that cover Indic + Arabic scripts, so language names
    // always render correctly even if the OS doesn't have these fonts.
    if (!document.getElementById("multi-script-fonts")) {
      const link = document.createElement("link");
      link.id = "multi-script-fonts";
      link.rel = "stylesheet";
      link.href =
        "https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600&family=Noto+Sans+Devanagari:wght@400;600&family=Noto+Sans+Gujarati:wght@400;600&family=Noto+Sans+Tamil:wght@400;600&family=Noto+Sans+Telugu:wght@400;600&family=Noto+Sans+Bengali:wght@400;600&family=Noto+Sans+Kannada:wght@400;600&family=Noto+Sans+Malayalam:wght@400;600&family=Noto+Sans+Gurmukhi:wght@400;600&family=Noto+Sans+Arabic:wght@400;600&display=swap";
      document.head.appendChild(link);
    }

    // Initialize the Google Translate engine once. Because we use the
    // cookie method below, this runs on every load and auto-translates
    // based on whatever language cookie is already set.
    if (!window.googleTranslateElementInit) {
      window.googleTranslateElementInit = function () {
        new window.google.translate.TranslateElement(
          {
            pageLanguage: "en",
            includedLanguages: LANGUAGES.map((l) => l.code).join(","),
            layout: window.google.translate.TranslateElement.InlineLayout.SIMPLE,
            autoDisplay: false,
          },
          "google_translate_element"
        );
      };
    }

    if (!document.getElementById("google-translate-script")) {
      const script = document.createElement("script");
      script.id = "google-translate-script";
      script.src =
        "https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
      script.async = true;
      document.body.appendChild(script);
    }
  }, []);

  function changeLanguage(code: string) {
    setOpen(false);
    if (code === "en") {
      // Clear the cookie to go back to the original English page
      setCookieForAllPaths("googtrans", "/en/en");
    } else {
      setCookieForAllPaths("googtrans", `/en/${code}`);
    }
    localStorage.setItem("site-lang", code);
    window.location.reload();
  }

  const currentLabel = LANGUAGES.find((l) => l.code === current)?.label ?? "English";

  return (
    <div className="relative inline-block" style={{ fontFamily: "'Noto Sans', sans-serif" }}>
      <div id="google_translate_element" className="hidden" />

      <button
        onClick={() => setOpen((o) => !o)}
        className="notranslate flex items-center gap-2 border border-gray-300 rounded-lg px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
      >
        <Globe className="w-4 h-4" />
        <span style={{ fontFamily: "'Noto Sans Devanagari','Noto Sans Gujarati','Noto Sans Tamil','Noto Sans Telugu','Noto Sans Bengali','Noto Sans Kannada','Noto Sans Malayalam','Noto Sans Gurmukhi','Noto Sans Arabic','Noto Sans',sans-serif" }}>
          {currentLabel}
        </span>
        <ChevronDown className="w-4 h-4" />
      </button>

      {open && (
        <div className="notranslate absolute right-0 mt-2 w-44 bg-white border border-gray-200 rounded-lg shadow-lg z-50 max-h-72 overflow-y-auto">
          {LANGUAGES.map((lang) => (
            <button
              key={lang.code}
              onClick={() => changeLanguage(lang.code)}
              style={{ fontFamily: "'Noto Sans Devanagari','Noto Sans Gujarati','Noto Sans Tamil','Noto Sans Telugu','Noto Sans Bengali','Noto Sans Kannada','Noto Sans Malayalam','Noto Sans Gurmukhi','Noto Sans Arabic','Noto Sans',sans-serif" }}
              className={`block w-full text-left px-4 py-2 text-sm hover:bg-gray-50 ${
                current === lang.code ? "text-[#5b4ef9] font-semibold" : "text-gray-700"
              }`}
            >
              {lang.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}