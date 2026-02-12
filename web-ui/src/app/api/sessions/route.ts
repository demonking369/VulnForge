
import { NextResponse } from 'next/server';
import fs from 'fs/promises';
import path from 'path';
import os from 'os';

export async function GET() {
    try {
        const sessionsDir = path.join(os.homedir(), '.vulnforge', 'sessions');

        // Check if directory exists
        try {
            await fs.access(sessionsDir);
        } catch {
            return NextResponse.json([]);
        }

        const targets = await fs.readdir(sessionsDir, { withFileTypes: true });

        const sessions = [];

        for (const target of targets) {
            if (!target.isDirectory()) continue;

            const targetPath = path.join(sessionsDir, target.name);
            const timestamps = await fs.readdir(targetPath, { withFileTypes: true });

            for (const ts of timestamps) {
                if (!ts.isDirectory()) continue;

                // Try to read metadata if it exists
                const sessionPath = path.join(targetPath, ts.name);
                let metadata = { toolCount: 0, status: 'completed' }; // Defaults

                // You might want to define a metadata.json in each session folder in the python backend

                sessions.push({
                    id: `${target.name}__${ts.name}`, // Composite ID
                    target: target.name,
                    startTime: parseTimestamp(ts.name), // Helper needed
                    mode: 'recon', // Default or read from metadata
                    status: metadata.status,
                    toolCount: metadata.toolCount
                });
            }
        }

        // Sort by recent first
        sessions.sort((a, b) => new Date(b.startTime).getTime() - new Date(a.startTime).getTime());

        return NextResponse.json(sessions);
    } catch (e) {
        return NextResponse.json({ error: 'Failed to list sessions' }, { status: 500 });
    }
}

function parseTimestamp(ts: string) {
    // Expected format: YYYYMMDD_HHMMSS
    // Simple fallback
    try {
        const parts = ts.split('_');
        const dateStr = parts[0];
        const timeStr = parts[1];
        const year = parseInt(dateStr.substring(0, 4));
        const month = parseInt(dateStr.substring(4, 6)) - 1;
        const day = parseInt(dateStr.substring(6, 8));
        const hour = parseInt(timeStr.substring(0, 2));
        const min = parseInt(timeStr.substring(2, 4));
        const sec = parseInt(timeStr.substring(4, 6));
        return new Date(year, month, day, hour, min, sec).toISOString();
    } catch {
        return new Date().toISOString();
    }
}
