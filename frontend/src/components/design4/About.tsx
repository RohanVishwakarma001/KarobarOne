"use client";

import { motion } from "framer-motion";
const bgImage = "/assets/design4/about.webp";
// Data
const stats = [
  ["14+", "Countries"],
  ["2,400", "Employees"],
  ["₹840Cr", "Revenue"],
  ["16yrs", "Experience"],
];

const missionVisionItems = [
  [
    "Mission",
    "teal",
    "To deliver transformative technology solutions with integrity and innovation.",
  ],
  [
    "Vision",
    "teal",
    "Most trusted tech partner in Asia by 2030, creating lasting value.",
  ],
  [
    "Values",
    "cyan",
    "Integrity. Innovation. Impact — measured by lives improved.",
  ],
  [
    "Commitment",
    "cyan",
    "Carbon neutral by 2027. 1% profits to rural digital literacy.",
  ],
];

const awards = [
  [
    "✅",
    "ISO 9001:2015 — Quality Management",
    "Certified since 2011 · Renewed 2024",
  ],
  ["🔒", "ISO 27001 — Information Security", "All data centres · 2023"],
  ["🌿", "GreenTech Sustainability Award", "CII National Awards · 2022 & 2024"],
  [
    "⭐",
    "Great Place to Work® Certified",
    "Top 50 Best Workplaces in Tech · 2024",
  ],
];

const AboutCompanyContent = () => (
  <>
    <p className="text-sm text-slate-300/70 leading-relaxed">
      Founded in 2008, Nexora Solutions operates across 14 countries, delivering
      cutting-edge technology that empowers businesses and communities alike.
    </p>
    <div className="flex gap-5 mt-4 pt-4 h-28 border-t border-white/[0.07]">
      {stats.map(([n, l]) => (
        <div key={l}>
          <div className="text-lg font-bold text-slate-100">{n}</div>
          <div className="text-[10px] text-slate-400/50 mt-0.5">{l}</div>
        </div>
      ))}
    </div>
  </>
);

const PromoterContent = () => (
  <>
    <div className="flex items-center gap-3 mb-3">
      <div
        className="w-12 h-12 rounded-full flex items-center justify-center font-bold text-white shrink-0"
        style={{ background: "linear-gradient(135deg,#b06fff,#ff6fb0)" }}
      >
        AR
      </div>
      <div>
        <p className="text-sm font-medium text-slate-100">Arjun Raghavan</p>
        <p className="text-[11px] text-slate-400/50">Founder & Chairman</p>
      </div>
    </div>
    <p className="text-sm text-slate-300/70 leading-relaxed">
      25+ years in technology & infrastructure. IIT Bombay · Harvard Business
      School. Forbes Asia Power Leaders — three consecutive years.
    </p>
    <p className="mt-3 text-xs italic text-purple-200/45">
      "Growth without purpose is just noise. We build to matter."
    </p>
  </>
);

const MissionVisionContent = () => (
  <div className="grid grid-cols-2 gap-2">
    {missionVisionItems.map(([h, c, t]) => (
      <div
        key={h}
        className={`rounded-xl p-3 bg-${c}-400/[0.07] border border-slate-400/20`}
      >
        <p className={`text-[10px] font-medium text-white mb-1`}>{h}</p>
        <p className="text-[11px] text-slate-300/60 leading-relaxed">{t}</p>
      </div>
    ))}
  </div>
);

const CertificatesContent = () => (
  <div className="flex flex-col gap-2">
    {awards.map(([ic, n, d]) => (
      <div
        key={n}
        className="flex items-center gap-3 rounded-xl px-3 py-2.5 bg-amber-400/[0.06] border border-amber-400/[0.18]"
      >
        <span className="text-base w-8 h-8 flex items-center justify-center rounded-lg bg-amber-400/10 shrink-0">
          {ic}
        </span>
        <div>
          <p className="text-[12px] font-medium text-slate-100">{n}</p>
          <p className="text-[10px] text-amber-200/40">{d}</p>
        </div>
      </div>
    ))}
  </div>
);

const cards = [
  {
    id: "01",
    label: "About",
    icon: "🏢",
    accent: "#4a9eff",
    bg: "rgba(20,28,58,0.85)",
    title: "About the Company",
    content: <AboutCompanyContent />,
  },
  {
    id: "02",
    label: "Leadership",
    icon: "👤",
    accent: "#b06fff",
    bg: "rgba(28,20,48,0.85)",
    title: "About the Promoter",
    content: <PromoterContent />,
  },
  {
    id: "03",
    label: "Purpose",
    icon: "🎯",
    accent: "#00d4aa",
    bg: "rgba(15,35,40,0.85)",
    title: "Mission & Vision",
    content: <MissionVisionContent />,
  },
  {
    id: "04",
    label: "Accreditation",
    icon: "🏆",
    accent: "#ffaa44",
    bg: "rgba(35,22,15,0.85)",
    title: "Certificates & Awards",
    content: <CertificatesContent />,
  },
];

//Card
function Card({ card, index }: any) {
  return (
    <motion.div
      id="about"
      initial={{ opacity: 0, y: 64 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: false, amount: 0.25 }}
      transition={{
        duration: 0.7,
        delay: index * 0.08,
        ease: [0.22, 1, 0.36, 1],
      }}
      className="relative rounded-2xl p-6 border border-white/10 overflow-hidden w-full"
      style={{ background: card.bg, backdropFilter: "blur(16px)" }}
    >
      {/* Top accent bar */}
      <div
        className="absolute top-0 left-0 right-0 h-[3px] rounded-t-2xl"
        style={{
          background: `linear-gradient(90deg,${card.accent},${card.accent}66)`,
        }}
      />

      <p
        className="text-[10px] font-medium tracking-[2px] uppercase mb-1.5"
        style={{ color: card.accent }}
      >
        {card.id} — {card.label}
      </p>
      <h2 className="text-xl font-bold text-slate-100 mb-4">{card.title}</h2>
      {card.content}
    </motion.div>
  );
}

//Main
export default function About() {
  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?500&display=swap');
        .pulse{animation:pulse 2s infinite}
      `}</style>

      <section
        id="about"
        className="relative overflow-hidden min-h-screen py-5"
        style={{
          backgroundImage: `url(${bgImage})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          backgroundRepeat: "no-repeat",
          backgroundAttachment: "fixed",
        }}
      >
        {/* ── Fixed business background ── */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute inset-0 bg-slate-950/60" />
        </div>

        {/* ── Scroll content ── */}
        <div className="relative z-10 flex flex-col items-center gap-14 px-5 pt-14 pb-24">
          {/* Hero header */}
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
            className="text-center"
          >
            <h1 className="text-4xl font-bold text-slate-100 mb-2">
              Our Story
            </h1>
            <p className="pulse text-[11px] tracking-widest text-slate-400/35">
              ▼ scroll ▼
            </p>
          </motion.div>

          <div className="grid w-full md:w-[1000px] grid-cols-1 gap-8 sm:grid-cols-2">
            {cards.map((card, i) => (
              <Card key={card.id} card={card} index={i} />
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
