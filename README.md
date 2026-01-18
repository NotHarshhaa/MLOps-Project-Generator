# 🧠 MLOps Project Generator

<p align="center">
  <img src="https://raw.githubusercontent.com/NotHarshhaa/MLOps-Project-Generator/master/images/banner.png" alt="MLOps Project Generator Banner" width="800"/>
</p>

A CLI tool that generates production-ready MLOps project templates for Scikit-learn, PyTorch, and TensorFlow.

This stack supports the **full MLOps lifecycle:**

```mathematica
Data → Train → Track → Orchestrate → Deploy → Monitor → Improve
```

## 🚀 Features

- **🔧 Framework Support**: Scikit-learn, PyTorch, TensorFlow/Keras
- **📊 Task Types**: Classification, Regression, Time-Series
- **🔬 Experiment Tracking**: MLflow, W&B
- **🎯 Orchestration**: Airflow, Kubeflow
- **🚀 Deployment**: FastAPI, Docker, Kubernetes
- **📈 Monitoring**: Evidently AI, Custom solutions
- **🛠️ Production-Ready**: CI/CD, monitoring, best practices by default
- **🤖 CI/CD Automation**: Non-interactive mode for DevOps pipelines

## 🌟 NEW: v1.0.5 Advanced Features

### 🚀 **Non-Interactive CLI Mode (CI/CD Ready)**
- **One-liner project generation** with command-line flags
- **Perfect for automation** and CI/CD pipelines
- **Enterprise-ready** with clean, log-friendly output
- **Zero prompts** when flags are provided
- **Smart defaults** for unspecified options

```bash
# Generate a complete project in one command
mlops-project-generator init \
  --framework pytorch \
  --tracking mlflow \
  --deployment docker \
  --monitoring evidently \
  --project-name my-ml-project
```

### 🔍 **Smart System Validation**
- **Automatic system check** for Python, Git, Docker, Conda
- **Real-time status indicators** (✅/❌) with visual feedback
- **System information display** (OS, Python version, architecture)
- **Early validation** to prevent setup issues

### 🧠 **Intelligent Project Generation**
- **Smart project naming** based on framework and task type
- **Framework comparison table** with complexity indicators
- **Project size estimation** (files, lines of code, storage)
- **Impact analysis** for each configuration choice

### 📊 **Enhanced User Experience**
- **Beautiful progress indicators** with real-time updates
- **Interactive framework recommendations** with use cases
- **Comprehensive project summary** before generation
- **Step-by-step next steps** after project creation

### 🔧 **Advanced Template Features**
- **Dynamic .gitignore generation** based on tools selected
- **Framework-specific patterns** (PyTorch: *.pth, TensorFlow: *.pb)
- **Tool-specific configurations** (MLflow, W&B, Airflow, Kubeflow)
- **Comprehensive MLOps artifact management**

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install mlops-project-generator
```

### From Source

```bash
git clone https://github.com/NotHarshhaa/MLOps-Project-Generator.git
cd MLOps-Project-Generator
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/NotHarshhaa/MLOps-Project-Generator.git
cd MLOps-Project-Generator
pip install -e ".[dev]"
```

## 🖼️ Screenshots

### CLI Commands

<p align="center">
  <img src="https://raw.githubusercontent.com/NotHarshhaa/MLOps-Project-Generator/master/images/cli-commands.png" alt="CLI Version and Help Commands" width="700"/>
</p>

### Scikit-learn Project Generation

<p align="center">
  <img src="https://raw.githubusercontent.com/NotHarshhaa/MLOps-Project-Generator/master/images/sklearn-generation.png" alt="Scikit-learn Project Generation" width="700"/>
</p>

### PyTorch Project Generation

<p align="center">
  <img src="https://raw.githubusercontent.com/NotHarshhaa/MLOps-Project-Generator/master/images/pytorch-generation.png" alt="PyTorch Project Generation" width="700"/>
</p>

### TensorFlow Project Generation

<p align="center">
  <img src="https://raw.githubusercontent.com/NotHarshhaa/MLOps-Project-Generator/master/images/tensorflow-generation.png" alt="TensorFlow Project Generation" width="700"/>
</p>

## 🎯 Quick Start

### 🚀 **Option 1: Interactive Mode (Recommended for beginners)**
```bash
mlops-project-generator init
```

### 🤖 **Option 2: Non-Interactive Mode (Perfect for CI/CD)**
```bash
# Quick start with defaults
mlops-project-generator init --framework sklearn --project-name my-project

