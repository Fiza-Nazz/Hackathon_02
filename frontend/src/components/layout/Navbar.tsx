'use client';
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter, usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { Sun, Moon, Menu, X, LogIn, UserPlus, LayoutDashboard, LogOut, Globe } from 'lucide-react';
import { useAuth } from '@/store/auth';
import { cn } from '@/utils/cn';

const Navbar: React.FC = () => {
    const [isScrolled, setIsScrolled] = useState(false);
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const [isDarkMode, setIsDarkMode] = useState(true);
    const { isAuthenticated, logout } = useAuth();
    const router = useRouter();
    const pathname = usePathname();

    useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 20);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const toggleTheme = () => {
        setIsDarkMode(!isDarkMode);
        document.documentElement.classList.toggle('light-theme');
    };

    const navLinks = [
        { name: 'Home', href: '/', icon: Globe, show: true },
        { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard, show: isAuthenticated },
        { name: 'Login', href: '/login', icon: LogIn, show: !isAuthenticated },
        { name: 'Register', href: '/register', icon: UserPlus, show: !isAuthenticated },
    ];

    return (
        <nav
            className={cn(
                'fixed top-0 left-0 right-0 z-50 transition-all duration-300 ease-in-out px-6 md:px-12',
                isScrolled ? 'py-4 glass-morphism border-b border-white/10' : 'py-6 bg-transparent'
            )}
        >
            <div className="max-w-7xl mx-auto flex items-center justify-between">
                {/* Logo */}
                <Link href="/" className="flex items-center space-x-2 group">
                    <div className="w-10 h-10 bg-electric-blue rounded-lg flex items-center justify-center shadow-glow group-hover:shadow-glow-lg transition-all duration-300">
                        <span className="text-black font-bold text-xl">T</span>
                    </div>
                    <span className="text-white font-bold text-xl tracking-tighter electric-glow">
                        TODO<span className="text-electric-blue">AI</span>
                    </span>
                </Link>

                {/* Desktop Links */}
                <div className="hidden md:flex items-center space-x-8">
                    {navLinks.map((link) => link.show && (
                        <Link
                            key={link.name}
                            href={link.href}
                            className={cn(
                                "text-sm font-medium transition-colors hover:text-electric-blue flex items-center space-x-2",
                                pathname === link.href ? "text-electric-blue" : "text-gray-400"
                            )}
                        >
                            <link.icon size={18} />
                            <span>{link.name}</span>
                        </Link>
                    ))}

                    {isAuthenticated && (
                        <button
                            onClick={() => {
                                logout();
                                router.push('/');
                            }}
                            className="text-sm font-medium text-gray-400 hover:text-red-400 flex items-center space-x-2 transition-colors"
                        >
                            <LogOut size={18} />
                            <span>Logout</span>
                        </button>
                    )}

                    {/* Theme Toggle */}
                    <button
                        onClick={toggleTheme}
                        className="w-10 h-10 rounded-full flex items-center justify-center bg-white/5 border border-white/10 hover:border-electric-blue transition-all duration-300"
                    >
                        <AnimatePresence mode="wait">
                            {isDarkMode ? (
                                <motion.div
                                    key="moon"
                                    initial={{ rotate: -90, opacity: 0 }}
                                    animate={{ rotate: 0, opacity: 1 }}
                                    exit={{ rotate: 90, opacity: 0 }}
                                >
                                    <Moon size={20} className="text-electric-blue" />
                                </motion.div>
                            ) : (
                                <motion.div
                                    key="sun"
                                    initial={{ rotate: -90, opacity: 0 }}
                                    animate={{ rotate: 0, opacity: 1 }}
                                    exit={{ rotate: 90, opacity: 0 }}
                                >
                                    <Sun size={20} className="text-orange-400" />
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </button>
                </div>

                {/* Mobile Menu Button */}
                <button
                    className="md:hidden p-2 text-gray-400 hover:text-white"
                    onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                >
                    {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
                </button>
            </div>

            {/* Mobile Menu */}
            <AnimatePresence>
                {isMobileMenuOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        className="absolute top-full left-0 right-0 glass-morphism border-b border-white/10 p-6 flex flex-col space-y-4 md:hidden"
                    >
                        {navLinks.map((link) => link.show && (
                            <Link
                                key={link.name}
                                href={link.href}
                                className="text-lg font-medium text-gray-300 hover:text-electric-blue flex items-center space-x-3"
                                onClick={() => setIsMobileMenuOpen(false)}
                            >
                                <link.icon size={20} />
                                <span>{link.name}</span>
                            </Link>
                        ))}
                        {isAuthenticated && (
                            <button
                                onClick={() => {
                                    logout();
                                    router.push('/');
                                    setIsMobileMenuOpen(false);
                                }}
                                className="text-lg font-medium text-red-400 flex items-center space-x-3"
                            >
                                <LogOut size={20} />
                                <span>Logout</span>
                            </button>
                        )}
                    </motion.div>
                )}
            </AnimatePresence>
        </nav>
    );
};

export default Navbar;
