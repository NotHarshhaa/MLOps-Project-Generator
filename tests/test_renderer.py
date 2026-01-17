"""
Tests for template renderer functionality
"""

import shutil
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

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
            "description": "Test project description",
            "python_version": "3.10",
            "year": "2026",
        }

    def teardown_method(self):
        """Cleanup test environment"""
        shutil.rmtree(self.temp_dir)

    def test_renderer_initialization(self):
        """Test renderer initialization"""
        renderer = ProjectRenderer(self.choices)

        assert renderer.choices == self.choices
        assert renderer.project_name == "test-project"
        assert renderer.framework == "sklearn"
        assert renderer.template_dir.exists()

    def test_create_project_directory(self):
        """Test project directory creation"""
        renderer = ProjectRenderer(self.choices)

        # Mock output directory
        output_dir = Path(self.temp_dir) / "test-project"
        renderer.output_dir = output_dir

        renderer._create_project_directory()

        assert output_dir.exists()
        assert output_dir.is_dir()

    def test_copy_common_files(self):
        """Test copying common files"""
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

    def test_copy_framework_files(self):
        """Test copying framework-specific files"""
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

    def test_render_templates(self):
        """Test template rendering"""
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
        assert (
            "{{ project_name }}" not in content
        )  # Template variable should be replaced

    def test_create_additional_directories(self):
        """Test creation of additional directories"""
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

    def test_generate_project_complete(self):
        """Test complete project generation"""
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

    def test_copy_directory(self):
        """Test directory copying functionality"""
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
