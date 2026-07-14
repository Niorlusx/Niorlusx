#!/usr/bin/env python3
"""
Niorlusx Repository Scanner Agent
Scans for workflow issues, dependency problems, and code quality issues.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class RepositoryScanner:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.issues = []
        self.warnings = []
        self.report = {}

    def scan_workflows(self) -> Dict[str, Any]:
        """Scan GitHub Actions workflows for issues."""
        workflow_issues = {
            "critical": [],
            "warnings": [],
            "info": []
        }
        
        workflows_dir = self.repo_path / ".github/workflows"
        if not workflows_dir.exists():
            workflow_issues["warnings"].append("No .github/workflows directory found")
            return workflow_issues
        
        for workflow_file in workflows_dir.glob("*.yml"):
            with open(workflow_file, 'r') as f:
                content = f.read()
                
            # Check for outdated Python versions
            if 'python-version: "3.10"' in content or "python-version: '3.10'" in content:
                workflow_issues["warnings"].append(
                    f"{workflow_file.name}: Python 3.10 detected - consider upgrading to 3.11+"
                )
            
            # Check for outdated action versions
            if 'uses: actions/setup-python@v3' in content:
                workflow_issues["warnings"].append(
                    f"{workflow_file.name}: Using setup-python@v3 - upgrade to v4+"
                )
            
            # Check for missing error handling
            if 'pytest' in content and ' || echo' not in content:
                workflow_issues["info"].append(
                    f"{workflow_file.name}: pytest may fail silently"
                )
        
        return workflow_issues

    def scan_requirements(self) -> Dict[str, List[str]]:
        """Scan requirements.txt files for outdated dependencies."""
        req_issues = {"outdated": [], "conflicts": [], "info": []}
        
        for req_file in self.repo_path.rglob("requirements.txt"):
            with open(req_file, 'r') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Check for very old pinned versions (pre-2022)
                if '==' in line:
                    pkg, version = line.split('==')
                    # Extract major.minor.patch
                    parts = version.split('.')
                    if len(parts) >= 2:
                        major, minor = int(parts[0]), int(parts[1])
                        # Flag versions from before 2022
                        if major == 0 or (major <= 2 and minor <= 1):
                            req_issues["outdated"].append(
                                f"{req_file}: {line} (very old version detected)"
                            )
            
            # Check for known conflict patterns
            content = ''.join(lines)
            if 'tensorflow' in content and 'numpy' in content:
                # Check for compatibility
                if 'tensorflow==2.5' in content and 'numpy==1.21' in content:
                    req_issues["conflicts"].append(
                        f"{req_file}: TensorFlow 2.5 + NumPy 1.21 may have compatibility issues"
                    )
        
        return req_issues

    def scan_python_code(self) -> Dict[str, List[str]]:
        """Scan Python files for common issues."""
        code_issues = {"errors": [], "warnings": [], "style": []}
        
        for py_file in self.repo_path.rglob("*.py"):
            # Skip venv and __pycache__
            if 'venv' in str(py_file) or '__pycache__' in str(py_file):
                continue
            
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                # Check for common issues
                if 'import *' in line:
                    code_issues["warnings"].append(
                        f"{py_file}:{i}: Avoid wildcard imports"
                    )
                
                if 'print(' in line and 'logging' not in ''.join(lines[:i]):
                    code_issues["style"].append(
                        f"{py_file}:{i}: Consider using logging instead of print"
                    )
        
        return code_issues

    def scan_project_structure(self) -> Dict[str, Any]:
        """Scan overall project structure."""
        structure = {
            "main_dirs": [],
            "config_files": [],
            "issues": []
        }
        
        # List main directories
        for item in self.repo_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                structure["main_dirs"].append(item.name)
        
        # Check for important config files
        important_files = ['README.md', 'LICENSE', '.gitignore', 'setup.py', 'pyproject.toml']
        for fname in important_files:
            fpath = self.repo_path / fname
            if fpath.exists():
                structure["config_files"].append(fname)
            elif fname in ['README.md', 'LICENSE']:
                structure["issues"].append(f"Missing {fname}")
        
        return structure

    def generate_report(self) -> Dict[str, Any]:
        """Generate complete scan report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "repository": str(self.repo_path),
            "scans": {
                "workflows": self.scan_workflows(),
                "requirements": self.scan_requirements(),
                "python_code": self.scan_python_code(),
                "project_structure": self.scan_project_structure()
            },
            "summary": {}
        }
        
        # Generate summary
        total_issues = 0
        for scan_type, results in report["scans"].items():
            if isinstance(results, dict):
                for severity, items in results.items():
                    if isinstance(items, list):
                        total_issues += len(items)
        
        report["summary"]["total_issues"] = total_issues
        report["summary"]["status"] = "HEALTHY" if total_issues < 5 else "NEEDS_ATTENTION"
        
        return report

    def print_report(self, report: Dict[str, Any]) -> None:
        """Pretty print the report."""
        print("\n" + "="*60)
        print("NIORLUSX REPOSITORY SCAN REPORT")
        print("="*60)
        print(f"Timestamp: {report['timestamp']}")
        print(f"Status: {report['summary']['status']}")
        print(f"Total Issues: {report['summary']['total_issues']}")
        print("\n" + "-"*60)
        
        for scan_type, results in report["scans"].items():
            print(f"\n[{scan_type.upper()}]")
            if isinstance(results, dict):
                for severity, items in results.items():
                    if isinstance(items, list) and items:
                        print(f"  {severity.upper()}:")
                        for item in items:
                            print(f"    - {item}")
            elif isinstance(results, list) and results:
                for item in results:
                    print(f"  - {item}")
        
        print("\n" + "="*60)


if __name__ == "__main__":
    scanner = RepositoryScanner(".")
    report = scanner.generate_report()
    scanner.print_report(report)
    
    # Save report to JSON
    with open("scan_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("\nReport saved to scan_report.json")
