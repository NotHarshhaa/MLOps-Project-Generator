"""
Tests for validator functionality
"""

import pytest

from generator.validators import (
    get_validation_warnings,
    validate_author_name,
    validate_choices,
    validate_framework_combinations,
    validate_project_name,
)


class TestValidators:
    """Test cases for validator functionality"""

    def test_validate_project_name_valid(self):
        """Test valid project names"""
        valid_names = [
            "valid-project",
            "valid_project",
            "validproject123",
            "Valid-Project_123",
        ]

        for name in valid_names:
            # Should not raise any exception
            validate_project_name(name)

    def test_validate_project_name_invalid(self):
        """Test invalid project names"""
        invalid_names = [
            "",  # Empty
            "project with spaces",  # Contains spaces
            "project@with#symbols",  # Invalid symbols
            "a" * 51,  # Too long
            "test",  # Reserved
            "src",  # Reserved
            "data",  # Reserved
        ]

        for name in invalid_names:
            with pytest.raises(ValueError):
                validate_project_name(name)

    def test_validate_author_name_valid(self):
        """Test valid author names"""
        valid_names = [
            "Valid Author",
            "author",
            "Author With Spaces",
            "A. B. Author",
            "Author-Name",
        ]

        for name in valid_names:
            # Should not raise any exception
            validate_author_name(name)

    def test_validate_author_name_invalid(self):
        """Test invalid author names"""
        invalid_names = [
            "",  # Empty
            "a" * 101,  # Too long
        ]

        for name in invalid_names:
            with pytest.raises(ValueError):
                validate_author_name(name)

    def test_validate_framework_combinations_valid(self):
        """Test valid framework combinations"""
        valid_choices = [
            {
                "framework": "sklearn",
                "task_type": "classification",
                "deployment": "fastapi",
                "monitoring": "evidently",
            },
            {
                "framework": "pytorch",
                "task_type": "regression",
                "deployment": "docker",
                "monitoring": "custom",
            },
            {
                "framework": "tensorflow",
                "task_type": "timeseries",
                "deployment": "kubernetes",
                "monitoring": "none",
            },
        ]

        for choices in valid_choices:
            # Should not raise any exception
            validate_framework_combinations(choices)

    def test_validate_choices_complete_valid(self):
        """Test complete validation with valid choices"""
        valid_choices = {
            "framework": "sklearn",
            "task_type": "classification",
            "experiment_tracking": "mlflow",
            "orchestration": "airflow",
            "deployment": "fastapi",
            "monitoring": "evidently",
            "project_name": "valid-project-name",
            "author_name": "Valid Author",
        }

        # Should not raise any exception
        validate_choices(valid_choices)

    def test_validate_choices_invalid_framework(self):
        """Test validation with invalid framework"""
        invalid_choices = {
            "framework": "invalid_framework",
            "task_type": "classification",
            "experiment_tracking": "mlflow",
            "orchestration": "airflow",
            "deployment": "fastapi",
            "monitoring": "evidently",
            "project_name": "valid-project-name",
            "author_name": "Valid Author",
        }

        with pytest.raises(ValueError, match="Invalid framework"):
            validate_choices(invalid_choices)

    def test_validate_choices_invalid_task_type(self):
        """Test validation with invalid task type"""
        invalid_choices = {
            "framework": "sklearn",
            "task_type": "invalid_task",
            "experiment_tracking": "mlflow",
            "orchestration": "airflow",
            "deployment": "fastapi",
            "monitoring": "evidently",
            "project_name": "valid-project-name",
            "author_name": "Valid Author",
        }

        with pytest.raises(ValueError, match="Invalid task type"):
            validate_choices(invalid_choices)

    def test_validate_choices_invalid_experiment_tracking(self):
        """Test validation with invalid experiment tracking"""
        invalid_choices = {
            "framework": "sklearn",
            "task_type": "classification",
            "experiment_tracking": "invalid_tracking",
            "orchestration": "airflow",
            "deployment": "fastapi",
            "monitoring": "evidently",
            "project_name": "valid-project-name",
            "author_name": "Valid Author",
        }

        with pytest.raises(ValueError, match="Invalid experiment tracking"):
            validate_choices(invalid_choices)

    def test_validate_choices_invalid_orchestration(self):
        """Test validation with invalid orchestration"""
        invalid_choices = {
            "framework": "sklearn",
            "task_type": "classification",
            "experiment_tracking": "mlflow",
            "orchestration": "invalid_orchestration",
            "deployment": "fastapi",
            "monitoring": "evidently",
            "project_name": "valid-project-name",
            "author_name": "Valid Author",
        }

        with pytest.raises(ValueError, match="Invalid orchestration"):
            validate_choices(invalid_choices)

    def test_validate_choices_invalid_deployment(self):
        """Test validation with invalid deployment"""
        invalid_choices = {
            "framework": "sklearn",
            "task_type": "classification",
            "experiment_tracking": "mlflow",
            "orchestration": "airflow",
            "deployment": "invalid_deployment",
            "monitoring": "evidently",
            "project_name": "valid-project-name",
            "author_name": "Valid Author",
        }

        with pytest.raises(ValueError, match="Invalid deployment"):
            validate_choices(invalid_choices)

    def test_validate_choices_invalid_monitoring(self):
        """Test validation with invalid monitoring"""
        invalid_choices = {
            "framework": "sklearn",
            "task_type": "classification",
            "experiment_tracking": "mlflow",
            "orchestration": "airflow",
            "deployment": "fastapi",
            "monitoring": "invalid_monitoring",
            "project_name": "valid-project-name",
            "author_name": "Valid Author",
        }

        with pytest.raises(ValueError, match="Invalid monitoring"):
            validate_choices(invalid_choices)

    def test_get_validation_warnings_simple_setup(self):
        """Test warnings for simple setup"""
        simple_choices = {
            "framework": "sklearn",
            "task_type": "classification",
            "orchestration": "none",
            "deployment": "fastapi",
            "monitoring": "none",
        }

        warnings = get_validation_warnings(simple_choices)
        assert len(warnings) == 0

    def test_get_validation_warnings_complex_setup(self):
        """Test warnings for complex setup"""
        complex_choices = {
            "framework": "tensorflow",
            "task_type": "classification",
            "orchestration": "kubeflow",
            "deployment": "kubernetes",
            "monitoring": "evidently",
        }

        warnings = get_validation_warnings(complex_choices)
        assert len(warnings) > 0
        assert any("complex setup" in warning.lower() for warning in warnings)

    def test_get_validation_warnings_framework_specific(self):
        """Test framework-specific warnings"""
        # TensorFlow for simple classification
        tensorflow_choices = {
            "framework": "tensorflow",
            "task_type": "classification",
            "orchestration": "none",
            "deployment": "fastapi",
            "monitoring": "none",
        }

        warnings = get_validation_warnings(tensorflow_choices)
        assert len(warnings) > 0
        assert any("overkill" in warning.lower() for warning in warnings)

    def test_validate_choices_all_valid_frameworks(self):
        """Test validation with all valid frameworks"""
        valid_frameworks = ["sklearn", "pytorch", "tensorflow"]

        for framework in valid_frameworks:
            choices = {
                "framework": framework,
                "task_type": "classification",
                "experiment_tracking": "mlflow",
                "orchestration": "airflow",
                "deployment": "fastapi",
                "monitoring": "evidently",
                "project_name": f"valid-{framework}-project",
                "author_name": "Valid Author",
            }

            # Should not raise any exception
            validate_choices(choices)

    def test_validate_choices_all_valid_task_types(self):
        """Test validation with all valid task types"""
        valid_task_types = ["classification", "regression", "timeseries"]

        for task_type in valid_task_types:
            choices = {
                "framework": "sklearn",
                "task_type": task_type,
                "experiment_tracking": "mlflow",
                "orchestration": "airflow",
                "deployment": "fastapi",
                "monitoring": "evidently",
                "project_name": f"valid-{task_type}-project",
                "author_name": "Valid Author",
            }

            # Should not raise any exception
            validate_choices(choices)

    def test_validate_choices_all_valid_tracking(self):
        """Test validation with all valid experiment tracking options"""
        valid_tracking = ["mlflow", "wandb", "none"]

        for tracking in valid_tracking:
            choices = {
                "framework": "sklearn",
                "task_type": "classification",
                "experiment_tracking": tracking,
                "orchestration": "airflow",
                "deployment": "fastapi",
                "monitoring": "evidently",
                "project_name": f"valid-{tracking}-project",
                "author_name": "Valid Author",
            }

            # Should not raise any exception
            validate_choices(choices)

    def test_validate_choices_wandb_handling(self):
        """Test W&B handling in validation"""
        choices = {
            "framework": "sklearn",
            "task_type": "classification",
            "experiment_tracking": "wandb",  # Should be converted from "W&B"
            "orchestration": "airflow",
            "deployment": "fastapi",
            "monitoring": "evidently",
            "project_name": "valid-wandb-project",
            "author_name": "Valid Author",
        }

        # Should not raise any exception
        validate_choices(choices)


if __name__ == "__main__":
    pytest.main([__file__])
