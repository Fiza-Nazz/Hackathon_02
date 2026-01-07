import React, { useState } from 'react';
import { useTasks } from '@/store/tasks';
import { motion } from 'framer-motion';
import { Plus, Loader2 } from 'lucide-react';
import { cn } from '@/utils/cn';

interface CreateTaskFormProps {
  onSuccess?: () => void;
}

interface CreateTaskData {
  title: string;
  description?: string;
  priority: number;
  category: string;
}

const CreateTask: React.FC<CreateTaskFormProps> = ({ onSuccess }) => {
  const [formData, setFormData] = useState<CreateTaskData>({
    title: '',
    description: '',
    priority: 1,
    category: 'General',
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const { createTask } = useTasks();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'priority' ? parseInt(value) : value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.title.trim()) {
      setError('Signal required: Title must be provided');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      await createTask({
        title: formData.title,
        description: formData.description || undefined,
        priority: formData.priority,
        category: formData.category,
        completed: false,
      });

      setFormData({ title: '', description: '', priority: 1, category: 'General' });
      if (onSuccess) onSuccess();
    } catch (err: any) {
      setError(err.message || 'Transmission failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full">
      {error && (
        <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 text-red-500 text-xs rounded-xl">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:outline-none focus:border-electric-blue transition-all placeholder:text-gray-600 text-sm"
            placeholder="Identity Title"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <select
            name="priority"
            value={formData.priority}
            onChange={handleChange}
            className="px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:outline-none focus:border-electric-blue transition-all text-xs text-gray-400"
          >
            <option value={1}>Low Priority</option>
            <option value={2}>Medium Priority</option>
            <option value={3}>High Priority</option>
          </select>
          <input
            type="text"
            name="category"
            value={formData.category}
            onChange={handleChange}
            className="px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:outline-none focus:border-electric-blue transition-all text-xs text-gray-400"
            placeholder="Category (e.g. Work)"
          />
        </div>

        <div>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows={2}
            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:outline-none focus:border-electric-blue transition-all placeholder:text-gray-600 text-sm resize-none"
            placeholder="Neural Details (Optional)"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className={cn(
            "w-full py-3 rounded-xl font-bold uppercase tracking-[0.2em] text-[10px] flex items-center justify-center space-x-2 transition-all duration-300",
            loading
              ? "bg-gray-800 text-gray-500"
              : "bg-electric-blue text-black hover:shadow-glow"
          )}
        >
          {loading ? (
            <Loader2 size={16} className="animate-spin" />
          ) : (
            <>
              <Plus size={16} />
              <span>Deploy Task</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default CreateTask;