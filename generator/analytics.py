"""
Project analytics and metrics for MLOps Project Generator
"""

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn

console = Console()


class ProjectAnalytics:
    """
    Analytics and metrics for generated projects
    """

    def __init__(self):
        self.analytics_dir = Path.home() / ".mlops-project-generator" / "analytics"
        self.analytics_dir.mkdir(parents=True, exist_ok=True)
        self.projects_file = self.analytics_dir / "projects.json"
        self._ensure_analytics_file()

    def _ensure_analytics_file(self):
        """Ensure analytics file exists"""
        if not self.projects_file.exists():
            with open(self.projects_file, "w", encoding="utf-8") as f:
                json.dump({"projects": []}, f)

    def record_project_generation(self, choices: Dict[str, Any], project_path: str):
        """Record a project generation event"""
        projects = self.load_projects()
        
        project_record = {
            "timestamp": datetime.now().isoformat(),
            "project_name": choices.get("project_name", "unknown"),
            "project_path": project_path,
            "framework": choices.get("framework", "unknown"),
            "task_type": choices.get("task_type", "unknown"),
            "experiment_tracking": choices.get("experiment_tracking", "none"),
            "orchestration": choices.get("orchestration", "none"),
            "deployment": choices.get("deployment", "none"),
            "monitoring": choices.get("monitoring", "none"),
            "author_name": choices.get("author_name", "unknown"),
            "complexity_score": self._calculate_complexity_score(choices),
            "estimated_files": self._estimate_file_count(choices),
            "estimated_lines": self._estimate_line_count(choices)
        }
        
        projects["projects"].append(project_record)
        
        with open(self.projects_file, "w", encoding="utf-8") as f:
            json.dump(projects, f, indent=2)

    def load_projects(self) -> Dict[str, Any]:
        """Load all project records"""
        try:
            with open(self.projects_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"projects": []}

    def get_project_stats(self) -> Dict[str, Any]:
        """Get overall project statistics"""
        projects = self.load_projects()["projects"]
        
        if not projects:
            return {"total_projects": 0}
        
        # Framework distribution
        frameworks = {}
        task_types = {}
        deployments = {}
        tracking_tools = {}
        
        total_complexity = 0
        total_files = 0
        total_lines = 0
        
        for project in projects:
            # Count frameworks
            framework = project.get("framework", "unknown")
            frameworks[framework] = frameworks.get(framework, 0) + 1
            
            # Count task types
            task_type = project.get("task_type", "unknown")
            task_types[task_type] = task_types.get(task_type, 0) + 1
            
            # Count deployments
            deployment = project.get("deployment", "unknown")
            deployments[deployment] = deployments.get(deployment, 0) + 1
            
            # Count tracking tools
            tracking = project.get("experiment_tracking", "none")
            tracking_tools[tracking] = tracking_tools.get(tracking, 0) + 1
            
            # Sum metrics
            total_complexity += project.get("complexity_score", 0)
            total_files += project.get("estimated_files", 0)
            total_lines += project.get("estimated_lines", 0)
        
        return {
            "total_projects": len(projects),
            "frameworks": frameworks,
            "task_types": task_types,
            "deployments": deployments,
            "tracking_tools": tracking_tools,
            "avg_complexity": total_complexity / len(projects),
            "total_files_generated": total_files,
            "total_lines_generated": total_lines,
            "recent_projects": projects[-5:] if len(projects) > 5 else projects
        }

    def display_project_stats(self):
        """Display project statistics in a formatted way"""
        stats = self.get_project_stats()
        
        if stats["total_projects"] == 0:
            console.print("No projects generated yet.")
            return
        
        # Main stats table
        stats_table = Table(title="📊 Project Generation Statistics")
        stats_table.add_column("Metric", style="cyan", width=20)
        stats_table.add_column("Value", style="white", width=15)
        
        stats_table.add_row("Total Projects", str(stats["total_projects"]))
        stats_table.add_row("Avg Complexity", f"{stats['avg_complexity']:.1f}")
        stats_table.add_row("Total Files Generated", f"{stats['total_files_generated']:,}")
        stats_table.add_row("Total Lines Generated", f"{stats['total_lines_generated']:,}")
        
        console.print(stats_table)
        console.print()
        
        # Framework distribution
        self._display_distribution("🔧 Framework Distribution", stats["frameworks"])
        
        # Task type distribution
        self._display_distribution("📊 Task Type Distribution", stats["task_types"])
        
        # Deployment distribution
        self._display_distribution("🚀 Deployment Distribution", stats["deployments"])
        
        # Tracking tools distribution
        self._display_distribution("🔬 Tracking Tools", stats["tracking_tools"])

    def _display_distribution(self, title: str, distribution: Dict[str, int]):
        """Display a distribution as a table"""
        table = Table(title=title)
        table.add_column("Item", style="cyan", width=15)
        table.add_column("Count", style="white", width=8)
        table.add_column("Percentage", style="green", width=10)
        
        total = sum(distribution.values())
        
        for item, count in sorted(distribution.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total) * 100
            table.add_row(
                item.title(),
                str(count),
                f"{percentage:.1f}%"
            )
        
        console.print(table)
        console.print()

    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """Analyze a generated project"""
        project_path = Path(project_path)
        
        if not project_path.exists():
            return {"error": "Project path does not exist"}
        
        analysis = {
            "project_path": str(project_path),
            "total_files": 0,
            "total_lines": 0,
            "file_types": {},
            "directory_structure": {},
            "python_files": 0,
            "config_files": 0,
            "doc_files": 0,
            "test_files": 0
        }
        
        # Analyze files
        for file_path in project_path.rglob("*"):
            if file_path.is_file():
                analysis["total_files"] += 1
                
                # Count file types
                suffix = file_path.suffix.lower()
                analysis["file_types"][suffix] = analysis["file_types"].get(suffix, 0) + 1
                
                # Count lines for text files
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = len(f.readlines())
                        analysis["total_lines"] += lines
                        
                        # Categorize files
                        if suffix == ".py":
                            analysis["python_files"] += 1
                        elif suffix in [".yml", ".yaml", ".json", ".toml", ".cfg"]:
                            analysis["config_files"] += 1
                        elif suffix in [".md", ".rst", ".txt"]:
                            analysis["doc_files"] += 1
                        elif "test" in file_path.name.lower():
                            analysis["test_files"] += 1
                except (UnicodeDecodeError, PermissionError):
                    # Skip binary files
                    pass
        
        # Analyze directory structure
        for dir_path in project_path.rglob("*"):
            if dir_path.is_dir():
                depth = len(dir_path.relative_to(project_path).parts)
                if depth not in analysis["directory_structure"]:
                    analysis["directory_structure"][depth] = 0
                analysis["directory_structure"][depth] += 1
        
        return analysis

    def display_project_analysis(self, project_path: str):
        """Display detailed project analysis"""
        analysis = self.analyze_project(project_path)
        
        if "error" in analysis:
            console.print(f"❌ {analysis['error']}")
            return
        
        # Project overview
        overview_table = Table(title=f"📁 Project Analysis: {Path(project_path).name}")
        overview_table.add_column("Metric", style="cyan", width=20)
        overview_table.add_column("Value", style="white", width=15)
        
        overview_table.add_row("Total Files", str(analysis["total_files"]))
        overview_table.add_row("Total Lines", f"{analysis['total_lines']:,}")
        overview_table.add_row("Python Files", str(analysis["python_files"]))
        overview_table.add_row("Config Files", str(analysis["config_files"]))
        overview_table.add_row("Documentation", str(analysis["doc_files"]))
        overview_table.add_row("Test Files", str(analysis["test_files"]))
        
        console.print(overview_table)
        console.print()
        
        # File type distribution
        self._display_distribution("📄 File Type Distribution", analysis["file_types"])

    def _calculate_complexity_score(self, choices: Dict[str, Any]) -> int:
        """Calculate complexity score for a project configuration"""
        score = 0
        
        # Framework complexity
        framework_scores = {"sklearn": 1, "tensorflow": 2, "pytorch": 3}
        score += framework_scores.get(choices.get("framework", "sklearn"), 1)
        
        # Task type complexity
        task_scores = {"classification": 1, "regression": 1, "time-series": 2, "nlp": 3, "computer-vision": 3}
        score += task_scores.get(choices.get("task_type", "classification"), 1)
        
        # Tool complexity
        if choices.get("experiment_tracking") != "none":
            score += 1
        if choices.get("orchestration") != "none":
            score += 2
        if choices.get("deployment") == "kubernetes":
            score += 3
        elif choices.get("deployment") == "docker":
            score += 2
        else:
            score += 1
        if choices.get("monitoring") != "none":
            score += 1
        
        return score

    def _estimate_file_count(self, choices: Dict[str, Any]) -> int:
        """Estimate number of files for a project configuration"""
        base_files = 10  # Basic files like README, requirements, etc.
        
        # Framework-specific files
        framework_files = {"sklearn": 8, "tensorflow": 12, "pytorch": 12}
        base_files += framework_files.get(choices.get("framework", "sklearn"), 8)
        
        # Tool-specific files
        if choices.get("experiment_tracking") != "none":
            base_files += 3
        if choices.get("orchestration") != "none":
            base_files += 5
        if choices.get("deployment") == "kubernetes":
            base_files += 8
        elif choices.get("deployment") == "docker":
            base_files += 4
        if choices.get("monitoring") != "none":
            base_files += 3
        
        return base_files

    def _estimate_line_count(self, choices: Dict[str, Any]) -> int:
        """Estimate number of lines of code for a project configuration"""
        base_lines = 100  # Basic configuration and setup
        
        # Framework-specific lines
        framework_lines = {"sklearn": 200, "tensorflow": 400, "pytorch": 450}
        base_lines += framework_lines.get(choices.get("framework", "sklearn"), 200)
        
        # Tool-specific lines
        if choices.get("experiment_tracking") != "none":
            base_lines += 50
        if choices.get("orchestration") != "none":
            base_lines += 100
        if choices.get("deployment") == "kubernetes":
            base_lines += 150
        elif choices.get("deployment") == "docker":
            base_lines += 80
        if choices.get("monitoring") != "none":
            base_lines += 60
        
        return base_lines

    def get_recommendations(self, choices: Dict[str, Any]) -> List[str]:
        """Get recommendations based on project configuration"""
        recommendations = []
        
        framework = choices.get("framework", "sklearn")
        deployment = choices.get("deployment", "fastapi")
        tracking = choices.get("experiment_tracking", "none")
        
        # Framework recommendations
        if framework == "sklearn" and choices.get("task_type") == "time-series":
            recommendations.append("Consider using specialized time-series libraries like Prophet or statsmodels")
        
        # Deployment recommendations
        if deployment == "fastapi" and choices.get("orchestration") == "kubeflow":
            recommendations.append("Consider using Docker for better containerization with Kubeflow")
        
        # Tracking recommendations
        if tracking == "none" and framework in ["pytorch", "tensorflow"]:
            recommendations.append("Consider adding experiment tracking for better model management")
        
        # Production recommendations
        if choices.get("monitoring") == "none" and deployment in ["docker", "kubernetes"]:
            recommendations.append("Add monitoring for production deployments")
        
        return recommendations
