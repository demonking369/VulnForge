# NeuroRift Next-Generation Web Mode

## Quick Start

### Installation

```bash
# Install all dependencies (Rust, npm, Python packages)
./scripts/install_deps.sh
```

### Launch

```bash
# Start all services (Rust core, Python bridge, Next.js frontend)
./scripts/launch_web.sh
```

Then open: **http://localhost:3000**

---

## Architecture

NeuroRift Web Mode uses a three-layer architecture:

1. **Rust Orchestration Core** (Port 8765)
   - High-performance state management
   - WebSocket server for real-time communication
   - Session persistence (.nrs files)
   - Auto-save every 5 minutes

2. **Python Bridge** (Port 8766)
   - FastAPI server
   - Thin adapter for AI and tool integration
   - Connects Rust core to existing Python modules

3. **Next.js Frontend** (Port 3000)
   - Modern React UI with TypeScript
   - TailwindCSS design system
   - Real-time WebSocket updates
   - Grid-based security IDE layout

---

## Features

### ✅ Implemented

- **Professional UI**: Dark theme, clean layout, responsive design
- **Real-Time Updates**: WebSocket-based event system
- **Session Management**: .nrs file format with auto-save
- **Dashboard**: Stats, severity breakdown, agent status
- **Type Safety**: Full TypeScript + Rust type coverage

### 🔲 Pending (Future Work)

- Robin (Dark Web) section
- Browser Automation section
- Security Tools section
- Agent panels (Planner, Operator, Navigator, Analyst, Scribe)
- Session timeline and controls
- Vulnerability table and details
- Log viewer with streaming

---

## Services

| Service | Port | Purpose |
|---------|------|---------|
| Rust Core | 8765 | WebSocket server, state management |
| Python Bridge | 8766 | AI/tool adapter |
| Next.js Frontend | 3000 | User interface |

---

## File Structure

```
VulnForge/
├── core/                          # Rust orchestration core
│   └── neurorift-core/
│       └── src/
│           ├── main.rs            # Entry point
│           ├── lib.rs             # Core orchestrator
│           ├── state/             # State models
│           ├── session/           # .nrs persistence
│           ├── websocket/         # WebSocket server
│           └── python_bridge/     # HTTP client
├── modules/web/
│   └── bridge_server.py           # Python FastAPI adapter
├── web-ui/                        # Next.js frontend
│   └── src/
│       ├── app/                   # Pages
│       ├── components/            # React components
│       ├── lib/                   # Utilities
│       └── styles/                # CSS
└── scripts/
    ├── install_deps.sh            # Install dependencies
    └── launch_web.sh              # Launch all services
```

---

## Development

### Build Rust Core

```bash
cd core
cargo build --release
```

### Run Frontend Dev Server

```bash
cd web-ui
npm run dev
```

### Run Python Bridge

```bash
python3 -m uvicorn modules.web.bridge_server:app --reload
```

---

## Design System

### Colors

```
Background:     #0a0e1a (neuro-bg)
Surface:        #141b2d (neuro-surface)
Border:         #1e293b (neuro-border)
Primary:        #3b82f6 (blue)
Success:        #10b981 (green)
Warning:        #f59e0b (orange)
Danger:         #ef4444 (red)

Severity:
  Critical:     #dc2626
  High:         #f97316
  Medium:       #eab308
  Low:          #22c55e
  Info:         #3b82f6
```

### Typography

- **Sans**: Inter
- **Mono**: JetBrains Mono

---

## Contributors

- NeuroRift Core Team
- demonking369 (NeuroRift creator)
- Anti-Gravity AI
