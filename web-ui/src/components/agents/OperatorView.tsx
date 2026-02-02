'use client';

import { AgentStatus } from '@/lib/types';
import { Terminal, Shield, PlayCircle } from 'lucide-react';

interface OperatorViewProps {
    status: AgentStatus;
}

export function OperatorView({ status }: OperatorViewProps) {
    return (
        <div className="space-y-4">
            <div className="p-3 bg-black/50 rounded-lg border border-neuro-border font-mono text-sm max-h-40 overflow-y-auto">
                <div className="flex items-center gap-2 text-neuro-text-muted mb-2 border-b border-neuro-border pb-2">
                    <Terminal className="w-3 h-3" />
                    Command Output
                </div>
                <div className="space-y-1 text-neuro-text-primary">
                    <div className="opacity-50">$ nmap -sV -p- 10.10.11.24</div>
                    <div>Starting Nmap 7.94 ( https://nmap.org ) at 2024-02-02 12:00 UTC</div>
                    <div>Nmap scan report for 10.10.11.24</div>
                    <div className="text-yellow-400">Host is up (0.045s latency).</div>
                    <div>Not shown: 65532 closed tcp ports (reset)</div>
                    <div className="text-green-400">PORT   STATE SERVICE VERSION</div>
                    <div className="text-green-400">22/tcp open  ssh     OpenSSH 8.2p1</div>
                    <div className="text-green-400">80/tcp open  http    Apache httpd 2.4.41</div>
                    <div className="animate-pulse">_</div>
                </div>
            </div>

            <div className="bg-neuro-surface rounded-lg border border-neuro-border overflow-hidden">
                <div className="px-3 py-2 border-b border-neuro-border bg-neuro-bg/50 flex items-center justify-between">
                    <span className="text-xs font-medium text-neuro-text-secondary flex items-center gap-2">
                        <PlayCircle className="w-3 h-3" />
                        Active Processes
                    </span>
                    <span className="text-xs px-1.5 py-0.5 rounded bg-green-500/20 text-green-400">1 Running</span>
                </div>
                <div className="p-2 space-y-2">
                    <div className="flex items-center justify-between text-sm p-2 hover:bg-neuro-bg rounded transition-colors">
                        <div className="flex items-center gap-3">
                            <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                            <span className="text-neuro-text-primary">nmap_scan_01</span>
                        </div>
                        <span className="text-neuro-text-muted text-xs">Running (45s)</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
