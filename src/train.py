#!/usr/bin/env python3
"""
Training script for digit classification using Logistic Regression.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from utils import load_config, load_digits_data, save_model


def train_model(X_train, y_train, config):
    """
    Train a Logistic Regression model with given configuration.
    
    Args:
        X_train: Training features
        y_train: Training labels
        config (dict): Model configuration
        
    Returns:
        LogisticRegression: Trained model
    """
    model = LogisticRegression(
        C=config['C'],
        solver=config['solver'],
        max_iter=config['max_iter'],
        random_state=config['random_state']
    )
    
    model.fit(X_train, y_train)
    return model


def main():
    """Main training function."""
    print("Starting digit classification training...")
    
    # Load configuration
    try:
        config = load_config()
        print("Configuration loaded successfully")
        print(f"Hyperparameters: C={config['C']}, solver={config['solver']}, max_iter={config['max_iter']}")
    except Exception as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)
    
    # Load and split data
    try:
        X_train, X_test, y_train, y_test = load_digits_data(
            test_size=config['test_size'],
            random_state=config['random_state']
        )
        print(f"Data loaded: {X_train.shape[0]} training samples, {X_test.shape[0]} test samples")
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)
    
    # Train model
    try:
        model = train_model(X_train, y_train, config)
        print("Model training completed successfully")
    except Exception as e:
        print(f"Error training model: {e}")
        sys.exit(1)
    
    # Evaluate model
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {accuracy:.4f}")
        
        # Print detailed classification report
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Check if accuracy meets threshold
        if accuracy >= config['accuracy_threshold']:
            print(f"✓ Accuracy ({accuracy:.4f}) meets threshold ({config['accuracy_threshold']})")
        else:
            print(f"⚠ Accuracy ({accuracy:.4f}) below threshold ({config['accuracy_threshold']})")
            
    except Exception as e:
        print(f"Error evaluating model: {e}")
        sys.exit(1)
    
    # Save model
    try:
        save_model(model, "model_train.pkl")
        print("Training pipeline completed successfully!")
    except Exception as e:
        print(f"Error saving model: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 