# Full configuration
mlops-project-generator init \
  --framework pytorch \
  --task-type classification \
  --tracking mlflow \
  --orchestration airflow \
  --deployment docker \
  --monitoring evidently \
  --project-name enterprise-ml \
  --author-name "ML Team" \
  --description "Production ML pipeline"
```

### 📋 **Available CLI Flags**
| Flag | Short | Description | Options |
|------|-------|-------------|---------|
| `--framework` | `-f` | ML framework | `sklearn`, `pytorch`, `tensorflow` |
| `--task-type` | `-t` | Task type | `classification`, `regression`, `time-series`, `nlp`, `computer-vision` |
| `--tracking` | `-r` | Experiment tracking | `mlflow`, `wandb`, `custom`, `none` |
| `--orchestration` | `-o` | Orchestration | `airflow`, `kubeflow`, `none` |
| `--deployment` | `-d` | Deployment | `fastapi`, `docker`, `kubernetes` |
| `--monitoring` | `-m` | Monitoring | `evidently`, `custom`, `none` |
| `--project-name` | `-p` | Project name | Any valid name |
| `--author-name` | `-a` | Author name | Any string |
| `--description` | `--desc` | Project description | Any string |

### 🎯 **Use Case Examples**

#### **🔬 Data Science Quick Start**
```bash
mlops-project-generator init \
  --framework sklearn \
  --task-type classification \
  --tracking mlflow \
  --project-name fraud-detection
```

#### **🚀 Deep Learning Production**
```bash
mlops-project-generator init \
  --framework pytorch \
  --deployment docker \
  --monitoring evidently \
  --project-name image-classifier
```

#### **🏢 Enterprise MLOps**
```bash
mlops-project-generator init \
  --framework tensorflow \
  --orchestration kubeflow \
  --deployment kubernetes \
  --tracking mlflow \
  --project-name enterprise-ml
```

#### **⚡ CI/CD Pipeline Integration**
```bash
# In GitHub Actions, GitLab CI, or Jenkins
mlops-project-generator init \
  --framework $FRAMEWORK \
  --deployment $DEPLOYMENT \
  --project-name $PROJECT_NAME \
  --author-name "CI/CD Pipeline"
```

This will launch an **enhanced interactive CLI** that guides you through:

### 🔍 **Step 1: System Validation**
- **Automatic system check** for required tools
- **Visual status indicators** (✅/❌) 
- **System information display**
- **Early problem detection**

### 🔧 **Step 2: Framework Selection** 
- **Interactive comparison table** with use cases
- **Complexity indicators** (Low/Medium/High)
- **Smart recommendations** based on your needs
- **Framework guidance** for better decisions

### 📊 **Step 3: Configuration**
- **Task type selection** (Classification/Regression/Time-Series)
- **Experiment tracking** (MLflow/W&B/Custom)
- **Orchestration** (Airflow/Kubeflow/None)
- **Deployment** (FastAPI/Docker/Kubernetes)
- **Monitoring** (Evidently/Custom/None)

### 🧠 **Step 4: Smart Project Setup**
- **Intelligent project naming** suggestions
- **Directory validation** to prevent conflicts
- **Project size estimation** (files, lines, storage)
- **Impact analysis** of your choices

### 📋 **Step 5: Enhanced Summary**
- **Comprehensive project overview**
- **Next steps preview** before generation
- **Real-time progress tracking**
- **Step-by-step guidance** after creation

### 🎯 **Step 6: Ready-to-Go Project**
- **Framework-specific code** ready to run
- **Production-ready structure**
- **Comprehensive documentation**
- **Next steps checklist**

### Example Usage

```bash
# Generate a Scikit-learn classification project with MLflow tracking
mlops-project-generator init

