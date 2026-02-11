'use client';

<<<<<<< HEAD
import React, { createContext, useContext, useReducer, useEffect, ReactNode, useMemo, useState } from 'react';
import {
    WebModeState,
    WebModeAction,
    DeviceTier,
    IntentDraft,
    PermissionRequest,
    WebModeConfig,
    AgentNode,
    MemoryMetric
} from '../../lib/webmode/types';
import {
    webModeReducer,
    initialState,
    bootSequence,
    useDeviceTier
} from '../../lib/webmode/state';
import { initialConfig } from '../../lib/webmode/config-schema';
import { WebModeAdapter } from '../../lib/webmode/adapter/interface';
import { PrototypeAdapter } from '../../lib/webmode/adapter/prototype';
import { RealAdapter } from '../../lib/webmode/adapter/real';

// 1. Context Definition
interface WebModeContextType {
    state: WebModeState;
    config: WebModeConfig;
    adapter: WebModeAdapter; // Expose adapter
    dispatch: React.Dispatch<WebModeAction>;
    updateConfig: (section: keyof WebModeConfig, key: string, value: any) => void;
    queueIntent: (text: string) => void;
    resolvePermission: (id: string, decision: 'approved' | 'denied') => void;
    sendSignal: (signal: string) => void;

    // Legacy/Computed properties for compatibility
    deviceTier: DeviceTier;
    controlMode: 'read' | 'control';
    phase: string;
    lastSignal: string;
    intentQueue: IntentDraft[];
    agentState: Record<string, AgentNode>;
    memoryPulse: MemoryMetric[];
    permissionQueue: PermissionRequest[];
}

const WebModeContext = createContext<WebModeContextType | undefined>(undefined);

// 2. Provider Component
export function WebModeProvider({ children }: { children: ReactNode }) {
    const [state, dispatch] = useReducer(webModeReducer, initialState);
    const [config, setConfig] = useState<WebModeConfig>(initialConfig);
    const deviceTier = useDeviceTier();

    // Initialize Adapter based on Env Var
    const adapter = useMemo(() => {
        // In a real app we might use a compile-time constant or a robust env check.
        // Here we assume NEXT_PUBLIC_NR_MODE is injected by the launcher.
        const mode = process.env.NEXT_PUBLIC_NR_MODE;
        console.log(`[WebMode] Initializing Adapter. Mode: ${mode}`);
        if (mode === 'real') {
            return new RealAdapter();
        }
        return new PrototypeAdapter();
    }, []);

    // Boot Sequence
    useEffect(() => {
        let mounted = true;
        (async () => {
            await bootSequence(dispatch);
            if (mounted) {
                // Hydrate initial data from adapter
                try {
                    const sessions = await adapter.listSessions();
                    console.log('[WebMode] Loaded sessions:', sessions.length);
                    // dispatch({ type: 'LOAD_SESSIONS', payload: sessions }); // TODO: Add action
                } catch (e) {
                    console.error('[WebMode] Failed to load initial data:', e);
                }
            }
        })();
        return () => { mounted = false; };
    }, [adapter]);

    // Helper Actions
    const updateConfig = (section: keyof WebModeConfig, key: string, value: any) => {
        setConfig(prev => ({
            ...prev,
            [section]: { ...prev[section], [key]: value }
        }));
    };

    const queueIntent = (text: string) => {
        const id = `intent-${Date.now()}`;
        dispatch({
            type: 'QUEUE_INTENT',
            payload: {
                id,
                text,
                status: 'analyzing',
                confidence: 0,
                timestamp: Date.now(), // timestamp added to match local type, might need to check IntentDraft definition
                origin: 'user'
            } as IntentDraft
        });

        // Simulation of async analysis (would be replaced by backend/adapter call in real usage)
        setTimeout(() => {
            dispatch({
                type: 'UPDATE_INTENT_STATUS',
                payload: { id, status: 'policy-check', outcome: 'Likely compliant.' }
            });
        }, 800);

        setTimeout(() => {
            dispatch({
                type: 'UPDATE_INTENT_STATUS',
                payload: { id, status: 'ready', outcome: 'Approved.' }
            });
        }, 1600);
    };

    const resolvePermission = (id: string, approved: boolean | 'approved' | 'denied') => {
        // Handle legacy boolean vs new string union
        const decision = approved === true || approved === 'approved';
        dispatch({ type: 'RESOLVE_PERMISSION', payload: { id, approved: decision } });
    };

    const sendSignal = (signal: string) => {
        dispatch({ type: 'SIGNAL', payload: signal });
    };

    // Computed properties
    const controlMode = (config.onlineMode.access === 'control' ? 'control' : 'read') as 'read' | 'control';

    return (
        <WebModeContext.Provider value={{
            state,
            config,
            adapter,
            dispatch,
            updateConfig,
            queueIntent,
            resolvePermission: (id, decision) => resolvePermission(id, decision),
            sendSignal,

            // Compatibility
            deviceTier,
            controlMode,
            phase: state.phase,
            lastSignal: state.lastSignal,
            intentQueue: state.intentQueue,
            agentState: state.agentState,
            memoryPulse: state.memoryPulse,
            permissionQueue: state.permissionQueue
        }}>
=======
import { createContext, useContext } from 'react';
import { useDeviceTier, useWebModeState } from '@/lib/webmode/state';
import type { DeviceTier, WebModeConfig } from '@/lib/webmode/types';

interface WebModeContextValue {
    deviceTier: DeviceTier;
    config: WebModeConfig;
    controlMode: 'read' | 'control';
    phase: string;
    lastSignal: string;
    updateConfig: (path: string, value: boolean | number | string) => void;
    sendSignal: (message: string) => void;
}

const WebModeContext = createContext<WebModeContextValue | null>(null);

export function WebModeProvider({ children }: { children: React.ReactNode }) {
    const deviceTier = useDeviceTier();
    const { state, config, controlMode, dispatch, updateConfig } = useWebModeState();

    const sendSignal = (message: string) => {
        dispatch({ type: 'SIGNAL', payload: message });
    };

    return (
        <WebModeContext.Provider
            value={{
                deviceTier,
                config,
                controlMode,
                phase: state.phase,
                lastSignal: state.lastSignal,
                updateConfig,
                sendSignal,
            }}
        >
>>>>>>> main
            {children}
        </WebModeContext.Provider>
    );
}

<<<<<<< HEAD
export const useWebModeContext = () => {
    const context = useContext(WebModeContext);
    if (!context) throw new Error('useWebModeContext must be used within WebModeProvider');
    return context;
};
=======
export function useWebModeContext() {
    const context = useContext(WebModeContext);
    if (!context) {
        throw new Error('useWebModeContext must be used within WebModeProvider');
    }
    return context;
}
>>>>>>> main
