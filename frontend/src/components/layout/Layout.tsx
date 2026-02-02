'use client';
import React, { ReactNode } from 'react';
import Navbar from './Navbar';
import Footer from './Footer';
import { motion, AnimatePresence } from 'framer-motion';

interface LayoutProps {
    children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
    return (
        <div className="min-h-screen bg-black text-white selection:bg-electric-blue selection:text-black">
            {/* Dynamic Background */}
            <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
                <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-electric-blue/5 blur-[120px] rounded-full" />
                <div className="absolute bottom-[-10%] right-[-10%] w-[30%] h-[30%] bg-electric-blue/10 blur-[100px] rounded-full" />
            </div>

            <Navbar />

            <main className="relative z-10 pt-24 min-h-[calc(100-300px)]">
                <AnimatePresence mode="wait">
                    <motion.div
                        initial={{ opacity: 0, y: 20, scale: 0.98 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: -20, scale: 0.98 }}
                        transition={{
                            duration: 0.6,
                            ease: [0.16, 1, 0.3, 1] // Custom premium easing
                        }}
                    >
                        {children}
                    </motion.div>
                </AnimatePresence>
            </main>

            <Footer />
        </div>
    );
};

export default Layout;