# Follow the prompts:
# ✔ ML Framework: Scikit-learn
# ✔ Task Type: Classification
# ✔ Experiment Tracking: MLflow
# ✔ Orchestration: None
# ✔ Deployment: FastAPI
# ✔ Monitoring: Evidently
# ✔ Project Name: ml-classification-project
# ✔ Author Name: Your Name
```

## 📁 Generated Project Structure

```
your-project/
├── data/                   # Data files
│   ├── raw/               # Raw data
│   ├── processed/         # Processed data
│   └── external/          # External data
├── models/                 # Model files
│   ├── checkpoints/       # Model checkpoints
│   └── production/        # Production models
├── notebooks/              # Jupyter notebooks
├── scripts/                # Utility scripts
├── src/                    # Source code
│   ├── data/              # Data loading utilities
│   ├── models/            # Model implementations
│   ├── features/          # Feature engineering (sklearn)
│   └── utils/             # Training utilities (pytorch/tensorflow)
├── configs/                # Configuration files
├── tests/                  # Test files
├── requirements.txt        # Dependencies
├── pyproject.toml         # Project configuration
├── Makefile               # Build commands
├── .gitignore             # Git ignore rules
└── README.md              # Project documentation
```

## 🛠️ Framework-Specific Features

### Scikit-learn Projects
- **Models**: RandomForest, LogisticRegression, SVM, etc.
- **Feature Engineering**: Scaling, selection, PCA
- **Evaluation**: Cross-validation, comprehensive metrics
- **Deployment**: Joblib serialization, FastAPI integration

### PyTorch Projects
- **Models**: Neural networks with residual connections, attention mechanisms
- **Training**: Advanced optimizers, learning rate schedulers, early stopping
- **Utilities**: Gradient clipping, data augmentation, model profiling
- **Deployment**: TorchScript, FastAPI integration

### TensorFlow Projects
- **Models**: Keras models with batch normalization, attention mechanisms
- **Training**: Callbacks, custom loss functions, gradient clipping
- **Utilities**: Model profiling, data augmentation, custom schedulers
- **Deployment**: SavedModel format, FastAPI integration

## 📊 Experiment Tracking Integration

### MLflow Integration
```python
# Automatically logged metrics
mlflow.log_metrics({
    "train_loss": 0.123,
    "val_accuracy": 0.95,
    "learning_rate": 0.001
})

# Model artifacts
mlflow.log_artifact("models/production/model.joblib")
```

### W&B Integration
```python
# Automatic logging with W&B callback
wandb.init(project="my-project")
wandb.log({"loss": 0.123, "accuracy": 0.95})
```

## 🚀 Deployment Options

### FastAPI Deployment
```bash
# Start the API server
uvicorn src.inference:app --reload

# API documentation at http://localhost:8000/docs
```

### Docker Deployment
```bash
# Build and run
docker build -t my-ml-project .
docker run -p 8000:8000 my-ml-project
```

### Kubernetes Deployment
```bash
# Deploy to Kubernetes
kubectl apply -f k8s/
```

## 📈 Monitoring Solutions

### Evidently AI Integration
```python
# Data drift monitoring
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

report = Report(metrics=[DataDriftPreset()])
report.run(current_data=current, reference_data=reference)
```

### Custom Monitoring
```python
# Custom monitoring implementation
class ModelMonitor:
    def check_performance(self, predictions, ground_truth):
        # Custom performance checks
        pass
```

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/NotHarshhaa/MLOps-Project-Generator.git
cd MLOps-Project-Generator

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run linting
black generator/ tests/
isort generator/ tests/
flake8 generator/ tests/
mypy generator/
```

### Project Structure

```
mlops-project-generator/
├── generator/              # CLI tool source code
│   ├── cli.py             # Main CLI interface
│   ├── prompts.py         # Interactive prompts
│   ├── renderer.py        # Template rendering
│   └── validators.py      # Input validation
├── templates/              # Project templates
│   ├── common/            # Common files across frameworks
│   ├── sklearn/           # Scikit-learn specific templates
│   ├── pytorch/           # PyTorch specific templates
│   └── tensorflow/        # TensorFlow specific templates
├── tests/                  # Test files
├── docs/                   # Documentation
├── pyproject.toml         # Project configuration
└── README.md              # This file
```

