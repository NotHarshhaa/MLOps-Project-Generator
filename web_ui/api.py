#!/usr/bin/env python3
"""
FastAPI backend for MLOps Project Generator Web UI
"""

import os
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import uuid

# Import the existing generator
import sys
sys.path.append(str(Path(__file__).parent.parent))
from generator.renderer import ProjectRenderer
from generator.validators import validate_choices

app = FastAPI(
    title="MLOps Project Generator API",
    description="Web API for generating MLOps project templates",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage for temporary projects
TEMP_DIR = Path(tempfile.gettempdir()) / "mlops_projects"
TEMP_DIR.mkdir(exist_ok=True)

class ProjectConfig(BaseModel):
    """Project configuration model"""
    framework: str = Field(..., description="ML framework (sklearn, pytorch, tensorflow)")
    task_type: str = Field(..., description="Task type (classification, regression, timeseries)")
    experiment_tracking: str = Field(..., description="Experiment tracking (mlflow, wandb, none)")
    orchestration: str = Field(..., description="Orchestration (airflow, kubeflow, none)")
    deployment: str = Field(..., description="Deployment (fastapi, docker, kubernetes)")
    monitoring: str = Field(..., description="Monitoring (evidently, custom, none)")
    project_name: str = Field(..., description="Project name")
    author_name: str = Field(default="ML Engineer", description="Author name")
    description: str = Field(default="A production-ready ML project", description="Project description")

class GenerationResponse(BaseModel):
    """Response model for project generation"""
    task_id: str = Field(..., description="Unique task ID")
    status: str = Field(..., description="Generation status")
    message: str = Field(..., description="Status message")

class TaskStatus(BaseModel):
    """Task status model"""
    task_id: str
    status: str  # pending, processing, completed, failed
    message: str
    download_url: str = None

# In-memory task storage (in production, use Redis or database)
tasks: Dict[str, TaskStatus] = {}

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "MLOps Project Generator API", "version": "1.0.0"}

@app.get("/api/options")
async def get_options():
    """Get available options for each configuration field"""
    return {
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

@app.post("/api/generate", response_model=GenerationResponse)
async def generate_project(config: ProjectConfig, background_tasks: BackgroundTasks):
    """Generate a new MLOps project"""
    # Validate configuration
    try:
        choices = config.dict()
        validate_choices(choices)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Generate unique task ID
    task_id = str(uuid.uuid4())
    
    # Initialize task status
    tasks[task_id] = TaskStatus(
        task_id=task_id,
        status="pending",
        message="Project generation queued"
    )
    
    # Start background generation
    background_tasks.add_task(generate_project_background, task_id, choices)
    
    return GenerationResponse(
        task_id=task_id,
        status="pending",
        message="Project generation started"
    )

async def generate_project_background(task_id: str, choices: Dict[str, Any]):
    """Background task for project generation"""
    try:
        # Update status
        tasks[task_id].status = "processing"
        tasks[task_id].message = "Generating project structure..."
        
        # Create temporary directory
        project_dir = TEMP_DIR / task_id
        project_dir.mkdir(exist_ok=True)
        
        # Generate project using existing renderer
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(project_dir)
            renderer = ProjectRenderer(choices)
            renderer.generate_project()
        finally:
            os.chdir(original_cwd)
        
        # Create ZIP file
        zip_path = TEMP_DIR / f"{task_id}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in project_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(project_dir)
                    zipf.write(file_path, arcname)
        
        # Update status
        tasks[task_id].status = "completed"
        tasks[task_id].message = "Project generated successfully"
        tasks[task_id].download_url = f"/api/download/{task_id}"
        
    except Exception as e:
        # Update status with error
        tasks[task_id].status = "failed"
        tasks[task_id].message = f"Generation failed: {str(e)}"
        
        # Cleanup on failure
        try:
            project_dir = TEMP_DIR / task_id
            if project_dir.exists():
                shutil.rmtree(project_dir)
            zip_path = TEMP_DIR / f"{task_id}.zip"
            if zip_path.exists():
                zip_path.unlink()
        except:
            pass

@app.get("/api/status/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str):
    """Get the status of a generation task"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return tasks[task_id]

@app.get("/api/download/{task_id}")
async def download_project(task_id: str):
    """Download the generated project as ZIP"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks[task_id]
    if task.status != "completed":
        raise HTTPException(status_code=400, detail="Project not ready for download")
    
    zip_path = TEMP_DIR / f"{task_id}.zip"
    if not zip_path.exists():
        raise HTTPException(status_code=404, detail="Project file not found")
    
    return FileResponse(
        path=zip_path,
        filename=f"{task_id}.zip",
        media_type="application/zip"
    )

@app.delete("/api/cleanup/{task_id}")
async def cleanup_task(task_id: str):
    """Clean up task files"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    try:
        # Remove project directory
        project_dir = TEMP_DIR / task_id
        if project_dir.exists():
            shutil.rmtree(project_dir)
        
        # Remove ZIP file
        zip_path = TEMP_DIR / f"{task_id}.zip"
        if zip_path.exists():
            zip_path.unlink()
        
        # Remove from memory
        del tasks[task_id]
        
        return {"message": "Task cleaned up successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
