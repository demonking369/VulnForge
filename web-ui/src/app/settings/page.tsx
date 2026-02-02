'use client';

import { GeneralSettings } from '@/components/settings/GeneralSettings';
import { APIKeys } from '@/components/settings/APIKeys';
import { ThemeSelector } from '@/components/settings/ThemeSelector';
import { Save } from 'lucide-react';

export default function SettingsPage() {
    return (
        <div className="p-6 h-full overflow-y-auto">
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-neuro-text-primary">System Configuration</h1>
                    <p className="text-neuro-text-secondary mt-1">Manage global preferences and integrations</p>
                </div>

                <button className="px-4 py-2 bg-neuro-primary text-white rounded-md flex items-center gap-2 hover:bg-neuro-primary/90 transition-colors shadow-lg shadow-neuro-primary/20">
                    <Save className="w-4 h-4" />
                    Save Changes
                </button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-6xl">
                <div className="space-y-8">
                    <section className="bg-neuro-surface border border-neuro-border rounded-lg p-6">
                        <GeneralSettings />
                    </section>

                    <section className="bg-neuro-surface border border-neuro-border rounded-lg p-6">
                        <ThemeSelector />
                    </section>
                </div>

                <div className="space-y-8">
                    <section className="bg-neuro-surface border border-neuro-border rounded-lg p-6">
                        <APIKeys />
                    </section>

                    <section className="bg-neuro-surface border border-neuro-border rounded-lg p-6">
                        <div className="flex items-center gap-2 mb-4">
                            <h2 className="text-lg font-semibold text-neuro-text-primary">About NeuroRift</h2>
                        </div>
                        <div className="space-y-2 text-sm text-neuro-text-secondary">
                            <div className="flex justify-between py-2 border-b border-neuro-border/50">
                                <span>Version</span>
                                <span className="font-mono text-neuro-text-primary">2.0.0-alpha</span>
                            </div>
                            <div className="flex justify-between py-2 border-b border-neuro-border/50">
                                <span>Core Build</span>
                                <span className="font-mono text-neuro-text-primary">rust-native-v1</span>
                            </div>
                            <div className="flex justify-between py-2 border-b border-neuro-border/50">
                                <span>Web Interface</span>
                                <span className="font-mono text-neuro-text-primary">next-14-rsc</span>
                            </div>
                        </div>
                    </section>
                </div>
            </div>
        </div>
    );
}
