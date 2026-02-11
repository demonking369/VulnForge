type WebSocketPayload = Record<string, any> & { type: string };

class MockWebSocket {
    private listeners = new Map<string, (payload: any) => void>();

    send(payload: WebSocketPayload) {
        switch (payload.type) {
            case 'chat':
                setTimeout(() => {
                    window.dispatchEvent(
                        new CustomEvent('neurorift:chat_response', {
                            detail: {
                                response: `Echoed intent received: ${payload.message}`
                            }
                        })
                    );
                }, 500);
                break;
            case 'get_session_list':
                setTimeout(() => {
                    window.dispatchEvent(
                        new CustomEvent('neurorift:session_list', {
                            detail: {
                                type: 'session_list',
                                sessions: sampleSessions
                            }
                        })
                    );
                }, 250);
                break;
            case 'create_session':
                sampleSessions.unshift({
                    id: `session-${Date.now()}`,
                    name: payload.name,
                    mode: payload.mode,
                    status: 'active',
                    updated_at: new Date().toISOString(),
                    findings: [],
                    artifacts: [],
                    metadata: payload.metadata || {},
                });
                window.dispatchEvent(
                    new CustomEvent('neurorift:session_list', {
                        detail: {
                            type: 'session_list',
                            sessions: sampleSessions
                        }
                    })
                );
                break;
            default:
                break;
        }
    }

    on(event: string, handler: (payload: any) => void) {
        this.listeners.set(event, handler);
    }
}

const sampleSessions = [
    {
        id: 'session-aurora',
        name: 'Aurora Lattice Sweep',
        mode: 'DEFENSIVE',
        status: 'active',
        updated_at: new Date(Date.now() - 1000 * 60 * 12).toISOString(),
        findings: [],
        artifacts: [],
        metadata: { description: 'Continuous defense posture validation.' }
    },
    {
        id: 'session-echo',
        name: 'Echo Vector Audit',
        mode: 'OFFENSIVE',
        status: 'paused',
        updated_at: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
        findings: [],
        artifacts: [],
        metadata: { description: 'Red-team simulation across agent mesh.' }
    }
];

let instance: MockWebSocket | null = null;

export function getWebSocket() {
    if (!instance) {
        instance = new MockWebSocket();
    }

    return instance;
}
