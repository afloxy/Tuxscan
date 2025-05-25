#!/usr/bin/env python3

import os
import re
import argparse
import fnmatch
from pathlib import Path
from typing import List, Dict, Set
from dataclasses import dataclass
from datetime import datetime
import colorama
from colorama import Fore, Style
from jinja2 import Template

# Initialize colorama
colorama.init()

@dataclass
class Finding:
    file_path: str
    line_number: int
    content: str
    pattern_name: str
    severity: str  # Added severity field

class TuxScan:
    def __init__(self, ignore_patterns: List[str] = None):
        self.ignore_patterns = ignore_patterns or []
        self.findings: List[Finding] = []
        
        # Define patterns for sensitive information with severity levels
        self.patterns = {
            'API Key': {
                'pattern': r'(?i)(api[_-]?key|apikey|secret[_-]?key|secretkey)[\s]*[=:]\s*[\'"]([^\'"]+)[\'"]',
                'severity': 'HIGH'
            },
            'Password': {
                'pattern': r'(?i)(password|passwd|pwd)[\s]*[=:]\s*[\'"]([^\'"]+)[\'"]',
                'severity': 'HIGH'
            },
            'Username': {
                'pattern': r'(?i)(username|user[_-]?id|user)[\s]*[=:]\s*[\'"]([^\'"]+)[\'"]',
                'severity': 'MEDIUM'
            },
            'Token': {
                'pattern': r'(?i)(token|access[_-]?token|auth[_-]?token)[\s]*[=:]\s*[\'"]([^\'"]+)[\'"]',
                'severity': 'HIGH'
            },
            'IP Address': {
                'pattern': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
                'severity': 'MEDIUM'
            },
            'URL': {
                'pattern': r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',
                'severity': 'LOW'
            },
            'Email': {
                'pattern': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
                'severity': 'MEDIUM'
            },
            'Aadhaar': {
                'pattern': r'\b[0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{4}\b',
                'severity': 'HIGH'
            },
            'PAN': {
                'pattern': r'[A-Z]{5}[0-9]{4}[A-Z]{1}',
                'severity': 'HIGH'
            },
            'Common Credentials': {
                'pattern': r'(?i)(admin:admin|root:root|guest:guest|user:password)',
                'severity': 'HIGH'
            }
        }

    def get_severity_color(self, severity: str) -> str:
        """Get color code for severity level."""
        colors = {
            'HIGH': Fore.RED,
            'MEDIUM': Fore.YELLOW,
            'LOW': Fore.GREEN
        }
        return colors.get(severity, Fore.WHITE)

    def should_ignore(self, path: str) -> bool:
        """Check if the path should be ignored based on patterns."""
        return any(fnmatch.fnmatch(path, pattern) for pattern in self.ignore_patterns)

    def scan_file(self, file_path: str) -> None:
        """Scan a single file for sensitive information."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    for pattern_name, pattern_info in self.patterns.items():
                        matches = re.finditer(pattern_info['pattern'], line)
                        for match in matches:
                            self.findings.append(Finding(
                                file_path=file_path,
                                line_number=line_num,
                                content=match.group(0),
                                pattern_name=pattern_name,
                                severity=pattern_info['severity']
                            ))
        except Exception as e:
            print(f"{Fore.RED}Error scanning {file_path}: {str(e)}{Style.RESET_ALL}")

    def scan_directory(self, directory: str) -> None:
        """Recursively scan a directory for sensitive information."""
        for root, dirs, files in os.walk(directory):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if not self.should_ignore(os.path.join(root, d))]
            
            for file in files:
                file_path = os.path.join(root, file)
                if not self.should_ignore(file_path):
                    self.scan_file(file_path)

    def generate_html_report(self, output_file: str = None) -> str:
        """Generate an HTML report of findings."""
        if output_file is None:
            # Create reports directory if it doesn't exist
            reports_dir = os.path.join(os.getcwd(), 'reports')
            os.makedirs(reports_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(reports_dir, f'tuxscan_report_{timestamp}.html')
        
        template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>TuxScan Security Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .finding { margin: 10px 0; padding: 10px; border: 1px solid #ddd; }
                .file-path { color: #0066cc; }
                .line-number { color: #666; }
                .content { background-color: #f5f5f5; padding: 5px; }
                .pattern-name { font-weight: bold; }
                .severity-high { color: #cc0000; }
                .severity-medium { color: #cc8800; }
                .severity-low { color: #00cc00; }
                .summary { margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-radius: 5px; }
                .summary h3 { margin-top: 0; }
                .summary ul { margin-bottom: 0; }
                .severity-stats { display: flex; gap: 20px; margin: 10px 0; }
                .severity-stat { padding: 10px; border-radius: 5px; }
                .severity-stat.high { background-color: #ffebee; }
                .severity-stat.medium { background-color: #fff3e0; }
                .severity-stat.low { background-color: #e8f5e9; }
            </style>
        </head>
        <body>
            <h1>TuxScan Security Report</h1>
            <p>Generated on: {{ timestamp }}</p>
            
            <div class="summary">
                <h3>Scan Summary</h3>
                <div class="severity-stats">
                    <div class="severity-stat high">
                        <strong>High Severity:</strong> {{ high_count }}
                    </div>
                    <div class="severity-stat medium">
                        <strong>Medium Severity:</strong> {{ medium_count }}
                    </div>
                    <div class="severity-stat low">
                        <strong>Low Severity:</strong> {{ low_count }}
                    </div>
                </div>
                <ul>
                    <li>Total Findings: {{ findings|length }}</li>
                    <li>Patterns Checked: {{ patterns_checked }}</li>
                    <li>Scan Time: {{ scan_time }}</li>
                </ul>
            </div>

            <h2>Findings ({{ findings|length }})</h2>
            {% for finding in findings %}
            <div class="finding">
                <div class="file-path">File: {{ finding.file_path }}</div>
                <div class="line-number">Line: {{ finding.line_number }}</div>
                <div class="pattern-name severity-{{ finding.severity|lower }}">Pattern: {{ finding.pattern_name }} ({{ finding.severity }})</div>
                <div class="content">Content: {{ finding.content }}</div>
            </div>
            {% endfor %}
        </body>
        </html>
        """
        
        # Count findings by severity
        high_count = sum(1 for f in self.findings if f.severity == 'HIGH')
        medium_count = sum(1 for f in self.findings if f.severity == 'MEDIUM')
        low_count = sum(1 for f in self.findings if f.severity == 'LOW')
        
        template = Template(template_str)
        html_content = template.render(
            findings=self.findings,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            patterns_checked=len(self.patterns),
            scan_time=datetime.now().strftime("%H:%M:%S"),
            high_count=high_count,
            medium_count=medium_count,
            low_count=low_count
        )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_file

