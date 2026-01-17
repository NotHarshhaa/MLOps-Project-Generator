"""
Interactive prompts for user configuration
"""

from typing import Any, Dict

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text

from generator.utils import (
    check_system_requirements,
    get_next_steps,
    get_project_size_estimate,
    get_system_info,
    suggest_project_name,
    validate_project_directory,
)

console = Console()


def show_system_check():
    """Show system requirements check"""
    console.print(Panel(Text("🔍 System Check", style="bold cyan")))

    requirements = check_system_requirements()
    system_info = get_system_info()

    # Create requirements table
    req_table = Table(show_header=False, box=None)
    req_table.add_column("Component", style="cyan", width=20)
    req_table.add_column("Status", width=15)

    status_icons = {True: "✅ Available", False: "❌ Missing"}

    for component, available in requirements.items():
        status = status_icons[available]
        style = "green" if available else "red"
        component_name = component.replace("_", " ").title()
        req_table.add_row(component_name, Text(status, style=style))

    console.print(req_table)

    # Show system info
    info_text = Text()
    info_text.append(f"OS: {system_info['os']} | ", style="white")
    info_text.append(f"Python: {system_info['python_version']} | ", style="white")
    info_text.append(f"Arch: {system_info['architecture']}", style="white")

    console.print(Panel(info_text, border_style="dim"))
    console.print()


def show_project_summary(choices: Dict[str, Any]) -> bool:
    """Show enhanced project summary with size estimate"""
    console.print(Panel(Text("📋 Project Configuration Summary", style="bold cyan")))

    # Main configuration table
    table = Table(show_header=True, box=None)
    table.add_column("Setting", style="bold cyan", width=20)
    table.add_column("Choice", style="white", width=25)
    table.add_column("Impact", style="yellow", width=15)

    # Display mapping
    display_mapping = {
        "framework": "Framework",
        "task_type": "Task Type",
        "experiment_tracking": "Experiment Tracking",
        "orchestration": "Orchestration",
        "deployment": "Deployment",
        "monitoring": "Monitoring",
        "project_name": "Project Name",
        "author_name": "Author Name",
        # Task types
        "classification": "Basic setup",
        "regression": "Standard setup",
        "timeseries": "Advanced setup",
        # Experiment tracking
        "mlflow": "Full tracking",
        "wandb": "Cloud tracking",
        "tracking_none": "Basic setup",
        # Orchestration
        "airflow": "Advanced pipeline",
        "kubeflow": "Enterprise pipeline",
        "orchestration_none": "Simple workflow",
        # Deployment
        "fastapi": "Quick deploy",
        "docker": "Container deploy",
        "kubernetes": "Production deploy",
        # Monitoring
        "evidently": "Auto monitoring",
        "custom": "Manual monitoring",
        "monitoring_none": "Basic monitoring",
    }

    impact_mapping = {
        "sklearn": "Low complexity",
        "pytorch": "High complexity",
        "tensorflow": "Medium complexity",
        "classification": "Standard setup",
        "regression": "Standard setup",
        "timeseries": "Advanced setup",
        "mlflow": "Full tracking",
        "wandb": "Cloud tracking",
        "tracking_none": "Basic setup",
        "airflow": "Advanced pipeline",
        "kubeflow": "Enterprise pipeline",
        "orchestration_none": "Simple workflow",
        "fastapi": "Quick deploy",
        "docker": "Container deploy",
        "kubernetes": "Production deploy",
        "evidently": "Auto monitoring",
        "custom": "Manual monitoring",
        "monitoring_none": "Basic monitoring",
    }

    for key, display_name in display_mapping.items():
        value = choices.get(key, "N/A")
        # Format display values
        if value == "none":
            value = "None"
        elif value == "wandb":
            value = "W&B"
        elif value == "sklearn":
            value = "Scikit-learn"
        elif value == "pytorch":
            value = "PyTorch"
        elif value == "tensorflow":
            value = "TensorFlow"

        impact = impact_mapping.get(value, "Standard")

        table.add_row(display_name, value, impact)

    console.print(table)

    # Show project size estimate
    features = [
        choices["experiment_tracking"],
        choices["orchestration"],
        choices["deployment"],
        choices["monitoring"],
    ]
    size_estimate = get_project_size_estimate(choices["framework"], features)

    size_text = Text()
    size_text.append(f"📁 Estimated: {size_estimate['files']} files | ", style="white")
    size_text.append(f"📝 {size_estimate['lines']:,} lines | ", style="white")
    size_text.append(f"💾 {size_estimate['size_mb']} MB", style="white")

    console.print(
        Panel(size_text, title="Project Size Estimate", border_style="yellow")
    )

    # Show next steps preview
    next_steps = get_next_steps(
        choices["framework"], choices["task_type"], choices["deployment"]
    )
    steps_text = Text("\n".join(f"• {step}" for step in next_steps[:3]), style="dim")
    console.print(Panel(steps_text, title="Next Steps Preview", border_style="dim"))

    return Confirm.ask("Proceed with these choices?", default=True)


