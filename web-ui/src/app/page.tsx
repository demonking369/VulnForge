'use client';

<<<<<<< HEAD
import { useState } from 'react';
import { WebModeProvider } from '@/components/webmode/WebModeProvider';
import { CommandPanel } from '@/components/webmode/panels/CommandPanel';
import { AgentGraphPanel } from '@/components/webmode/panels/AgentGraphPanel';
import { MemoryPulsePanel } from '@/components/webmode/panels/MemoryPulsePanel';
import { PermissionsPanel } from '@/components/webmode/panels/PermissionsPanel';
import { ConfigMatrixPanel } from '@/components/webmode/panels/ConfigMatrixPanel';
import { OnlineModePanel } from '@/components/webmode/panels/OnlineModePanel';
import { ActivityStreamPanel } from '@/components/webmode/panels/ActivityStreamPanel';
import { ExecutionTimelinePanel } from '@/components/webmode/panels/ExecutionTimelinePanel';
import { IntentFlowPanel } from '@/components/webmode/panels/IntentFlowPanel';
import { ManualToolPanel } from '@/components/webmode/panels/ManualToolPanel';
import { SessionManagerPanel } from '@/components/webmode/panels/SessionManagerPanel';
import { ArtifactViewerPanel } from '@/components/webmode/panels/ArtifactViewerPanel';
import { cn } from '@/lib/utils';
import { useWebModeContext } from '@/components/webmode/WebModeProvider'; // Import context hook

const TABS = [
    { id: 'command', label: 'Command' },
    { id: 'operator', label: 'Operator' }, // New Operator Tab
    { id: 'agents', label: 'Agents' },
    { id: 'memory', label: 'Memory' },
    { id: 'permissions', label: 'Permissions' },
    { id: 'config', label: 'Config' },
    { id: 'online', label: 'Online' },
] as const;

type TabId = (typeof TABS)[number]['id'];

function ModeBanner() {
    const { adapter } = useWebModeContext();
    // Check if adapter is prototype (this check is a bit naive, ideally we check config or adapter type property)
    // But since we don't expose type, we can infer or rely on config injection
    const isPrototype = adapter.constructor.name === 'PrototypeAdapter';

    if (isPrototype) {
        return (
            <div className="bg-yellow-500/10 border-b border-yellow-500/20 text-yellow-500 text-[10px] font-mono text-center py-1 uppercase tracking-widest">
                ⚠ Prototype Mode — Simulated Environment
            </div>
        );
    }
    return null;
}


function Dashboard() {
    const [activeTab, setActiveTab] = useState<TabId>('command');

    return (
        <div className="min-h-screen bg-neuro-bg flex flex-col">
            <ModeBanner />
            {/* Header */}
            <header className="border-b border-neuro-border/40 bg-neuro-surface/50 backdrop-blur-sm sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center text-white font-bold text-sm">N</div>
                        <div>
                            <h1 className="text-sm font-bold uppercase tracking-[0.2em] text-neuro-text-primary">NeuroRift</h1>
                            <div className="text-[9px] uppercase tracking-wider text-neuro-text-muted">Web Mode — Control Plane</div>
                        </div>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
                        <span className="text-[10px] uppercase tracking-wider text-emerald-300">Online</span>
                    </div>
                </div>
            </header>

            {/* Tab Navigation */}
            <nav className="border-b border-neuro-border/30 bg-neuro-bg/80 backdrop-blur-sm sticky top-[52px] z-40">
                <div className="max-w-7xl mx-auto px-4 flex gap-1 overflow-x-auto">
                    {TABS.map(tab => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={cn(
                                "px-4 py-2.5 text-xs uppercase tracking-[0.2em] border-b-2 transition-all whitespace-nowrap",
                                activeTab === tab.id
                                    ? "border-cyan-400 text-cyan-300"
                                    : "border-transparent text-neuro-text-muted hover:text-neuro-text-secondary"
                            )}
                        >
                            {tab.label}
                        </button>
                    ))}
                </div>
            </nav>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 py-6 flex-1 min-h-0">
                {activeTab === 'operator' ? (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[calc(100vh-140px)]">
                        <div className="flex flex-col gap-6 h-full min-h-0">
                            <div className="flex-1 min-h-0">
                                <ManualToolPanel />
                            </div>
                            <div className="flex-1 min-h-0">
                                <SessionManagerPanel />
                            </div>
                        </div>
                        <div className="h-full min-h-0">
                            <ArtifactViewerPanel />
                        </div>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 lg:grid-cols-[1fr_320px] gap-6">
                        {/* Primary Panel */}
                        <div className="rounded-2xl border border-neuro-border/40 bg-neuro-surface/30 backdrop-blur-sm p-6">
                            {activeTab === 'command' && <CommandPanel />}
                            {activeTab === 'agents' && <AgentGraphPanel />}
                            {activeTab === 'memory' && <MemoryPulsePanel />}
                            {activeTab === 'permissions' && <PermissionsPanel />}
                            {activeTab === 'config' && <ConfigMatrixPanel />}
                            {activeTab === 'online' && <OnlineModePanel />}
                        </div>

                        {/* Sidebar */}
                        <div className="space-y-6">
                            <div className="rounded-2xl border border-neuro-border/40 bg-neuro-surface/30 backdrop-blur-sm p-4">
                                <ActivityStreamPanel />
                            </div>
                            <div className="rounded-2xl border border-neuro-border/40 bg-neuro-surface/30 backdrop-blur-sm p-4">
                                <ExecutionTimelinePanel />
                            </div>
                            <div className="rounded-2xl border border-neuro-border/40 bg-neuro-surface/30 backdrop-blur-sm p-4">
                                <IntentFlowPanel />
                            </div>
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}

export default function WebModePage() {
    return (
        <WebModeProvider>
            <Dashboard />
        </WebModeProvider>
    );
=======
import { CommandCenter } from '@/components/webmode/CommandCenter';

export default function DashboardPage() {
    return <CommandCenter />;
>>>>>>> main
}
