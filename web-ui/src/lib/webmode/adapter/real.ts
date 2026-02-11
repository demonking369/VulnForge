
import { WebModeAdapter, Session, ToolExecution, FileNode } from './interface';

/**
 * RealAdapter: Production implementation connecting to Next.js API routes.
 * These routes bridge to the Python backend (VulnForge/NeuroRift).
 */
export class RealAdapter implements WebModeAdapter {

    private async fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
        const res = await fetch(url, options);
        if (!res.ok) {
            throw new Error(`API Error: ${res.status} ${res.statusText}`);
        }
        return res.json();
    }

    async listSessions(): Promise<Session[]> {
        return this.fetchJson<Session[]>('/api/sessions');
    }

    async loadSession(id: string): Promise<void> {
        await this.fetchJson(`/api/sessions/${id}/load`, { method: 'POST' });
    }

    async deleteSession(id: string): Promise<void> {
        await this.fetchJson(`/api/sessions/${id}`, { method: 'DELETE' });
    }

    async runTool(tool: string, args: string): Promise<string> {
        const res = await this.fetchJson<{ executionId: string }>('/api/tools/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tool, args })
        });
        return res.executionId;
    }

    async getToolStatus(executionId: string): Promise<ToolExecution> {
        return this.fetchJson<ToolExecution>(`/api/tools/status/${executionId}`);
    }

    async cancelTool(executionId: string): Promise<void> {
        await this.fetchJson(`/api/tools/cancel/${executionId}`, { method: 'POST' });
    }

    async listArtifacts(sessionId: string): Promise<FileNode[]> {
        return this.fetchJson<FileNode[]>(`/api/sessions/${sessionId}/artifacts`);
    }

    async getArtifactContent(path: string): Promise<string> {
        const res = await fetch(`/api/fs/content?path=${encodeURIComponent(path)}`);
        if (!res.ok) throw new Error("Failed to fetch content");
        return res.text();
    }

    async getSystemMetrics() {
        return this.fetchJson<{ cpu: number; memory: number; network: { in: number; out: number } }>('/api/system/metrics');
    }
}
