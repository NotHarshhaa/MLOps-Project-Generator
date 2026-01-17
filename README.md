# 🧠 MLOps Project Generator

<p align="center">
  <img src="images/banner.png" alt="MLOps Project Generator Banner" width="800"/>
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

## 🌟 NEW: Advanced Features

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

### From Source

```bash
git clone https://github.com/NotHarshhaa/MLOps-Project-Generator.git
cd MLOps-Project-Generator
pip install -e .
```

### Using pip (when published)

```bash
pip install mlops-project-generator
```

## 🖼️ Screenshots

### CLI Commands

<p align="center">
  <img src="images/cli-commands.png" alt="CLI Version and Help Commands" width="700"/>
</p>

### Scikit-learn Project Generation

<p align="center">
  <img src="images/sklearn-generation.png" alt="Scikit-learn Project Generation" width="700"/>
</p>

### PyTorch Project Generation

<p align="center">
  <img src="images/pytorch-generation.png" alt="PyTorch Project Generation" width="700"/>
</p>

### TensorFlow Project Generation

<p align="center">
  <img src="images/tensorflow-generation.png" alt="TensorFlow Project Generation" width="700"/>
</p>

## 🎯 Quick Start

### Generate a New Project

```bash
mlops-project-generator init
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

## 🔮 Roadmap

- [ ] **v1.1**: Additional frameworks (XGBoost, LightGBM)
- [ ] **v1.2**: Cloud deployment templates (AWS, GCP, Azure)
- [ ] **v1.3**: Advanced monitoring solutions
- [ ] **v2.0**: GUI interface for project generation
- [ ] **v2.1**: Template marketplace

---

⭐ If you find this tool helpful, please give us a star on GitHub!

Generated with ❤️ by [MLOps Project Generator](https://github.com/NotHarshhaa/MLOps-Project-Generator)
