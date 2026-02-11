'use client';

import { useState, useEffect } from 'react';
import { useNeuroRift } from '@/lib/hooks';
import { AgentType, AgentStatus } from '@/lib/types';
import { AgentPanel } from '@/components/agents/AgentPanel';
import { PlannerView } from '@/components/agents/PlannerView';
import { OperatorView } from '@/components/agents/OperatorView';
import { NavigatorView } from '@/components/agents/NavigatorView';
import { AnalystView } from '@/components/agents/AnalystView';
import { ScribeView } from '@/components/agents/ScribeView';
import { getWebSocket } from '@/lib/websocket';

const AGENTS: AgentType[] = ['Planner', 'Operator', 'Navigator', 'Analyst', 'Scribe'];

export default function AgentsPage() {
    const { agents } = useNeuroRift();
    const [activeAgent, setActiveAgent] = useState<AgentType | null>(null);

    // Initial data fetch
    useEffect(() => {
        const ws = getWebSocket();
        AGENTS.forEach(agent => {
            ws.send({
                type: 'get_agent_status',
                agent
            });
        });
    }, []);

    const renderAgentContent = (agent: AgentType, status: AgentStatus) => {
        switch (agent) {
            case 'Planner':
                return <PlannerView status={status} />;
            case 'Operator':
                return <OperatorView status={status} />;
            case 'Navigator':
                return <NavigatorView status={status} />;
            case 'Analyst':
                return <AnalystView status={status} />;
            case 'Scribe':
                return <ScribeView status={status} />;
            default:
                return null;
        }
    };

    return (
        <div className="p-6 space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-neuro-text-primary">Cybernetic Agents</h1>
                <p className="text-neuro-text-secondary mt-1">Monitor and interact with autonomous security agents</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
                {AGENTS.map((agent) => (
                    <div key={agent} className={activeAgent === agent ? 'col-span-full' : ''}>
                        <AgentPanel
                            agent={agent}
                            status={agents[agent] || {
                                agent,
                                state: 'idle',
                                current_task: null,
                                last_update: new Date().toISOString()
                            }}
                            isActive={activeAgent === agent}
                            onClick={() => setActiveAgent(activeAgent === agent ? null : agent)}
                        >
                            {renderAgentContent(agent, agents[agent])}
                        </AgentPanel>
                    </div>
                ))}
            </div>
        </div>
    );
}
