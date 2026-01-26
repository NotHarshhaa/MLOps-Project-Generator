"""
Configuration management for MLOps Project Generator
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


class ConfigManager:
    """
    Manages project configurations, templates, and presets
    """

    def __init__(self):
        self.config_dir = Path.home() / ".mlops-project-generator"
        self.config_dir.mkdir(exist_ok=True)
        self.presets_file = self.config_dir / "presets.json"
        self.templates_file = self.config_dir / "custom_templates.json"
        self._ensure_default_configs()

    def _ensure_default_configs(self):
        """Ensure default configuration files exist"""
        if not self.presets_file.exists():
            self._create_default_presets()
        if not self.templates_file.exists():
            self._create_default_templates()

    def _create_default_presets(self):
        """Create default project presets"""
        default_presets = {
            "quick-start": {
                "name": "Quick Start",
                "description": "Fast setup for prototyping",
                "config": {
                    "framework": "sklearn",
                    "task_type": "classification",
                    "experiment_tracking": "none",
                    "orchestration": "none",
                    "deployment": "fastapi",
                    "monitoring": "none"
                }
            },
            "production-ready": {
                "name": "Production Ready",
                "description": "Full MLOps stack for production",
                "config": {
                    "framework": "pytorch",
                    "task_type": "classification",
                    "experiment_tracking": "mlflow",
                    "orchestration": "airflow",
                    "deployment": "kubernetes",
                    "monitoring": "evidently"
                }
            },
            "research": {
                "name": "Research",
                "description": "Experiment tracking focused setup",
                "config": {
                    "framework": "pytorch",
                    "task_type": "classification",
                    "experiment_tracking": "wandb",
                    "orchestration": "none",
                    "deployment": "fastapi",
                    "monitoring": "custom"
                }
            },
            "enterprise": {
                "name": "Enterprise",
                "description": "Enterprise-grade MLOps pipeline",
                "config": {
                    "framework": "tensorflow",
                    "task_type": "classification",
                    "experiment_tracking": "mlflow",
                    "orchestration": "kubeflow",
                    "deployment": "kubernetes",
                    "monitoring": "evidently"
                }
            }
        }
        
        with open(self.presets_file, "w", encoding="utf-8") as f:
            json.dump(default_presets, f, indent=2)

    def _create_default_templates(self):
        """Create default custom templates configuration"""
        default_templates = {
            "custom_templates": [],
            "template_paths": [],
            "overrides": {}
        }
        
        with open(self.templates_file, "w", encoding="utf-8") as f:
            json.dump(default_templates, f, indent=2)

    def save_preset(self, name: str, config: Dict[str, Any], description: str = ""):
        """Save a project configuration as a preset"""
        presets = self.load_presets()
        
        presets[name] = {
            "name": name,
            "description": description,
            "config": config
        }
        
        with open(self.presets_file, "w", encoding="utf-8") as f:
            json.dump(presets, f, indent=2)
        
        console.print(f"✅ Preset '{name}' saved successfully!")

    def load_presets(self) -> Dict[str, Any]:
        """Load all saved presets"""
        try:
            with open(self.presets_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def get_preset(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific preset by name"""
        presets = self.load_presets()
        return presets.get(name)

    def delete_preset(self, name: str) -> bool:
        """Delete a preset"""
        presets = self.load_presets()
        if name in presets:
            del presets[name]
            with open(self.presets_file, "w", encoding="utf-8") as f:
                json.dump(presets, f, indent=2)
            return True
        return False

    def list_presets(self) -> List[Dict[str, Any]]:
        """List all available presets"""
        presets = self.load_presets()
        preset_list = []
        
        for key, preset in presets.items():
            preset_list.append({
                "key": key,
                "name": preset.get("name", key),
                "description": preset.get("description", ""),
                "config": preset.get("config", {})
            })
        
        return preset_list

    def display_presets(self):
        """Display all presets in a formatted table"""
        presets = self.list_presets()
        
        if not presets:
            console.print("No presets found. Use 'save-preset' to create one.")
            return
        
        table = Table(title="📋 Available Presets")
        table.add_column("Name", style="cyan", width=15)
        table.add_column("Description", style="white", width=25)
        table.add_column("Framework", style="green", width=12)
        table.add_column("Deployment", style="yellow", width=12)
        table.add_column("Tracking", style="blue", width=12)
        
        for preset in presets:
            config = preset["config"]
            table.add_row(
                preset["name"],
                preset["description"],
                config.get("framework", "N/A").title(),
                config.get("deployment", "N/A").title(),
                config.get("experiment_tracking", "N/A").title()
            )
        
        console.print(table)

    def save_config(self, config: Dict[str, Any], filename: str):
        """Save a configuration to a file"""
        config_file = self.config_dir / f"{filename}.json"
        
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        
        console.print(f"✅ Configuration saved to {config_file}")

    def load_config(self, filename: str) -> Optional[Dict[str, Any]]:
        """Load a configuration from a file"""
        config_file = self.config_dir / f"{filename}.json"
        
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def list_saved_configs(self) -> List[str]:
        """List all saved configuration files"""
        configs = []
        for file in self.config_dir.glob("*.json"):
            if file.name not in ["presets.json", "custom_templates.json"]:
                configs.append(file.stem)
        return configs

    def export_preset(self, preset_name: str, export_path: str):
        """Export a preset to a file"""
        preset = self.get_preset(preset_name)
        if not preset:
            console.print(f"❌ Preset '{preset_name}' not found")
            return
        
        export_file = Path(export_path)
        if not export_file.suffix:
            export_file = export_file.with_suffix(".json")
        
        with open(export_file, "w", encoding="utf-8") as f:
            json.dump(preset, f, indent=2)
        
        console.print(f"✅ Preset exported to {export_file}")

    def import_preset(self, import_path: str, preset_name: str = None):
        """Import a preset from a file"""
        import_file = Path(import_path)
        
        try:
            with open(import_file, "r", encoding="utf-8") as f:
                preset_data = json.load(f)
            
            if isinstance(preset_data, dict) and "config" in preset_data:
                # It's a full preset object
                name = preset_name or preset_data.get("name", import_file.stem)
                preset = preset_data
            else:
                # It's just a config dict
                name = preset_name or import_file.stem
                preset = {
                    "name": name,
                    "description": f"Imported from {import_file.name}",
                    "config": preset_data
                }
            
            self.save_preset(name, preset["config"], preset["description"])
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            console.print(f"❌ Error importing preset: {e}")

    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        """Validate a configuration and return any errors"""
        errors = []
        required_fields = [
            "framework", "task_type", "experiment_tracking", 
            "orchestration", "deployment", "monitoring"
        ]
        
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")
        
        # Validate framework
        valid_frameworks = ["sklearn", "pytorch", "tensorflow"]
        if config.get("framework") not in valid_frameworks:
            errors.append(f"Invalid framework. Must be one of: {valid_frameworks}")
        
        # Validate task types
        valid_task_types = ["classification", "regression", "time-series", "nlp", "computer-vision"]
        if config.get("task_type") not in valid_task_types:
            errors.append(f"Invalid task type. Must be one of: {valid_task_types}")
        
        return errors