## 🔧 Configuration

The generated projects use YAML configuration files:

```yaml
# configs/config.yaml
project:
  name: "my-project"
  author: "Your Name"
  version: "0.1.0"

model:
  type: "RandomForestClassifier"
  n_estimators: 100
  max_depth: 10

training:
  batch_size: 32
  learning_rate: 0.001
  epochs: 100

experiment_tracking:
  tool: "mlflow"
  tracking_uri: "http://localhost:5000"

deployment:
  method: "fastapi"
  host: "0.0.0.0"
  port: 8000
```

## 🚀 CI/CD Integration

### GitHub Actions Example
```yaml
name: Generate ML Project
on:
  workflow_dispatch:
    inputs:
      framework:
        type: choice
        options: [sklearn, pytorch, tensorflow]
        default: sklearn
      project_name:
        type: string
        default: ml-project

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install MLOps Generator
        run: pip install mlops-project-generator
      
      - name: Generate ML Project
        run: |
          mlops-project-generator init \
            --framework ${{ github.event.inputs.framework }} \
            --project-name ${{ github.event.inputs.project_name }} \
            --tracking mlflow \
            --deployment docker
      
      - name: Upload generated project
        uses: actions/upload-artifact@v3
        with:
          name: ${{ github.event.inputs.project_name }}
          path: ${{ github.event.inputs.project_name }}/
```

### GitLab CI Example
```yaml
stages:
  - generate

generate_ml_project:
  stage: generate
  image: python:3.11
  script:
    - pip install mlops-project-generator
    - mlops-project-generator init \
        --framework $FRAMEWORK \
        --project-name $PROJECT_NAME \
        --tracking mlflow \
        --deployment docker
  artifacts:
    paths:
      - $PROJECT_NAME/
    expire_in: 1 week
```

### Jenkins Pipeline Example
```groovy
pipeline {
    agent any
    parameters {
        choice(name: 'FRAMEWORK', choices: ['sklearn', 'pytorch', 'tensorflow'], description: 'ML Framework')
        string(name: 'PROJECT_NAME', defaultValue: 'ml-project', description: 'Project Name')
    }
    
    stages {
        stage('Generate ML Project') {
            steps {
                sh 'pip install mlops-project-generator'
                sh """
                    mlops-project-generator init \
                        --framework ${params.FRAMEWORK} \
                        --project-name ${params.PROJECT_NAME} \
                        --tracking mlflow \
                        --deployment docker
                """
                archiveArtifacts artifacts: "${params.PROJECT_NAME}/**/*", fingerprint: true
            }
        }
    }
}
```

### Docker Integration
```dockerfile
FROM python:3.11-slim

WORKDIR /app
RUN pip install mlops-project-generator

# Copy project generation script
COPY generate-project.sh .
RUN chmod +x generate-project.sh

# Generate project on container start
CMD ["./generate-project.sh"]
```

### Environment Variables Support
```bash
# Using environment variables in CI/CD
export FRAMEWORK=pytorch
export DEPLOYMENT=kubernetes
export PROJECT_NAME=prod-ml

mlops-project-generator init \
  --framework $FRAMEWORK \
  --deployment $DEPLOYMENT \
  --project-name $PROJECT_NAME \
  --author-name "CI/CD Pipeline"
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Typer** - For the beautiful CLI interface
- **Jinja2** - For powerful template rendering
- **Rich** - For stunning terminal output
- **Cookiecutter** - For project template inspiration

## 📞 Support

- 📧 Email: contact@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/NotHarshhaa/MLOps-Project-Generator/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/NotHarshhaa/MLOps-Project-Generator/discussions)

## � Roadmap

- [ ] **v1.1**: Additional frameworks (XGBoost, LightGBM)
- [ ] **v1.2**: Cloud deployment templates (AWS, GCP, Azure)
- [ ] **v1.3**: Advanced monitoring solutions
- [ ] **v2.0**: GUI interface for project generation
- [ ] **v2.1**: Template marketplace

---

⭐ If you find this tool helpful, please give us a star on GitHub!

Generated with ❤️ by [MLOps Project Generator](https://github.com/NotHarshhaa/MLOps-Project-Generator)
