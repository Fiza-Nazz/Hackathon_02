import React from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Github, Twitter, Linkedin, ExternalLink, Globe, Shield, Zap } from 'lucide-react';

const Footer: React.FC = () => {
    const socialLinks = [
        { name: 'Twitter', icon: Twitter, url: 'https://x.com/FizaNazzx' },
        { name: 'GitHub', icon: Github, url: 'https://github.com/Fiza-Nazz' },
        { name: 'LinkedIn', icon: Linkedin, url: 'https://www.linkedin.com/in/fiza-nazz-765241355/' },
    ];

    return (
        <footer className="relative bg-black border-t border-white/5 pt-20 pb-10 overflow-hidden">
            {/* Background Glow */}
            <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-full h-[300px] bg-electric-blue/5 blur-[120px] rounded-full pointer-events-none" />

            <div className="max-w-7xl mx-auto px-6 md:px-12 relative z-10">
                <div className="grid grid-cols-1 lg:grid-cols-4 gap-16 mb-20">
                    {/* Brand Section */}
                    <div className="lg:col-span-2">
                        <Link href="/" className="flex items-center space-x-3 group mb-8">
                            <div className="w-10 h-10 bg-electric-blue rounded-xl flex items-center justify-center shadow-glow rotate-3 group-hover:rotate-0 transition-transform duration-500">
                                <span className="text-black font-black text-xl">T</span>
                            </div>
                            <span className="text-white font-black text-2xl tracking-tighter">
                                TODO<span className="text-electric-blue">AI</span>
                            </span>
                        </Link>
                        <p className="text-gray-500 text-lg max-w-sm leading-relaxed mb-8">
                            Experience the next evolution of productivity. Our neural-driven engine is designed for those who demand <span className="text-white font-bold">extreme precision</span> and elite performance.
                        </p>
                        <div className="flex items-center space-x-4">
                            {socialLinks.map((social) => (
                                <motion.a
                                    key={social.name}
                                    href={social.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    whileHover={{ y: -5, scale: 1.1 }}
                                    className="p-3 bg-white/5 border border-white/10 rounded-xl text-gray-400 hover:text-electric-blue hover:border-electric-blue/50 transition-colors"
                                >
                                    <social.icon size={20} />
                                </motion.a>
                            ))}
                        </div>
                    </div>

                    {/* Navigation */}
                    <div>
                        <h4 className="text-white font-black text-xs uppercase tracking-[0.3em] mb-8">Ecosystem</h4>
                        <ul className="space-y-4">
                            {[
                                { name: 'Neural Home', href: '/' },
                                { name: 'Control Center', href: '/dashboard' },
                                { name: 'Authentication', href: '/login' },
                                { name: 'Join Network', href: '/register' },
                            ].map((link) => (
                                <li key={link.name}>
                                    <Link
                                        href={link.href}
                                        className="text-gray-500 hover:text-electric-blue text-sm font-medium transition-all flex items-center group"
                                    >
                                        <span className="w-0 group-hover:w-4 h-px bg-electric-blue mr-0 group-hover:mr-2 transition-all duration-300" />
                                        {link.name}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    </div>

                    {/* Meta */}
                    <div>
                        <h4 className="text-white font-black text-xs uppercase tracking-[0.3em] mb-8">Integrity</h4>
                        <div className="space-y-6">
                            <div className="flex items-center space-x-3 text-gray-500 hover:text-white transition-colors cursor-default">
                                <Shield size={18} className="text-electric-blue" />
                                <span className="text-sm font-medium uppercase tracking-widest text-[10px]">Vault Secured</span>
                            </div>
                            <div className="flex items-center space-x-3 text-gray-500 hover:text-white transition-colors cursor-default">
                                <Zap size={18} className="text-electric-blue" />
                                <span className="text-sm font-medium uppercase tracking-widest text-[10px]">Zero Latency</span>
                            </div>
                            <div className="flex items-center space-x-3 text-gray-500 hover:text-white transition-colors cursor-default">
                                <Globe size={18} className="text-electric-blue" />
                                <span className="text-sm font-medium uppercase tracking-widest text-[10px]">Global Sync</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Bottom Bar */}
                <div className="pt-10 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-6">
                    <div className="flex items-center space-x-2 text-[10px] font-black uppercase tracking-[0.4em] text-gray-600">
                        <span>© 2026 TODOAI ENGINE</span>
                        <span className="text-electric-blue/30">•</span>
                        <span>DESIGNED BY FIZA NAZZ</span>
                    </div>

                    <div className="flex items-center space-x-6 text-[10px] font-black uppercase tracking-[0.2em] text-gray-600">
                        <a href="#" className="hover:text-electric-blue transition-colors">Privacy Protcol</a>
                        <a href="#" className="hover:text-electric-blue transition-colors">Neural Terms</a>
                        <div className="flex items-center text-electric-blue shadow-glow px-3 py-1 bg-electric-blue/10 rounded-full border border-electric-blue/20">
                            <div className="w-1 h-1 rounded-full bg-electric-blue animate-pulse mr-2" />
                            SYSTEMS NOMINAL
                        </div>
                    </div>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
