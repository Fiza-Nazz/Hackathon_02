'use client';

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageSquare, Bot, Sparkles, Minimize2, X, Send, User, Trash2 } from 'lucide-react';
import { useAuthStore } from '../../store/auth';
import { useTasksStore } from '../../store/tasks';
import ReactMarkdown from 'react-markdown';
import { useChat, Message } from 'ai/react';

const ChatWidget = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [language, setLanguage] = useState<'en' | 'ur'>('en');
    const { user } = useAuthStore();
    const { fetchTasks } = useTasksStore();
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const { messages, input, handleInputChange, handleSubmit: originalHandleSubmit, isLoading, setMessages } = useChat({
        api: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'}/api/chat/message`,
        initialMessages: [],
        body: {
            user_id: String(user?.id || '1'),
            language: language
        },
        headers: {
            Authorization: `Bearer ${typeof window !== 'undefined' ? localStorage.getItem('access_token') : ''}`
        },
        onFinish: (_message: Message) => {
            console.log("Neural Command Finalized. Syncing Dashboard...");
            setTimeout(() => fetchTasks(), 500);
            setTimeout(() => fetchTasks(), 1500);
            setTimeout(() => fetchTasks(), 4000);
        },
        onError: (error: Error) => {
            console.error("Neural Link Error:", error);
        }
    });

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isLoading]);

    useEffect(() => {
        if (isOpen && messages.length === 0) {
            loadHistory();
        }
    }, [isOpen]);

    const loadHistory = async () => {
        try {
            const userId = String(user?.id || '1');
            const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';
            const response = await fetch(`${baseUrl}/api/chat/history/${userId}`);
            if (response.ok) {
                const history = await response.json();
                const mappedHistory: Message[] = history.map((msg: any) => ({
                    id: msg.id || Math.random().toString(),
                    role: (msg.role === 'user' || msg.role === 'assistant' || msg.role === 'system' || msg.role === 'data' ? msg.role : 'assistant') as any,
                    content: msg.content
                }));
                setMessages(mappedHistory);
            }
        } catch (error) {
            console.error("Failed to load history:", error);
        }
    };

    const handleToggleChat = () => {
        setIsOpen(!isOpen);
    };

    const onSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!input?.trim() || isLoading) return;
        originalHandleSubmit(e);
    };

    const handleClearChat = async () => {
        if (!confirm("Wipe all neural logs?")) return;
        try {
            const userId = String(user?.id || '1');
            const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';
            await fetch(`${baseUrl}/api/chat/history/${userId}`, { method: 'DELETE' });
            setMessages([]);
        } catch (error) {
            console.error("Failed to clear history:", error);
        }
    };

    return (
        <div className="fixed bottom-8 right-8 z-[1000] flex flex-col items-end font-sans">
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.8, y: 100, rotateX: 10 }}
                        animate={{ opacity: 1, scale: 1, y: 0, rotateX: 0 }}
                        exit={{ opacity: 0, scale: 0.8, y: 100, rotateX: 10 }}
                        className="mb-6 w-[350px] md:w-[380px] h-[500px] max-h-[70vh] flex flex-col overflow-hidden rounded-[2rem] bg-black/80 backdrop-blur-3xl border border-white/10 shadow-[0_0_60px_rgba(0,242,255,0.1)] ring-1 ring-white/5"
                    >
                        {/* Header */}
                        <div className="relative p-6 bg-gradient-to-r from-electric-blue/20 to-transparent border-b border-white/5 flex justify-between items-center z-10">
                            <div className="flex items-center gap-4">
                                <div className="relative">
                                    <div className="absolute inset-0 bg-electric-blue/40 blur-xl rounded-full animate-pulse" />
                                    <div className="relative bg-black/50 p-2.5 rounded-2xl border border-electric-blue/30 w-12 h-12 flex items-center justify-center">
                                        <Bot className="w-7 h-7 text-electric-blue" />
                                    </div>
                                    <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 border-4 border-black rounded-full" />
                                </div>
                                <div>
                                    <h3 className="font-black text-xl tracking-tighter uppercase italic text-white leading-none">
                                        NEURAL <span className="text-electric-blue">AGENT</span>
                                    </h3>
                                    <div className="flex items-center gap-2 mt-1">
                                        <Sparkles className="w-3 h-3 text-electric-blue animate-spin-slow" />
                                        <span className="text-[10px] text-gray-400 font-bold tracking-widest uppercase">Link Active</span>
                                    </div>
                                </div>
                            </div>
                            <div className="flex items-center gap-2">
                                <button
                                    onClick={() => setLanguage(language === 'en' ? 'ur' : 'en')}
                                    className={`relative px-3 py-1.5 rounded-xl text-[9px] font-black tracking-widest uppercase transition-all duration-500 border ${language === 'ur'
                                        ? 'bg-electric-blue text-black border-electric-blue shadow-[0_0_15px_rgba(0,242,255,0.4)]'
                                        : 'bg-black/40 text-electric-blue border-white/10 hover:border-electric-blue/40'
                                        }`}
                                >
                                    {language === 'en' ? 'EN' : 'UR'}
                                </button>
                                <button
                                    onClick={handleClearChat}
                                    className="p-2 hover:bg-red-500/20 rounded-xl transition-colors text-gray-400 hover:text-red-400"
                                    title="Wipe Logs"
                                >
                                    <Trash2 className="w-4 h-4" />
                                </button>
                                <button onClick={() => handleToggleChat()} className="p-2 hover:bg-white/10 rounded-xl transition-colors text-gray-400">
                                    <Minimize2 className="w-4 h-4" />
                                </button>
                            </div>
                        </div>

                        {/* Messages Area */}
                        <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar bg-black/10">
                            {messages.length === 0 && !isLoading && (
                                <div className="h-full flex flex-col items-center justify-center text-center p-8">
                                    <div className="w-16 h-16 bg-electric-blue/5 rounded-full flex items-center justify-center mb-4 border border-electric-blue/10">
                                        <MessageSquare className="w-8 h-8 text-electric-blue/30" />
                                    </div>
                                    <p className="text-gray-500 text-sm font-medium">Neural history is empty. <br />Awaiting command sequence...</p>
                                </div>
                            )}

                            {messages.map((msg: Message, idx: number) => (
                                <motion.div
                                    initial={{ opacity: 0, x: msg.role === 'user' ? 20 : -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    key={msg.id || idx}
                                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                                >
                                    <div className={`max-w-[85%] flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                                        <div className={`mt-1 flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center border ${msg.role === 'user'
                                            ? 'bg-electric-blue/10 border-electric-blue/20'
                                            : 'bg-white/5 border-white/10'
                                            }`}>
                                            {msg.role === 'user' ? <User className="w-4 h-4 text-electric-blue" /> : <Bot className="w-4 h-4 text-white" />}
                                        </div>
                                        <div className={`p-4 rounded-2xl text-sm leading-relaxed shadow-sm ${msg.role === 'user'
                                            ? 'bg-electric-blue/10 border border-electric-blue/20 text-white rounded-tr-none'
                                            : 'bg-white/5 border border-white/10 text-gray-200 rounded-tl-none'
                                            } ${language === 'ur' && msg.role === 'assistant' ? 'font-urdu text-base text-right' : ''}`}>
                                            <ReactMarkdown
                                                components={{
                                                    strong: (props: any) => <span className="font-bold text-electric-blue">{props.children}</span>,
                                                    em: (props: any) => <span className="italic text-gray-400">{props.children}</span>,
                                                    ul: (props: any) => <ul className="list-disc pl-4 my-2 space-y-1">{props.children}</ul>,
                                                    li: (props: any) => <li className="text-gray-300">{props.children}</li>,
                                                    p: (props: any) => <p className="mb-2 last:mb-0">{props.children}</p>
                                                } as any}
                                            >
                                                {msg.content}
                                            </ReactMarkdown>
                                        </div>
                                    </div>
                                </motion.div>
                            ))}

                            {isLoading && (
                                <div className="flex justify-start">
                                    <div className="bg-white/5 border border-white/10 p-4 rounded-2xl rounded-tl-none flex items-center gap-3">
                                        <div className="flex gap-1">
                                            <div className="w-1.5 h-1.5 bg-electric-blue rounded-full animate-bounce" />
                                            <div className="w-1.5 h-1.5 bg-electric-blue rounded-full animate-bounce delay-75" />
                                            <div className="w-1.5 h-1.5 bg-electric-blue rounded-full animate-bounce delay-150" />
                                        </div>
                                        <span className="text-[10px] text-electric-blue font-bold uppercase tracking-widest">Processing...</span>
                                    </div>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </div>

                        {/* Input Area */}
                        <div className="p-6 bg-black/40 border-t border-white/5 backdrop-blur-xl">
                            <form onSubmit={onSubmit}>
                                <div className="relative group">
                                    <div className="absolute -inset-0.5 bg-gradient-to-r from-electric-blue/40 to-transparent rounded-2xl blur opacity-0 group-focus-within:opacity-100 transition duration-500" />
                                    <div className="relative flex gap-2 bg-black/60 border border-white/10 rounded-2xl p-1.5 focus-within:border-electric-blue/40 transition-all">
                                        <input
                                            type="text"
                                            value={input || ''}
                                            onChange={handleInputChange}
                                            placeholder="Enter Neural Command..."
                                            className="flex-1 bg-transparent px-4 py-3 text-white text-sm focus:outline-none placeholder:text-gray-600 font-mono"
                                        />
                                        <button
                                            type="submit"
                                            disabled={!input?.trim() || isLoading}
                                            className="bg-electric-blue hover:bg-electric-blue/80 disabled:opacity-50 disabled:cursor-not-allowed text-black p-3 rounded-xl transition-all shadow-glow-sm"
                                        >
                                            <Send className="w-5 h-5" />
                                        </button>
                                    </div>
                                </div>
                            </form>
                            <div className="mt-4 flex items-center justify-between px-2">
                                <div className="flex gap-1">
                                    <div className="w-1 h-1 bg-electric-blue rounded-full animate-pulse" />
                                    <div className="w-1 h-1 bg-electric-blue rounded-full animate-pulse delay-150" />
                                    <div className="w-1 h-1 bg-electric-blue rounded-full animate-pulse delay-300" />
                                </div>
                                <span className="text-[9px] text-gray-500 font-black tracking-[0.3em] uppercase">Status: <span className="text-electric-blue">Optimal</span></span>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            <motion.button
                whileHover={{ scale: 1.1, rotate: 5 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => handleToggleChat()}
                className="group relative w-20 h-20"
            >
                <div className="absolute inset-0 bg-electric-blue/20 rounded-3xl blur-2xl group-hover:bg-electric-blue/40 transition-all opacity-60" />
                <div className="relative w-full h-full bg-black/40 border border-white/10 rounded-3xl flex items-center justify-center backdrop-blur-xl group-hover:border-electric-blue/50 transition-all overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-br from-electric-blue/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                    <AnimatePresence mode="wait">
                        {isOpen ? (
                            <X key="x" className="w-8 h-8 text-white relative z-10" />
                        ) : (
                            <div key="bot" className="relative z-10">
                                <MessageSquare className="w-8 h-8 text-electric-blue group-hover:text-white transition-colors" />
                                <div className="absolute -top-1 -right-1 w-3 h-3 bg-electric-blue rounded-full shadow-glow animate-pulse" />
                            </div>
                        )}
                    </AnimatePresence>
                </div>
            </motion.button>
            <style jsx global>{`
                @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');

                .font-urdu {
                    font-family: 'Noto Nastaliq Urdu', serif;
                    line-height: 2.2;
                    direction: rtl;
                }

                .custom-scrollbar::-webkit-scrollbar {
                    width: 4px;
                }
                .custom-scrollbar::-webkit-scrollbar-track {
                    background: transparent;
                }
                .custom-scrollbar::-webkit-scrollbar-thumb {
                    background: rgba(0, 242, 255, 0.1);
                    border-radius: 10px;
                }
                .shadow-glow-sm {
                    box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
                }
                .animate-spin-slow {
                    animation: spin 3s linear infinite;
                }
                @keyframes spin {
                    from { transform: rotate(0deg); }
                    to { transform: rotate(360deg); }
                }
            `}</style>
        </div >
    );
};

export default ChatWidget;