"""
CVE Collector module for VulnForge
Handles gathering and analyzing CVEs from various sources
"""

import json
import asyncio
import aiohttp
import aiofiles
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from rich.console import Console
from rich.progress import Progress

from utils.logger import setup_logger
from utils.cli_utils import create_progress, print_results_table
from ai_wrapper.ollama_wrapper import OllamaWrapper

class CVECollector:
    def __init__(self, base_dir: Path, ai_wrapper: Optional[OllamaWrapper] = None):
        self.base_dir = base_dir
        self.console = Console()
        self.logger = setup_logger("vulnforge.cve_collector")
        self.ai_wrapper = ai_wrapper
        self.data_dir = base_dir / "data" / "cve_feeds"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    async def fetch_nvd_feed(self, start_date: Optional[str] = None) -> List[Dict]:
        """Fetch CVE data from NVD feed"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            
        self.console.print("[bold blue]Fetching NVD CVE feed...[/bold blue]")
        
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0"
        params = {
            "pubStartDate": f"{start_date}T00:00:00.000",
            "resultsPerPage": 2000
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("vulnerabilities", [])
                    else:
                        self.logger.error(f"NVD API error: {response.status}")
                        return []
            except Exception as e:
                self.logger.error(f"Error fetching NVD feed: {e}")
                return []
                
    async def fetch_exploit_db(self) -> List[Dict]:
        """Fetch exploit data from Exploit-DB"""
        self.console.print("[bold blue]Fetching Exploit-DB data...[/bold blue]")
        
        url = "https://raw.githubusercontent.com/offensive-security/exploitdb/master/files_exploits.csv"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        exploits = []
                        
                        # Parse CSV content
                        for line in content.splitlines()[1:]:  # Skip header
                            try:
                                parts = line.split(',')
                                if len(parts) >= 4:
                                    exploits.append({
                                        "id": parts[0],
                                        "file": parts[1],
                                        "description": parts[2],
                                        "date": parts[3],
                                        "author": parts[4] if len(parts) > 4 else "Unknown",
                                        "platform": parts[5] if len(parts) > 5 else "Unknown",
                                        "type": parts[6] if len(parts) > 6 else "Unknown"
                                    })
                            except:
                                continue
                                
                        return exploits
                    else:
                        self.logger.error(f"Exploit-DB fetch error: {response.status}")
                        return []
            except Exception as e:
                self.logger.error(f"Error fetching Exploit-DB: {e}")
                return []
                
    async def fetch_github_pocs(self, cve_id: str) -> List[Dict]:
        """Search for PoCs on GitHub"""
        self.console.print(f"[bold blue]Searching GitHub for {cve_id} PoCs...[/bold blue]")
        
        # GitHub API search query
        query = f"{cve_id} poc OR proof of concept OR exploit"
        url = "https://api.github.com/search/code"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "VulnForge/1.0"
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params={"q": query}, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("items", [])
                    else:
                        self.logger.error(f"GitHub API error: {response.status}")
                        return []
            except Exception as e:
                self.logger.error(f"Error searching GitHub: {e}")
                return []
                
    async def analyze_cve(self, cve_data: Dict) -> Dict:
        """Analyze CVE data using AI"""
        if not self.ai_wrapper:
            return cve_data
            
        prompt = f"""
        Analyze this CVE and provide:
        1. Severity assessment
        2. Exploitation complexity
        3. Potential impact
        4. Recommended mitigation
        5. Related CVEs
        
        CVE Data:
        {json.dumps(cve_data, indent=2)}
        """
        
        try:
            analysis = await self.ai_wrapper.generate(prompt)
            cve_data["ai_analysis"] = analysis
        except Exception as e:
            self.logger.error(f"Error analyzing CVE: {e}")
            
        return cve_data
        
    async def collect_cves(self, target_info: Dict) -> Dict[str, Any]:
        """Collect and analyze CVEs for target"""
        self.console.print("[bold blue]Starting CVE collection...[/bold blue]")
        
        # Fetch data from various sources
        nvd_cves = await self.fetch_nvd_feed()
        exploit_db = await self.fetch_exploit_db()
        
        # Match CVEs with target information
        matched_cves = []
        for cve in nvd_cves:
            # Check if CVE affects target's software/versions
            if self._matches_target(cve, target_info):
                # Get additional information
                github_pocs = await self.fetch_github_pocs(cve["cve"]["id"])
                
                # Analyze CVE
                analyzed_cve = await self.analyze_cve({
                    "cve": cve,
                    "exploits": [e for e in exploit_db if cve["cve"]["id"] in e["description"]],
                    "github_pocs": github_pocs
                })
                
                matched_cves.append(analyzed_cve)
                
        # Prepare results
        results = {
            "target": target_info,
            "timestamp": datetime.now().isoformat(),
            "total_cves": len(matched_cves),
            "matched_cves": matched_cves
        }
        
        # Save results
        await self._save_results(results)
        
        # Display summary
        print_results_table({
            "Total CVEs": len(matched_cves),
            "High Severity": len([c for c in matched_cves if c.get("ai_analysis", {}).get("severity") == "high"]),
            "With Exploits": len([c for c in matched_cves if c.get("exploits")]),
            "With PoCs": len([c for c in matched_cves if c.get("github_pocs")])
        })
        
        return results
        
    def _matches_target(self, cve: Dict, target_info: Dict) -> bool:
        """Check if CVE affects target"""
        # Implement matching logic based on target information
        # This is a simplified version - expand based on your needs
        try:
            cpe_matches = cve["cve"].get("configurations", [])
            for match in cpe_matches:
                for node in match.get("nodes", []):
                    for cpe in node.get("cpeMatch", []):
                        if self._check_cpe_match(cpe["criteria"], target_info):
                            return True
        except:
            pass
        return False
        
    def _check_cpe_match(self, cpe: str, target_info: Dict) -> bool:
        """Check if CPE string matches target information"""
        # Implement CPE matching logic
        # This is a simplified version - expand based on your needs
        try:
            parts = cpe.split(":")
            if len(parts) < 5:
                return False
                
            vendor = parts[3]
            product = parts[4]
            version = parts[5] if len(parts) > 5 else ""
            
            # Check against target information
            if vendor in target_info.get("technologies", []):
                return True
            if product in target_info.get("technologies", []):
                return True
                
        except:
            pass
        return False
        
    async def _save_results(self, results: Dict):
        """Save CVE collection results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = self.data_dir / f"cve_collection_{timestamp}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save JSON
        json_path = output_dir / "results.json"
        async with aiofiles.open(json_path, 'w') as f:
            await f.write(json.dumps(results, indent=2))
            
        # Generate Markdown report
        md_path = output_dir / "report.md"
        async with aiofiles.open(md_path, 'w') as f:
            await f.write(f"""# VulnForge CVE Collection Report

## Target Information
- Target: {results['target'].get('target', 'Unknown')}
- Scan Time: {results['timestamp']}

### Summary
- Total CVEs Found: {results['total_cves']}
- High Severity: {len([c for c in results['matched_cves'] if c.get('ai_analysis', {}).get('severity') == 'high'])}
- With Exploits: {len([c for c in results['matched_cves'] if c.get('exploits')])}
- With PoCs: {len([c for c in results['matched_cves'] if c.get('github_pocs')])}

### Detailed Findings
{chr(10).join(self._format_cve_entry(cve) for cve in results['matched_cves'])}
""")
            
        self.console.print(f"[green]Results saved to: {output_dir}[/green]")
        
    def _format_cve_entry(self, cve: Dict) -> str:
        """Format CVE entry for report"""
        cve_id = cve["cve"]["id"]
        description = cve["cve"]["descriptions"][0]["value"]
        severity = cve.get("ai_analysis", {}).get("severity", "Unknown")
        
        return f"""
#### {cve_id} ({severity.upper()})
{description}

**Exploits**: {len(cve.get('exploits', []))}
**GitHub PoCs**: {len(cve.get('github_pocs', []))}

**AI Analysis**:
{cve.get('ai_analysis', {}).get('analysis', 'No analysis available')}
""" 