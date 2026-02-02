'use client';

import { useNeuroRift } from '@/lib/hooks';
import { Home, Folder, Cpu, Wrench, Globe, Shield, FileText, Terminal, Settings } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';

const navItems = [
    { icon: Home, label: 'Dashboard', href: '/' },
    { icon: Folder, label: 'Sessions', href: '/sessions' },
    { icon: Cpu, label: 'Agents', href: '/agents' },
    { icon: Wrench, label: 'Tools', href: '/tools' },
    { icon: Globe, label: 'Browser', href: '/browser' },
    { icon: Shield, label: 'Robin', href: '/robin' },
    { icon: FileText, label: 'Vulnerabilities', href: '/vulnerabilities' },
    { icon: Terminal, label: 'Logs', href: '/logs' },
    { icon: Settings, label: 'Settings', href: '/settings' },
];

export function LeftNav() {
    const pathname = usePathname();

    return (
        <nav className="w-64 bg-neuro-surface border-r border-neuro-border flex flex-col">
            <div className="flex-1 py-4">
                {navItems.map((item) => {
                    const Icon = item.icon;
                    const isActive = pathname === item.href;

                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                'flex items-center gap-3 px-4 py-3 text-sm transition-colors',
                                isActive
                                    ? 'bg-neuro-primary/10 text-neuro-primary border-r-2 border-neuro-primary'
                                    : 'text-neuro-text-secondary hover:text-neuro-text-primary hover:bg-neuro-bg/50'
                            )}
                        >
                            <Icon className="w-5 h-5" />
                            <span>{item.label}</span>
                        </Link>
                    );
                })}
            </div>

            <div className="p-4 border-t border-neuro-border text-xs text-neuro-text-muted">
                <p>NeuroRift v1.0</p>
                <p className="mt-1">by demonking369</p>
            </div>
        </nav>
    );
}
