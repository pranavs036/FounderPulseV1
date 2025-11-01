import { Link } from "react-router-dom";
import { motion, useReducedMotion, useScroll, useTransform } from "framer-motion";
import { useState, useEffect } from "react";

const ease = [0.16, 1, 0.3, 1];

function AnimatedBackground() {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden">
      <div
        className="absolute inset-0 opacity-60"
        style={{
          background: `
            linear-gradient(135deg, #0D1117 0%, #11131A 50%, #0D1117 100%),
            radial-gradient(ellipse at 20% 20%, rgba(99,102,241,0.1) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 80%, rgba(124,58,237,0.1) 0%, transparent 50%)
          `,
          backgroundSize: '200% 200%',
          animation: 'diagonal-shimmer 20s ease-in-out infinite',
        }}
      />
    </div>
  );
}

function StickyNavbar({ scrolled }) {
  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.6, ease }}
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled 
          ? 'backdrop-blur-nav bg-[#0D1117]/80 border-b border-white/5' 
          : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="text-2xl font-bold text-white tracking-tight">
            North Star
          </div>

          {/* Center Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <a href="#product" className="text-[#F3F4F6]/80 hover:text-white transition-colors">
              Product
            </a>
            <a href="#how-it-works" className="text-[#F3F4F6]/80 hover:text-white transition-colors">
              How it works
            </a>
            <a href="#pricing" className="text-[#F3F4F6]/80 hover:text-white transition-colors">
              Pricing
            </a>
            <a href="#resources" className="text-[#F3F4F6]/80 hover:text-white transition-colors">
              Resources
            </a>
          </nav>

          {/* Right Actions */}
          <div className="flex items-center space-x-4">
            <Link
              to="/signin"
              className="text-[#F3F4F6]/80 hover:text-white transition-colors"
            >
              Sign In
            </Link>
            <Link
              to="/signup"
              className="px-4 py-2 rounded-lg bg-[#6366F1] text-white font-medium hover:glow-indigo-intense transition-all duration-300 hover:scale-105"
            >
              Sign Up
            </Link>
          </div>
        </div>
      </div>
    </motion.header>
  );
}

function HeroSection() {
  return (
    <section className="min-h-screen flex items-center justify-center relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-6 text-center">
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease, delay: 0.1 }}
          className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight"
        >
          From data chaos to{" "}
          <span className="bg-gradient-to-r from-[#6366F1] to-[#7C3AED] bg-clip-text text-transparent">
            decisive action
          </span>
          .
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease, delay: 0.2 }}
          className="text-xl md:text-2xl text-[#F3F4F6]/80 mb-12 max-w-4xl mx-auto leading-relaxed"
        >
          North Star unifies your tools, surfaces real-time signals, and tells teams exactly what to do next.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, ease, delay: 0.3 }}
        >
          <Link
            to="/signup"
            className="inline-flex items-center px-8 py-4 rounded-xl bg-[#6366F1] text-white font-semibold text-lg hover:glow-indigo-intense transition-all duration-300 hover:scale-105"
          >
            Get Started
          </Link>
        </motion.div>
      </div>
    </section>
  );
}

