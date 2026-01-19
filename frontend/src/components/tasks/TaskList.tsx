'use client';
import React, { useEffect } from 'react';
import { useTasks } from '@/store/tasks';
import { useAuth } from '@/store/auth';
import { motion, AnimatePresence } from 'framer-motion';
import TaskItem from './TaskItem';
import { Loader2, Inbox } from 'lucide-react';

const TaskList: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const { tasks, loading, error, fetchTasks } = useTasks();

  useEffect(() => {
    if (isAuthenticated) {
      fetchTasks();

      // Auto-refresh every 3 seconds when page is visible
      const refreshInterval = setInterval(() => {
        if (!document.hidden) {
          fetchTasks();
        }
      }, 3000);

      // Refresh when user comes back to this tab
      const handleVisibilityChange = () => {
        if (!document.hidden) {
          fetchTasks();
        }
      };
      document.addEventListener('visibilitychange', handleVisibilityChange);

      return () => {
        clearInterval(refreshInterval);
        document.removeEventListener('visibilitychange', handleVisibilityChange);
      };
    }
  }, [fetchTasks, isAuthenticated]);

  if (loading && tasks.length === 0) {
    return (
      <div className="flex flex-col justify-center items-center py-20 space-y-4">
        <Loader2 className="animate-spin text-electric-blue" size={40} />
        <p className="text-[10px] uppercase tracking-[0.3em] font-black text-gray-500">Syncing Neurons...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-500/10 border border-red-500/30 text-red-500 text-xs rounded-xl">
        Signal Error: {error}
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-20 flex flex-col items-center">
        <div className="w-16 h-16 bg-white/5 rounded-full flex items-center justify-center mb-6">
          <Inbox className="text-gray-600" size={24} />
        </div>
        <p className="text-gray-500 text-sm font-medium">Neural Log Empty. Initialize a new task entry.</p>
        <p className="text-[10px] text-gray-700 mt-2 font-mono">DEBUG: {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}</p>
      </div>
    );
  }

  return (
    <div className="w-full">
      <div className="space-y-4">
        <AnimatePresence mode="popLayout">
          {tasks.map((task, i) => (
            <motion.div
              key={task.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ delay: i * 0.05 }}
            >
              <TaskItem task={task} />
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
      <p className="text-[10px] text-gray-700 mt-8 font-mono text-center opacity-50">
        Connected to: {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'} | Tasks: {tasks.length}
      </p>
    </div>
  );
};

export default TaskList;