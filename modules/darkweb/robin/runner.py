"""
Wrapper utilities that integrate the Robin dark web OSINT workflow with VulnForge.
"""

from __future__ import annotations

import socket
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from rich.console import Console
from rich.panel import Panel

# Fix imports to work both as module and when run directly
try:
    from .llm import (
        get_llm,
        refine_query,
        filter_results,
        generate_summary,
    )
    from .llm_utils import get_model_choices
    from .search import get_search_results
    from .scrape import scrape_multiple
except ImportError:
    from llm import (
        get_llm,
        refine_query,
        filter_results,
        generate_summary,
    )
    from llm_utils import get_model_choices
    from search import get_search_results
    from scrape import scrape_multiple

ROBIN_DEFAULT_MODEL = "gpt-5-mini"
REPORT_DIR = Path.home() / ".vulnforge" / "darkweb_reports"
console = Console()


def _ensure_tor_proxy(host: str = "127.0.0.1", port: int = 9050) -> None:
    """Raise a helpful error if the Tor SOCKS proxy is not reachable."""
    try:
        with socket.create_connection((host, port), timeout=2):
            return
    except OSError as exc:
        raise RuntimeError(
            "Tor SOCKS proxy is not reachable on 127.0.0.1:9050. "
            "Install and start the tor service before running Robin."
        ) from exc


def _write_report(summary: str, output_path: Optional[Path]) -> Path:
    """Persist the generated summary to disk."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = REPORT_DIR / f"darkweb_report_{timestamp}.md"
    else:
        output_path = Path(output_path).expanduser()
        if output_path.is_dir():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = output_path / f"darkweb_report_{timestamp}.md"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(summary, encoding="utf-8")
    return output_path


def run_darkweb_osint(
    query: str,
    *,
    model: str = ROBIN_DEFAULT_MODEL,
    threads: int = 5,
    output: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Execute the Robin workflow and return metadata about the investigation.

    Returns a dict containing:
        refined_query
        search_results
        filtered_results
        scraped_count
        report_path
    """
    if not query or not query.strip():
        raise ValueError("Query must be a non-empty string.")

    _ensure_tor_proxy()

    console.print(
        Panel.fit(
            f"[bold blue]Robin Dark Web OSINT[/bold blue]\nModel: {model}\nThreads: {threads}",
            title="Dark Web Module",
        )
    )

    llm = get_llm(model)

    with console.status("Refining query with AI...", spinner="dots"):
        refined_query = refine_query(llm, query)

    with console.status("Querying dark web indices via Tor...", spinner="dots"):
        search_results = get_search_results(refined_query.replace(" ", "+"), max_workers=threads)

    if not search_results:
        console.print("[yellow]No search results returned. Verify Tor connectivity and try again.[/yellow]")
        return {
            "refined_query": refined_query,
            "search_results": [],
            "filtered_results": [],
            "scraped_count": 0,
            "report_path": None,
        }

    with console.status("Prioritising results with AI...", spinner="dots"):
        filtered_results = filter_results(llm, refined_query, search_results)

    with console.status("Scraping selected hidden services...", spinner="dots"):
        scraped_results = scrape_multiple(filtered_results, max_workers=threads)

    with console.status("Generating intelligence summary...", spinner="dots"):
        summary = generate_summary(llm, query, scraped_results)

    report_path = _write_report(summary, Path(output) if output else None)
    console.print(f"[green]✔ Dark web report saved to {report_path}[/green]")

    return {
        "refined_query": refined_query,
        "search_results": search_results,
        "filtered_results": filtered_results,
        "scraped_count": len(scraped_results),
        "report_path": str(report_path),
    }


def get_robin_model_choices():
    """Expose Robin model choices for CLI integration."""
    return get_model_choices()

