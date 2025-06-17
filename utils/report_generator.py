import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader

class ReportGenerator:
    """Handles generation of reports in multiple formats (HTML, Markdown, JSON)."""

    def __init__(self, session_dir: str):
        """Initialize the report generator.
        
        Args:
            session_dir: Directory to store reports
        """
        self.session_dir = Path(session_dir)
        self.report_dir = self.session_dir / "reports"
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup Jinja2 environment
        template_dir = Path(__file__).parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Add file handler if not already added
        if not self.logger.handlers:
            log_file = self.session_dir / "logs" / "report_generator.log"
            log_file.parent.mkdir(parents=True, exist_ok=True)
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def generate_reports(self, context: Dict[str, Any]) -> Dict[str, str]:
        """Generate reports in all supported formats.
        
        Args:
            context: Dictionary containing report data
            
        Returns:
            Dictionary mapping report types to their file paths
        """
        self.logger.info("Generating reports...")
        
        # Add timestamp if not present
        if "timestamp" not in context:
            context["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        report_paths = {}
        
        try:
            # Generate HTML report
            html_path = self._generate_html_report(context)
            report_paths["html"] = str(html_path)
            
            # Generate Markdown report
            md_path = self._generate_markdown_report(context)
            report_paths["markdown"] = str(md_path)
            
            # Generate JSON report
            json_path = self._generate_json_report(context)
            report_paths["json"] = str(json_path)
            
            self.logger.info("Reports generated successfully")
            return report_paths
            
        except Exception as e:
            self.logger.error(f"Error generating reports: {str(e)}")
            raise

    def _generate_html_report(self, context: Dict[str, Any]) -> Path:
        """Generate HTML report.
        
        Args:
            context: Dictionary containing report data
            
        Returns:
            Path to the generated HTML report
        """
        self.logger.info("Generating HTML report...")
        
        try:
            template = self.env.get_template("report.html")
            html_content = template.render(**context)
            
            output_path = self.report_dir / "report.html"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            self.logger.info(f"HTML report generated: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error generating HTML report: {str(e)}")
            raise

    def _generate_markdown_report(self, context: Dict[str, Any]) -> Path:
        """Generate Markdown report.
        
        Args:
            context: Dictionary containing report data
            
        Returns:
            Path to the generated Markdown report
        """
        self.logger.info("Generating Markdown report...")
        
        try:
            template = self.env.get_template("report.md")
            md_content = template.render(**context)
            
            output_path = self.report_dir / "report.md"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md_content)
                
            self.logger.info(f"Markdown report generated: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error generating Markdown report: {str(e)}")
            raise

    def _generate_json_report(self, context: Dict[str, Any]) -> Path:
        """Generate JSON report.
        
        Args:
            context: Dictionary containing report data
            
        Returns:
            Path to the generated JSON report
        """
        self.logger.info("Generating JSON report...")
        
        try:
            output_path = self.report_dir / "report.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(context, f, indent=2, default=str)
                
            self.logger.info(f"JSON report generated: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error generating JSON report: {str(e)}")
            raise

    def get_report_paths(self) -> Dict[str, str]:
        """Get paths to all generated reports.
        
        Returns:
            Dictionary mapping report types to their file paths
        """
        report_paths = {}
        
        html_path = self.report_dir / "report.html"
        if html_path.exists():
            report_paths["html"] = str(html_path)
            
        md_path = self.report_dir / "report.md"
        if md_path.exists():
            report_paths["markdown"] = str(md_path)
            
        json_path = self.report_dir / "report.json"
        if json_path.exists():
            report_paths["json"] = str(json_path)
            
        return report_paths 