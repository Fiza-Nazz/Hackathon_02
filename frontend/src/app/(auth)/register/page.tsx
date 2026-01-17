'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import dynamic from 'next/dynamic';
import { useAuth } from '@/store/auth';
import Register from '@/components/auth/Register';
import Layout from '@/components/layout/Layout';
import Link from 'next/link';

const LoginCanvas = dynamic(() => import('@/components/home/LoginCanvas'), { ssr: false });

export default function RegisterPage() {
    const router = useRouter();
    const { isAuthenticated } = useAuth();

    // If already authenticated, redirect to dashboard
    React.useEffect(() => {
        if (isAuthenticated) {
            router.push('/dashboard');
        }
    }, [isAuthenticated, router]);

    if (isAuthenticated) {
        return null;
    }

    return (
        <Layout>
            <div className="relative min-h-[90vh] flex items-center justify-center overflow-hidden">
                {/* Reuse LoginCanvas or similar 3D background */}
                <LoginCanvas />

                <div className="max-w-6xl w-full px-6 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center z-10">
                    <motion.div
                        initial={{ opacity: 0, x: -30 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.8 }}
                        className="hidden lg:block"
                    >
                        <h1 className="text-7xl font-black uppercase tracking-tighter leading-none mb-6">
                            JOIN THE <span className="text-electric-blue electric-glow">NETWORK</span>
                        </h1>
                        <p className="text-gray-500 text-lg max-w-sm leading-relaxed">
                            Create your profile to start managing tasks with AI precision and stunning 3D interfaces.
                        </p>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="w-full max-w-md mx-auto"
                    >
                        <div className="glass-morphism p-10 rounded-[2.5rem] electric-border bg-white/[0.03]">
                            <Register />

                            <div className="text-center mt-8">
                                <p className="text-[10px] text-gray-500 uppercase tracking-[0.3em] font-black">
                                    ALREADY INTEGRATED?{' '}
                                    <Link
                                        href="/login"
                                        className="text-electric-blue hover:text-white transition-colors border-b border-electric-blue/30"
                                    >
                                        LOGIN
                                    </Link>
                                </p>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </div>
        </Layout>
    );
}
