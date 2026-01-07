import React, { useEffect } from 'react';
import Head from 'next/head';
import { motion } from 'framer-motion';
import { useRouter } from 'next/router';
import dynamic from 'next/dynamic';
import { useAuth } from '@/store/auth';
import TaskList from '@/components/tasks/TaskList';
import CreateTask from '@/components/tasks/CreateTask';
import Layout from '@/components/layout/Layout';
import { LayoutDashboard, Plus, Settings, User as UserIcon } from 'lucide-react';

const DashboardBackground = dynamic(() => import('@/components/layout/DashboardBackground'), { ssr: false });

const DashboardPage: React.FC = () => {
  const router = useRouter();
  const { isAuthenticated, user, checkAuthStatus, loading } = useAuth();

  useEffect(() => {
    checkAuthStatus();
  }, [checkAuthStatus]);

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, loading, router]);

  if (loading || !isAuthenticated) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex flex-col items-center space-y-4"
        >
          <div className="w-12 h-12 border-2 border-electric-blue/30 border-t-electric-blue rounded-full animate-spin" />
          <p className="text-[10px] uppercase tracking-[0.4em] font-black text-electric-blue animate-pulse">Neural Handshake...</p>
        </motion.div>
      </div>
    );
  }

  return (
    <Layout>
      <Head>
        <title>Dashboard | TODOAI</title>
      </Head>

      {/* 3D Neural Grid Background */}
      <DashboardBackground />

      <div className="max-w-7xl mx-auto px-6 md:px-12 py-12 relative">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-16 space-y-8 md:space-y-0">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <div className="flex items-center space-x-2 text-electric-blue mb-4">
              <div className="p-2 bg-electric-blue/10 rounded-lg">
                <LayoutDashboard size={18} />
              </div>
              <span className="text-[10px] uppercase tracking-[0.5em] font-black">Operator Core</span>
            </div>
            <h1 className="text-5xl md:text-6xl font-black uppercase tracking-tight leading-none">
              NEURAL <br />
              <span className="text-electric-blue electric-glow">DASHBOARD</span>
            </h1>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center space-x-6 bg-white/[0.03] border border-white/10 p-4 rounded-2xl backdrop-blur-xl"
          >
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-electric-blue/20 rounded-xl flex items-center justify-center border border-electric-blue/30">
                <UserIcon size={20} className="text-electric-blue" />
              </div>
              <div className="flex flex-col">
                <span className="text-[10px] uppercase tracking-widest font-black text-gray-500">Active Operator</span>
                <span className="text-sm font-bold text-white">{user?.email?.split('@')[0] || 'Unknown'}</span>
              </div>
            </div>
            <div className="h-10 w-px bg-white/10 mx-2" />
            <button className="p-2 hover:bg-white/5 rounded-lg transition-colors text-gray-400 hover:text-white">
              <Settings size={20} />
            </button>
          </motion.div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
          {/* Action Column */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="lg:col-span-4"
          >
            <div className="sticky top-28 space-y-8">
              <div className="glass-morphism p-10 rounded-[2rem] electric-border bg-white/[0.02] relative overflow-hidden group">
                <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                  <Plus size={80} className="text-electric-blue" />
                </div>
                <h3 className="text-lg font-black uppercase tracking-widest mb-8 flex items-center space-x-3">
                  <span className="w-2 h-2 rounded-full bg-electric-blue shadow-glow" />
                  <span>Deploy Task</span>
                </h3>
                <CreateTask />
              </div>

              {/* Stats Card (Optional) */}
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.5 }}
                className="glass-morphism p-8 rounded-[2rem] border border-white/5 bg-white/[0.01] relative overflow-hidden group"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-electric-blue/5 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
                <p className="text-[10px] uppercase tracking-widest font-black text-gray-600 mb-2">Efficiency Rating</p>
                <div className="text-3xl font-black text-white group-hover:text-electric-blue transition-colors duration-500">98.4%</div>
                <div className="mt-4 w-full h-1 bg-white/5 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: "98.4%" }}
                    transition={{ duration: 1.5, delay: 0.8 }}
                    className="h-full bg-electric-blue shadow-glow"
                  />
                </div>
              </motion.div>
            </div>
          </motion.div>

          {/* Data Column */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="lg:col-span-8"
          >
            <div className="glass-morphism p-10 rounded-[2.5rem] min-h-[700px] border border-white/5 bg-white/[0.02] backdrop-blur-3xl relative overflow-hidden">
              {/* Scanning Line Animation */}
              <motion.div
                animate={{ y: ["0%", "1000%"] }}
                transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
                className="absolute top-0 left-0 right-0 h-px bg-electric-blue/20 shadow-glow pointer-events-none"
              />

              <div className="flex items-center justify-between mb-12 relative z-10">
                <div className="space-y-1">
                  <h3 className="text-xl font-black uppercase tracking-widest text-white">Neural Task Log</h3>
                  <p className="text-[10px] uppercase tracking-[0.2em] font-bold text-gray-500">Real-time processing active</p>
                </div>
                <div className="flex items-center space-x-2 px-3 py-1 bg-electric-blue/10 border border-electric-blue/30 rounded-full">
                  <div className="w-1.5 h-1.5 rounded-full bg-electric-blue animate-pulse" />
                  <span className="text-[9px] font-black tracking-widest text-electric-blue">SYNCED</span>
                </div>
              </div>

              <TaskList />
            </div>
          </motion.div>
        </div>
      </div>
    </Layout>
  );
};

export default DashboardPage;