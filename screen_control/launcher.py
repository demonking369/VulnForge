import os
import subprocess
import json
from python.screen_control import ScreenControl

# --- Build Instructions ---
# This script assumes you are in the `screen_control` directory.
# Ensure you have build-essential, g++, rustc, cargo, and nasm installed.
# sudo apt-get install build-essential g++ rustc cargo nasm xdotool

def build_modules():
    """Compiles all native C++, Rust, and Assembly modules."""
    print("--- Building native modules ---")
    
    # Build C++
    print("Building C++ module...")
    subprocess.run(
        "g++ -shared -fPIC -o cpp/screen.so cpp/screen.cpp -lX11 -lXext",
        shell=True, check=True
    )

    # Build Rust
    print("Building Rust module...")
    subprocess.run("cargo build --release", cwd="rust", shell=True, check=True)

    # Build Assembly
    print("Building Assembly module...")
    subprocess.run("nasm -f elf64 assembly/hook.asm -o assembly/hook.o", shell=True, check=True)
    subprocess.run("ld -shared -o assembly/hook.so assembly/hook.o", shell=True, check=True)
    
    print("--- Build complete ---")

def run_demo(controller):
    """Runs a demo sequence to showcase the system."""
    print("\n--- Running Demo Sequence ---")

    # 1. Focus on the Terminal window
    focus_cmd = {
        "action": "window_focus",
        "params": {"window_title": "Terminal"}
    }
    controller.execute_command(focus_cmd)
    
    # 2. Type a command
    type_cmd = {
        "action": "key_type",
        "params": {"text": "echo 'Hello from VulnForge Screen AI!' && ls -l"}
    }
    controller.execute_command(type_cmd)

    # 3. Simulate pressing Enter (using a separate key_type for special keys)
    enter_cmd = {
        "action": "key_type",
        "params": {"text": "\n"}
    }
    controller.execute_command(enter_cmd)

    # 4. Move mouse to corner
    move_cmd = {
        "action": "mouse_move",
        "params": {"x": 10, "y": 10}
    }
    controller.execute_command(move_cmd)

    print("\n--- Demo Complete ---")

if __name__ == "__main__":
    # Ensure current directory is the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    build_modules()
    
    screen_controller = ScreenControl(os.getcwd())
    
    run_demo(screen_controller) 