import React from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import { motion } from 'framer-motion';
import dynamic from 'next/dynamic';
import { useAuth } from '@/store/auth';
import Login from '@/components/auth/Login';
import Layout from '@/components/layout/Layout';
import Link from 'next/link';

const LoginCanvas = dynamic(() => import('@/components/home/LoginCanvas'), { ssr: false });

const LoginPage: React.FC = () => {
  const router = useRouter();
  const { isAuthenticated } = useAuth();

  // If already authenticated, redirect to dashboard
  if (typeof window !== 'undefined' && isAuthenticated) {
    router.push('/dashboard');
    return null;
  }

  return (
    <Layout>
      <Head>
        <title>Login | TODOAI</title>
      </Head>

      <div className="relative min-h-[90vh] flex items-center justify-center overflow-hidden">
        {/* Extreme 3D Background */}
        <LoginCanvas />

        <div className="max-w-6xl w-full px-6 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center z-10">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="hidden lg:block"
          >
            <h1 className="text-7xl font-black uppercase tracking-tighter leading-none mb-6">
              THE <span className="text-electric-blue electric-glow">APEX</span> <br />
              OF CONTROL
            </h1>
            <p className="text-gray-500 text-lg max-w-sm leading-relaxed">
              Login to access your high-frequency neural productivity engine. Optimized for extreme performance.
            </p>

            <div className="mt-12 flex space-x-4">
              {[1, 2, 3].map((i) => (
                <div key={i} className="w-12 h-1 bg-white/10 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ x: "-100%" }}
                    animate={{ x: "0%" }}
                    transition={{ duration: 2, delay: i * 0.5, repeat: Infinity }}
                    className="w-full h-full bg-electric-blue shadow-glow"
                  />
                </div>
              ))}
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full max-w-md mx-auto"
          >
            <div className="text-center lg:text-left mb-8 block lg:hidden">
              <h1 className="text-4xl font-black uppercase tracking-tighter electric-glow">
                ACCESS <span className="text-electric-blue">PORTAL</span>
              </h1>
            </div>

            <div className="glass-morphism p-10 rounded-[2.5rem] electric-border bg-white/[0.03]">
              <Login />

              <div className="text-center mt-8">
                <p className="text-[10px] text-gray-500 uppercase tracking-[0.3em] font-black">
                  NEW TO THE ECOSYSTEM?{' '}
                  <Link
                    href="/register"
                    className="text-electric-blue hover:text-white transition-colors border-b border-electric-blue/30"
                  >
                    REGISTER
                  </Link>
                </p>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </Layout>
  );
};

export default LoginPage;