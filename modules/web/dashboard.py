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
from concurrent.futures import ThreadPoolExecutor

# Set up paths
BASE_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = Path(__file__).resolve().parent / "assets"
sys.path.append(str(BASE_DIR))

# Import VulnForge components
try:
    from vulnforge_main import VulnForge
    from recon_module import EnhancedReconModule
    from ai_integration import AIAnalyzer, OllamaClient
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
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Scans", str(recon_scans))
    with col2:
        st.metric("Vulnerabilities", str(total_vulns))
    with col3:
        st.metric("System Health", "Optimal")
    with col4:
        # Check if Ollama is running
        from modules.darkweb.robin.llm_utils import fetch_ollama_models

        ollama_status = "Connected" if fetch_ollama_models() else "Disconnected"
        st.metric("Ollama AI", ollama_status)

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

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.vulnforge.ai_analyzer.ollama.generate(
                    prompt
                )
                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )


def show_reports():
    st.title("📑 Intelligence Reports")

    results_dir = st.session_state.vulnforge.results_dir
    reports = list(results_dir.glob("**/*.md")) + list(results_dir.glob("**/*.json"))

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