def get_user_choices() -> Dict[str, Any]:
    """
    Get user choices through interactive prompts

    Returns:
        Dict containing all user choices
    """
    choices = {}

    # System check
    show_system_check()

    # Framework selection with recommendations
    console.print(Panel(Text("🔧 Choose ML Framework", style="bold cyan")))
    framework_choices = ["Scikit-learn", "PyTorch", "TensorFlow"]

    # Show framework recommendations
    framework_table = Table(show_header=True, box=None)
    framework_table.add_column("Framework", style="bold cyan")
    framework_table.add_column("Best For", style="white")
    framework_table.add_column("Complexity", style="yellow")

    framework_table.add_row("Scikit-learn", "Tabular data, Classic ML", "Low")
    framework_table.add_row("PyTorch", "Deep learning, Research", "High")
    framework_table.add_row("TensorFlow", "Production, Enterprise", "Medium")

    console.print(framework_table)
    console.print()

    framework = Prompt.ask(
        "Select framework", choices=framework_choices, default="Scikit-learn"
    )
    if framework == "Scikit-learn":
        choices["framework"] = "sklearn"
    else:
        choices["framework"] = framework.lower().replace("-", "")

    # Task type selection
    console.print(Panel(Text("📊 Choose Task Type", style="bold cyan")))
    task_choices = ["Classification", "Regression", "Time-Series"]
    task_type = Prompt.ask(
        "Select task type", choices=task_choices, default="Classification"
    )
    choices["task_type"] = task_type.lower().replace("-", "")

    # Experiment tracking
    console.print(Panel(Text("🔬 Experiment Tracking", style="bold cyan")))
    tracking_choices = ["MLflow", "W&B", "None"]
    experiment_tracking = Prompt.ask(
        "Select experiment tracking", choices=tracking_choices, default="MLflow"
    )
    if experiment_tracking == "W&B":
        choices["experiment_tracking"] = "wandb"
    else:
        choices["experiment_tracking"] = experiment_tracking.lower()

    # Orchestration
    console.print(Panel(Text("🎯 Orchestration", style="bold cyan")))
    orchestration_choices = ["Airflow", "Kubeflow", "None"]
    orchestration = Prompt.ask(
        "Select orchestration tool", choices=orchestration_choices, default="None"
    )
    choices["orchestration"] = orchestration.lower()

    # Deployment
    console.print(Panel(Text("🚀 Deployment", style="bold cyan")))
    deployment_choices = ["FastAPI", "Docker", "Kubernetes"]
    deployment = Prompt.ask(
        "Select deployment method", choices=deployment_choices, default="FastAPI"
    )
    choices["deployment"] = deployment.lower()

    # Monitoring
    console.print(Panel(Text("📈 Monitoring", style="bold cyan")))
    monitoring_choices = ["Evidently", "Custom", "None"]
    monitoring = Prompt.ask(
        "Select monitoring solution", choices=monitoring_choices, default="Evidently"
    )
    choices["monitoring"] = monitoring.lower()

    # Project name with smart suggestions
    console.print(Panel(Text("📝 Project Details", style="bold cyan")))

    # Generate smart suggestion
    suggested_name = suggest_project_name(choices["framework"], choices["task_type"])

    project_name = Prompt.ask("Enter project name", default=suggested_name)

    # Validate project directory
    while not validate_project_directory(project_name):
        console.print(
            Panel(
                Text(
                    f"❌ Directory '{project_name}' already exists or cannot be created",
                    style="bold red",
                ),
                border_style="red",
            )
        )
        project_name = Prompt.ask("Enter a different project name")

    choices["project_name"] = project_name

    # Author name
    author_name = Prompt.ask("Enter author name", default="ML Engineer")
    choices["author_name"] = author_name

    # Display enhanced summary and confirm
    if not show_project_summary(choices):
        console.print("❌ Project generation cancelled.")
        exit(0)

    return choices


def display_summary(choices: Dict[str, Any]) -> None:
    """Display a summary of user choices"""
    table = Table(title="📋 Project Configuration Summary")
    table.add_column("Setting", style="cyan")
    table.add_column("Choice", style="green")

    display_mapping = {
        "framework": "ML Framework",
        "task_type": "Task Type",
        "experiment_tracking": "Experiment Tracking",
        "orchestration": "Orchestration",
        "deployment": "Deployment",
        "monitoring": "Monitoring",
        "project_name": "Project Name",
        "author_name": "Author",
    }

    for key, display_name in display_mapping.items():
        value = choices.get(key, "N/A")
        # Format display values
        if value == "none":
            value = "None"
        elif value == "wandb":
            value = "W&B"
        elif value == "sklearn":
            value = "Scikit-learn"
        elif value == "pytorch":
            value = "PyTorch"
        elif value == "tensorflow":
            value = "TensorFlow"

        table.add_row(display_name, value)

    console.print(table)
