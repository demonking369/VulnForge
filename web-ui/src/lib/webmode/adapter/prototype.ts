
import { WebModeAdapter, Session, ToolExecution, FileNode } from './interface';

/**
 * PrototypeAdapter: Mock implementation for safe demos and UI development.
 * Simulates backend behavior without actual execution.
 */
export class PrototypeAdapter implements WebModeAdapter {
    private mockSessions: Session[] = [
        {
            id: 'sess_proto_001',
            target: '192.168.1.10',
            mode: 'recon',
            startTime: new Date(Date.now() - 3600000).toISOString(),
            status: 'completed',
            toolCount: 5
        },
        {
            id: 'sess_proto_002',
            target: 'example.com',
            mode: 'scan',
            startTime: new Date().toISOString(),
            status: 'active',
            toolCount: 2
        }
    ];

    private activeExecutions: Map<string, ToolExecution> = new Map();

    async listSessions(): Promise<Session[]> {
        return this.mockSessions;
    }

    async loadSession(id: string): Promise<void> {
        console.log(`[Prototype] Loading session ${id}`);
        return Promise.resolve();
    }

    async deleteSession(id: string): Promise<void> {
        console.log(`[Prototype] Deleting session ${id}`);
        this.mockSessions = this.mockSessions.filter(s => s.id !== id);
        return Promise.resolve();
    }

    async runTool(tool: string, args: string): Promise<string> {
        const id = `exec_${Date.now()}`;
        const startTime = Date.now();

        const execution: ToolExecution = {
            id,
            tool,
            args,
            status: 'running',
            startTime,
            stdout: [`[Prototype] Starting ${tool} ${args}...`],
            stderr: []
        };

        this.activeExecutions.set(id, execution);

        // Simulate output streaming
        this.simulateToolOutput(id, tool);

        return id;
    }

    private simulateToolOutput(id: string, tool: string) {
        let step = 0;
        const interval = setInterval(() => {
            const exec = this.activeExecutions.get(id);
            if (!exec || exec.status !== 'running') {
                clearInterval(interval);
                return;
            }

            step++;

            // Mock output based on tool
            const mockLines: Record<string, string[]> = {
                'nmap': [
                    `Starting Nmap 7.94 ( https://nmap.org ) at ${new Date().toISOString()}`,
                    `Nmap scan report for target (192.168.1.1)`,
                    `Host is up (0.0023s latency).`,
                    `Not shown: 998 closed tcp ports (conn-refused)`,
                    `PORT   STATE SERVICE`,
                    `22/tcp open  ssh`,
                    `80/tcp open  http`,
                    `Nmap done: 1 IP address (1 host up) scanned in 4.23 seconds`
                ],
                'default': [
                    `[Process] Working... (${step}0%)`,
                    `[Process] Generating results...`
                ]
            };

            const lines = mockLines[tool] || mockLines['default'];
            const line = lines[step % lines.length];

            if (line) {
                exec.stdout.push(line);
            }

            if (step >= 5 && Math.random() > 0.5) {
                exec.status = 'completed';
                exec.duration = Date.now() - exec.startTime;
                exec.stdout.push(`[Prototype] Execution completed successfully.`);
                clearInterval(interval);
            }

            this.activeExecutions.set(id, { ...exec }); // Trigger update? In a real app this would push to state or stream
        }, 1000);
    }

    async getToolStatus(executionId: string): Promise<ToolExecution> {
        const exec = this.activeExecutions.get(executionId);
        if (!exec) throw new Error("Execution not found");
        return { ...exec }; // Return copy
    }

    async cancelTool(executionId: string): Promise<void> {
        const exec = this.activeExecutions.get(executionId);
        if (exec) {
            exec.status = 'failed';
            exec.stderr.push('[Prototype] Execution cancelled by user.');
            this.activeExecutions.set(executionId, exec);
        }
    }

    async listArtifacts(sessionId: string): Promise<FileNode[]> {
        return [
            {
                name: 'scans',
                type: 'directory',
                path: '/scans',
                children: [
                    { name: 'nmap_results.txt', type: 'file', path: '/scans/nmap_results.txt', size: 1024 },
                    { name: 'nuclei_report.json', type: 'file', path: '/scans/nuclei_report.json', size: 2048 }
                ]
            },
            { name: 'summary.md', type: 'file', path: '/summary.md', size: 512 }
        ];
    }

    async getArtifactContent(path: string): Promise<string> {
        return `[Prototype] Content for ${path}\n\nThis is simulated content for demonstration purposes.`;
    }

    async getSystemMetrics() {
        // Simulate fluctuating metrics
        return {
            cpu: 10 + Math.random() * 20,
            memory: 30 + Math.random() * 10,
            network: { in: Math.random() * 1000, out: Math.random() * 500 }
        };
    }
}
