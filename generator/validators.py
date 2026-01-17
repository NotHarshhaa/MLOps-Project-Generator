"""
Validators for user choices and project configuration
"""

import re
from typing import Any, Dict, List

from rich.console import Console

console = Console()


def validate_choices(choices: Dict[str, Any]) -> None:
    """
    Validate user choices for project generation

    Args:
        choices: Dictionary containing user choices

    Raises:
        ValueError: If any choice is invalid
    """
    # Validate framework
    valid_frameworks = ["sklearn", "pytorch", "tensorflow"]
    if choices.get("framework") not in valid_frameworks:
        raise ValueError(f"Invalid framework: {choices.get('framework')}")

    # Validate task type
    valid_tasks = ["classification", "regression", "timeseries"]
    if choices.get("task_type") not in valid_tasks:
        raise ValueError(f"Invalid task type: {choices.get('task_type')}")

    # Validate experiment tracking
    valid_tracking = ["mlflow", "wandb", "none"]
    if choices.get("experiment_tracking") not in valid_tracking:
        raise ValueError(
            f"Invalid experiment tracking: {choices.get('experiment_tracking')}"
        )

    # Validate orchestration
    valid_orchestration = ["airflow", "kubeflow", "none"]
    if choices.get("orchestration") not in valid_orchestration:
        raise ValueError(f"Invalid orchestration: {choices.get('orchestration')}")

    # Validate deployment
    valid_deployment = ["fastapi", "docker", "kubernetes"]
    if choices.get("deployment") not in valid_deployment:
        raise ValueError(f"Invalid deployment: {choices.get('deployment')}")

    # Validate monitoring
    valid_monitoring = ["evidently", "custom", "none"]
    if choices.get("monitoring") not in valid_monitoring:
        raise ValueError(f"Invalid monitoring: {choices.get('monitoring')}")

    # Validate project name
    validate_project_name(choices.get("project_name", ""))

    # Validate author name
    validate_author_name(choices.get("author_name", ""))

    # Validate framework-specific combinations
    validate_framework_combinations(choices)


def validate_project_name(name: str) -> None:
    """
    Validate project name

    Args:
        name: Project name to validate

    Raises:
        ValueError: If project name is invalid
    """
    if not name or not name.strip():
        raise ValueError("Project name cannot be empty")

    # Check for valid characters (letters, numbers, hyphens, underscores)
    if not re.match(r"^[a-zA-Z0-9_-]+$", name):
        raise ValueError(
            "Project name can only contain letters, numbers, hyphens, and underscores"
        )

    # Check length
    if len(name) > 50:
        raise ValueError("Project name must be 50 characters or less")

    # Check for reserved names
    reserved_names = ["test", "src", "data", "models", "config", "scripts", "notebooks"]
    if name.lower() in reserved_names:
        raise ValueError(f"Project name '{name}' is reserved and cannot be used")


def validate_author_name(name: str) -> None:
    """
    Validate author name

    Args:
        name: Author name to validate

    Raises:
        ValueError: If author name is invalid
    """
    if not name or not name.strip():
        raise ValueError("Author name cannot be empty")

    if len(name) > 100:
        raise ValueError("Author name must be 100 characters or less")


def validate_framework_combinations(choices: Dict[str, Any]) -> None:
    """
    Validate framework-specific combinations

    Args:
        choices: Dictionary containing user choices

    Raises:
        ValueError: If combination is invalid
    """
    framework = choices.get("framework")
    task_type = choices.get("task_type")
    deployment = choices.get("deployment")

    # Validate framework-task combinations
    if framework == "sklearn" and task_type == "timeseries":
        console.print("⚠️  Warning: Scikit-learn has limited time series capabilities")

    # Validate deployment-framework compatibility
    if deployment == "kubernetes" and framework == "sklearn":
        console.print(
            "ℹ️  Note: Kubernetes deployment might be overkill for simple Scikit-learn models"
        )

    # Validate experiment tracking compatibility
    tracking = choices.get("experiment_tracking")
    if tracking == "wandb" and framework == "sklearn":
        console.print("ℹ️  Note: W&B integration for Scikit-learn requires manual setup")


def get_validation_warnings(choices: Dict[str, Any]) -> List[str]:
    """
    Get validation warnings for user choices

    Args:
        choices: Dictionary containing user choices

    Returns:
        List of warning messages
    """
    warnings = []

    framework = choices.get("framework")
    orchestration = choices.get("orchestration")
    deployment = choices.get("deployment")

    # Check for complex setups
    complexity_score = 0
    if orchestration != "none":
        complexity_score += 2
    if deployment == "kubernetes":
        complexity_score += 2
    elif deployment == "docker":
        complexity_score += 1
    if choices.get("monitoring") != "none":
        complexity_score += 1

    if complexity_score >= 4:
        warnings.append(
            "This is a complex setup. Consider starting with a simpler configuration."
        )

    # Framework-specific warnings
    if framework == "tensorflow" and choices.get("task_type") == "classification":
        warnings.append("TensorFlow might be overkill for simple classification tasks.")

    return warnings
