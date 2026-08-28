import { Rocket, Building2, Zap, Trophy } from "lucide-react";

export function Timeline() {
  const phases = [
    {
      icon: Rocket,
      phase: "Phase 1",
      title: "Launch",
      description: "Set up your online store with our ready-to-use templates and integrations within 48 hours.",
      highlight: false
    },
    {
      icon: Building2,
      phase: "Phase 2",
      title: "Build",
      description: "Customize your brand, add products, and configure payment and shipping options.",
      highlight: false
    },
    {
      icon: Zap,
      phase: "Phase 3",
      title: "Scale",
      description: "Deploy advanced marketing strategies, automation, and analytics to skyrocket your growth.",
      highlight: true
    },
    {
      icon: Trophy,
      phase: "Phase 4",
      title: "Dominate",
      description: "Become a market leader with our enterprise-grade tools and dedicated success team.",
      highlight: false
    }
  ];
  
  return (
    <section className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Your Growth Journey</h2>
          <p className="text-xl text-gray-600">From zero to hero in 4 simple phases</p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {phases.map((phase, index) => (
            <div
              key={index}
              className={`rounded-2xl p-8 ${
                phase.highlight
                  ? "bg-gradient-to-br from-blue-500 to-blue-600 text-white shadow-xl"
                  : "bg-white border border-gray-200"
              }`}
            >
              <div className={`w-14 h-14 rounded-xl flex items-center justify-center mb-6 ${
  phase.highlight ? "bg-white/20" : "bg-[#5b4ef9]/10"
}`}>
                <phase.icon className={`w-7 h-7 ${
                  phase.highlight ? "text-white" : "text-[#5b4ef9]"
                }`} />
              </div>
              <div className={`text-sm font-semibold mb-2 ${
                phase.highlight ? "text-white/80" : "text-[#5b4ef9]"
              }`}>
                {phase.phase}
              </div>
              <h3 className={`text-xl font-bold mb-3 ${
                phase.highlight ? "text-white" : "text-gray-900"
              }`}>
                {phase.title}
              </h3>
              <p className={phase.highlight ? "text-white/90" : "text-gray-600"}>
                {phase.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
