'use client';

import { List, CheckCircle2, Clock, AlertTriangle } from 'lucide-react';

interface Task {
    id: string;
    type: string;
    target: string;
    status: 'pending' | 'running' | 'completed' | 'failed';
    progress: number;
}

interface TaskQueueProps {
    tasks: Task[];
}

export function TaskQueue({ tasks }: TaskQueueProps) {
    return (
        <div className="bg-neuro-surface border border-neuro-border rounded-lg flex flex-col h-full">
            <div className="p-3 border-b border-neuro-border flex items-center justify-between">
                <h3 className="text-sm font-medium text-neuro-text-primary flex items-center gap-2">
                    <List className="w-4 h-4" />
                    Task Queue
                </h3>
                <span className="text-xs bg-neuro-bg px-2 py-0.5 rounded text-neuro-text-secondary border border-neuro-border">
                    {tasks.length} Active
                </span>
            </div>

            <div className="flex-1 overflow-y-auto p-3 space-y-3">
                {tasks.map((task) => (
                    <div key={task.id} className="p-3 bg-neuro-bg/30 border border-neuro-border rounded-lg">
                        <div className="flex items-center justify-between mb-2">
                            <span className="text-xs font-semibold text-neuro-text-primary">{task.type}</span>
                            <div className={`
                flex items-center gap-1 text-xs px-1.5 py-0.5 rounded
                ${task.status === 'running' ? 'bg-blue-500/10 text-blue-400' :
                                    task.status === 'completed' ? 'bg-green-500/10 text-green-400' :
                                        task.status === 'failed' ? 'bg-red-500/10 text-red-400' :
                                            'bg-neuro-bg text-neuro-text-muted'}
              `}>
                                {task.status === 'running' && <div className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse" />}
                                {task.status}
                            </div>
                        </div>

                        <p className="text-xs text-neuro-text-secondary mb-2 truncate" title={task.target}>
                            {task.target}
                        </p>

                        <div className="w-full h-1.5 bg-neuro-bg rounded-full overflow-hidden">
                            <div
                                className={`h-full transition-all duration-300 ${task.status === 'failed' ? 'bg-red-500' :
                                        task.status === 'completed' ? 'bg-green-500' :
                                            'bg-blue-500'
                                    }`}
                                style={{ width: `${task.progress}%` }}
                            />
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
