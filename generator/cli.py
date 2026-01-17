#!/usr/bin/env python3
"""
CLI interface for MLOps Project Generator
"""

import typer
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from generator.prompts import get_user_choices
from generator.renderer import ProjectRenderer
from generator.utils import get_next_steps
from generator.validators import validate_choices

app = typer.Typer(
    name="mlops-project-generator",
    help="🚀 Generate production-ready MLOps project templates",
    no_args_is_help=True,
)
console = Console()


@app.command()
def init():
    """
    Initialize a new MLOps project with interactive prompts
    """
    # Create impressive banner with better layout
    title = Text("🧠 MLOps Project Generator", style="bold cyan")
    title.stylize("bold magenta", 0, 2)  # 🧠 in magenta
    title.stylize("bold cyan", 3, 28)  # MLOps Project Generator in cyan

    # Create feature highlights with better formatting
    features_text = Text()
    features_text.append("🔧 Frameworks: ", style="bold cyan")
    features_text.append("Scikit-learn • PyTorch • TensorFlow\n", style="white")
    features_text.append("📊 Task Types: ", style="bold cyan")
    features_text.append("Classification • Regression • Time-Series\n", style="white")
    features_text.append("🔬 Tracking: ", style="bold cyan")
    features_text.append("MLflow • W&B • Custom\n", style="white")
    features_text.append("🚀 Deployment: ", style="bold cyan")
    features_text.append("FastAPI • Docker • Kubernetes", style="white")

    # Create author credit
    author_text = Text("Created by H A R S H H A A", style="italic dim cyan")

    # Main banner panel with better content
    main_panel = Panel(
        features_text,
        title=title,
        subtitle=author_text,
        border_style="cyan",
        padding=(1, 3),
        title_align="center",
        subtitle_align="center",
    )

    console.print(main_panel)
    console.print()  # Add spacing

    try:
        # Get user choices through interactive prompts
        choices = get_user_choices()

        # Validate choices
        validate_choices(choices)

        # Render the project
        renderer = ProjectRenderer(choices)
        renderer.generate_project()

        # Success message with great UI
        success_title = Text("🎉 Project Generated Successfully!", style="bold green")
        success_title.stylize("bold yellow", 0, 2)  # 🎉 in yellow

        # Create project summary
        summary_table = Table(show_header=False, box=None, padding=0)
        summary_table.add_column(justify="left", style="cyan", width=15)
        summary_table.add_column(justify="left", style="white", width=25)

        summary_table.add_row("📁 Project", choices["project_name"])
        summary_table.add_row("🔧 Framework", choices["framework"].title())
        summary_table.add_row("📊 Task Type", choices["task_type"].title())
        summary_table.add_row("🔬 Tracking", choices["experiment_tracking"].title())
        summary_table.add_row("🚀 Deploy", choices["deployment"].title())

        success_panel = Panel(
            Align.center(summary_table),
            title=success_title,
            subtitle=f"Created by H A R S H H A A • Ready to build! 🚀",
            border_style="green",
            padding=(1, 2),
        )

        console.print(success_panel)

        # Show next steps
        next_steps = get_next_steps(
            choices["framework"], choices["task_type"], choices["deployment"]
        )

        steps_text = Text()
        for i, step in enumerate(next_steps, 1):
            steps_text.append(f"{i}. {step}\n", style="cyan")

        next_steps_panel = Panel(
            steps_text, title="🎯 Next Steps", border_style="blue", padding=(1, 2)
        )

        console.print(next_steps_panel)
        console.print(
            Text(
                f"\n✨ Happy coding with {choices['project_name']}! ✨",
                style="bold green",
            )
        )

    except Exception as e:
        console.print(
            Panel(Text(f"❌ Error: {str(e)}", style="bold red"), border_style="red")
        )
        raise typer.Exit(1)


@app.command()
def version():
    """Show version information"""
    console.print(f"mlops-project-generator v1.0.0")


if __name__ == "__main__":
    app()
