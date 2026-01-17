"""
Tests for template renderer functionality
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

from generator.renderer import ProjectRenderer


class TestProjectRenderer:
    """Test cases for project renderer"""
    
    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.choices = {
            "framework": "sklearn",
            "task_type": "classification",
            "experiment_tracking": "mlflow",
            "orchestration": "none",
            "deployment": "fastapi",
            "monitoring": "evidently",
            "project_name": "test-project",
            "author_name": "Test Author",
            "python_version": "3.10",
            "year": "2026"
        }
        
        # Create mock template structure
        self.templates_dir = Path(self.temp_dir) / "templates"
        self.templates_dir.mkdir()
        
        # Create common templates
        common_dir = self.templates_dir / "common"
        common_dir.mkdir()
        
        # Create sklearn templates
        sklearn_dir = self.templates_dir / "sklearn"
        sklearn_dir.mkdir()
        (sklearn_dir / "src").mkdir()
        (sklearn_dir / "src" / "models").mkdir()
        
        # Create test template files
        (common_dir / "README.md.j2").write_text("# {{ project_name }}\nAuthor: {{ author_name }}")
        (sklearn_dir / "src" / "models" / "model.py.j2").write_text("# {{ framework }} model\n# {{ task_type }}")
        
        # Update template directory in renderer
        self.original_template_dir = Path("templates")
    
    def teardown_method(self):
        """Cleanup test environment"""
        shutil.rmtree(self.temp_dir)
    
    def test_renderer_initialization(self):
        """Test renderer initialization"""
        with patch('generator.renderer.Path') as mock_path:
            mock_path.return_value = self.templates_dir
            renderer = ProjectRenderer(self.choices)
            
            assert renderer.choices == self.choices
            assert renderer.project_name == "test-project"
            assert renderer.framework == "sklearn"
    
    @patch('generator.renderer.Path')
    def test_create_project_directory(self, mock_path):
        """Test project directory creation"""
        mock_path.return_value = self.templates_dir
        renderer = ProjectRenderer(self.choices)
        
        # Mock output directory
        output_dir = Path(self.temp_dir) / "test-project"
        renderer.output_dir = output_dir
        
        renderer._create_project_directory()
        
        assert output_dir.exists()
        assert output_dir.is_dir()
    
    @patch('generator.renderer.Path')
    def test_copy_common_files(self, mock_path):
        """Test copying common files"""
        mock_path.return_value = self.templates_dir
        renderer = ProjectRenderer(self.choices)
        
        # Mock output directory
        output_dir = Path(self.temp_dir) / "test-project"
        output_dir.mkdir()
        renderer.output_dir = output_dir
        
        renderer._copy_common_files()
        
        # Check if .gitignore was created (this is what _copy_common_files actually does)
        gitignore_file = output_dir / ".gitignore"
        assert gitignore_file.exists()
        
        # Check if Makefile was copied from common templates
        makefile = output_dir / "Makefile"
        assert makefile.exists()
    
    @patch('generator.renderer.Path')
    def test_copy_framework_files(self, mock_path):
        """Test copying framework-specific files"""
        mock_path.return_value = self.templates_dir
        renderer = ProjectRenderer(self.choices)
        
        # Mock output directory
        output_dir = Path(self.temp_dir) / "test-project"
        output_dir.mkdir()
        (output_dir / "src").mkdir()
        renderer.output_dir = output_dir
        
        renderer._copy_framework_files()
        
        # Check if framework files were copied
        copied_file = output_dir / "src" / "models" / "model.py.j2"
        assert copied_file.exists()
    
    @patch('generator.renderer.Path')
    def test_render_templates(self, mock_path):
        """Test template rendering"""
        mock_path.return_value = self.templates_dir
        renderer = ProjectRenderer(self.choices)
        
        # Mock output directory
        output_dir = Path(self.temp_dir) / "test-project"
        output_dir.mkdir()
        renderer.output_dir = output_dir
        
        # Copy template files first
        renderer._copy_common_files()
        renderer._copy_framework_files()
        
        renderer._render_templates()
        
        # Check if templates were rendered
        rendered_readme = output_dir / "README.md"
        assert rendered_readme.exists()
        
        content = rendered_readme.read_text()
        assert "test-project" in content
        assert "Test Author" in content
        assert "{{ project_name }}" not in content  # Template variable should be replaced
    
    @patch('generator.renderer.Path')
    def test_create_additional_directories(self, mock_path):
        """Test creation of additional directories"""
        mock_path.return_value = self.templates_dir
        renderer = ProjectRenderer(self.choices)
        
        # Mock output directory
        output_dir = Path(self.temp_dir) / "test-project"
        output_dir.mkdir()
        renderer.output_dir = output_dir
        
        renderer._create_additional_directories()
        
        # Check if additional directories were created
        assert (output_dir / "data" / "raw").exists()
        assert (output_dir / "data" / "processed").exists()
        assert (output_dir / "models" / "checkpoints").exists()
        assert (output_dir / "notebooks").exists()
        assert (output_dir / "scripts").exists()
        assert (output_dir / "configs").exists()
    
    @patch('generator.renderer.Path')
    def test_generate_project_complete(self, mock_path):
        """Test complete project generation"""
        mock_path.return_value = self.templates_dir
        renderer = ProjectRenderer(self.choices)
        
        # Mock output directory
        output_dir = Path(self.temp_dir) / "test-project"
        renderer.output_dir = output_dir
        
        # Generate complete project
        renderer.generate_project()
        
        # Check if project was generated completely
        assert output_dir.exists()
        assert (output_dir / "README.md").exists()
        assert (output_dir / "src" / "models" / "model.py").exists()
        assert (output_dir / "data" / "raw").exists()
        assert (output_dir / "models" / "checkpoints").exists()
        assert (output_dir / "notebooks").exists()
        assert (output_dir / "scripts").exists()
        assert (output_dir / "configs").exists()
    
    def test_get_template_context(self):
        """Test template context generation"""
        renderer = ProjectRenderer(self.choices)
        context = renderer.get_template_context()
        
        assert context["project_name"] == "test-project"
        assert context["project_slug"] == "test-project"
        assert context["framework_display"] == "Sklearn"
        assert context["task_display"] == "Classification"
        assert context["python_version"] == "3.10"
        assert context["year"] == "2026"
    
    @patch('generator.renderer.Path')
    def test_copy_directory(self, mock_path):
        """Test directory copying functionality"""
        mock_path.return_value = self.templates_dir
        renderer = ProjectRenderer(self.choices)
        
        # Create source directory with files
        src_dir = Path(self.temp_dir) / "source"
        src_dir.mkdir()
        (src_dir / "file1.txt").write_text("content1")
        (src_dir / "file2.txt").write_text("content2")
        
        # Create destination directory
        dst_dir = Path(self.temp_dir) / "destination"
        
        renderer._copy_directory(src_dir, dst_dir)
        
        # Check if files were copied
        assert dst_dir.exists()
        assert (dst_dir / "file1.txt").exists()
        assert (dst_dir / "file2.txt").exists()
        assert (dst_dir / "file1.txt").read_text() == "content1"
        assert (dst_dir / "file2.txt").read_text() == "content2"


if __name__ == "__main__":
    pytest.main([__file__])