def main():
    parser = argparse.ArgumentParser(description='TuxScan - Internal Security Scanner')
    parser.add_argument('path', help='Path to scan (file or directory)')
    parser.add_argument('--ignore', '-i', nargs='+', help='Patterns to ignore (e.g., "*.git/*" "venv/*")')
    parser.add_argument('--output', '-o', help='Custom output file name (will be placed in reports directory)')
    parser.add_argument('--min-severity', '-s', choices=['LOW', 'MEDIUM', 'HIGH'], 
                      help='Minimum severity level to report (default: all)')
    
    args = parser.parse_args()
    
    scanner = TuxScan(ignore_patterns=args.ignore)
    
    print(f"{Fore.CYAN}Starting TuxScan...{Style.RESET_ALL}")
    
    if os.path.isfile(args.path):
        scanner.scan_file(args.path)
    else:
        scanner.scan_directory(args.path)
    
    if scanner.findings:
        # Filter findings by minimum severity if specified
        if args.min_severity:
            severity_levels = {'LOW': 1, 'MEDIUM': 2, 'HIGH': 3}
            min_level = severity_levels[args.min_severity]
            scanner.findings = [f for f in scanner.findings 
                              if severity_levels[f.severity] >= min_level]
        
        # Print summary with color-coded severity
        print(f"\n{Fore.CYAN}Scan Summary:{Style.RESET_ALL}")
        high_count = sum(1 for f in scanner.findings if f.severity == 'HIGH')
        medium_count = sum(1 for f in scanner.findings if f.severity == 'MEDIUM')
        low_count = sum(1 for f in scanner.findings if f.severity == 'LOW')
        
        print(f"{Fore.RED}High Severity: {high_count}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Medium Severity: {medium_count}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Low Severity: {low_count}{Style.RESET_ALL}")
        print(f"Total Findings: {len(scanner.findings)}")
        
        report_path = scanner.generate_html_report(args.output)
        print(f"\n{Fore.GREEN}Report generated: {report_path}{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}No security issues found!{Style.RESET_ALL}")

if __name__ == '__main__':
    main() 