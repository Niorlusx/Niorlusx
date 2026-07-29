#!/usr/bin/env python3
"""
Workflow Debugger - Identifies why GitHub Actions workflows fail
"""

import json
from pathlib import Path
from typing import List, Dict

class WorkflowDebugger:
    def __init__(self):
        self.common_issues = {
            "dependency_issues": [
                {
                    "pattern": "ERROR: pip's dependency resolver does not currently take into account",
                    "cause": "Incompatible package versions",
                    "solution": "Update requirements.txt with compatible versions"
                },
                {
                    "pattern": "error: Microsoft Visual C++ 14.0 is required",
                    "cause": "Missing build dependencies on Windows",
                    "solution": "Add build-essential for Linux or use pre-built wheels"
                }
            ],
            "python_issues": [
                {
                    "pattern": "ModuleNotFoundError",
                    "cause": "Package not installed or incorrect import",
                    "solution": "Check requirements.txt and import statements"
                },
                {
                    "pattern": "SyntaxError",
                    "cause": "Invalid Python syntax",
                    "solution": "Review code syntax and Python version compatibility"
                }
            ],
            "workflow_issues": [
                {
                    "pattern": "permission denied",
                    "cause": "File permissions or repository settings",
                    "solution": "Check branch protection rules and file permissions"
                },
                {
                    "pattern": "Job timed out",
                    "cause": "Long-running build or infinite loop",
                    "solution": "Optimize build process or increase timeout"
                }
            ]
        }
    
    def analyze_log(self, log_content: str) -> Dict:
        """Analyze workflow log for issues."""
        results = {
            "errors": [],
            "warnings": [],
            "suggestions": []
        }
        
        for category, issues in self.common_issues.items():
            for issue in issues:
                if issue["pattern"].lower() in log_content.lower():
                    results["errors"].append({
                        "pattern": issue["pattern"],
                        "cause": issue["cause"],
                        "solution": issue["solution"]
                    })
        
        return results
    
    def suggest_fixes(self) -> List[str]:
        """Generate suggested fixes for common issues."""
        return [
            "1. PYTHON VERSION: Upgrade to Python 3.11+ for better compatibility",
            "2. DEPENDENCIES: Use pip-compile or Poetry for reproducible builds",
            "3. CACHING: Add dependency caching to speed up workflows",
            "4. TESTING: Add proper test discovery and error handling",
            "5. LINTING: Implement pre-commit hooks for code quality",
            "6. MONITORING: Add workflow status badges to README",
            "7. SECRETS: Use GitHub Secrets for API keys",
            "8. MATRIX STRATEGY: Consider separating projects into individual workflows"
        ]


if __name__ == "__main__":
    debugger = WorkflowDebugger()
    suggestions = debugger.suggest_fixes()
    
    print("\n" + "="*60)
    print("WORKFLOW DEBUGGER - RECOMMENDED FIXES")
    print("="*60)
    for suggestion in suggestions:
        print(f"  {suggestion}")
    print("\n" + "="*60)
