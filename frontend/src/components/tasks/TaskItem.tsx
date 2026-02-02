import React, { useState } from 'react';
import { useTasks } from '@/store/tasks';
import { Task } from '@/types';
import { motion } from 'framer-motion';
import { CheckCircle, Circle, Trash2, Edit3, Save, X, Clock } from 'lucide-react';
import { cn } from '@/utils/cn';

interface TaskItemProps {
  task: Task;
}

const TaskItem: React.FC<TaskItemProps> = ({ task }) => {
  const { toggleTaskCompletion, deleteTask, updateTask } = useTasks();
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');

  const handleToggleCompletion = async () => {
    try {
      await toggleTaskCompletion(task.id);
    } catch (error) {
      console.error('Failed to toggle task completion:', error);
    }
  };

  const handleDelete = async () => {
    try {
      if (window.confirm('Delete this neural entry permanently?')) {
        await deleteTask(task.id);
      }
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  const handleEdit = async () => {
    try {
      await updateTask(task.id, {
        title: editTitle,
        description: editDescription || undefined,
      });
      setIsEditing(false);
    } catch (error) {
      console.error('Failed to update task:', error);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className={cn(
      "group relative p-6 rounded-2xl border transition-all duration-500",
      task.completed
        ? "bg-white/[0.02] border-white/5 opacity-60"
        : "glass-morphism border-white/10 hover:border-electric-blue/50",
      !task.completed && task.priority === 3 && "border-red-500/30 bg-red-500/[0.02]",
      !task.completed && task.priority === 2 && "border-yellow-500/30 bg-yellow-500/[0.02]"
    )}>
      {isEditing ? (
        <div className="space-y-4">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="w-full px-4 py-2 bg-white/5 border border-white/20 rounded-xl focus:outline-none focus:border-electric-blue text-sm"
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            rows={2}
            className="w-full px-4 py-2 bg-white/5 border border-white/20 rounded-xl focus:outline-none focus:border-electric-blue text-sm resize-none"
          />
          <div className="flex space-x-2">
            <button onClick={handleEdit} className="p-2 bg-electric-blue text-black rounded-lg hover:scale-105 transition-transform">
              <Save size={16} />
            </button>
            <button onClick={() => setIsEditing(false)} className="p-2 bg-white/10 text-white rounded-lg hover:bg-white/20 transition-all">
              <X size={16} />
            </button>
          </div>
        </div>
      ) : (
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-4 flex-1">
            <button
              onClick={handleToggleCompletion}
              className="mt-1 flex-shrink-0 transition-transform active:scale-90"
            >
              {task.completed ? (
                <CheckCircle className="text-electric-blue" size={24} />
              ) : (
                <Circle className={cn(
                  "transition-colors",
                  task.priority === 3 ? "text-red-500" : task.priority === 2 ? "text-yellow-500" : "text-gray-600"
                )} size={24} />
              )}
            </button>

            <div className="flex-1 min-w-0">
              <div className="flex items-center space-x-3 mb-1">
                <h3 className={cn(
                  "text-lg font-bold transition-all duration-500",
                  task.completed ? "text-gray-600 line-through" : "text-white group-hover:text-electric-blue"
                )}>
                  {task.title}
                </h3>
                {task.category && (
                  <span className="px-2 py-0.5 rounded-md bg-white/5 border border-white/10 text-[9px] font-black uppercase tracking-widest text-gray-500">
                    {task.category}
                  </span>
                )}
              </div>
              {task.description && (
                <p className={cn(
                  "mt-1 text-sm leading-relaxed",
                  task.completed ? "text-gray-700 font-medium" : "text-gray-500"
                )}>
                  {task.description}
                </p>
              )}

              <div className="mt-4 flex items-center space-x-4 text-[10px] uppercase tracking-widest font-black text-gray-700">
                <div className="flex items-center space-x-1">
                  <Clock size={12} />
                  <span>{formatDate(task.created_at)}</span>
                </div>
                {task.priority === 3 && <span className="text-red-500/50">CRITICAL</span>}
                {task.priority === 2 && <span className="text-yellow-500/50">ELEVATED</span>}
                {task.completed && <span className="text-electric-blue/50">ARCHIVED</span>}
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-1 ml-4 opacity-0 group-hover:opacity-100 transition-opacity">
            <button
              onClick={() => setIsEditing(true)}
              className="p-2 text-gray-500 hover:text-white hover:bg-white/5 rounded-lg transition-all"
            >
              <Edit3 size={18} />
            </button>
            <button
              onClick={handleDelete}
              className="p-2 text-gray-500 hover:text-red-500 hover:bg-red-500/10 rounded-lg transition-all"
            >
              <Trash2 size={18} />
            </button>
          </div>
        </div>
      )}

      {/* Selection Glow */}
      {!task.completed && (
        <div className="absolute inset-0 rounded-2xl bg-electric-blue/0 group-hover:bg-electric-blue/[0.02] pointer-events-none transition-colors duration-500" />
      )}
    </div>
  );
};

export default TaskItem;