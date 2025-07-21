# VulnForge: The Polyglot AI Security Framework

VulnForge is an advanced, AI-powered vulnerability research framework built for authorized security testing. It now features a sophisticated, multi-language architecture and a pipelined AI reasoning system, enabling it to tackle complex security tasks with greater speed, efficiency, and intelligence.

## Key Enhancements

- **🧠 Advanced AI Pipeline:** Utilizes a multi-step reasoning process inspired by leading AI agents like Devin and Manus. The AI now formulates a high-level plan, selects the appropriate tools, executes them, and analyzes the results in a continuous loop.
- **⚡ Polyglot Performance:** VulnForge is no longer just a Python script. It's a high-performance system leveraging multiple languages for what they do best:
  - **Python:** High-level orchestration and `asyncio` for I/O concurrency.
  - **C/C++ & Rust:** For CPU-bound tasks like high-speed data parsing and native OS interaction.
  - **Assembly:** For fine-grained, "metal-to-the-metal" optimizations on critical code paths.
  - **Bash:** For robust system-level automation and tool chaining.
- **🤖 AI-Powered Screen Control:** A groundbreaking modular system allowing the AI to see and interact with the screen like a human. It can move the mouse, click, type, and manage windows across different platforms, using the most efficient language for each task.

## Features

- **AI-Autonomous Operation (`--ai-pipeline`)**: Engages the new multi-step AI orchestrator for complex, autonomous testing.
- **Modular Reconnaissance**: Concurrently runs tools like `nmap`, `subfinder`, and `httpx` for fast and comprehensive data gathering.
- **Multi-Language Screen Interaction**: A complete module allowing the AI to control the desktop environment.
- **Custom Tool Generation**: AI-powered tool creation for novel security tasks.
- **Dynamic Reporting**: Generates detailed reports in Markdown, JSON, and HTML.

## New Architecture

VulnForge's architecture is designed for performance and modularity: 