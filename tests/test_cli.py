"""
Tests for CLI functionality
"""

import pytest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from generator.cli import app
from generator.prompts import get_user_choices
from generator.validators import validate_choices


class TestCLI:
    """Test cases for CLI functionality"""
    
    def setup_method(self):
        """Setup test environment"""
        self.runner = CliRunner()
    
    def test_version_command(self):
        """Test version command"""
        result = self.runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "mlops-project-generator v1.0.0" in result.stdout
    
    @patch('generator.prompts.get_user_choices')
    @patch('generator.renderer.ProjectRenderer')
    @patch('generator.validators.validate_choices')
    def test_init_command_success(self, mock_validate, mock_renderer, mock_choices):
        """Test successful init command"""
        # Mock user choices
        mock_choices.return_value = {
            "framework": "sklearn",
            "task_type": "classification",
            "experiment_tracking": "mlflow",
            "orchestration": "none",
            "deployment": "fastapi",
            "monitoring": "evidently",
            "project_name": "test-project",
            "author_name": "Test Author",
            "description": "Test project description"
        }
        
        # Mock renderer
        mock_renderer_instance = MagicMock()
        mock_renderer.return_value = mock_renderer_instance
        
        result = self.runner.invoke(app, ["init"])
        
        assert result.exit_code == 0
        mock_choices.assert_called_once()
        mock_validate.assert_called_once()
        mock_renderer_instance.generate_project.assert_called_once()
    
    @patch('generator.prompts.get_user_choices')
    def test_init_command_validation_error(self, mock_choices):
        """Test init command with validation error"""
        # Mock invalid choices
        mock_choices.return_value = {
            "framework": "invalid_framework",
            "task_type": "classification",
            "experiment_tracking": "mlflow",
            "orchestration": "none",
            "deployment": "fastapi",
            "monitoring": "evidently",
            "project_name": "test-project",
            "author_name": "Test Author"
        }
        
        result = self.runner.invoke(app, ["init"])
        
        assert result.exit_code == 1
        assert "Error:" in result.stdout


class TestPrompts:
    """Test cases for prompt functionality"""
    
    @patch('generator.prompts.Prompt.ask')
    @patch('generator.prompts.Confirm.ask')
    def test_get_user_choices(self, mock_confirm, mock_ask):
        """Test user choices collection"""
        # Mock user inputs
        mock_ask.side_effect = [
            "Scikit-learn",  # framework
            "Classification",  # task_type
            "MLflow",  # experiment_tracking
            "None",  # orchestration
            "FastAPI",  # deployment
            "Evidently",  # monitoring
            "test-project",  # project_name
            "Test Author"  # author_name
        ]
        mock_confirm.return_value = True
        
        choices = get_user_choices()
        
        assert choices["framework"] == "sklearn"
        assert choices["task_type"] == "classification"
        assert choices["experiment_tracking"] == "mlflow"
        assert choices["orchestration"] == "none"
        assert choices["deployment"] == "fastapi"
        assert choices["monitoring"] == "evidently"
        assert choices["project_name"] == "test-project"
        assert choices["author_name"] == "Test Author"
    
    @patch('generator.prompts.Prompt.ask')
    @patch('generator.prompts.Confirm.ask')
    def test_get_user_choices_cancellation(self, mock_confirm, mock_ask):
        """Test user cancellation"""
        # Mock user inputs
        mock_ask.side_effect = [
            "Scikit-learn",  # framework
            "Classification",  # task_type
            "MLflow",  # experiment_tracking
            "None",  # orchestration
            "FastAPI",  # deployment
            "Evidently",  # monitoring
            "test-project",  # project_name
            "Test Author"  # author_name
        ]
        mock_confirm.return_value = False  # User cancels
        
        with pytest.raises(SystemExit):
            get_user_choices()


class TestValidators:
    """Test cases for validation functionality"""
    
    def test_validate_choices_valid(self):
        """Test validation with valid choices"""
        valid_choices = {
            "framework": "sklearn",
            "task_type": "classification",
            "experiment_tracking": "mlflow",
            "orchestration": "none",
            "deployment": "fastapi",
            "monitoring": "evidently",
            "project_name": "valid-project-name",
            "author_name": "Valid Author"
        }
        
        # Should not raise any exception
        validate_choices(valid_choices)
    
    def test_validate_choices_invalid_framework(self):
        """Test validation with invalid framework"""
        invalid_choices = {
            "framework": "invalid_framework",
            "task_type": "classification",
            "experiment_tracking": "mlflow",
            "orchestration": "none",
            "deployment": "fastapi",
            "monitoring": "evidently",
            "project_name": "valid-project-name",
            "author_name": "Valid Author"
        }
        
        with pytest.raises(ValueError, match="Invalid framework"):
            validate_choices(invalid_choices)
    
    def test_validate_choices_invalid_task_type(self):
        """Test validation with invalid task type"""
        invalid_choices = {
            "framework": "sklearn",
            "task_type": "invalid_task",
            "experiment_tracking": "mlflow",
            "orchestration": "none",
            "deployment": "fastapi",
            "monitoring": "evidently",
            "project_name": "valid-project-name",
            "author_name": "Valid Author"
        }
        
        with pytest.raises(ValueError, match="Invalid task type"):
            validate_choices(invalid_choices)
    
    def test_validate_choices_invalid_project_name(self):
        """Test validation with invalid project name"""
        invalid_choices = {
            "framework": "sklearn",
            "task_type": "classification",
            "experiment_tracking": "mlflow",
            "orchestration": "none",
            "deployment": "fastapi",
            "monitoring": "evidently",
            "project_name": "",  # Empty project name
            "author_name": "Valid Author"
        }
        
        with pytest.raises(ValueError, match="Project name cannot be empty"):
            validate_choices(invalid_choices)
    
    def test_validate_choices_reserved_project_name(self):
        """Test validation with reserved project name"""
        invalid_choices = {
            "framework": "sklearn",
            "task_type": "classification",
            "experiment_tracking": "mlflow",
            "orchestration": "none",
            "deployment": "fastapi",
            "monitoring": "evidently",
            "project_name": "test",  # Reserved name
            "author_name": "Valid Author"
        }
        
        with pytest.raises(ValueError, match="is reserved"):
            validate_choices(invalid_choices)
    
    def test_validate_choices_invalid_author_name(self):
        """Test validation with invalid author name"""
        invalid_choices = {
            "framework": "sklearn",
            "task_type": "classification",
            "experiment_tracking": "mlflow",
            "orchestration": "none",
            "deployment": "fastapi",
            "monitoring": "evidently",
            "project_name": "valid-project-name",
            "author_name": ""  # Empty author name
        }
        
        with pytest.raises(ValueError, match="Author name cannot be empty"):
            validate_choices(invalid_choices)


if __name__ == "__main__":
    pytest.main([__file__])
