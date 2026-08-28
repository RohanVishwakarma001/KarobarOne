"use client";

import Link from "next/link";

type Partner = { name: string; file: string };

const COLUMN_1: Partner[] = [
  { name: "Razorpay", file: "razorpay" },
  { name: "PayU", file: "payu" },
  { name: "PhonePe", file: "phonepe" },
  { name: "Paytm", file: "paytm" },
  { name: "CCAvenue", file: "ccavenue" },
  { name: "Stripe", file: "stripe" },
];

const COLUMN_2: Partner[] = [
  { name: "Google Analytics", file: "google-analytics" },
  { name: "Google Tag Manager", file: "google-tag-manager" },
  { name: "Google Shopping", file: "google-shopping" },
  { name: "Meta", file: "meta" },
  { name: "Instagram", file: "instagram" },
  { name: "Pinterest", file: "pinterest" },
];

const COLUMN_3: Partner[] = [
  { name: "Shiprocket", file: "shiprocket" },
  { name: "Delhivery", file: "delhivery" },
  { name: "Blue Dart", file: "bluedart" },
  { name: "DTDC", file: "dtdc" },
  { name: "Ekart", file: "ekart" },
  { name: "Browntape", file: "browntape" },
];

const COLUMN_4: Partner[] = [
  { name: "WhatsApp Business", file: "whatsapp-business" },
  { name: "Zoho Books", file: "zoho-books" },
  { name: "Tally", file: "tally" },
  { name: "Unicommerce", file: "unicommerce" },
  { name: "Cashfree", file: "cashfree" },
  { name: "Instamojo", file: "instamojo" },
];

function LogoCard({ name, file }: Partner) {
  return (
    <div className="bg-white rounded-2xl border border-gray-200 shadow-sm px-6 py-8 flex items-center justify-center hover:shadow-md transition-shadow">
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={`/assets/partners/${file}.webp`}
        alt={`${name} logo`}
        className="max-h-16 md:max-h-20 w-auto object-contain"
      />
    </div>
  );
}

function MarqueeColumn({
  items,
  direction = "up",
  duration = 24,
}: {
  items: Partner[];
  direction?: "up" | "down";
  duration?: number;
}) {
  const doubled = [...items, ...items];

  return (
    <div className="relative h-[620px] overflow-hidden">
      <div
        className={`flex flex-col gap-4 ${direction === "up" ? "animate-marquee-up" : "animate-marquee-down"}`}
        style={{ animationDuration: `${duration}s` }}
      >
        {doubled.map((partner, i) => (
          <LogoCard key={`${partner.name}-${i}`} {...partner} />
        ))}
      </div>
    </div>
  );
}

export function Partnerships() {
  return (
    <section className="bg-white py-24">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          {/* Left: text content */}
          <div className="text-left">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Partnerships
            </h2>
            <p className="text-lg text-gray-600 leading-relaxed mb-8 max-w-xl">
              KarobarOne partners with India&apos;s leading payment gateways,
              logistics providers, marketing platforms, and business tools. We
              help ambitious Indian entrepreneurs build a complete commerce
              ecosystem by connecting with partners that drive innovation,
              reliability, and growth at every step of their journey.
            </p>
            <Link
              href="/book-demo"
              className="inline-block bg-[#5b4ef9] text-white px-8 py-4 rounded-lg font-semibold hover:bg-[#4a3ee0] transition-colors"
            >
              Learn More
            </Link>
          </div>

          {/* Right: vertical auto-scrolling logo marquee, pauses on hover */}
          <div className="marquee-wrap grid grid-cols-2 md:grid-cols-4 gap-4">
            <MarqueeColumn items={COLUMN_1} direction="up" duration={22} />
            <MarqueeColumn items={COLUMN_2} direction="down" duration={28} />
            <MarqueeColumn items={COLUMN_3} direction="up" duration={26} />
            <MarqueeColumn items={COLUMN_4} direction="down" duration={20} />
          </div>
        </div>
      </div>

      <style jsx global>{`
        @keyframes marquee-up {
          from {
            transform: translateY(0);
          }
          to {
            transform: translateY(-50%);
          }
        }
        @keyframes marquee-down {
          from {
            transform: translateY(-50%);
          }
          to {
            transform: translateY(0);
          }
        }
        .animate-marquee-up {
          animation-name: marquee-up;
          animation-timing-function: linear;
          animation-iteration-count: infinite;
        }
        .animate-marquee-down {
          animation-name: marquee-down;
          animation-timing-function: linear;
          animation-iteration-count: infinite;
        }
        .marquee-wrap:hover .animate-marquee-up,
        .marquee-wrap:hover .animate-marquee-down {
          animation-play-state: paused;
        }
      `}</style>
    </section>
  );
}