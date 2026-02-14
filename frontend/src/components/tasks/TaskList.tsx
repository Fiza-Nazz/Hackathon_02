'use client';
import React, { useEffect, useState, useMemo } from 'react';
import { useTasks } from '@/store/tasks';
import { useAuth } from '@/store/auth';
import { motion, AnimatePresence } from 'framer-motion';
import TaskItem from './TaskItem';
import { Loader2, Inbox, Search, Filter, SortAsc, X } from 'lucide-react';

const TaskList: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const { tasks, loading, error, fetchTasks } = useTasks();
  
  // Search and Filter State
  const [searchQuery, setSearchQuery] = useState('');
  const [filterPriority, setFilterPriority] = useState<string>('all');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [sortBy, setSortBy] = useState<string>('created_at');
  const [showFilters, setShowFilters] = useState(false);

  // Filtered and Sorted Tasks
  const filteredTasks = useMemo(() => {
    let filtered = tasks.filter(task => {
      // Search filter
      const matchesSearch = searchQuery === '' || 
        task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (task.description && task.description.toLowerCase().includes(searchQuery.toLowerCase())) ||
        (task.tags && task.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase())));

      // Priority filter
      const matchesPriority = filterPriority === 'all' || task.priority === filterPriority;

      // Status filter
      const matchesStatus = filterStatus === 'all' || 
        (filterStatus === 'completed' && task.completed) ||
        (filterStatus === 'pending' && !task.completed) ||
        (filterStatus === 'overdue' && task.due_date && new Date(task.due_date) < new Date() && !task.completed);

      return matchesSearch && matchesPriority && matchesStatus;
    });

    // Sort tasks
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'priority':
          const priorityOrder = { high: 3, medium: 2, low: 1 };
          return (priorityOrder[b.priority as keyof typeof priorityOrder] || 1) - 
                 (priorityOrder[a.priority as keyof typeof priorityOrder] || 1);
        case 'due_date':
          if (!a.due_date && !b.due_date) return 0;
          if (!a.due_date) return 1;
          if (!b.due_date) return -1;
          return new Date(a.due_date).getTime() - new Date(b.due_date).getTime();
        case 'title':
          return a.title.localeCompare(b.title);
        case 'created_at':
        default:
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
      }
    });

    return filtered;
  }, [tasks, searchQuery, filterPriority, filterStatus, sortBy]);

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

  const clearFilters = () => {
    setSearchQuery('');
    setFilterPriority('all');
    setFilterStatus('all');
    setSortBy('created_at');
  };

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

  return (
    <div className="w-full">
      {/* Search and Filter Controls */}
      <div className="mb-6 space-y-4">
        {/* Search Bar */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500" size={16} />
          <input
            type="text"
            placeholder="Search tasks, descriptions, tags..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:outline-none focus:border-electric-blue transition-all text-sm"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-white"
            >
              <X size={16} />
            </button>
          )}
        </div>

        {/* Filter Toggle */}
        <div className="flex items-center justify-between">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center space-x-2 px-4 py-2 bg-white/5 border border-white/10 rounded-lg hover:border-electric-blue/50 transition-all text-sm"
          >
            <Filter size={16} />
            <span>Filters</span>
          </button>
          
          {(searchQuery || filterPriority !== 'all' || filterStatus !== 'all' || sortBy !== 'created_at') && (
            <button
              onClick={clearFilters}
              className="text-xs text-gray-500 hover:text-electric-blue transition-colors"
            >
              Clear All
            </button>
          )}
        </div>

        {/* Filter Controls */}
        {showFilters && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 bg-white/5 border border-white/10 rounded-xl"
          >
            <div>
              <label className="block text-xs font-bold text-gray-400 mb-2">PRIORITY</label>
              <select
                value={filterPriority}
                onChange={(e) => setFilterPriority(e.target.value)}
                className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-sm"
              >
                <option value="all">All Priorities</option>
                <option value="high">🔴 High</option>
                <option value="medium">🟡 Medium</option>
                <option value="low">🟢 Low</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-gray-400 mb-2">STATUS</label>
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-sm"
              >
                <option value="all">All Tasks</option>
                <option value="pending">Pending</option>
                <option value="completed">Completed</option>
                <option value="overdue">Overdue</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-gray-400 mb-2">SORT BY</label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-sm"
              >
                <option value="created_at">Created Date</option>
                <option value="priority">Priority</option>
                <option value="due_date">Due Date</option>
                <option value="title">Title (A-Z)</option>
              </select>
            </div>
          </motion.div>
        )}

        {/* Results Summary */}
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>
            Showing {filteredTasks.length} of {tasks.length} tasks
          </span>
          {filteredTasks.length !== tasks.length && (
            <span className="text-electric-blue">Filtered results</span>
          )}
        </div>
      </div>

      {/* Task List */}
      {filteredTasks.length === 0 ? (
        <div className="text-center py-20 flex flex-col items-center">
          <div className="w-16 h-16 bg-white/5 rounded-full flex items-center justify-center mb-6">
            <Inbox className="text-gray-600" size={24} />
          </div>
          <p className="text-gray-500 text-sm font-medium">
            {tasks.length === 0 ? 'Neural Log Empty. Initialize a new task entry.' : 'No tasks match your filters.'}
          </p>
          {tasks.length > 0 && (
            <button
              onClick={clearFilters}
              className="mt-4 px-4 py-2 bg-electric-blue/10 border border-electric-blue/20 text-electric-blue text-xs rounded-lg hover:bg-electric-blue/20 transition-all"
            >
              Clear Filters
            </button>
          )}
        </div>
      ) : (
        <div className="space-y-4">
          <AnimatePresence mode="popLayout">
            {filteredTasks.map((task, i) => (
              <motion.div
                key={`${task.id}-${i}`}
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
      )}

      <p className="text-[10px] text-gray-700 mt-8 font-mono text-center opacity-50">
        Connected to: {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'} | Tasks: {tasks.length}
      </p>
    </div>
  );
};

export default TaskList;