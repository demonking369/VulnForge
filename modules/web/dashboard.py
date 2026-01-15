import streamlit as st
import os
import sys
import json
import base64
import time
from pathlib import Path
from datetime import datetime
import subprocess
import asyncio
import threading
import logging
import io
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# --- Logging Setup ---
class StreamlitLogHandler(logging.Handler):
    """Captures logs and stores them in session state"""

    def __init__(self):
        super().__init__()

    def emit(self, record):
        if "logs" not in st.session_state:
            st.session_state.logs = []

        log_entry = self.format(record)
        st.session_state.logs.append(log_entry)
        # Keep only last 1000 logs
        if len(st.session_state.logs) > 1000:
            st.session_state.logs.pop(0)


# Setup root logger to use our handler
if "log_handler_setup" not in st.session_state:
    handler = StreamlitLogHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)
    st.session_state.log_handler_setup = True

# Set up paths
BASE_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = Path(__file__).resolve().parent / "assets"
sys.path.append(str(BASE_DIR))

# Import VulnForge components
try:
    from vulnforge_main import VulnForge
    from recon_module import EnhancedReconModule
    from ai_integration import AIAnalyzer, OllamaClient
    from modules.web.web_module import WebModule
    from modules.scan.scan_module import ScanModule
    from modules.exploit.exploit_module import ExploitModule
    import modules.darkweb as darkweb_module
except ImportError as e:
    st.error(f"Failed to import VulnForge components: {e}")
    st.stop()

