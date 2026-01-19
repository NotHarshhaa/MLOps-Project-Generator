from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        options = {
            "framework": [
                {"value": "sklearn", "label": "Scikit-learn", "description": "Tabular data, Classic ML"},
                {"value": "pytorch", "label": "PyTorch", "description": "Deep learning, Research"},
                {"value": "tensorflow", "label": "TensorFlow", "description": "Production, Enterprise"}
            ],
            "task_type": [
                {"value": "classification", "label": "Classification", "description": "Predict categories"},
                {"value": "regression", "label": "Regression", "description": "Predict continuous values"},
                {"value": "timeseries", "label": "Time Series", "description": "Time-based predictions"}
            ],
            "experiment_tracking": [
                {"value": "mlflow", "label": "MLflow", "description": "Open-source ML tracking"},
                {"value": "wandb", "label": "W&B", "description": "Cloud-based experiment tracking"},
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
            ]
        }
        
        self.wfile.write(json.dumps(options).encode())
        return
