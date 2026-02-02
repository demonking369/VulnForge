'use client';

import { useState, useEffect, useRef } from 'react';
import { MessageCircle, X, Send, Bot, User, Minimize2, Maximize2 } from 'lucide-react';
import { getWebSocket } from '@/lib/websocket';
import { cn } from '@/lib/utils';

interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
}

export function ChatWidget() {
    const [isOpen, setIsOpen] = useState(false);
    const [isMinimized, setIsMinimized] = useState(false);
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState<Message[]>([
        {
            id: 'welcome',
            role: 'assistant',
            content: 'Hello! I am your NeuroRift AI assistant. How can I help you with your security operations today?',
            timestamp: new Date()
        }
    ]);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const [isTyping, setIsTyping] = useState(false);

    useEffect(() => {
        const handleChatResponse = (event: CustomEvent) => {
            const { response } = event.detail;
            setIsTyping(false);

            setMessages(prev => [
                ...prev,
                {
                    id: Date.now().toString(),
                    role: 'assistant',
                    content: response,
                    timestamp: new Date()
                }
            ]);
        };

        window.addEventListener('neurorift:chat_response', handleChatResponse as EventListener);
        return () => {
            window.removeEventListener('neurorift:chat_response', handleChatResponse as EventListener);
        };
    }, []);

    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages, isOpen]);

    const sendMessage = (e?: React.FormEvent) => {
        e?.preventDefault();
        if (!input.trim()) return;

        const userMsg: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: input,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setIsTyping(true);

        const ws = getWebSocket();
        ws.send({
            type: 'chat',
            message: userMsg.content,
            model: 'llama3' // Default model
        });
    };

    if (!isOpen) {
        return (
            <button
                onClick={() => setIsOpen(true)}
                className="fixed bottom-6 right-6 w-14 h-14 bg-neuro-primary rounded-full flex items-center justify-center shadow-lg shadow-neuro-primary/20 hover:scale-105 transition-all z-50 group"
            >
                <MessageCircle className="w-7 h-7 text-white group-hover:rotate-12 transition-transform" />
            </button>
        );
    }

    return (
        <div className={cn(
            "fixed right-6 bg-neuro-surface border border-neuro-border rounded-lg shadow-2xl flex flex-col z-50 transition-all duration-300 overflow-hidden",
            isMinimized ? "bottom-6 w-72 h-14" : "bottom-6 w-96 h-[500px]"
        )}>
            {/* Header */}
            <div
                className="flex items-center justify-between p-3 bg-neuro-bg border-b border-neuro-border cursor-pointer"
                onClick={() => setIsMinimized(!isMinimized)}
            >
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-full bg-neuro-primary/20 flex items-center justify-center">
                        <Bot className="w-5 h-5 text-neuro-primary" />
                    </div>
                    <div>
                        <h3 className="text-sm font-semibold text-neuro-text-primary">NeuroRift AI</h3>
                        {!isMinimized && <p className="text-[10px] text-neuro-text-secondary flex items-center gap-1">
                            <span className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse" />
                            Online
                        </p>}
                    </div>
                </div>
                <div className="flex items-center gap-1">
                    <button
                        onClick={(e) => { e.stopPropagation(); setIsMinimized(!isMinimized); }}
                        className="p-1 hover:bg-neuro-surface rounded text-neuro-text-muted hover:text-neuro-text-primary"
                    >
                        {isMinimized ? <Maximize2 className="w-4 h-4" /> : <Minimize2 className="w-4 h-4" />}
                    </button>
                    <button
                        onClick={() => setIsOpen(false)}
                        className="p-1 hover:bg-red-500/10 rounded text-neuro-text-muted hover:text-red-400"
                    >
                        <X className="w-4 h-4" />
                    </button>
                </div>
            </div>

            {/* Messages */}
            {!isMinimized && (
                <>
                    <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-neuro-bg/50">
                        {messages.map((msg) => (
                            <div
                                key={msg.id}
                                className={cn(
                                    "flex gap-3 max-w-[85%]",
                                    msg.role === 'user' ? "ml-auto flex-row-reverse" : ""
                                )}
                            >
                                <div className={cn(
                                    "w-8 h-8 rounded-full flex items-center justify-center shrink-0",
                                    msg.role === 'user' ? "bg-neuro-primary text-white" : "bg-neuro-surface border border-neuro-border text-neuro-primary"
                                )}>
                                    {msg.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                                </div>
                                <div className={cn(
                                    "p-3 rounded-lg text-sm",
                                    msg.role === 'user'
                                        ? "bg-neuro-primary text-white"
                                        : "bg-neuro-surface border border-neuro-border text-neuro-text-primary"
                                )}>
                                    <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                                    <span className={cn(
                                        "text-[10px] block mt-1",
                                        msg.role === 'user' ? "text-white/70" : "text-neuro-text-muted"
                                    )}>
                                        {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                    </span>
                                </div>
                            </div>
                        ))}
                        {isTyping && (
                            <div className="flex gap-3 max-w-[85%]">
                                <div className="w-8 h-8 rounded-full bg-neuro-surface border border-neuro-border flex items-center justify-center shrink-0">
                                    <Bot className="w-4 h-4 text-neuro-primary" />
                                </div>
                                <div className="bg-neuro-surface border border-neuro-border rounded-lg p-3 flex items-center gap-1">
                                    <span className="w-1.5 h-1.5 bg-neuro-text-muted rounded-full animate-bounce [animation-delay:-0.3s]" />
                                    <span className="w-1.5 h-1.5 bg-neuro-text-muted rounded-full animate-bounce [animation-delay:-0.15s]" />
                                    <span className="w-1.5 h-1.5 bg-neuro-text-muted rounded-full animate-bounce" />
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input */}
                    <form onSubmit={sendMessage} className="p-3 bg-neuro-surface border-t border-neuro-border">
                        <div className="relative">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                placeholder="Ask NeuroRift anything..."
                                className="w-full bg-neuro-bg border border-neuro-border rounded-md py-2.5 pl-4 pr-10 text-sm text-neuro-text-primary focus:outline-none focus:ring-1 focus:ring-neuro-primary placeholder:text-neuro-text-muted"
                            />
                            <button
                                type="submit"
                                disabled={!input.trim()}
                                className="absolute right-2 top-1/2 -translate-y-1/2 p-1.5 text-neuro-text-muted hover:text-neuro-primary disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                            >
                                <Send className="w-4 h-4" />
                            </button>
                        </div>
                    </form>
                </>
            )}
        </div>
    );
}
