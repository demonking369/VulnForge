'use client';

import { Wrench, Search, Play, Info } from 'lucide-react';
import { useState } from 'react';

interface Tool {
    name: string;
    category: string;
    description: string;
    risk_level: 'low' | 'medium' | 'high';
    allowed_modes: string[];
}

const MOCK_TOOLS: Tool[] = [
    {
        name: 'nmap',
        category: 'Reconnaissance',
        description: 'Network exploration and security auditing',
        risk_level: 'low',
        allowed_modes: ['OFFENSIVE', 'DEFENSIVE']
    },
    {
        name: 'nuclei',
        category: 'Scanning',
        description: 'Fast vulnerability scanner based on templates',
        risk_level: 'medium',
        allowed_modes: ['OFFENSIVE', 'DEFENSIVE']
    },
    {
        name: 'sqlmap',
        category: 'Exploitation',
        description: 'Automatic SQL injection and database takeover',
        risk_level: 'high',
        allowed_modes: ['OFFENSIVE']
    },
    {
        name: 'subfinder',
        category: 'Reconnaissance',
        description: 'Subdomain discovery tool',
        risk_level: 'low',
        allowed_modes: ['OFFENSIVE', 'DEFENSIVE']
    },
    {
        name: 'httpx',
        category: 'Reconnaissance',
        description: 'Fast HTTP toolkit',
        risk_level: 'low',
        allowed_modes: ['OFFENSIVE', 'DEFENSIVE']
    },
    {
        name: 'ffuf',
        category: 'Scanning',
        description: 'Fast web fuzzer',
        risk_level: 'medium',
        allowed_modes: ['OFFENSIVE']
    },
];

const CATEGORIES = ['All', 'Reconnaissance', 'Scanning', 'Exploitation', 'Analysis'];

const RISK_COLORS = {
    low: 'text-severity-low',
    medium: 'text-severity-medium',
    high: 'text-severity-critical'
};

export default function ToolsPage() {
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('All');

    const filteredTools = MOCK_TOOLS.filter(tool => {
        const matchesSearch = tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            tool.description.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesCategory = selectedCategory === 'All' || tool.category === selectedCategory;
        return matchesSearch && matchesCategory;
    });

    return (
        <div className="p-6 space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-neuro-text-primary">Security Tools</h1>
                <p className="text-neuro-text-secondary mt-1">Browse and execute security assessment tools</p>
            </div>

            {/* Search and Filter */}
            <div className="glass-card p-4">
                <div className="flex items-center gap-4">
                    <div className="flex-1 relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-neuro-text-muted" />
                        <input
                            type="text"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            placeholder="Search tools..."
                            className="w-full pl-10 pr-4 py-2 bg-neuro-surface border border-neuro-border rounded-lg text-neuro-text-primary placeholder-neuro-text-muted focus:outline-none focus:border-neuro-primary"
                        />
                    </div>
                </div>

                {/* Category Tabs */}
                <div className="flex items-center gap-2 mt-4 overflow-x-auto">
                    {CATEGORIES.map((category) => (
                        <button
                            key={category}
                            onClick={() => setSelectedCategory(category)}
                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors whitespace-nowrap ${selectedCategory === category
                                    ? 'bg-neuro-primary text-white'
                                    : 'bg-neuro-surface text-neuro-text-secondary hover:bg-neuro-bg'
                                }`}
                        >
                            {category}
                        </button>
                    ))}
                </div>
            </div>

            {/* Tools Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredTools.map((tool) => (
                    <div key={tool.name} className="glass-card p-5 hover:border-neuro-primary/50 transition-all">
                        <div className="flex items-start justify-between mb-3">
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 rounded-lg bg-neuro-primary/20 flex items-center justify-center">
                                    <Wrench className="w-5 h-5 text-neuro-primary" />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-neuro-text-primary">{tool.name}</h3>
                                    <span className="text-xs text-neuro-text-muted">{tool.category}</span>
                                </div>
                            </div>
                            <span className={`text-xs font-medium capitalize ${RISK_COLORS[tool.risk_level]}`}>
                                {tool.risk_level}
                            </span>
                        </div>

                        <p className="text-sm text-neuro-text-secondary mb-4 line-clamp-2">
                            {tool.description}
                        </p>

                        <div className="flex items-center gap-2">
                            <button className="flex-1 btn-primary flex items-center justify-center gap-2 text-sm py-2">
                                <Play className="w-4 h-4" />
                                Execute
                            </button>
                            <button className="p-2 bg-neuro-surface border border-neuro-border rounded-lg hover:bg-neuro-bg transition-colors">
                                <Info className="w-4 h-4 text-neuro-text-muted" />
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            {filteredTools.length === 0 && (
                <div className="glass-card p-12 text-center">
                    <Wrench className="w-16 h-16 text-neuro-text-muted mx-auto mb-4" />
                    <h2 className="text-xl font-semibold text-neuro-text-primary mb-2">No tools found</h2>
                    <p className="text-neuro-text-secondary">Try adjusting your search or filter</p>
                </div>
            )}
        </div>
    );
}
