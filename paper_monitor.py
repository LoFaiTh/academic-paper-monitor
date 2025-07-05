#!/usr/bin/env python3
"""
Academic Paper Monitor for Computer Vision Fields
Monitors new papers in SFM, SLAM, 3DGS, and NeRF research areas
Supports Slack notifications and GitHub deployment
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

# Third-party imports
import arxiv
import feedparser
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PaperMonitor:
    """
    A class to monitor new academic papers in computer vision research fields
    """

    def __init__(self, config_file: str = "config.json"):
        """Initialize the paper monitor with configuration"""
        self.config = self.load_config(config_file)
        self.client = arxiv.Client()
        self.data_file = "papers_data.json"
        self.previous_papers = self.load_previous_papers()

        # Research field search queries
        self.search_queries = {
            "SFM": ["Structure from Motion", "SfM", "bundle adjustment", "visual SLAM"],
            "SLAM": ["SLAM", "simultaneous localization mapping", "visual odometry", "loop closure"],
            "3DGS": ["3D Gaussian Splatting", "3DGS", "Gaussian splatting", "neural splatting"],
            "NeRF": ["Neural Radiance Fields", "NeRF", "neural rendering", "novel view synthesis"]
        }

    def load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        default_config = {
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "",
                "sender_password": "",
                "recipient_emails": []
            },
            "slack": {
                "enabled": False,
                "webhook_url": "",
                "channel": "#general",
                "username": "Paper Monitor Bot"
            },
            "monitoring": {
                "days_back": 3,
                "max_results_per_query": 20,
                "categories": ["cs.CV", "cs.RO", "cs.AI"]
            },
            "github": {
                "enabled": False,
                "repo_name": "",
                "branch": "main",
                "pages_branch": "gh-pages",
                "token": ""
            }
        }

        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            # Merge with defaults
            for key in default_config:
                if key not in config:
                    config[key] = default_config[key]
            return config
        except FileNotFoundError:
            logger.warning(f"Config file {config_file} not found, using defaults")
            return default_config

    def load_previous_papers(self) -> Dict[str, List[str]]:
        """Load previously seen papers from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"paper_ids": [], "last_check": ""}

    def save_papers_data(self, papers_data: Dict[str, Any]):
        """Save papers data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(papers_data, f, indent=2)

    def search_papers_by_field(self, field: str) -> List[arxiv.Result]:
        """Search for papers in a specific research field"""
        queries = self.search_queries.get(field, [])
        all_papers = []

        for query_term in queries:
            # Create search with category filter and recent papers
            search_query = f"({query_term}) AND cat:{' OR cat:'.join(self.config['monitoring']['categories'])}"

            search = arxiv.Search(
                query=search_query,
                max_results=self.config['monitoring']['max_results_per_query'],
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )

            try:
                results = list(self.client.results(search))
                all_papers.extend(results)
                logger.info(f"Found {len(results)} papers for {field} query: {query_term}")
                time.sleep(1)  # Rate limiting
            except Exception as e:
                logger.error(f"Error searching for {query_term}: {e}")

        return all_papers

    def filter_recent_papers(self, papers: List[arxiv.Result]) -> List[arxiv.Result]:
        """Filter papers to only include recent ones"""
        cutoff_date = datetime.now() - timedelta(days=self.config['monitoring']['days_back'])
        recent_papers = []

        for paper in papers:
            if paper.published.replace(tzinfo=None) > cutoff_date:
                recent_papers.append(paper)

        return recent_papers

    def check_for_new_papers(self) -> Dict[str, List[Dict[str, Any]]]:
        """Check for new papers across all research fields"""
        new_papers_by_field = {}
        all_new_paper_ids = []

        for field in self.search_queries.keys():
            logger.info(f"Searching for {field} papers...")
            papers = self.search_papers_by_field(field)
            recent_papers = self.filter_recent_papers(papers)

            # Filter out papers we've already seen
            new_papers = []
            for paper in recent_papers:
                if paper.entry_id not in self.previous_papers.get("paper_ids", []):
                    new_papers.append({
                        "id": paper.entry_id,
                        "title": paper.title,
                        "authors": [author.name for author in paper.authors],
                        "summary": paper.summary[:500] + "..." if len(paper.summary) > 500 else paper.summary,
                        "published": paper.published.isoformat(),
                        "pdf_url": paper.pdf_url,
                        "categories": paper.categories,
                        "field": field
                    })
                    all_new_paper_ids.append(paper.entry_id)

            new_papers_by_field[field] = new_papers
            logger.info(f"Found {len(new_papers)} new {field} papers")

        # Update our records
        current_paper_ids = self.previous_papers.get("paper_ids", [])
        current_paper_ids.extend(all_new_paper_ids)

        # Keep only recent papers to prevent unbounded growth
        papers_data = {
            "paper_ids": current_paper_ids[-1000:],  # Keep last 1000 paper IDs
            "last_check": datetime.now().isoformat(),
            "new_papers": new_papers_by_field
        }

        self.save_papers_data(papers_data)
        return new_papers_by_field

    def generate_report(self, new_papers: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate a text report of new papers"""
        total_papers = sum(len(papers) for papers in new_papers.values())

        if total_papers == 0:
            return "No new papers found in the monitored research fields."

        report = f"# New Papers Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += f"Found {total_papers} new papers across all research fields.\n\n"

        for field, papers in new_papers.items():
            if papers:
                report += f"## {field} ({len(papers)} papers)\n\n"
                for paper in papers:
                    report += f"**{paper['title']}**\n"
                    report += f"Authors: {', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''}\n"
                    report += f"Published: {paper['published'][:10]}\n"
                    report += f"Categories: {', '.join(paper['categories'])}\n"
                    report += f"URL: {paper['pdf_url']}\n"
                    report += f"Summary: {paper['summary']}\n\n"
                report += "---\n\n"

        return report

    def send_email_notification(self, report: str):
        """Send email notification with new papers"""
        if not self.config["email"]["enabled"]:
            logger.info("Email notifications are disabled")
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = self.config["email"]["sender_email"]
            msg['Subject'] = f"New Academic Papers - {datetime.now().strftime('%Y-%m-%d')}"

            msg.attach(MIMEText(report, 'plain'))

            server = smtplib.SMTP(self.config["email"]["smtp_server"], self.config["email"]["smtp_port"])
            server.starttls()
            server.login(self.config["email"]["sender_email"], self.config["email"]["sender_password"])

            for recipient in self.config["email"]["recipient_emails"]:
                msg['To'] = recipient
                server.send_message(msg)
                logger.info(f"Email sent to {recipient}")

            server.quit()

        except Exception as e:
            logger.error(f"Error sending email: {e}")

    def send_slack_notification(self, new_papers: Dict[str, List[Dict[str, Any]]]):
        """Send Slack notification with new papers"""
        if not self.config["slack"]["enabled"]:
            logger.info("Slack notifications are disabled")
            return

        total_papers = sum(len(papers) for papers in new_papers.values())
        
        if total_papers == 0:
            message = "📚 No new papers found in the monitored research fields."
        else:
            message = f"📚 Found {total_papers} new papers!\n\n"
            
            for field, papers in new_papers.items():
                if papers:
                    message += f"*{field}* ({len(papers)} papers):\n"
                    for paper in papers[:3]:  # Limit to 3 papers per field to avoid message length issues
                        authors_text = ', '.join(paper['authors'][:2])
                        if len(paper['authors']) > 2:
                            authors_text += f" and {len(paper['authors']) - 2} others"
                        
                        message += f"• <{paper['pdf_url']}|{paper['title']}>\n"
                        message += f"  _by {authors_text}_\n"
                    
                    if len(papers) > 3:
                        message += f"  _... and {len(papers) - 3} more papers_\n"
                    message += "\n"

        payload = {
            "channel": self.config["slack"]["channel"],
            "username": self.config["slack"]["username"],
            "text": message,
            "icon_emoji": ":books:"
        }

        try:
            response = requests.post(
                self.config["slack"]["webhook_url"],
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            logger.info("Slack notification sent successfully")
        except Exception as e:
            logger.error(f"Error sending Slack notification: {e}")

    def generate_web_report(self, new_papers: Dict[str, List[Dict[str, Any]]]):
        """Generate HTML report for web deployment"""
        total_papers = sum(len(papers) for papers in new_papers.values())

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Academic Paper Monitor</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .field-section {{ margin-bottom: 30px; }}
        .paper {{ border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; }}
        .paper-title {{ font-weight: bold; color: #0366d6; margin-bottom: 5px; }}
        .paper-meta {{ color: #666; font-size: 14px; margin-bottom: 10px; }}
        .paper-summary {{ line-height: 1.5; }}
        .field-title {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px; }}
        .last-updated {{ text-align: right; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Academic Paper Monitor</h1>
        <p>Monitoring new papers in: Structure from Motion (SFM), SLAM, 3D Gaussian Splatting (3DGS), and Neural Radiance Fields (NeRF)</p>
        <p><strong>Total new papers found:</strong> {total_papers}</p>
        <p class="last-updated">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
    </div>
"""

        if total_papers == 0:
            html_content += "<p><em>No new papers found in the monitored research fields.</em></p>"
        else:
            for field, papers in new_papers.items():
                if papers:
                    html_content += f'<div class="field-section"><h2 class="field-title">{field} ({len(papers)} papers)</h2>'
                    for paper in papers:
                        authors_text = ', '.join(paper['authors'][:3])
                        if len(paper['authors']) > 3:
                            authors_text += f" and {len(paper['authors']) - 3} others"

                        html_content += f"""
                        <div class="paper">
                            <div class="paper-title">{paper['title']}</div>
                            <div class="paper-meta">
                                <strong>Authors:</strong> {authors_text}<br>
                                <strong>Published:</strong> {paper['published'][:10]}<br>
                                <strong>Categories:</strong> {', '.join(paper['categories'])}<br>
                                <strong>URL:</strong> <a href="{paper['pdf_url']}" target="_blank">View Paper</a>
                            </div>
                            <div class="paper-summary">{paper['summary']}</div>
                        </div>
                        """
                    html_content += "</div>"

        html_content += "</body></html>"

        # Save HTML report
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        logger.info("Generated HTML report: index.html")

    def deploy_to_github_pages(self):
        """Deploy the HTML report to GitHub Pages"""
        if not self.config["github"]["enabled"]:
            logger.info("GitHub deployment is disabled")
            return

        try:
            # Create a simple deployment script
            deploy_script = f"""#!/bin/bash
# Deploy to GitHub Pages
git config --global user.name "Paper Monitor Bot"
git config --global user.email "bot@example.com"

# Add the HTML file
git add index.html
git commit -m "Update paper monitor report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# Push to GitHub Pages branch
git push origin {self.config['github']['branch']}:{self.config['github']['pages_branch']}
"""
            
            with open("deploy.sh", "w") as f:
                f.write(deploy_script)
            
            # Make the script executable
            os.chmod("deploy.sh", 0o755)
            
            logger.info("GitHub Pages deployment script created: deploy.sh")
            logger.info("Run './deploy.sh' to deploy to GitHub Pages")
            
        except Exception as e:
            logger.error(f"Error creating GitHub deployment script: {e}")

    def run(self):
        """Main execution method"""
        logger.info("Starting paper monitoring...")
        new_papers = self.check_for_new_papers()

        # Generate reports
        text_report = self.generate_report(new_papers)
        logger.info("Generated text report")

        # Save text report
        with open("report.txt", "w", encoding="utf-8") as f:
            f.write(text_report)

        # Generate web report
        self.generate_web_report(new_papers)

        # Send notifications
        self.send_email_notification(text_report)
        self.send_slack_notification(new_papers)

        # Deploy to GitHub Pages if enabled
        self.deploy_to_github_pages()

        total_papers = sum(len(papers) for papers in new_papers.values())
        logger.info(f"Monitoring complete. Found {total_papers} new papers.")

        return new_papers

def main():
    """Main function for command line execution"""
    monitor = PaperMonitor()
    monitor.run()

if __name__ == "__main__":
    main()
