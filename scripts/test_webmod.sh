#!/bin/bash
# Test script to verify web mode launches correctly

echo "🧪 Testing VulnForge Web Mode..."
echo ""

# Activate venv
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ No virtual environment found"
    exit 1
fi

# Test 1: Check if ui.py compiles
echo ""
echo "Test 1: Checking ui.py syntax..."
if python -m py_compile modules/darkweb/robin/ui.py 2>/dev/null; then
    echo "✅ ui.py compiles successfully"
else
    echo "❌ ui.py has syntax errors"
    exit 1
fi

# Test 2: Check imports
echo ""
echo "Test 2: Testing imports..."
python -c "
import sys
sys.path.insert(0, 'modules/darkweb/robin')
try:
    import ui
    print('✅ All imports successful')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
" || exit 1

echo ""
echo "=================================="
echo "✅ All tests passed!"
echo ""
echo "To start web mode:"
echo "  ./start_webmod.sh"
echo ""
