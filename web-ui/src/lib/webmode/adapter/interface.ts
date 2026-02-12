
import { WebModeConfig } from '../types';

export interface FileNode {
    name: string;
    type: 'file' | 'directory';
    path: string;
    children?: FileNode[];
    size?: number;
    lastModified?: string;
}

export interface Session {
    id: string;
    target: string;
    mode: string;
    startTime: string;
    status: 'active' | 'completed' | 'failed';
    toolCount: number;
}

export interface ToolExecution {
    id: string;
    tool: string;
    args: string;
    status: 'running' | 'completed' | 'failed';
    startTime: number;
    duration?: number;
    stdout: string[];
    stderr: string[];
}

export interface Artifact {
    id: string;
    sessionId: string;
    filename: string;
    type: 'json' | 'markdown' | 'html' | 'text';
    content?: string;
}

export interface WebModeAdapter {
    // Session Management
    listSessions(): Promise<Session[]>;
    loadSession(id: string): Promise<void>;
    deleteSession(id: string): Promise<void>;

    // Tool Execution
    runTool(tool: string, args: string): Promise<string>; // Returns execution ID
    getToolStatus(executionId: string): Promise<ToolExecution>;
    cancelTool(executionId: string): Promise<void>;

    // Filesystem / Artifacts
    listArtifacts(sessionId: string): Promise<FileNode[]>;
    getArtifactContent(path: string): Promise<string>;

    // System State
    getSystemMetrics(): Promise<{ cpu: number; memory: number; network: { in: number; out: number } }>;
}
