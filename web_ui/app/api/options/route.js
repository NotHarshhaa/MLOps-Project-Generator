import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({
    "framework": [
      {"value": "sklearn", "label": "Scikit-learn", "description": "Tabular data, Classic ML"},
      {"value": "pytorch", "label": "PyTorch", "description": "Deep learning, Research"},
      {"value": "tensorflow", "label": "TensorFlow", "description": "Production, Enterprise"}
    ],
    "task_type": [
      {"value": "classification", "label": "Classification", "description": "Predict categories"},
      {"value": "regression", "label": "Regression", "description": "Predict continuous values"},
      {"value": "timeseries", "label": "Time Series", "description": "Time-based predictions"},
      {"value": "nlp", "label": "NLP", "description": "Natural language processing"},
      {"value": "computer-vision", "label": "Computer Vision", "description": "Image and video analysis"}
    ],
    "experiment_tracking": [
      {"value": "mlflow", "label": "MLflow", "description": "Open-source ML tracking"},
      {"value": "wandb", "label": "W&B", "description": "Cloud-based experiment tracking"},
      {"value": "custom", "label": "Custom", "description": "Custom tracking solution"},
      {"value": "none", "label": "None", "description": "No experiment tracking"}
    ],
    "orchestration": [
      {"value": "airflow", "label": "Airflow", "description": "Workflow orchestration"},
      {"value": "kubeflow", "label": "Kubeflow", "description": "Kubernetes-native ML pipelines"},
      {"value": "none", "label": "None", "description": "No orchestration"}
    ],
    "deployment": [
      {"value": "fastapi", "label": "FastAPI", "description": "REST API deployment"},
      {"value": "docker", "label": "Docker", "description": "Container deployment"},
      {"value": "kubernetes", "label": "Kubernetes", "description": "Production-scale deployment"}
    ],
    "monitoring": [
      {"value": "evidently", "label": "Evidently", "description": "Automated ML monitoring"},
      {"value": "custom", "label": "Custom", "description": "Custom monitoring solution"},
      {"value": "none", "label": "None", "description": "No monitoring"}
    ],
    "cloud_provider": [
      {"value": "", "label": "No Cloud Deployment", "description": "Skip cloud deployment templates"},
      {"value": "aws", "label": "Amazon Web Services", "description": "Deploy to AWS with SageMaker, ECS, Lambda"},
      {"value": "gcp", "label": "Google Cloud Platform", "description": "Deploy to GCP with Vertex AI, Cloud Run"},
      {"value": "azure", "label": "Microsoft Azure", "description": "Deploy to Azure with ML Studio, Functions"}
    ],
    "cloud_service": [
      {"value": "", "label": "Select Provider First", "description": "Choose a cloud provider above"},
      {"value": "sagemaker", "label": "SageMaker", "description": "AWS managed ML service"},
      {"value": "ecs", "label": "ECS", "description": "Elastic Container Service"},
      {"value": "lambda", "label": "Lambda", "description": "Serverless functions"},
      {"value": "vertex-ai", "label": "Vertex AI", "description": "GCP unified ML platform"},
      {"value": "cloud-run", "label": "Cloud Run", "description": "Serverless containers"},
      {"value": "ai-platform", "label": "AI Platform", "description": "GCP ML training and deployment"},
      {"value": "ml-studio", "label": "Azure ML Studio", "description": "Azure ML workspace"},
      {"value": "container-instances", "label": "Container Instances", "description": "Azure container service"},
      {"value": "functions", "label": "Functions", "description": "Azure serverless functions"}
    ],
    "preset_config": [
      {"value": "", "label": "Custom Configuration", "description": "Use your current selections"},
      {"value": "quick-start", "label": "Quick Start", "description": "Basic setup for rapid prototyping"},
      {"value": "production-ready", "label": "Production Ready", "description": "Enterprise-grade configuration"},
      {"value": "research", "label": "Research", "description": "Optimized for ML research projects"},
      {"value": "enterprise", "label": "Enterprise", "description": "Full enterprise MLOps stack"}
    ],
    "custom_template": [
      {"value": "", "label": "Standard Template", "description": "Use the standard framework template"},
      {"value": "minimal", "label": "Minimal", "description": "Lightweight template with essentials only"},
      {"value": "comprehensive", "label": "Comprehensive", "description": "Full-featured template with all options"},
      {"value": "microservice", "label": "Microservice", "description": "Microservice-oriented template"}
    ]
  })
}
