'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Sparkles, Zap, Shield, Globe } from 'lucide-react';
import dynamic from 'next/dynamic';
import Layout from '@/components/layout/Layout';
import Link from 'next/link';

const HeroCanvas = dynamic(() => import('@/components/home/HeroCanvas'), { ssr: false });

export default function HomePage() {
    return (
        <Layout>
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

                        <div className="flex flex-col sm:flex-row items-center space-y-4 sm:space-y-0 sm:space-x-6">
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

            {/* Feature Section */}
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
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>
        </Layout>
    );
}
