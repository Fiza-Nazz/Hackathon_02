'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/store/auth';
import { motion } from 'framer-motion';
import { Mail, Lock, User, Loader2 } from 'lucide-react';
import { cn } from '@/utils/cn';

interface RegisterFormData {
  email: string;
  password: string;
  confirmPassword: string;
}

const Register: React.FC = () => {
  const [formData, setFormData] = useState<RegisterFormData>({
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const router = useRouter();
  const { register } = useAuth();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      setError('Neural mismatch: Passwords do not correlate');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      await register(formData.email, formData.password);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Initialization failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full">
      {error && (
        <motion.div
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          className="mb-6 p-4 bg-red-500/10 border border-red-500/50 text-red-400 rounded-xl text-sm"
        >
          {error}
        </motion.div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="email" className="block text-[10px] uppercase tracking-widest font-black text-gray-500 mb-2 ml-1">
            Primary Designation (Email)
          </label>
          <div className="relative group">
            <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none text-gray-500 group-focus-within:text-electric-blue transition-colors">
              <Mail size={18} />
            </div>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="w-full pl-12 pr-4 py-4 bg-white/5 border border-white/10 rounded-2xl focus:outline-none focus:border-electric-blue focus:ring-1 focus:ring-electric-blue/30 transition-all placeholder:text-gray-600"
              placeholder="operator@base.com"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="password" className="block text-[10px] uppercase tracking-widest font-black text-gray-500 mb-2 ml-1">
              New Key
            </label>
            <div className="relative group">
              <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none text-gray-500 group-focus-within:text-electric-blue transition-colors">
                <Lock size={18} />
              </div>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                className="w-full pl-12 pr-4 py-4 bg-white/5 border border-white/10 rounded-2xl focus:outline-none focus:border-electric-blue focus:ring-1 focus:ring-electric-blue/30 transition-all placeholder:text-gray-600"
                placeholder="••••••••"
              />
            </div>
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-[10px] uppercase tracking-widest font-black text-gray-500 mb-2 ml-1">
              Verify Key
            </label>
            <div className="relative group">
              <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none text-gray-500 group-focus-within:text-electric-blue transition-colors">
                <Lock size={18} />
              </div>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
                className="w-full pl-12 pr-4 py-4 bg-white/5 border border-white/10 rounded-2xl focus:outline-none focus:border-electric-blue focus:ring-1 focus:ring-electric-blue/30 transition-all placeholder:text-gray-600"
                placeholder="••••••••"
              />
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className={cn(
            "w-full py-4 rounded-2xl font-black uppercase tracking-widest flex items-center justify-center space-x-3 transition-all duration-300",
            loading
              ? "bg-gray-800 text-gray-500 cursor-not-allowed"
              : "bg-electric-blue text-black hover:shadow-glow hover:scale-[1.02] active:scale-[0.98]"
          )}
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin" size={20} />
              <span>Initializing Sync...</span>
            </>
          ) : (
            <span>Begin Integration</span>
          )}
        </button>
      </form>
    </div>
  );
};

export default Register;