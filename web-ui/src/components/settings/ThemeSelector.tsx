'use client';

import { Moon, Sun, Monitor, Palette } from 'lucide-react';

export function ThemeSelector() {
    return (
        <div className="space-y-6">
            <div className="flex items-center gap-2 mb-4">
                <Palette className="w-5 h-5 text-neuro-primary" />
                <h2 className="text-lg font-semibold text-neuro-text-primary">Appearance</h2>
            </div>

            <div className="grid grid-cols-3 gap-4">
                <button className="flex flex-col items-center gap-3 p-4 rounded-lg border border-neuro-border bg-neuro-surface hover:border-neuro-primary transition-all group">
                    <div className="w-10 h-10 rounded-full bg-neuro-bg flex items-center justify-center group-hover:text-neuro-primary transition-colors">
                        <Sun className="w-5 h-5" />
                    </div>
                    <span className="text-sm font-medium text-neuro-text-primary">Light</span>
                </button>

                <button className="flex flex-col items-center gap-3 p-4 rounded-lg border border-neuro-primary bg-neuro-primary/5 ring-1 ring-neuro-primary transition-all">
                    <div className="w-10 h-10 rounded-full bg-neuro-bg flex items-center justify-center text-neuro-primary">
                        <Moon className="w-5 h-5" />
                    </div>
                    <span className="text-sm font-medium text-neuro-text-primary">Dark</span>
                </button>

                <button className="flex flex-col items-center gap-3 p-4 rounded-lg border border-neuro-border bg-neuro-surface hover:border-neuro-primary transition-all group">
                    <div className="w-10 h-10 rounded-full bg-neuro-bg flex items-center justify-center group-hover:text-neuro-primary transition-colors">
                        <Monitor className="w-5 h-5" />
                    </div>
                    <span className="text-sm font-medium text-neuro-text-primary">System</span>
                </button>
            </div>

            <div className="pt-4 border-t border-neuro-border">
                <h3 className="text-sm font-medium text-neuro-text-primary mb-3">Accent Color</h3>
                <div className="flex gap-3">
                    {['bg-cyan-500', 'bg-blue-500', 'bg-purple-500', 'bg-green-500', 'bg-red-500', 'bg-orange-500'].map((color) => (
                        <button
                            key={color}
                            className={`w-8 h-8 rounded-full ${color} hover:ring-2 ring-offset-2 ring-offset-neuro-bg ring-neuro-text-primary transition-all`}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
}
