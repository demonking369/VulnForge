#!/bin/bash

# A simple wrapper around xdotool for window management.

ACTION=$1
WINDOW_TITLE=$2

if [[ "$ACTION" == "focus" ]]; then
    if [[ -z "$WINDOW_TITLE" ]]; then
        echo "Error: Window title required for focus action."
        exit 1
    fi
    
    # Search for the window ID and activate it
    WINDOW_ID=$(xdotool search --onlyvisible --name "$WINDOW_TITLE" | head -1)
    
    if [[ -n "$WINDOW_ID" ]]; then
        x 