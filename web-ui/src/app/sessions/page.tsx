'use client';

import { useState, useEffect } from 'react';
import { useNeuroRift } from '@/lib/hooks';
import { Folder, Plus, Search, Filter } from 'lucide-react';
import { SessionCard } from '@/components/sessions/SessionCard';
import { CreateSessionModal } from '@/components/modals/CreateSessionModal';
import { OperationalMode } from '@/lib/types';
import { getWebSocket } from '@/lib/websocket';

export default function SessionsPage() {
    const { session } = useNeuroRift();
    const [sessions, setSessions] = useState<any[]>([]);
    const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [filterMode, setFilterMode] = useState<'all' | OperationalMode>('all');

    useEffect(() => {
        // Request session list on mount
        const ws = getWebSocket();
        ws.send({
            type: 'get_session_list'
        });

        // Listen for session list updates
        const handleSessionList = (event: CustomEvent) => {
            if (event.detail.type === 'session_list') {
                setSessions(event.detail.sessions || []);
            }
        };

        window.addEventListener('neurorift:session_list', handleSessionList as EventListener);

        return () => {
            window.removeEventListener('neurorift:session_list', handleSessionList as EventListener);
        };
    }, []);

    const handleCreateSession = (name: string, mode: OperationalMode, description?: string) => {
        const ws = getWebSocket();
        ws.send({
            type: 'create_session',
            name,
            mode,
            metadata: description ? { description } : {}
        });
    };

    const handleLoadSession = (id: string) => {
        const ws = getWebSocket();
        ws.send({
            type: 'load_session',
            session_id: id
        });
    };

    const handleDeleteSession = (id: string) => {
        if (confirm('Are you sure you want to delete this session? This action cannot be undone.')) {
            const ws = getWebSocket();
            ws.send({
                type: 'delete_session',
                session_id: id
            });
        }
    };

    const handleExportSession = (id: string) => {
        const ws = getWebSocket();
        ws.send({
            type: 'export_session',
            session_id: id
        });
    };

    // Filter sessions
    const filteredSessions = sessions.filter(s => {
        const matchesSearch = s.name.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesFilter = filterMode === 'all' || s.mode === filterMode;
        return matchesSearch && matchesFilter;
    });

    return (
        <div className="p-6 space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-neuro-text-primary">Sessions</h1>
                    <p className="text-neuro-text-secondary mt-1">Manage your security assessment sessions</p>
                </div>
                <button
                    onClick={() => setIsCreateModalOpen(true)}
                    className="btn-primary flex items-center gap-2"
                >
                    <Plus className="w-5 h-5" />
                    New Session
                </button>
            </div>

            {/* Search and Filter */}
            <div className="glass-card p-4">
                <div className="flex items-center gap-4">
                    <div className="flex-1 relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-neuro-text-muted" />
                        <input
                            type="text"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            placeholder="Search sessions..."
                            className="w-full pl-10 pr-4 py-2 bg-neuro-surface border border-neuro-border rounded-lg text-neuro-text-primary placeholder-neuro-text-muted focus:outline-none focus:border-neuro-primary"
                        />
                    </div>

                    <div className="flex items-center gap-2">
                        <Filter className="w-4 h-4 text-neuro-text-muted" />
                        <select
                            value={filterMode}
                            onChange={(e) => setFilterMode(e.target.value as any)}
                            className="px-3 py-2 bg-neuro-surface border border-neuro-border rounded-lg text-neuro-text-primary focus:outline-none focus:border-neuro-primary"
                        >
                            <option value="all">All Modes</option>
                            <option value="OFFENSIVE">Offensive</option>
                            <option value="DEFENSIVE">Defensive</option>
                        </select>
                    </div>
                </div>
            </div>

            {/* Session List */}
            <div className="space-y-3">
                {filteredSessions.length > 0 ? (
                    filteredSessions.map((s) => (
                        <SessionCard
                            key={s.id}
                            session={s}
                            onLoad={handleLoadSession}
                            onDelete={handleDeleteSession}
                            onExport={handleExportSession}
                            isActive={session?.id === s.id}
                        />
                    ))
                ) : (
                    <div className="glass-card p-12 text-center">
                        <Folder className="w-16 h-16 text-neuro-text-muted mx-auto mb-4" />
                        <h2 className="text-xl font-semibold text-neuro-text-primary mb-2">
                            {searchQuery || filterMode !== 'all' ? 'No sessions found' : 'No sessions yet'}
                        </h2>
                        <p className="text-neuro-text-secondary mb-4">
                            {searchQuery || filterMode !== 'all'
                                ? 'Try adjusting your search or filter'
                                : 'Create a new session to get started'
                            }
                        </p>
                        {!searchQuery && filterMode === 'all' && (
                            <button
                                onClick={() => setIsCreateModalOpen(true)}
                                className="btn-primary inline-flex items-center gap-2"
                            >
                                <Plus className="w-5 h-5" />
                                Create Your First Session
                            </button>
                        )}
                    </div>
                )}
            </div>

            {/* Create Session Modal */}
            <CreateSessionModal
                isOpen={isCreateModalOpen}
                onClose={() => setIsCreateModalOpen(false)}
                onCreate={handleCreateSession}
            />
        </div>
    );
}
