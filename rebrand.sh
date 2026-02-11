#!/bin/bash
# NeuroRift Rebranding Script
# Replaces all NeuroRift branding with NeuroRift

echo "Starting NeuroRift rebranding..."

# Define replacements
declare -A replacements=(
    ["NeuroRift"]="NeuroRift"
    ["NeuroRift"]="NeuroRift"
    ["neurorift"]="neurorift"
    ["neurorift"]="neurorift"
    ["NR"]="NR"
    ["nr"]="nr"
    ["Agentic Mode"]="NeuroRift Intelligence Mode"
    ["agentic mode"]="NeuroRift Intelligence Mode"
)

# Files to process
find . -type f \( -name "*.md" -o -name "*.py" -o -name "*.json" -o -name "*.txt" -o -name "*.sh" \) \
    ! -path "./.git/*" \
    ! -path "./.venv/*" \
    ! -path "./venv/*" \
    ! -path "./build/*" \
    ! -path "./__pycache__/*" \
    ! -path "./system-prompts-and-models-of-ai-tools/*" \
    ! -path "./sim/*" \
    -print0 | while IFS= read -r -d '' file; do
    
    # Skip if file doesn't exist or is binary
    [ ! -f "$file" ] && continue
    
    # Create backup
    cp "$file" "$file.bak"
    
    # Apply replacements
    sed -i 's/NeuroRift/NeuroRift/g' "$file"
    sed -i 's/NeuroRift/NeuroRift/g' "$file"
    sed -i 's/neurorift/neurorift/g' "$file"
    sed -i 's/neurorift/neurorift/g' "$file"
    sed -i 's/NR/NR/g' "$file"
    sed -i 's/nr/nr/g' "$file"
    
    echo "Processed: $file"
done

echo "Rebranding complete!"
