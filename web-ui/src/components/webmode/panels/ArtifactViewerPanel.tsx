
import React, { useState, useEffect } from 'react';
import { useWebModeContext } from '../WebModeProvider';
import { FileText, Folder, Eye, FileCode, ChevronRight, ChevronDown } from 'lucide-react';
import { FileNode } from '@/lib/webmode/adapter/interface';

interface TreeNodeProps {
    node: FileNode;
    depth?: number;
    onSelect: (path: string) => void;
    selectedPath?: string;
}

const TreeNode: React.FC<TreeNodeProps> = ({ node, depth = 0, onSelect, selectedPath }) => {
    const [expanded, setExpanded] = useState(false);
    const isDir = node.type === 'directory';
    const isSelected = node.path === selectedPath;

    const handleClick = () => {
        if (isDir) {
            setExpanded(!expanded);
        } else {
            onSelect(node.path);
        }
    };

    return (
        <div>
            <div
                onClick={handleClick}
                className={`flex items-center gap-2 py-1 px-2 cursor-pointer transition-colors text-xs font-mono
                  ${isSelected ? 'bg-cyan-500/10 text-cyan-300 border-l-2 border-cyan-500' : 'text-white/60 hover:text-white hover:bg-white/5 border-l-2 border-transparent'}
                `}
                style={{ paddingLeft: `${depth * 12 + 8}px` }}
            >
                {isDir ? (
                    <span className="text-white/40">{expanded ? <ChevronDown className="w-3 h-3" /> : <ChevronRight className="w-3 h-3" />}</span>
                ) : <span className="w-3" />}

                {isDir ? <Folder className="w-3.5 h-3.5 text-yellow-500/80" /> : <FileCode className="w-3.5 h-3.5 text-blue-400/80" />}
                <span className="truncate">{node.name}</span>
            </div>
            {isDir && expanded && node.children && (
                <div>
                    {node.children.map(child => (
                        <TreeNode key={child.path} node={child} depth={depth + 1} onSelect={onSelect} selectedPath={selectedPath} />
                    ))}
                </div>
            )}
        </div>
    );
};

export function ArtifactViewerPanel() {
    const { adapter } = useWebModeContext();
    const [artifacts, setArtifacts] = useState<FileNode[]>([]);
    const [selectedPath, setSelectedPath] = useState<string | undefined>();
    const [content, setContent] = useState<string>('');
    const [loading, setLoading] = useState(false);
    const [sessionId, setSessionId] = useState('current'); // Simplified for now, should link to selected session

    useEffect(() => {
        const loadNodes = async () => {
            try {
                const data = await adapter.listArtifacts(sessionId);
                setArtifacts(data);
            } catch (e) {
                console.error("Failed", e);
            }
        };
        loadNodes();
    }, [sessionId, adapter]);

    const handleSelect = async (path: string) => {
        setSelectedPath(path);
        setLoading(true);
        try {
            const data = await adapter.getArtifactContent(path);
            setContent(data);
        } catch (e) {
            setContent(`Error loading content: ${e}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex h-full gap-2 bg-black/40 backdrop-blur-md border border-white/10 rounded-xl overflow-hidden shadow-xl p-2">
            {/* File Tree */}
            <div className="w-1/3 flex flex-col border-r border-white/10 pr-2">
                <div className="flex items-center gap-2 px-2 py-2 mb-2 border-b border-white/10 opacity-70">
                    <Folder className="w-3.5 h-3.5 text-amber-400" />
                    <span className="text-xs font-bold tracking-wider text-white/80">ARTIFACTS</span>
                </div>
                <div className="flex-1 overflow-y-auto">
                    {artifacts.map(node => (
                        <TreeNode key={node.path} node={node} onSelect={handleSelect} selectedPath={selectedPath} />
                    ))}
                </div>
            </div>

            {/* Content Preview */}
            <div className="flex-1 flex flex-col min-w-0">
                <div className="flex items-center justify-between px-2 py-2 mb-2 border-b border-white/10 opacity-70 bg-black/20 rounded-t">
                    <div className="flex items-center gap-2">
                        <FileText className="w-3.5 h-3.5 text-blue-400" />
                        <span className="text-xs font-mono text-white/60 truncate max-w-[200px]">{selectedPath || 'Select file...'}</span>
                    </div>
                </div>
                <div className="flex-1 bg-black/60 rounded border border-white/5 overflow-auto relative">
                    {loading ? (
                        <div className="absolute inset-0 flex items-center justify-center text-white/20 text-xs animate-pulse">Loading content...</div>
                    ) : selectedPath ? (
                        <pre className="p-3 text-[10px] font-mono text-white/70 leading-relaxed whitespace-pre-wrap">{content}</pre>
                    ) : (
                        <div className="absolute inset-0 flex items-center justify-center text-white/10 text-xs">No file selected</div>
                    )}
                </div>
            </div>
        </div>
    );
}
