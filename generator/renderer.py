"""
Template renderer for generating MLOps projects
"""

import shutil
from pathlib import Path
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader, select_autoescape
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from generator.utils import create_gitignore_content

console = Console()


class ProjectRenderer:
    """
    Renders and generates MLOps project templates based on user choices
    """

    def __init__(self, choices: Dict[str, Any]):
        self.choices = choices
        self.project_name = choices["project_name"]
        self.framework = choices["framework"]
        # Get the template directory relative to the package location
        package_dir = Path(__file__).parent.parent
        self.template_dir = package_dir / "templates"
        self.output_dir = Path.cwd() / self.project_name

    def generate_project(self) -> None:
        """
        Generate the complete project structure
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:

            # Create output directory
            task = progress.add_task("Creating project directory...", total=None)
            self._create_project_directory()
            progress.update(task, description="Project directory created")

            # Copy common files
            task = progress.add_task("Copying common files...", total=None)
            self._copy_common_files()
            progress.update(task, description="Common files copied")

            # Copy framework-specific files
            task = progress.add_task(f"Copying {self.framework} files...", total=None)
            self._copy_framework_files()
            progress.update(task, description=f"{self.framework} files copied")

            # Render templates
            task = progress.add_task("Rendering templates...", total=None)
            self._render_templates()
            progress.update(task, description="Templates rendered")

            # Create additional directories
            task = progress.add_task("Creating additional directories...", total=None)
            self._create_additional_directories()
            progress.update(task, description="Additional directories created")

    def _create_project_directory(self) -> None:
        """Create the main project directory"""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _copy_common_files(self) -> None:
        """Copy files from common template directory"""
        common_dir = self.template_dir / "common"
        if common_dir.exists():
            self._copy_directory(common_dir, self.output_dir)

        # Generate enhanced .gitignore
        gitignore_path = self.output_dir / ".gitignore"
        features = [
            self.choices["experiment_tracking"],
            self.choices["orchestration"],
            self.choices["deployment"],
            self.choices["monitoring"],
        ]
        gitignore_content = create_gitignore_content(self.framework, features)

        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write(gitignore_content)

    def _copy_framework_files(self) -> None:
        """Copy framework-specific files"""
        framework_dir = self.template_dir / self.framework
        if framework_dir.exists():
            self._copy_directory(framework_dir, self.output_dir)

    def _copy_directory(self, src: Path, dst: Path) -> None:
        """Copy directory contents recursively"""
        for item in src.rglob("*"):
            if item.is_file():
                relative_path = item.relative_to(src)
                dst_file = dst / relative_path
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dst_file)

    def _render_templates(self) -> None:
        """Render Jinja2 templates with user choices"""
        # Setup Jinja2 environment
        template_dirs = [
            str(self.template_dir / "common"),
            str(self.template_dir / self.framework),
        ]
        env = Environment(
            loader=FileSystemLoader(template_dirs),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Render all template files
        for template_dir in template_dirs:
            if Path(template_dir).exists():
                self._render_templates_in_dir(env, Path(template_dir))

    def _render_templates_in_dir(self, env: Environment, template_dir: Path) -> None:
        """Render templates in a specific directory"""
        for template_file in template_dir.rglob("*.j2"):
            relative_path = template_file.relative_to(template_dir)
            output_file = self.output_dir / relative_path.with_suffix("")

            # Load and render template
            template = env.get_template(str(relative_path).replace("\\", "/"))
            rendered_content = template.render(**self.get_template_context())

            # Write rendered content
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(rendered_content)

            # Remove the original template file from output directory
            output_template_file = self.output_dir / relative_path
            if output_template_file.exists():
                output_template_file.unlink()

    def _create_additional_directories(self) -> None:
        """Create additional directories based on choices"""
        directories = []

        # Data directories
        directories.extend(["data/raw", "data/processed", "data/external"])

        # Model directories
        directories.extend(["models/checkpoints", "models/production"])

        # Notebooks directory
        directories.append("notebooks")

        # Scripts directory
        directories.append("scripts")

        # Config directories
        directories.append("configs")

        # Framework-specific directories
        if self.framework == "pytorch":
            directories.extend(["src/data", "src/models", "src/training", "src/utils"])
        elif self.framework == "tensorflow":
            directories.extend(["src/data", "src/models", "src/training", "src/utils"])
        elif self.framework == "sklearn":
            directories.extend(["src/data", "src/models", "src/features", "src/utils"])

        # Tool-specific directories
        if self.choices["experiment_tracking"] != "none":
            tracking_dir = (
                "mlruns" if self.choices["experiment_tracking"] == "mlflow" else "wandb"
            )
            directories.append(tracking_dir)

        if self.choices["orchestration"] != "none":
            orchestration_dir = (
                "dags" if self.choices["orchestration"] == "airflow" else "pipelines"
            )
            directories.append(orchestration_dir)

        # Create directories
        for directory in directories:
            (self.output_dir / directory).mkdir(parents=True, exist_ok=True)

    def get_template_context(self) -> Dict[str, Any]:
        """Get template context with additional computed values"""
        context = self.choices.copy()

        # Add computed values
        project_slug = self.project_name.lower().replace(" ", "-").replace("_", "-")
        context.update(
            {
                "project_slug": project_slug,
                "python_version": "3.10",
                "year": "2026",
                "framework_display": self.framework.title(),
                "task_display": self.choices["task_type"].title(),
            }
        )

        return context
