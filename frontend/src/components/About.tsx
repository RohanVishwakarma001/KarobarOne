import { Users, Award, TrendingUp, Heart } from "lucide-react";

export function About() {
  const stats = [
    { number: "5000+", label: "Brands Served" },
    { number: "₹500Cr+", label: "GMV Generated" },
    { number: "98%", label: "Customer Satisfaction" },
    { number: "48hrs", label: "Store Setup Time" },
  ];

  const values = [
    {
      icon: Heart,
      title: "Customer First",
      description: "Every decision we make is centered around helping our customers grow profitably.",
    },
    {
      icon: TrendingUp,
      title: "Growth Mindset",
      description: "We constantly innovate and evolve to stay ahead of the e-commerce curve.",
    },
    {
      icon: Users,
      title: "Team Spirit",
      description: "Our diverse team of experts works together to deliver exceptional results.",
    },
    {
      icon: Award,
      title: "Excellence",
      description: "We hold ourselves to the highest standards in everything we do.",
    },
  ];

  return (
    <section id="about" className="bg-white">

      {/* Hero */}
      <div className="bg-gradient-to-br from-[#5b4ef9] to-[#3b82f6] py-24">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <span className="inline-block bg-white/20 text-white text-sm font-semibold px-4 py-2 rounded-full mb-6">
            About Us
          </span>
          <h1 className="text-5xl font-bold text-white mb-6 leading-tight">
            We're on a Mission to Make<br />
            <span className="text-yellow-300">D2C Profitable for Everyone</span>
          </h1>
          <p className="text-xl text-white/90 max-w-3xl mx-auto leading-relaxed">
            KarobarOne was founded with a simple belief — every entrepreneur deserves
            access to enterprise-grade tools that actually drive profit, not just growth.
          </p>
        </div>
      </div>

      {/* Stats */}
      <div className="bg-gray-50 py-16">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <p className="text-4xl lg:text-5xl font-bold text-[#5b4ef9] mb-2">
                  {stat.number}
                </p>
                <p className="text-gray-600 font-medium">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Story */}
      <div className="py-24">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div>
              <span className="text-[#5b4ef9] font-semibold text-sm uppercase tracking-wider">
                Our Story
              </span>
              <h2 className="text-4xl font-bold text-gray-900 mt-3 mb-6 leading-tight">
                Born from the Struggles of D2C Entrepreneurs
              </h2>
              <p className="text-gray-600 text-lg leading-relaxed mb-6">
                Our founders experienced firsthand the challenges of running a D2C business —
                juggling multiple tools, paying hefty retainers, and still not seeing profits.
              </p>
              <p className="text-gray-600 text-lg leading-relaxed mb-8">
                That's why we built KarobarOne — an all-in-one platform that aligns
                its success with yours. We only win when you win.
              </p>
              <div className="flex items-center gap-4">
                <div className="h-1 w-12 bg-[#5b4ef9] rounded-full" />
                <p className="text-gray-500 italic">
                  "Profitability is not a luxury, it's a right."
                </p>
              </div>
            </div>
            <div className="relative">
              <div className="bg-gradient-to-br from-[#5b4ef9]/10 to-[#3b82f6]/10 rounded-3xl p-8">
                <img
                  src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=600&h=400&fit=crop"
                  alt="Team working"
                  className="rounded-2xl w-full shadow-lg"
                  crossOrigin="anonymous"
                />
              </div>
              <div className="absolute -bottom-6 -left-6 bg-white rounded-2xl p-4 shadow-xl border border-gray-100">
                <p className="text-3xl font-bold text-[#5b4ef9]">4+ Years</p>
                <p className="text-gray-600 text-sm">of empowering D2C brands</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Values */}
      <div className="bg-gray-50 py-24">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <span className="text-[#5b4ef9] font-semibold text-sm uppercase tracking-wider">
              Our Values
            </span>
            <h2 className="text-4xl font-bold text-gray-900 mt-3">
              What Drives Us Every Day
            </h2>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {values.map((value, index) => (
              <div
                key={index}
                className="bg-white rounded-2xl p-8 border border-gray-200 hover:shadow-lg hover:-translate-y-1 transition-all duration-300"
              >
                <div className="bg-[#5b4ef9]/10 w-14 h-14 rounded-xl flex items-center justify-center mb-6">
                  <value.icon className="w-7 h-7 text-[#5b4ef9]" />
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-3">{value.title}</h3>
                <p className="text-gray-600 leading-relaxed">{value.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="bg-gradient-to-br from-[#5b4ef9] to-[#3b82f6] py-20">
        <div className="max-w-3xl mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Grow Profitably?
          </h2>
          <p className="text-white/90 text-xl mb-10">
            Join 5000+ brands who trust KarobarOne to run their D2C business.
          </p>
          <button className="bg-white text-[#5b4ef9] px-10 py-4 rounded-xl font-bold text-lg hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
            Get Started for Free
          </button>
        </div>
      </div>

    </section>
  );
}