from http.server import BaseHTTPRequestHandler
import json
import uuid
import sys
import os
from pathlib import Path

# Add parent directory to path to import generator
sys.path.append(str(Path(__file__).parent.parent.parent))

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Import here to avoid cold start issues
            from generator.validators import validate_choices
            from generator.renderer import ProjectRenderer
            
            # Validate configuration
            validate_choices(data)
            
            # Generate unique task ID
            task_id = str(uuid.uuid4())
            
            # For serverless, we generate synchronously but quickly
            # Note: This might timeout for large projects on Vercel's free tier (10s limit)
            try:
                import tempfile
                import zipfile
                
                temp_dir = Path(tempfile.mkdtemp())
                project_dir = temp_dir / task_id
                project_dir.mkdir(exist_ok=True)
                
                # Change to project directory and generate
                original_cwd = os.getcwd()
                try:
                    os.chdir(project_dir)
                    renderer = ProjectRenderer(data)
                    renderer.generate_project()
                finally:
                    os.chdir(original_cwd)
                
                # Create ZIP file
                zip_path = temp_dir / f"{task_id}.zip"
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in project_dir.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(project_dir)
                            zipf.write(file_path, arcname)
                
                # For serverless, we return the task as completed immediately
                # In a real production setup, you'd use a queue system
                response = {
                    "task_id": task_id,
                    "status": "completed",
                    "message": "Project generated successfully",
                    "download_url": f"/api/download?task_id={task_id}"
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {"error": f"Generation failed: {str(e)}"}
                self.wfile.write(json.dumps(error_response).encode())
                
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {"error": f"Invalid request: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
