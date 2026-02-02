'use client';

import { useState, useEffect } from 'react';
import { TorStatus } from '@/components/robin/TorStatus';
import { OnionNavigator } from '@/components/robin/OnionNavigator';
import { TaskQueue } from '@/components/robin/TaskQueue';
import { ContentViewer } from '@/components/robin/ContentViewer';

export default function RobinPage() {
    const [torStatus, setTorStatus] = useState<'connected' | 'connecting' | 'disconnected' | 'error'>('disconnected');
    const [activeTask, setActiveTask] = useState<string | null>(null);

    // Mock data
    const [tasks, setTasks] = useState<any[]>([
        { id: '1', type: 'Scrape', target: 'http://dread.onion/topic/123', status: 'completed', progress: 100 },
        { id: '2', type: 'Crawl', target: 'http://ahmia.onion/search', status: 'running', progress: 45 },
        { id: '3', type: 'Index', target: 'http://market.onion', status: 'pending', progress: 0 },
    ]);

    const [selectedContent, setSelectedContent] = useState<any>({
        title: 'Dread Forum - Topic #12345',
        summary: 'Discussion regarding recent CVE-2024-XXXX exploits suggests active trading of PoC code. User "DarkKnight" claims to have a working bypass for the patch.',
        content: 'Thread: New RCE in Popular Framework\nAuthor: DarkKnight\nDate: 2024-02-01\n\nI managed to bypass the filter using a double encoding trick. Here is the payload...',
        url: 'http://dread.onion/topic/12345'
    });

    useEffect(() => {
        // Simulate Tor connection sequence
        setTorStatus('connecting');
        const timer = setTimeout(() => {
            setTorStatus('connected');
        }, 2000);
        return () => clearTimeout(timer);
    }, []);

    const handleNavigate = (url: string) => {
        setTasks(prev => [
            { id: Date.now().toString(), type: 'Scrape', target: url, status: 'pending', progress: 0 },
            ...prev
        ]);
    };

    return (
        <div className="p-6 h-[calc(100vh-4rem)] flex flex-col gap-6">
            <div className="flex items-center justify-between shrink-0">
                <div>
                    <h1 className="text-3xl font-bold text-neuro-text-primary">Robin Intelligence</h1>
                    <p className="text-neuro-text-secondary mt-1">Dark web reconnaissance and monitoring</p>
                </div>
            </div>

            <div className="flex-1 grid grid-cols-12 gap-6 min-h-0">
                {/* Left Column - Navigation & Tasks (4 cols) */}
                <div className="col-span-12 xl:col-span-4 flex flex-col gap-6 min-h-0">
                    <TorStatus status={torStatus} ip="192.168.100.45" />
                    <OnionNavigator onNavigate={handleNavigate} isLoading={false} />
                    <div className="flex-1 min-h-0">
                        <TaskQueue tasks={tasks} />
                    </div>
                </div>

                {/* Right Column - Content Viewer (8 cols) */}
                <div className="col-span-12 xl:col-span-8 min-h-0">
                    <ContentViewer
                        title={selectedContent.title}
                        summary={selectedContent.summary}
                        content={selectedContent.content}
                        url={selectedContent.url}
                    />
                </div>
            </div>
        </div>
    );
}
