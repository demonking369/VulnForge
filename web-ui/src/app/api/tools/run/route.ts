
import { NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

const globalExecutions = (global as any)._nr_executions || new Map();
(global as any)._nr_executions = globalExecutions;

export async function POST(request: Request) {
    try {
        const { tool, args } = await request.json();

        // Security Guard: Only allow specific tools
        const allowedTools = ['nmap', 'nuclei', 'subfinder', 'ffuf', 'whois', 'dig'];
        if (!allowedTools.includes(tool)) {
            return NextResponse.json({ error: 'Tool not allowed' }, { status: 403 });
        }

        const executionId = `exec_${Date.now()}`;
        const cmdArgs = args.split(' ').filter((a: string) => a.length > 0);

        console.log(`[API] Spawning: ${tool} ${args}`);

        try {
            const child = spawn(tool, cmdArgs, { shell: false });

            globalExecutions.set(executionId, {
                id: executionId,
                tool,
                args,
                status: 'running',
                startTime: Date.now(),
                stdout: [],
                stderr: [],
                process: child
            });

            child.stdout.on('data', (data) => {
                const lines = data.toString().split('\n');
                const exec = globalExecutions.get(executionId);
                if (exec) exec.stdout.push(...lines);
            });

            child.stderr.on('data', (data) => {
                const lines = data.toString().split('\n');
                const exec = globalExecutions.get(executionId);
                if (exec) exec.stderr.push(...lines);
            });

            child.on('close', (code) => {
                const exec = globalExecutions.get(executionId);
                if (exec) {
                    exec.status = code === 0 ? 'completed' : 'failed';
                    exec.exitCode = code;
                }
            });

            child.on('error', (err) => {
                const exec = globalExecutions.get(executionId);
                if (exec) {
                    exec.status = 'failed';
                    exec.stderr.push(`Process error: ${err.message}`);
                }
            });

        } catch (spawnError) {
            return NextResponse.json({ error: `Failed to spawn: ${spawnError}` }, { status: 500 });
        }

        return NextResponse.json({ executionId });

    } catch (e) {
        return NextResponse.json({ error: String(e) }, { status: 500 });
    }
}
