#!/bin/bash
set -e

# Parse arguments
ONLINE_MODE=false
TUNNEL_PROVIDER="auto"

while [[ $# -gt 0 ]]; do
    case $1 in
        --online)
            ONLINE_MODE=true
            if [[ -n "$2" ]] && [[ "$2" != --* ]]; then
                TUNNEL_PROVIDER="$2"
                shift
            fi
            shift
            ;;
        *)
            shift
            ;;
    esac
done

echo "🧠 NeuroRift Web Mode Launcher"
echo "=============================="
echo ""

# Source Cargo environment if it exists
if [ -f "$HOME/.cargo/env" ]; then
    source "$HOME/.cargo/env"
fi

# Check dependencies
if ! command -v cargo &> /dev/null; then
    echo "❌ Rust not found. Please run: ./scripts/install_deps.sh"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Please run: ./scripts/install_deps.sh"
    exit 1
fi

# Set environment
export NEURORIFT_HOME="${NEURORIFT_HOME:-$HOME/.neurorift}"
mkdir -p "$NEURORIFT_HOME"

echo "📁 NeuroRift home: $NEURORIFT_HOME"
echo ""

# Start Rust core
echo "🦀 Starting Rust orchestration core..."
./core/target/release/neurorift-core &
RUST_PID=$!
echo "   PID: $RUST_PID"

# Wait for Rust to start
sleep 2

# Start Python bridge
echo "🐍 Starting Python bridge..."
python3 -m uvicorn modules.web.bridge_server:app --host 127.0.0.1 --port 8766 --log-level warning &
PYTHON_PID=$!
echo "   PID: $PYTHON_PID"

# Wait for Python to start
sleep 2

# Start Next.js frontend
echo "⚛️  Starting Next.js frontend..."
cd web-ui
npm run dev &
FRONTEND_PID=$!
echo "   PID: $FRONTEND_PID"
cd ..

# Wait for frontend to start
sleep 3

# Start tunnel if online mode
TUNNEL_PID=""
PUBLIC_URL=""
if [ "$ONLINE_MODE" = true ]; then
    echo ""
    echo "🌐 Starting tunnel with provider: $TUNNEL_PROVIDER"
    
    # Start tunnel in background and capture output
    python3 -m modules.web.tunnel_manager start --provider "$TUNNEL_PROVIDER" --port 3000 > /tmp/neurorift_tunnel.log 2>&1 &
    TUNNEL_PID=$!
    
    # Wait for tunnel to start and get URL
    echo "   Waiting for tunnel to establish..."
    for i in {1..15}; do
        if grep -q "Public URL:" /tmp/neurorift_tunnel.log 2>/dev/null; then
            PUBLIC_URL=$(grep "Public URL:" /tmp/neurorift_tunnel.log | tail -1 | awk '{print $NF}')
            break
        fi
        sleep 1
    done
    
    if [ -n "$PUBLIC_URL" ]; then
        echo "   ✅ Tunnel established"
    else
        echo "   ⚠️  Tunnel may still be starting..."
    fi
fi

echo ""
echo "=============================="
echo "✅ NeuroRift Web Mode is running!"
echo ""

if [ "$ONLINE_MODE" = true ] && [ -n "$PUBLIC_URL" ]; then
    echo "🌐 Public URL:  $PUBLIC_URL"
    echo "🏠 Local URL:   http://localhost:3000"
else
    echo "🌐 Open in browser: http://localhost:3000"
fi

echo ""
echo "Services:"
echo "  • Rust Core:      ws://localhost:8765"
echo "  • Python Bridge:  http://localhost:8766"
echo "  • Frontend:       http://localhost:3000"

if [ "$ONLINE_MODE" = true ]; then
    echo "  • Tunnel:         $TUNNEL_PROVIDER"
fi

echo ""
echo "Press Ctrl+C to stop all services"
echo "=============================="

# Trap Ctrl+C and cleanup
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $RUST_PID 2>/dev/null || true
    kill $PYTHON_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    if [ -n "$TUNNEL_PID" ]; then
        kill $TUNNEL_PID 2>/dev/null || true
        echo "   Tunnel stopped"
    fi
    rm -f /tmp/neurorift_tunnel.log
    echo "✅ All services stopped"
    exit 0
}

trap cleanup INT TERM

# Wait for any process to exit
wait
