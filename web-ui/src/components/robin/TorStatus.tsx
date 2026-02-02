'use client';

import { Shield, ShieldAlert, ShieldCheck } from 'lucide-react';

interface TorStatusProps {
    status: 'connected' | 'connecting' | 'disconnected' | 'error';
    ip?: string;
}

export function TorStatus({ status, ip }: TorStatusProps) {
    return (
        <div className="flex flex-col gap-2 p-4 bg-neuro-surface border border-neuro-border rounded-lg">
            <div className="flex items-center justify-between">
                <h3 className="text-sm font-medium text-neuro-text-primary flex items-center gap-2">
                    <Shield className="w-4 h-4" />
                    Tor Network Status
                </h3>
                <div className={`
          px-2 py-0.5 rounded text-xs font-medium border flex items-center gap-1.5
          ${status === 'connected' ? 'bg-green-500/10 border-green-500/30 text-green-400' :
                        status === 'connecting' ? 'bg-yellow-500/10 border-yellow-500/30 text-yellow-400' :
                            'bg-red-500/10 border-red-500/30 text-red-400'}
        `}>
                    <div className={`w-1.5 h-1.5 rounded-full ${status === 'connected' ? 'bg-green-500' :
                            status === 'connecting' ? 'bg-yellow-500 animate-pulse' :
                                'bg-red-500'
                        }`} />
                    {status.toUpperCase()}
                </div>
            </div>

            <div className="flex items-center gap-2 text-sm">
                <span className="text-neuro-text-secondary">Circuit IP:</span>
                <span className="font-mono text-neuro-text-primary bg-neuro-bg px-2 py-0.5 rounded border border-neuro-border/30">
                    {ip || '---.---.---.---'}
                </span>
            </div>

            {status === 'connected' && (
                <div className="text-xs text-neuro-text-muted mt-1 flex items-center gap-1">
                    <ShieldCheck className="w-3 h-3 text-green-500" />
                    Traffic is anonymized and routed through Tor
                </div>
            )}
        </div>
    );
}
