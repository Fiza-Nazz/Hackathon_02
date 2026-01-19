import React from 'react';
import Head from 'next/head';
import { motion } from 'framer-motion';
import { ArrowRight, CheckCircle2, Sparkles, Zap, Shield, Globe } from 'lucide-react';
import dynamic from 'next/dynamic';
import Layout from '@/components/layout/Layout';
import Link from 'next/link';

const HeroCanvas = dynamic(() => import('@/components/home/HeroCanvas'), { ssr: false });


const HomePage: React.FC = () => {
  return (
    <Layout>
      <Head>
        <title>TODOAI | Premium AI-Native Productivity</title>
        <meta name="description" content="Experience the extreme level of productivity with our AI-native todo application." />
      </Head>

      {/* Hero Section */}
      <section className="relative overflow-hidden min-h-[90vh] flex items-center">
        <div className="max-w-7xl mx-auto px-6 md:px-12 grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="z-10"
          >
            <div className="inline-flex items-center space-x-2 bg-white/5 border border-white/10 px-4 py-2 rounded-full mb-6">
              <Sparkles className="text-electric-blue w-4 h-4" />
              <span className="text-[10px] uppercase tracking-[0.2em] text-gray-400 font-bold">Evolutionizing Task Management</span>
            </div>

            <h1 className="text-6xl md:text-8xl font-black leading-tight mb-6">
              WORK <br />
              <span className="electric-glow text-electric-blue">SMARTER</span>
            </h1>

            <p className="text-xl text-gray-400 mb-10 max-w-lg leading-relaxed">
              Design your day with extreme precision. The world's first todo engine built with high-standard 3D aesthetics and AI intelligence.
            </p>

            <div className="flex flex-col sm:row items-center space-y-4 sm:space-y-0 sm:space-x-6">
              <Link href="/register" className="w-full sm:w-auto px-8 py-4 bg-electric-blue text-black font-bold rounded-lg hover:shadow-glow-lg transition-all duration-300 flex items-center justify-center space-x-2">
                <span>Start Building Now</span>
                <ArrowRight size={20} />
              </Link>
              <Link href="#features" className="w-full sm:w-auto px-8 py-4 bg-transparent border border-white/10 text-white font-bold rounded-lg hover:bg-white/5 transition-all duration-300">
                Explore Features
              </Link>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1 }}
            className="relative h-full"
          >
            <HeroCanvas />
          </motion.div>
        </div>
      </section>

      {/* Feature Page Section (Second "Page") */}
      <section id="features" className="py-24 relative">
        <div className="max-w-7xl mx-auto px-6 md:px-12">
          <div className="text-center mb-20">
            <h2 className="text-4xl md:text-6xl font-black mb-6 uppercase">Extreme <span className="text-electric-blue">Utility</span></h2>
            <p className="text-gray-500 max-w-2xl mx-auto text-lg">Precision engineering meets aesthetic perfection. Every interaction is designed to feel premium.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { title: "AI Insights", desc: "Automated task prioritization using advanced neural engines for elite decision making.", icon: Zap },
              { title: "Vault-Grade", desc: "Your data is secured with industrial encryption standards and biometric-level security.", icon: Shield },
              { title: "Global Sync", desc: "Real-time synchronization across all your professional devices with zero-latency protocols.", icon: Globe },
            ].map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                whileHover={{
                  scale: 1.05,
                  rotateY: 5,
                  rotateX: -5,
                  z: 50
                }}
                transition={{
                  delay: i * 0.1,
                  type: "spring",
                  stiffness: 300,
                  damping: 20
                }}
                className="glass-morphism p-10 rounded-[2.5rem] electric-border group perspective-1000 cursor-default bg-white/[0.02]"
              >
                <div className="w-16 h-16 bg-white/5 rounded-2xl flex items-center justify-center mb-8 group-hover:bg-electric-blue group-hover:shadow-glow transition-all duration-500">
                  <feature.icon className="text-electric-blue group-hover:text-black transition-colors" size={32} />
                </div>
                <h3 className="text-2xl font-black mb-4 uppercase tracking-tight">{feature.title}</h3>
                <p className="text-gray-500 leading-relaxed text-sm font-medium">{feature.desc}</p>

                <div className="mt-8 opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                  <div className="h-0.5 w-12 bg-electric-blue shadow-glow" />
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Showcase Page Section (Third "Page") */}
      <section className="py-24 bg-white/[0.02] border-y border-white/5 relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-6 md:px-12 grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9, rotateY: -10 }}
            whileInView={{ opacity: 1, scale: 1, rotateY: 0 }}
            whileHover={{ scale: 1.02, rotateX: 5 }}
            transition={{ duration: 1 }}
            className="order-2 lg:order-1 perspective-1000"
          >
            <div className="aspect-video glass-morphism rounded-[3rem] overflow-hidden electric-border flex items-center justify-center bg-white/[0.01] relative group">
              <div className="absolute inset-0 bg-gradient-to-br from-electric-blue/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
              <div className="text-center relative z-10">
                <motion.div
                  animate={{
                    y: [0, -10, 0],
                    scale: [1, 1.1, 1]
                  }}
                  transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                >
                  <CheckCircle2 className="text-electric-blue w-24 h-24 mx-auto mb-6 shadow-glow" />
                </motion.div>
                <p className="text-[12px] uppercase tracking-[0.5em] font-black text-gray-500 group-hover:text-white transition-colors">Neural Stream Active</p>
              </div>
            </div>
          </motion.div>

          <div className="order-1 lg:order-2">
            <h2 className="text-4xl md:text-5xl font-black mb-8 uppercase leading-tight">
              A New Era of <br />
              <span className="text-electric-blue">Performance</span>
            </h2>
            <div className="space-y-6">
              {[
                "Instant task categorization with zero latency.",
                "Hyper-focused interface minimizes cognitive load.",
                "Custom 3D avatars for professional identity."
              ].map((item, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: 20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.1 }}
                  className="flex items-start space-x-4"
                >
                  <div className="w-6 h-6 rounded-full bg-electric-blue/20 flex items-center justify-center mt-1">
                    <div className="w-2 h-2 rounded-full bg-electric-blue" />
                  </div>
                  <p className="text-gray-400">{item}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Final Call to Action */}
      <section className="py-32 text-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          className="max-w-4xl mx-auto px-6"
        >
          <h2 className="text-5xl md:text-7xl font-black mb-12">REACH THE <br /><span className="text-electric-blue">APEX</span></h2>
          <Link href="/register" className="inline-flex px-12 py-5 bg-white text-black font-black text-xl rounded-full hover:bg-electric-blue transition-colors duration-300 scale-100 hover:scale-105 active:scale-95">
            JOIN NOW
          </Link>
        </motion.div>
      </section>
    </Layout>
  );
};

export default HomePage;