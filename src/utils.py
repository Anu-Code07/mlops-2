import json
import os
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split


def load_config(config_path="config/config.json"):
    """
    Load configuration from JSON file.
    
    Args:
        config_path (str): Path to the configuration file
        
    Returns:
        dict: Configuration dictionary
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    return config


def load_digits_data(test_size=0.2, random_state=42):
    """
    Load and split the digits dataset.
    
    Args:
        test_size (float): Proportion of data to use for testing
        random_state (int): Random seed for reproducibility
        
    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    digits = load_digits()
    X, y = digits.data, digits.target
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    return X_train, X_test, y_train, y_test


def save_model(model, filepath="model_train.pkl"):
    """
    Save the trained model using joblib.
    
    Args:
        model: Trained model object
        filepath (str): Path where to save the model
    """
    import joblib
    joblib.dump(model, filepath)
    print(f"Model saved to {filepath}")


def load_model(filepath="model_train.pkl"):
    """
    Load a trained model using joblib.
    
    Args:
        filepath (str): Path to the saved model
        
    Returns:
        Trained model object
    """
    import joblib
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Model file not found: {filepath}")
    
    model = joblib.load(filepath)
    return model 