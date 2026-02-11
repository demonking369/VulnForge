
import React, { useState, useEffect } from 'react';
import { useWebModeContext } from '../WebModeProvider';
import { Folder, PlayCircle, Trash2, Database, RefreshCw } from 'lucide-react';
import { Session } from '@/lib/webmode/adapter/interface';

export function SessionManagerPanel() {
    const { adapter } = useWebModeContext();
    const [sessions, setSessions] = useState<Session[]>([]);
    const [loading, setLoading] = useState(false);

    const fetchSessions = async () => {
        setLoading(true);
        try {
            const data = await adapter.listSessions();
            setSessions(data);
        } catch (e) {
            console.error("Failed to load sessions", e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchSessions();
    }, [adapter]);

    const handleLoad = async (id: string) => {
        try {
            await adapter.loadSession(id);
            // Trigger a global refresh or notification if needed
        } catch (e) {
            console.error("Failed to load session", e);
        }
    };

    const handleDelete = async (id: string) => {
        if (!confirm('Are you sure you want to delete this session?')) return;
        try {
            await adapter.deleteSession(id);
            fetchSessions();
        } catch (e) {
            console.error("Failed to delete", e);
        }
    };

    return (
        <div className="flex flex-col h-full bg-black/40 backdrop-blur-md border border-white/10 rounded-xl overflow-hidden shadow-xl">
            <div className="flex items-center justify-between px-4 py-3 bg-white/5 border-b border-white/10">
                <div className="flex items-center gap-2">
                    <Database className="w-4 h-4 text-purple-400" />
                    <span className="font-mono text-sm font-medium text-purple-100/90 tracking-wide">SESSION MANAGER</span>
                </div>
                <button onClick={fetchSessions} className={`text-white/40 hover:text-white ${loading ? 'animate-spin' : ''}`}>
                    <RefreshCw className="w-3.5 h-3.5" />
                </button>
            </div>

            <div className="flex-1 overflow-y-auto p-2 space-y-2 min-h-0">
                {sessions.length === 0 ? (
                    <div className="text-center p-8 text-white/20 italic text-sm">No active sessions found.</div>
                ) : (
                    sessions.map(s => (
                        <div key={s.id} className="group flex items-center justify-between p-3 rounded bg-white/5 hover:bg-white/10 border border-white/5 hover:border-white/20 transition-all">
                            <div className="min-w-0 flex-1">
                                <div className="flex items-center gap-2 mb-1">
                                    <span className={`w-1.5 h-1.5 rounded-full ${s.status === 'active' ? 'bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.5)]' : 'bg-white/20'}`} />
                                    <span className="font-mono text-xs font-bold text-white/90 truncate">{s.target}</span>
                                    <span className="text-[10px] uppercase tracking-wider text-white/40 border border-white/10 px-1 rounded">{s.mode}</span>
                                </div>
                                <div className="flex items-center gap-3 text-[10px] text-white/50 font-mono">
                                    <span>{new Date(s.startTime).toLocaleDateString()}</span>
                                    <span>•</span>
                                    <span>{s.toolCount} tools</span>
                                </div>
                            </div>

                            <div className="flex items-center gap-1 opacity-100 sm:opacity-0 group-hover:opacity-100 transition-opacity">
                                <button
                                    onClick={() => handleLoad(s.id)}
                                    title="Load Session"
                                    className="p-1.5 hover:bg-purple-500/20 text-white/40 hover:text-purple-300 rounded"
                                >
                                    <PlayCircle className="w-3.5 h-3.5" />
                                </button>
                                <button
                                    onClick={() => handleDelete(s.id)}
                                    title="Delete Session"
                                    className="p-1.5 hover:bg-red-500/20 text-white/40 hover:text-red-300 rounded"
                                >
                                    <Trash2 className="w-3.5 h-3.5" />
                                </button>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}
