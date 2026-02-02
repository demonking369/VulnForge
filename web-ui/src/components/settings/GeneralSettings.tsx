'use client';

import { Label } from '@/components/ui/label';
import { Settings, Save } from 'lucide-react';

export function GeneralSettings() {
    return (
        <div className="space-y-6">
            <div className="flex items-center gap-2 mb-4">
                <Settings className="w-5 h-5 text-neuro-primary" />
                <h2 className="text-lg font-semibold text-neuro-text-primary">General Configuration</h2>
            </div>

            <div className="space-y-4">
                <div className="grid gap-2">
                    <Label>Proxy Configuration</Label>
                    <input
                        type="text"
                        placeholder="http://127.0.0.1:8080"
                        className="w-full bg-neuro-bg border border-neuro-border rounded-md px-3 py-2 text-sm text-neuro-text-primary focus:outline-none focus:ring-1 focus:ring-neuro-primary"
                    />
                    <p className="text-xs text-neuro-text-muted">Global proxy for all tools (except Tor routed traffic)</p>
                </div>

                <div className="grid gap-2">
                    <Label>Data Retention</Label>
                    <select className="w-full bg-neuro-bg border border-neuro-border rounded-md px-3 py-2 text-sm text-neuro-text-primary focus:outline-none focus:ring-1 focus:ring-neuro-primary">
                        <option>7 Days</option>
                        <option>30 Days</option>
                        <option>90 Days</option>
                        <option>Forever</option>
                    </select>
                    <p className="text-xs text-neuro-text-muted">How long to keep session logs and artifacts</p>
                </div>

                <div className="flex items-center gap-3 bg-neuro-surface border border-neuro-border rounded-lg p-3">
                    <input type="checkbox" id="telemetry" className="rounded border-neuro-border bg-neuro-bg text-neuro-primary focus:ring-neuro-primary" />
                    <div className="grid gap-1">
                        <label htmlFor="telemetry" className="text-sm font-medium text-neuro-text-primary">Anonymous Telemetry</label>
                        <p className="text-xs text-neuro-text-muted">Help improve NeuroRift by sending anonymous usage statistics</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