function UseCaseCards() {
  const cards = [
    {
      title: "For Operators",
      description: "Spot bottlenecks, track key metrics, and align execution in real time.",
      features: ["Real-time monitoring", "Automated alerts", "Team coordination"]
    },
    {
      title: "For Leaders", 
      description: "Get visibility across spend, growth, and impact — all in one place.",
      features: ["Executive dashboards", "ROI tracking", "Strategic insights"]
    }
  ];

  return (
    <section id="product" className="py-24 bg-[#11131A]">
      <div className="max-w-7xl mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6, ease }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Discover how North Star powers your growth.
          </h2>
          <p className="text-xl text-[#F3F4F6]/80 max-w-3xl mx-auto">
            Purpose-built for teams that need real-time clarity and faster execution.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8">
          {cards.map((card, index) => (
            <motion.div
              key={card.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ duration: 0.6, ease, delay: index * 0.1 }}
              className="group relative"
            >
              <div className="relative p-8 rounded-3xl bg-[#0D1117]/50 border border-[#6366F1]/20 hover:border-[#6366F1]/40 transition-all duration-300 hover:-translate-y-1 hover:glow-indigo">
                <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-[#6366F1]/5 to-[#7C3AED]/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                
                <div className="relative z-10">
                  <h3 className="text-2xl font-bold text-white mb-4">{card.title}</h3>
                  <p className="text-[#F3F4F6]/80 mb-6 text-lg leading-relaxed">
                    {card.description}
                  </p>
                  
                  <ul className="space-y-2">
                    {card.features.map((feature, i) => (
                      <li key={i} className="flex items-center text-[#F3F4F6]/70">
                        <div className="w-2 h-2 rounded-full bg-[#6366F1] mr-3" />
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

function HowItWorks() {
  const steps = [
    {
      number: "01",
      title: "Connect your data",
      description: "Integrate Mixpanel, Jira, Sheets, CRMs and all your data sources in minutes."
    },
    {
      number: "02", 
      title: "Get AI insights",
      description: "Anomalies, correlations, and next-best actions appear instantly with AI analysis."
    },
    {
      number: "03",
      title: "Act faster", 
      description: "Trigger tasks, messages, or campaigns right from insights with one click."
    }
  ];

  return (
    <section id="how-it-works" className="py-24 bg-[#0D1117]">
      <div className="max-w-7xl mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6, ease }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            How it works
          </h2>
          <p className="text-xl text-[#F3F4F6]/80 max-w-3xl mx-auto">
            Three simple steps to turn fragmented data into action.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8">
          {steps.map((step, index) => (
            <motion.div
              key={step.number}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ duration: 0.6, ease, delay: index * 0.15 }}
              className="text-center"
            >
              <div className="relative mb-8">
                <div className="relative w-20 h-20 mx-auto">
                  <div className="absolute inset-0 rounded-full bg-gradient-to-r from-[#6366F1] to-[#7C3AED] p-0.5">
                    <div className="w-full h-full rounded-full bg-[#0D1117] flex items-center justify-center">
                      <span className="text-2xl font-bold text-white">{step.number}</span>
                    </div>
                  </div>
                  <div 
                    className="absolute inset-0 rounded-full border-2 border-[#6366F1]/30 animate-pulse"
                    style={{
                      animation: 'pulse-ring 2s cubic-bezier(0.16, 1, 0.3, 1) infinite',
                      animationDelay: `${index * 0.5}s`
                    }}
                  />
                </div>
              </div>
              
              <h3 className="text-2xl font-bold text-white mb-4">{step.title}</h3>
              <p className="text-[#F3F4F6]/80 text-lg leading-relaxed">
                {step.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

function FinalCTA() {
  return (
    <section id="contact" className="py-24 landing-gradient">
      <div className="max-w-7xl mx-auto px-6 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6, ease }}
        >
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Ready to turn your data into action?
          </h2>
          <p className="text-xl text-white/90 mb-12 max-w-3xl mx-auto">
            Book a demo and see how North Star can power your team.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/signup"
              className="px-8 py-4 rounded-xl bg-white text-[#6366F1] font-semibold text-lg hover:bg-white/90 transition-all duration-300 hover:scale-105"
            >
              Get Started
            </Link>
            <Link
              to="/signin"
              className="px-8 py-4 rounded-xl border-2 border-white text-white font-semibold text-lg hover:bg-white hover:text-[#6366F1] transition-all duration-300 hover:scale-105"
            >
              Sign In
            </Link>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

export default function Landing() {
  const [scrolled, setScrolled] = useState(false);
  const { scrollY } = useScroll();
  const reduce = useReducedMotion();

  useEffect(() => {
    const unsubscribe = scrollY.onChange((latest) => {
      setScrolled(latest > 50);
    });
    return () => unsubscribe();
  }, [scrollY]);

  return (
    <div className="min-h-screen bg-[#0D1117] text-[#F3F4F6]">
      <AnimatedBackground />
      <StickyNavbar scrolled={scrolled} />
      <HeroSection />
      <UseCaseCards />
      <HowItWorks />
      <FinalCTA />
    </div>
  );
}