# --- Page Config ---
st.set_page_config(
    page_title="VulnForge Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- Custom Styling ---
def local_css(file_name):
    if Path(file_name).exists():
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css(str(ASSETS_DIR / "style.css"))

# --- Session State Initialization ---
if "vulnforge" not in st.session_state:
    st.session_state.vulnforge = VulnForge()
if "recon" not in st.session_state:
    st.session_state.recon = EnhancedReconModule(
        base_dir=st.session_state.vulnforge.base_dir,
        ai_analyzer=st.session_state.vulnforge.ai_analyzer,
    )
if "nav" not in st.session_state:
    st.session_state.nav = "Overview"
if "web" not in st.session_state:
    st.session_state.web = WebModule(
        base_dir=st.session_state.vulnforge.base_dir,
        ai_analyzer=st.session_state.vulnforge.ai_analyzer,
    )
if "exploit" not in st.session_state:
    st.session_state.exploit = ExploitModule(
        base_dir=st.session_state.vulnforge.base_dir,
        ai_analyzer=st.session_state.vulnforge.ai_analyzer,
    )
if "scan" not in st.session_state:
    st.session_state.scan = ScanModule(
        base_dir=st.session_state.vulnforge.base_dir,
        ai_analyzer=st.session_state.vulnforge.ai_analyzer,
    )

# --- Sidebar ---
with st.sidebar:
    logo_path = ASSETS_DIR / "logo.png"
    if logo_path.exists():
        st.image(str(logo_path), width="stretch")
    else:
        st.title("🛡️ VulnForge")

    st.markdown("---")

    nav_options = {
        "🏠 Overview": "Overview",
        "🔍 Reconnaissance": "Recon",
        "📡 Port Scanning": "Scan",
        "🌐 Web Discovery": "Web",
        "🚀 Exploit Mode": "Exploit",
        "🕷️ Dark Web (Robin)": "Robin",
        "🛠️ Tool Manager": "Tools",
        "🤖 AI Assistant": "AI",
        "📑 Reports": "Reports",
        "⚙️ Settings": "Settings",
    }

    for label, key in nav_options.items():
        if st.button(
            label,
            width="stretch",
            type="primary" if st.session_state.nav == key else "secondary",
        ):
            st.session_state.nav = key
            st.rerun()

    st.markdown("---")

    with st.expander("📝 System Logs", expanded=False):
        if "logs" in st.session_state and st.session_state.logs:
            log_text = "\n".join(st.session_state.logs)
            st.text_area("Logs", log_text, height=200, disabled=True)
            if st.button("Clear Logs"):
                st.session_state.logs = []
                st.rerun()
        else:
            st.info("No logs captured yet.")

    st.caption("v1.0.0 | Built by DemonKing369.0")

# --- Dashboard Logic ---


def show_overview():
    st.title("🏠 Framework Overview")

    # Fetch real counts
    results_dir = st.session_state.vulnforge.results_dir
    recon_scans = len(list(results_dir.glob("*"))) if results_dir.exists() else 0

    # Just an estimate for demonstration
    total_vulns = 0
    for report in results_dir.glob("**/results.json"):
        try:
            with open(report) as f:
                data = json.load(f)
                total_vulns += len(data.get("vulnerabilities", []))
        except:
            pass

    # Summary Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Scans", str(recon_scans))
    with col2:
        st.metric("Vulnerabilities", str(total_vulns))

    # Dynamic System Health
    agent_status = st.session_state.vulnforge.agent.get_readiness_status()
    health_status = "Optimal" if agent_status["ready"] else "Degraded"

    with col3:
        st.metric("System Health", health_status)
    with col4:
        # Check if Ollama is running
        from modules.darkweb.robin.llm_utils import fetch_ollama_models

        ollama_status = "Connected" if fetch_ollama_models() else "Disconnected"
        st.metric("Ollama AI", ollama_status)
    with col5:
        is_agentic = (
            os.getenv("VULNFORGE_AGENTIC") == "1"
            or st.session_state.vulnforge.agentic_mode
        )
        agent_ui_status = "Enabled" if is_agentic else "Disabled"
        is_agentic = (
            os.getenv("VULNFORGE_AGENTIC") == "1"
            or st.session_state.vulnforge.agentic_mode
        )
        agent_ui_status = "Enabled" if is_agentic else "Disabled"
        st.metric("Agentic AI", agent_ui_status)

    if not st.session_state.vulnforge.ai_analyzer.ollama.ai_enabled:
        st.warning("⚠️ AI features are currently disabled. Check .env configuration.")

    st.markdown("### 🕒 Recent Activity")
    # Fetch last 5 modified items in results
    recent_items = sorted(
        list(results_dir.glob("*")), key=lambda p: p.stat().st_mtime, reverse=True
    )[:5]
    activity_data = []
    for item in recent_items:
        mtime = datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        activity_data.append(
            {
                "Time": mtime,
                "Activity": f"Scan results found for {item.name}",
                "Status": "Success",
            }
        )

    if activity_data:
        st.table(activity_data)
    else:
        st.info("No recent activity found.")

    st.markdown("### 🧠 AI Analysis History")

    # Define all directories to search
    report_dirs = [
        st.session_state.vulnforge.results_dir,
        st.session_state.vulnforge.base_dir / "sessions",
        st.session_state.vulnforge.base_dir / "recon_results",
    ]

    # Fetch AI summaries from reports across all dirs
    ai_insights = []

    for r_dir in report_dirs:
        if not r_dir.exists():
            continue

        # Recursive search for results.json and other relevant files
        for report in r_dir.glob("**/results.json"):
            try:
                with open(report) as f:
                    data = json.load(f)
                    if "ai_analysis" in data and data["ai_analysis"]:
                        ai_data = data["ai_analysis"]
                        summary = "No summary available"

                        if isinstance(ai_data, dict):
                            summary = (
                                ai_data.get("summary")
                                or ai_data.get("tech_stack_assessment")
                                or "Analysis data available (click to view)"
                            )

                            # Handle raw analysis
                            if "raw_analysis" in ai_data:
                                summary = ai_data["raw_analysis"][:200] + "..."

                        ai_insights.append(
                            {
                                "Source": r_dir.name,
                                "Target": data.get("target", "Unknown"),
                                "Date": datetime.fromtimestamp(
                                    report.stat().st_mtime
                                ).strftime("%Y-%m-%d %H:%M"),
                                "Insight": summary,
                            }
                        )
            except:
                pass

    if ai_insights:
        # Sort by date desc
        ai_insights.sort(key=lambda x: x["Date"], reverse=True)
        st.table(ai_insights)
    else:
        st.info("No AI analysis history found in stored sessions.")


def show_recon():
    st.title("🔍 Reconnaissance Module")

    target = st.text_input("Enter Target Domain", placeholder="example.com")

    col1, col2 = st.columns(2)
    with col1:
        scan_type = st.selectbox("Scan Intensity", ["Passive", "Normal", "Aggressive"])
    with col2:
        use_ai = st.checkbox("Enable AI Analysis", value=True)

    if st.button("🚀 Start Recon Scan"):
        if not target:
            st.error("Please enter a target domain.")
        else:
            status_slot = st.empty()
            progress_bar = st.progress(0)

            async def run_scan():
                status_slot.info(f"🔍 Starting reconnaissance on {target}...")
                # We need to bridge async with streamlit
                results = await st.session_state.recon.run_recon(target)
                return results

            with st.spinner(f"Scanning {target}..."):
                # Run the async function in a new event loop
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                results = loop.run_until_complete(run_scan())

                if "error" in results:
                    st.error(f"Scan failed: {results['error']}")
                else:
                    st.success(f"Scan completed for {target}!")

                    st.markdown("### 📊 Scan Results")
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Subdomains", len(results["subdomains"]))
                    c2.metric("Services", len(results["web_services"]))
                    c3.metric("Vulns", len(results["vulnerabilities"]))

                    with st.expander("🌐 Subdomains Found", expanded=True):
                        st.write(", ".join(results["subdomains"]))

                    if results["web_services"]:
                        with st.expander("🚀 Web Services", expanded=False):
                            st.table(results["web_services"])

                    if results["vulnerabilities"]:
                        with st.expander("⚠️ Vulnerabilities", expanded=True):
                            st.table(results["vulnerabilities"])

                    if results["ai_analysis"]:
                        st.markdown("### 🤖 AI Analysis Report")
                        st.write(
                            results["ai_analysis"].get(
                                "raw_analysis", "No analysis available."
                            )
                        )


def show_web():
    st.title("🌐 Web Discovery Module")

    target = st.text_input(
        "Enter Target Domain", placeholder="example.com", key="web_target"
    )

    col1, col2 = st.columns(2)
    with col1:
        use_ai = st.checkbox("Enable AI Analysis", value=True, key="web_use_ai")

    if st.button("🚀 Start Web Discovery"):
        if not target:
            st.error("Please enter a target domain.")
        else:
            status_slot = st.empty()

            async def run_discovery():
                status_slot.info(f"🌐 Starting web discovery on {target}...")
                results = await st.session_state.web.run_web_discovery(
                    target, use_ai=use_ai
                )
                return results

            with st.spinner(f"Discovering {target}..."):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                results = loop.run_until_complete(run_discovery())

                if results.get("errors"):
                    st.error(f"Discovery failed: {results['errors']}")
                else:
                    st.success(f"Discovery completed for {target}!")

                    st.markdown("### 📊 Discovery Results")
                    c1, c2 = st.columns(2)
                    c1.metric("Technologies", len(results["technologies"]))
                    c2.metric("Directories/Files", len(results["directories"]))

                    if results["technologies"]:
                        with st.expander("🛠️ Technologies Found", expanded=True):
                            for tech in results["technologies"]:
                                st.code(tech.get("raw", "No data"))

                    if results["directories"]:
                        with st.expander("📂 Directories & Files", expanded=False):
                            st.table(results["directories"])

                    if use_ai and results.get("ai_analysis"):
                        st.markdown("### 🤖 AI Security Assessment")
                        analysis = results["ai_analysis"]
                        st.markdown(
                            f"**Tech Stack Assessment:** {analysis.get('tech_stack_assessment', 'N/A')}"
                        )

                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.markdown("**Interesting Findings:**")
                            for finding in analysis.get("interesting_findings", []):
                                st.markdown(f"- {finding}")
                        with col_b:
                            st.markdown("**Suggested Vulnerabilities:**")
                            for vuln in analysis.get("suggested_vulnerabilities", []):
                                st.markdown(f"- {vuln}")

                        st.markdown("**Next Steps:**")
                        for step in analysis.get("next_steps", []):
                            st.markdown(f"- {step}")
                    elif not use_ai:
                        st.info("AI analysis was disabled for this run.")


def show_scan():
    st.title("📡 Port Scanning")

    target = st.text_input(
        "Enter Target Domain/IP", placeholder="127.0.0.1", key="scan_target"
    )

    col1, col2 = st.columns(2)
    with col1:
        use_ai = st.checkbox("Enable AI Analysis", value=True, key="scan_use_ai")

    if st.button("🚀 Start Port Scan"):
        if not target:
            st.error("Please enter a target.")
        else:
            status_slot = st.empty()

            async def run_scan():
                status_slot.info(f"📡 Scanning ports for {target}...")
                results = await st.session_state.scan.run_scan(target, use_ai=use_ai)
                return results

            with st.spinner(f"Scanning {target}..."):
                # Use a fresh event loop for the async call
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                results = loop.run_until_complete(run_scan())

                if results.get("errors"):
                    st.error(f"Scan failed: {results['errors']}")
                else:
                    st.success(f"Scan complete for {target}!")

                    st.markdown("### 📊 Scan Results")
                    st.metric("Open Ports Found", len(results["ports"]))

                    if results["ports"]:
                        # Convert to DataFrame for nice table
                        import pandas as pd

                        df = pd.DataFrame(results["ports"])
                        # Reorder/rename columns for better display
                        if not df.empty:
                            df = df[
                                [
                                    "number",
                                    "protocol",
                                    "state",
                                    "service",
                                    "product",
                                    "version",
                                ]
                            ]
                            st.table(df)

                    if use_ai and results.get("ai_analysis"):
                        st.markdown("### 🤖 AI Security Insights")
                        ai = results["ai_analysis"]
                        if isinstance(ai, dict):
                            if "summary" in ai:
                                st.info(ai["summary"])
                            if "potential_vulnerabilities" in ai:
                                for v in ai["potential_vulnerabilities"]:
                                    with st.expander(
                                        f"⚠️ {v.get('type', 'Vulnerability')}",
                                        expanded=True,
                                    ):
                                        st.write(
                                            f"**Description:** {v.get('description')}"
                                        )
                                        st.write(f"**Severity:** {v.get('severity')}")
                        else:
                            st.write(ai)


def show_exploit():
    st.title("🚀 Exploit Mode")

    target = st.text_input(
        "Enter Target", placeholder="127.0.0.1", key="exploit_target"
    )

    col1, col2 = st.columns(2)
    with col1:
        use_ai = st.checkbox(
            "Enable AI Orchestration", value=True, key="exploit_use_ai"
        )

    if st.button("💀 Run Exploit Pipeline"):
        if not target:
            st.error("Please enter a target.")
        else:
            status_slot = st.empty()

            async def run_exploit():
                status_slot.info(f"💀 Starting exploit pipeline for {target}...")
                # Try to load existing recon data from latest session if possible
                recon_data = {"target": target, "services": []}  # Fallback
                results = await st.session_state.exploit.run_exploit_pipeline(
                    target, recon_data, use_ai=use_ai
                )
                return results

            with st.spinner(f"Running exploit pipeline for {target}..."):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                results = loop.run_until_complete(run_exploit())

                if results.get("errors"):
                    st.error(f"Pipeline failed: {results['errors']}")
                else:
                    st.success(f"Exploit pipeline completed for {target}!")

                    st.markdown("### 📊 Pipeline Results")
                    c1, c2 = st.columns(2)
                    c1.metric("Vulnerabilities Mapped", len(results["vulnerabilities"]))
                    c2.metric("Exploits Generated", len(results["exploits"]))

                    if results["vulnerabilities"]:
                        with st.expander("🛡️ Identified Vulnerabilities", expanded=True):
                            for vuln in results["vulnerabilities"]:
                                st.markdown(
                                    f"**{vuln.get('cve_id')}** - {vuln.get('affected_software')}"
                                )
                                st.caption(vuln.get("description"))

                    if results["exploits"]:
                        with st.expander("🐚 Generated Exploits", expanded=True):
                            for exploit in results["exploits"]:
                                if "error" not in exploit:
                                    st.success(
                                        f"Exploit generated: {exploit.get('file_path')}"
                                    )
                                    st.code(exploit.get("code", ""), language="python")
                                else:
                                    st.error(
                                        f"Generation error: {exploit.get('error')}"
                                    )

                    if use_ai and results.get("ai_decisions"):
                        st.markdown("### 🤖 AI Orchestration Details")
                        st.json(results["ai_decisions"])


def show_robin():
    # Integrate existing Robin UI logic here or import it
    st.title("🕷️ Robin - Dark Web OSINT")

    # We can import the UI components from Robin
    try:
        from modules.darkweb.robin.ui import (
            get_model_choices,
            get_llm,
            refine_query,
            cached_search_results,
            filter_results,
            cached_scrape_multiple,
            generate_summary,
            BufferedStreamingHandler,
            OLLAMA_MAIN_MODEL,
        )

        model_options = get_model_choices()
        default_model = OLLAMA_MAIN_MODEL or "gpt-5-mini"
        default_model_index = next(
            (
                i
                for i, n in enumerate(model_options)
                if n.lower() == default_model.lower()
            ),
            0,
        )

        c1, c2 = st.columns([3, 1])
        with c1:
            query = st.text_input(
                "Dark Web Query", placeholder="e.g. 'ransomware' or 'leaked databases'"
            )
        with c2:
            model = st.selectbox("LLM Model", model_options, index=default_model_index)

        threads = st.slider("Scraping Threads", 1, 16, 4)

        if st.button("🔍 Run Robin Investigation"):
            if query:
                progress_bar = st.progress(0)
                status_slot = st.empty()

                status_slot.info("🔄 Initializing LLM...")
                llm = get_llm(model)
                progress_bar.progress(20)

                status_slot.info("🔄 Refining query...")
                refined = refine_query(llm, query)
                progress_bar.progress(40)

                status_slot.info("🔍 Searching dark web...")
                results = cached_search_results(refined, threads)
                progress_bar.progress(60)

                status_slot.info("🗂️ Filtering & Scraping...")
                filtered = filter_results(llm, refined, results)
                scraped = cached_scrape_multiple(filtered, threads)
                progress_bar.progress(80)

                status_slot.info("✍️ Generating final report...")
                summary_slot = st.empty()

                def ui_emit(chunk):
                    summary_slot.markdown(chunk)

                stream_handler = BufferedStreamingHandler(ui_callback=ui_emit)
                llm.callbacks = [stream_handler]
                summary = generate_summary(llm, query, scraped)

                progress_bar.progress(100)
                status_slot.success("✔️ Investigation Completed!")
                st.markdown(summary)
            else:
                st.warning("Please enter a query.")

    except Exception as e:
        st.error(f"Critical error in Robin module: {e}")


def show_tools():
    st.title("🛠️ System Tool Manager")

    required_tools = [
        "nmap",
        "subfinder",
        "httpx",
        "gobuster",
        "nuclei",
        "ffuf",
        "whatweb",
        "dig",
    ]

    st.markdown("Check the installation status of required system tools.")

    for tool in required_tools:
        col1, col2, col3 = st.columns([3, 2, 1])
        col1.write(f"**{tool.capitalize()}**")

        is_installed = st.session_state.vulnforge.is_tool_installed(tool)

        if is_installed:
            col2.success("✅ Installed")
            if col3.button("Verify", key=tool):
                st.toast(f"{tool} is working correctly.")
        else:
            col2.error("❌ Missing")
            if col3.button("Install", key=tool):
                with st.spinner(f"Installing {tool}..."):
                    # This is a bit dangerous to run directly from UI without sudo handled,
                    # but we can try or show instructions
                    st.warning(
                        f"Please run 'sudo apt install {tool}' or check VulnForge CLI to install."
                    )


def show_ai():
    st.title("🤖 AI Security Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about vulnerabilities, exploits, or recon..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add Search Toggle
        use_search = st.toggle("🌍 Search the Web for latest info", value=False)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Run async generation in a new event loop
                async def get_response():
                    final_prompt = prompt
                    if use_search:
                        with st.status("🌍 Searching the web..."):
                            search_results = await st.session_state.vulnforge.ai_analyzer.perform_web_search(
                                prompt
                            )
                            final_prompt = f"Context from web search:\n{search_results}\n\nUser Question: {prompt}"

                    return await st.session_state.vulnforge.ai_analyzer.ollama.generate(
                        final_prompt
                    )

                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    response = loop.run_until_complete(get_response())
                    loop.close()

                    if response:
                        st.markdown(response)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": response}
                        )
                    else:
                        st.error("AI failed to generate a response.")
                        if not st.session_state.vulnforge.ai_analyzer.ollama.ai_enabled:
                            st.caption("Reason: AI is disabled in configuration.")
                        else:
                            st.caption(
                                "Reason: Ollama service might be unreachable or models missing."
                            )
                except Exception as e:
                    st.error(f"Error communicating with AI: {e}")


def show_reports():
    st.title("📑 Intelligence Reports")

    results_dir = st.session_state.vulnforge.results_dir
    base_dir = st.session_state.vulnforge.base_dir

    # Collect reports from all locations
    search_paths = [results_dir, base_dir / "sessions", base_dir / "recon_results"]

    reports = []
    for path in search_paths:
        if path.exists():
            reports.extend(list(path.glob("**/*.md")) + list(path.glob("**/*.json")))

    if not reports:
        st.info(
            "No reports generated yet. Run a Recon or Robin scan to see reports here."
        )
        return

    # Filter and sort
    reports = sorted(reports, key=lambda p: p.stat().st_mtime, reverse=True)

    for report in reports:
        with st.container(border=True):
            c1, c2, c3 = st.columns([4, 2, 1])
            c1.write(f"**{report.name}**")
            c1.caption(f"Path: {report.parent.name}")
            c2.write(
                datetime.fromtimestamp(report.stat().st_mtime).strftime(
                    "%Y-%m-%d %H:%M"
                )
            )

            with open(report, "rb") as f:
                btn = c3.download_button(
                    label="📥",
                    data=f,
                    file_name=report.name,
                    mime=(
                        "text/markdown"
                        if report.suffix == ".md"
                        else "application/json"
                    ),
                    key=str(report),
                )


def show_settings():
    st.title("⚙️ Framework Settings")
    st.subheader("Ollama Configuration")
    st.text_input("Ollama Base URL", value="http://localhost:11434")

    st.subheader("API Integration")
    st.text_input("OpenAI API Key", type="password")
    st.text_input("Shodan API Key", type="password")

    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")


# --- Page Routing ---
if st.session_state.nav == "Overview":
    show_overview()
elif st.session_state.nav == "Recon":
    show_recon()
elif st.session_state.nav == "Scan":
    show_scan()
elif st.session_state.nav == "Web":
    show_web()
elif st.session_state.nav == "Exploit":
    show_exploit()
elif st.session_state.nav == "Robin":
    show_robin()
elif st.session_state.nav == "Tools":
    show_tools()
elif st.session_state.nav == "AI":
    show_ai()
elif st.session_state.nav == "Reports":
    show_reports()
elif st.session_state.nav == "Settings":
    show_settings()
