"""
Utility functions for the MLOps Project Generator
"""

import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional


def check_system_requirements() -> Dict[str, bool]:
    """Check if system meets requirements for generated projects"""
    requirements = {
        "python_version": sys.version_info >= (3, 8),
        "git_available": check_command_available("git"),
        "docker_available": check_command_available("docker"),
        "conda_available": check_command_available("conda"),
        "pip_available": check_command_available("pip"),
    }
    return requirements


def check_command_available(command: str) -> bool:
    """Check if a command is available in the system"""
    try:
        subprocess.run(
            [command, "--version"], capture_output=True, check=True, timeout=5
        )
        return True
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        subprocess.TimeoutExpired,
    ):
        return False


def get_system_info() -> Dict[str, str]:
    """Get system information for project recommendations"""
    return {
        "os": platform.system(),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "architecture": platform.architecture()[0],
        "processor": platform.processor(),
    }


def suggest_project_name(framework: str, task_type: str) -> str:
    """Suggest a project name based on framework and task type"""
    suggestions = {
        "sklearn": {
            "classification": [
                "ml-classifier",
                "predictive-model",
                "classification-ml",
            ],
            "regression": ["ml-regressor", "prediction-model", "regression-ml"],
            "timeseries": ["time-series-ml", "forecasting-model", "temporal-predictor"],
        },
        "pytorch": {
            "classification": ["deep-classifier", "neural-net", "torch-classifier"],
            "regression": ["deep-regressor", "neural-predictor", "torch-regressor"],
            "timeseries": ["lstm-forecast", "sequence-model", "torch-timeseries"],
        },
        "tensorflow": {
            "classification": ["tf-classifier", "keras-model", "tensorflow-ml"],
            "regression": ["tf-regressor", "keras-predictor", "tensorflow-regression"],
            "timeseries": ["tf-forecast", "keras-lstm", "tensorflow-timeseries"],
        },
    }

    import random

    return random.choice(suggestions.get(framework, {}).get(task_type, ["ml-project"]))


def validate_project_directory(
    project_name: str, base_path: Optional[Path] = None
) -> bool:
    """Validate if project directory can be created"""
    if base_path is None:
        base_path = Path.cwd()

    project_path = base_path / project_name

    # Check if directory already exists
    if project_path.exists():
        return False

    # Check if parent directory is writable
    try:
        base_path.mkdir(parents=True, exist_ok=True)
        return True
    except PermissionError:
        return False


def get_project_size_estimate(framework: str, features: List[str]) -> Dict[str, int]:
    """Estimate project size based on framework and features"""
    base_sizes = {
        "sklearn": {"files": 15, "lines": 2000, "size_mb": 2},
        "pytorch": {"files": 20, "lines": 3500, "size_mb": 4},
        "tensorflow": {"files": 22, "lines": 4000, "size_mb": 5},
    }

    feature_multipliers = {
        "mlflow": 1.2,
        "wandb": 1.1,
        "airflow": 1.3,
        "kubeflow": 1.4,
        "docker": 1.2,
        "kubernetes": 1.5,
        "evidently": 1.1,
        "custom": 1.0,
    }

    base = base_sizes.get(framework, base_sizes["sklearn"])

    # Apply feature multipliers
    total_multiplier = 1.0
    for feature in features:
        total_multiplier *= feature_multipliers.get(feature, 1.0)

    return {
        "files": int(base["files"] * total_multiplier),
        "lines": int(base["lines"] * total_multiplier),
        "size_mb": round(base["size_mb"] * total_multiplier, 1),
    }


def create_gitignore_content(framework: str, features: List[str]) -> str:
    """Generate comprehensive .gitignore content"""
    base_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Temporary files
tmp/
temp/

# Data files
data/raw/*
data/processed/*
data/external/*
!data/raw/.gitkeep
!data/processed/.gitkeep
!data/external/.gitkeep

# Model artifacts
models/checkpoints/*
models/production/*
!models/checkpoints/.gitkeep
!models/production/.gitkeep
"""

    # Framework-specific additions
    framework_specific = {
        "pytorch": """
# PyTorch
*.pth
*.pt
runs/
*.onnx
""",
        "tensorflow": """
# TensorFlow
*.pb
*.h5
*.ckpt
logs/
checkpoints/
saved_models/
""",
        "sklearn": """
# Scikit-learn
*.pkl
*.joblib
*.model
""",
    }

    # Feature-specific additions
    feature_specific = {
        "mlflow": """
# MLflow
mlruns/
mlartifacts/
""",
        "wandb": """
# Weights & Biases
wandb/
""",
        "airflow": """
# Airflow
airflow.cfg
dags/__pycache__/
plugins/__pycache__/
""",
        "kubeflow": """
# Kubeflow
.pipeline/
.metadata/
""",
    }

    content = base_content

    # Add framework-specific content
    if framework in framework_specific:
        content += framework_specific[framework]

    # Add feature-specific content
    for feature in features:
        if feature in feature_specific:
            content += feature_specific[feature]

    return content


def get_next_steps(framework: str, task_type: str, deployment: str) -> List[str]:
    """Generate next steps for the user"""
    base_steps = [
        f"cd <your-project-name>",
        "pip install -r requirements.txt",
        "python src/train.py --help",
        "Add your data to data/raw/",
        "Configure configs/config.yaml",
    ]

    framework_steps = {
        "sklearn": [
            "Prepare your dataset in CSV format",
            "Run feature engineering pipeline",
            "Experiment with different models",
        ],
        "pytorch": [
            "Check GPU availability: python -c 'import torch; print(torch.cuda.is_available())'",
            "Prepare dataset in PyTorch format",
            "Adjust hyperparameters in configs/",
        ],
        "tensorflow": [
            "Check TensorFlow installation: python -c 'import tensorflow as tf; print(tf.__version__)'",
            "Prepare dataset for Keras models",
            "Configure model architecture in src/models/",
        ],
    }

    deployment_steps = {
        "fastapi": [
            "Start API server: python src/inference.py",
            "Test API: curl http://localhost:8000/docs",
        ],
        "docker": [
            "Build Docker image: docker build -t my-ml-app .",
            "Run container: docker run -p 8000:8000 my-ml-app",
        ],
        "kubernetes": [
            "Review k8s/ deployment files",
            "Apply to cluster: kubectl apply -f k8s/",
        ],
    }

    next_steps = (
        base_steps
        + framework_steps.get(framework, [])
        + deployment_steps.get(deployment, [])
    )

    return next_steps[:8]  # Return top 8 steps
