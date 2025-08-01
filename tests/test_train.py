#!/usr/bin/env python3
"""
Unit tests for the training pipeline.
"""

import sys
import os
import pytest
import json
import tempfile
import shutil

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from utils import load_config, load_digits_data, save_model, load_model
from train import train_model


class TestConfiguration:
    """Test configuration file loading and validation."""
    
    def test_config_file_exists(self):
        """Test that configuration file exists and can be loaded."""
        config = load_config()
        assert isinstance(config, dict)
        assert len(config) > 0
    
    def test_required_hyperparameters_exist(self):
        """Test that all required hyperparameters exist in configuration."""
        config = load_config()
        
        required_params = ['C', 'solver', 'max_iter', 'random_state', 'test_size', 'accuracy_threshold']
        for param in required_params:
            assert param in config, f"Missing required parameter: {param}"
    
    def test_hyperparameter_data_types(self):
        """Test that hyperparameters have correct data types."""
        config = load_config()
        
        # Check data types
        assert isinstance(config['C'], (int, float)), "C should be numeric"
        assert isinstance(config['solver'], str), "solver should be string"
        assert isinstance(config['max_iter'], int), "max_iter should be integer"
        assert isinstance(config['random_state'], int), "random_state should be integer"
        assert isinstance(config['test_size'], float), "test_size should be float"
        assert isinstance(config['accuracy_threshold'], (int, float)), "accuracy_threshold should be numeric"
    
    def test_hyperparameter_values(self):
        """Test that hyperparameters have reasonable values."""
        config = load_config()
        
        assert config['C'] > 0, "C should be positive"
        assert config['solver'] in ['lbfgs', 'liblinear', 'newton-cg', 'sag', 'saga'], "Invalid solver"
        assert config['max_iter'] > 0, "max_iter should be positive"
        assert 0 < config['test_size'] < 1, "test_size should be between 0 and 1"
        assert 0 <= config['accuracy_threshold'] <= 1, "accuracy_threshold should be between 0 and 1"
    
    def test_config_file_not_found(self):
        """Test error handling when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            load_config("nonexistent_config.json")


class TestDataLoading:
    """Test data loading functionality."""
    
    def test_digits_data_loading(self):
        """Test that digits dataset can be loaded and split."""
        X_train, X_test, y_train, y_test = load_digits_data()
        
        # Check data shapes
        assert X_train.shape[1] == 64, "Features should have 64 dimensions"
        assert X_test.shape[1] == 64, "Features should have 64 dimensions"
        assert len(y_train) == X_train.shape[0], "Labels should match features"
        assert len(y_test) == X_test.shape[0], "Labels should match features"
        
        # Check data types
        assert X_train.dtype in ['float64', 'float32'], "Features should be numeric"
        assert y_train.dtype in ['int64', 'int32'], "Labels should be integer"
    
    def test_data_split_consistency(self):
        """Test that data split is consistent with random_state."""
        X_train1, X_test1, y_train1, y_test1 = load_digits_data(random_state=42)
        X_train2, X_test2, y_train2, y_test2 = load_digits_data(random_state=42)
        
        # Same random_state should produce same split
        assert (X_train1 == X_train2).all(), "Data split should be consistent"
        assert (y_train1 == y_train2).all(), "Data split should be consistent"


class TestModelCreation:
    """Test model creation and training."""
    
    def test_model_creation(self):
        """Test that train_model function returns a LogisticRegression object."""
        config = load_config()
        X_train, X_test, y_train, y_test = load_digits_data()
        
        model = train_model(X_train, y_train, config)
        
        assert isinstance(model, LogisticRegression), "Should return LogisticRegression object"
        assert hasattr(model, 'coef_'), "Model should be fitted (have coef_ attribute)"
        assert hasattr(model, 'classes_'), "Model should be fitted (have classes_ attribute)"
    
    def test_model_hyperparameters(self):
        """Test that model is created with correct hyperparameters."""
        config = load_config()
        X_train, X_test, y_train, y_test = load_digits_data()
        
        model = train_model(X_train, y_train, config)
        
        assert model.C == config['C'], "Model C parameter should match config"
        assert model.solver == config['solver'], "Model solver should match config"
        assert model.max_iter == config['max_iter'], "Model max_iter should match config"
        assert model.random_state == config['random_state'], "Model random_state should match config"


class TestModelAccuracy:
    """Test model accuracy and performance."""
    
    def test_model_accuracy_threshold(self):
        """Test that model accuracy meets the threshold specified in config."""
        config = load_config()
        X_train, X_test, y_train, y_test = load_digits_data(
            test_size=config['test_size'],
            random_state=config['random_state']
        )
        
        model = train_model(X_train, y_train, config)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        assert accuracy >= config['accuracy_threshold'], \
            f"Accuracy {accuracy:.4f} below threshold {config['accuracy_threshold']}"
    
    def test_model_performance_reasonable(self):
        """Test that model achieves reasonable accuracy (>0.8)."""
        config = load_config()
        X_train, X_test, y_train, y_test = load_digits_data()
        
        model = train_model(X_train, y_train, config)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        assert accuracy > 0.8, f"Model accuracy {accuracy:.4f} is too low"


class TestModelPersistence:
    """Test model saving and loading."""
    
    def test_model_save_load(self):
        """Test that model can be saved and loaded correctly."""
        config = load_config()
        X_train, X_test, y_train, y_test = load_digits_data()
        
        # Train model
        model = train_model(X_train, y_train, config)
        
        # Create temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = os.path.join(temp_dir, "test_model.pkl")
            
            # Save model
            save_model(model, model_path)
            assert os.path.exists(model_path), "Model file should be created"
            
            # Load model
            loaded_model = load_model(model_path)
            assert isinstance(loaded_model, LogisticRegression), "Loaded model should be LogisticRegression"
            
            # Test that loaded model makes same predictions
            original_pred = model.predict(X_test[:5])
            loaded_pred = loaded_model.predict(X_test[:5])
            assert (original_pred == loaded_pred).all(), "Loaded model should make same predictions"
    
    def test_load_nonexistent_model(self):
        """Test error handling when loading nonexistent model."""
        with pytest.raises(FileNotFoundError):
            load_model("nonexistent_model.pkl")


if __name__ == "__main__":
    pytest.main([__file__]) 