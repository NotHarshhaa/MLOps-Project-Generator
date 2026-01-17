"""
Pytest configuration and fixtures
"""

import shutil
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_choices():
    """Sample user choices for testing"""
    return {
        "framework": "sklearn",
        "task_type": "classification",
        "experiment_tracking": "mlflow",
        "orchestration": "none",
        "deployment": "fastapi",
        "monitoring": "evidently",
        "project_name": "test-project",
        "author_name": "Test Author",
        "python_version": "3.10",
        "year": "2026",
    }


@pytest.fixture
def sample_template_structure(temp_dir):
    """Create a sample template structure for testing"""
    templates_dir = temp_dir / "templates"
    templates_dir.mkdir()

    # Create common templates
    common_dir = templates_dir / "common"
    common_dir.mkdir()

    # Create framework-specific templates
    sklearn_dir = templates_dir / "sklearn"
    sklearn_dir.mkdir()
    (sklearn_dir / "src").mkdir()
    (sklearn_dir / "src" / "models").mkdir()
    (sklearn_dir / "src" / "data").mkdir()
    (sklearn_dir / "src" / "features").mkdir()

    pytorch_dir = templates_dir / "pytorch"
    pytorch_dir.mkdir()
    (pytorch_dir / "src").mkdir()
    (pytorch_dir / "src" / "models").mkdir()
    (pytorch_dir / "src" / "data").mkdir()
    (pytorch_dir / "src" / "utils").mkdir()

    tensorflow_dir = templates_dir / "tensorflow"
    tensorflow_dir.mkdir()
    (tensorflow_dir / "src").mkdir()
    (tensorflow_dir / "src" / "models").mkdir()
    (tensorflow_dir / "src" / "data").mkdir()
    (tensorflow_dir / "src" / "utils").mkdir()

    # Create sample template files
    (common_dir / "README.md.j2").write_text(
        "# {{ project_name }}\nAuthor: {{ author_name }}"
    )
    (common_dir / "requirements.txt.j2").write_text("numpy>=1.21.0\npandas>=1.3.0")
    (common_dir / "pyproject.toml.j2").write_text(
        '[project]\nname = "{{ project_name }}"'
    )
    (common_dir / "gitignore").write_text("*.pyc\n__pycache__/")
    (common_dir / "Makefile").write_text("install:\n\tpip install -e .")

    (common_dir / "configs").mkdir()
    (common_dir / "configs" / "config.yaml.j2").write_text(
        "project:\n  name: {{ project_name }}"
    )

    # Scikit-learn specific files
    (sklearn_dir / "src" / "train.py.j2").write_text(
        "# {{ framework }} training script"
    )
    (sklearn_dir / "src" / "inference.py.j2").write_text(
        "# {{ framework }} inference script"
    )
    (sklearn_dir / "src" / "models" / "__init__.py").write_text("")
    (sklearn_dir / "src" / "models" / "classification_model.py.j2").write_text(
        "# Classification model"
    )
    (sklearn_dir / "src" / "models" / "regression_model.py.j2").write_text(
        "# Regression model"
    )
    (sklearn_dir / "src" / "models" / "timeseries_model.py.j2").write_text(
        "# Time series model"
    )
    (sklearn_dir / "src" / "data" / "__init__.py").write_text("")
    (sklearn_dir / "src" / "data" / "data_loader.py.j2").write_text("# Data loader")
    (sklearn_dir / "src" / "features" / "__init__.py").write_text("")
    (sklearn_dir / "src" / "features" / "feature_engineering.py.j2").write_text(
        "# Feature engineering"
    )

    # PyTorch specific files
    (pytorch_dir / "src" / "train.py.j2").write_text(
        "# {{ framework }} training script"
    )
    (pytorch_dir / "src" / "inference.py.j2").write_text(
        "# {{ framework }} inference script"
    )
    (pytorch_dir / "src" / "models" / "__init__.py").write_text("")
    (pytorch_dir / "src" / "models" / "classification_model.py.j2").write_text(
        "# Classification model"
    )
    (pytorch_dir / "src" / "models" / "regression_model.py.j2").write_text(
        "# Regression model"
    )
    (pytorch_dir / "src" / "models" / "timeseries_model.py.j2").write_text(
        "# Time series model"
    )
    (pytorch_dir / "src" / "data" / "__init__.py").write_text("")
    (pytorch_dir / "src" / "data" / "data_loader.py.j2").write_text("# Data loader")
    (pytorch_dir / "src" / "utils" / "__init__.py").write_text("")
    (pytorch_dir / "src" / "utils" / "training_utils.py.j2").write_text(
        "# Training utilities"
    )

    # TensorFlow specific files
    (tensorflow_dir / "src" / "train.py.j2").write_text(
        "# {{ framework }} training script"
    )
    (tensorflow_dir / "src" / "inference.py.j2").write_text(
        "# {{ framework }} inference script"
    )
    (tensorflow_dir / "src" / "models" / "__init__.py").write_text("")
    (tensorflow_dir / "src" / "models" / "classification_model.py.j2").write_text(
        "# Classification model"
    )
    (tensorflow_dir / "src" / "models" / "regression_model.py.j2").write_text(
        "# Regression model"
    )
    (tensorflow_dir / "src" / "models" / "timeseries_model.py.j2").write_text(
        "# Time series model"
    )
    (tensorflow_dir / "src" / "data" / "__init__.py").write_text("")
    (tensorflow_dir / "src" / "data" / "data_loader.py.j2").write_text("# Data loader")
    (tensorflow_dir / "src" / "utils" / "__init__.py").write_text("")
    (tensorflow_dir / "src" / "utils" / "training_utils.py.j2").write_text(
        "# Training utilities"
    )

    return templates_dir


@pytest.fixture
def mock_project_dir(temp_dir):
    """Create a mock project directory for testing"""
    project_dir = temp_dir / "test-project"
    project_dir.mkdir()

    # Create basic project structure
    (project_dir / "data" / "raw").mkdir(parents=True)
    (project_dir / "data" / "processed").mkdir(parents=True)
    (project_dir / "data" / "external").mkdir(parents=True)
    (project_dir / "models" / "checkpoints").mkdir(parents=True)
    (project_dir / "models" / "production").mkdir(parents=True)
    (project_dir / "notebooks").mkdir()
    (project_dir / "scripts").mkdir()
    (project_dir / "src").mkdir()
    (project_dir / "configs").mkdir()
    (project_dir / "tests").mkdir()

    # Create placeholder files
    (project_dir / "data" / "raw" / ".gitkeep").write_text("")
    (project_dir / "data" / "processed" / ".gitkeep").write_text("")
    (project_dir / "data" / "external" / ".gitkeep").write_text("")
    (project_dir / "models" / "checkpoints" / ".gitkeep").write_text("")
    (project_dir / "models" / "production" / ".gitkeep").write_text("")

    return project_dir
