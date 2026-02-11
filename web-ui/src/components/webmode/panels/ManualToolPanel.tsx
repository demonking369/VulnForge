
import React, { useState, useEffect, useRef } from 'react';
import { useWebModeContext } from '../WebModeProvider';
import { Play, Square, Terminal, Loader2 } from 'lucide-react';

export function ManualToolPanel() {
    const { adapter } = useWebModeContext();
    const [selectedTool, setSelectedTool] = useState('nmap');
    const [args, setArgs] = useState('');
    const [isRunning, setIsRunning] = useState(false);
    const [executionId, setExecutionId] = useState<string | null>(null);
    const [output, setOutput] = useState<string[]>([]);
    const outputRef = useRef<HTMLDivElement>(null);

    const tools = ['nmap', 'nuclei', 'subfinder', 'ffuf', 'custom'];

    const handleRun = async () => {
        try {
            setIsRunning(true);
            setOutput([]);
            const id = await adapter.runTool(selectedTool, args);
            setExecutionId(id);
        } catch (e) {
            setOutput(prev => [...prev, `Error starting tool: ${e}`]);
            setIsRunning(false);
        }
    };

    const handleStop = async () => {
        if (executionId) {
            await adapter.cancelTool(executionId);
            setIsRunning(false);
            setOutput(prev => [...prev, '\n[Stopped by user]']);
        }
    };

    useEffect(() => {
        if (!isRunning || !executionId) return;

        const interval = setInterval(async () => {
            try {
                const status = await adapter.getToolStatus(executionId);
                setOutput([...status.stdout, ...status.stderr]);

                if (status.status !== 'running') {
                    setIsRunning(false);
                    setExecutionId(null);
                }
            } catch (e) {
                console.error("Failed to poll status", e);
            }
        }, 1000);

        return () => clearInterval(interval);
    }, [isRunning, executionId, adapter]);

    useEffect(() => {
        if (outputRef.current) {
            outputRef.current.scrollTop = outputRef.current.scrollHeight;
        }
    }, [output]);

    return (
        <div className="flex flex-col h-full bg-black/40 backdrop-blur-md border border-white/10 rounded-xl overflow-hidden shadow-xl">
            <div className="flex items-center justify-between px-4 py-3 bg-white/5 border-b border-white/10">
                <div className="flex items-center gap-2">
                    <Terminal className="w-4 h-4 text-cyan-400" />
                    <span className="font-mono text-sm font-medium text-cyan-100/90 tracking-wide">MANUAL OPERATOR PLANE</span>
                </div>
                {isRunning && <span className="text-xs text-green-400 animate-pulse flex items-center gap-1"><Loader2 className="w-3 h-3 animate-spin" /> EXECUTING</span>}
            </div>

            <div className="p-4 space-y-4 flex-1 flex flex-col min-h-0">
                <div className="flex gap-2">
                    <select
                        value={selectedTool}
                        onChange={(e) => setSelectedTool(e.target.value)}
                        disabled={isRunning}
                        className="bg-black/50 border border-white/20 rounded px-3 py-1.5 text-sm font-mono text-cyan-100 focus:outline-none focus:border-cyan-500/50"
                    >
                        {tools.map(t => <option key={t} value={t}>{t}</option>)}
                    </select>
                    <input
                        type="text"
                        value={args}
                        onChange={(e) => setArgs(e.target.value)}
                        placeholder="--flags target"
                        disabled={isRunning}
                        className="flex-1 bg-black/50 border border-white/20 rounded px-3 py-1.5 text-sm font-mono text-cyan-100 focus:outline-none focus:border-cyan-500/50 placeholder-white/20"
                    />
                    {!isRunning ? (
                        <button
                            onClick={handleRun}
                            disabled={!args && selectedTool === 'custom'}
                            className="bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 border border-cyan-500/30 rounded px-3 py-1.5 transition-colors flex items-center justify-center w-10"
                        >
                            <Play className="w-4 h-4" />
                        </button>
                    ) : (
                        <button
                            onClick={handleStop}
                            className="bg-red-500/20 hover:bg-red-500/30 text-red-300 border border-red-500/30 rounded px-3 py-1.5 transition-colors flex items-center justify-center w-10"
                        >
                            <Square className="w-4 h-4 fill-current" />
                        </button>
                    )}
                </div>

                <div
                    ref={outputRef}
                    className="flex-1 bg-black/80 rounded border border-white/10 p-3 font-mono text-xs overflow-y-auto min-h-[150px] shadow-inner font-light"
                >
                    {output.length === 0 ? (
                        <span className="text-white/20 italic">Ready for input...</span>
                    ) : (
                        output.map((line, i) => (
                            <div key={i} className="whitespace-pre-wrap break-all text-white/80 leading-relaxed border-l-2 border-transparent hover:border-white/10 hover:bg-white/5 px-1">{line}</div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
}
