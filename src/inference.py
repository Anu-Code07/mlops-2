#!/usr/bin/env python3
"""
Inference script for digit classification using trained model.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.metrics import accuracy_score, classification_report
from utils import load_model, load_digits_data


def main():
    """Main inference function."""
    print("Starting digit classification inference...")
    
    # Load the trained model
    try:
        model = load_model("model_train.pkl")
        print("Trained model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)
    
    # Load test data (using the same dataset for demonstration)
    try:
        X_train, X_test, y_train, y_test = load_digits_data()
        print(f"Test data loaded: {X_test.shape[0]} samples")
    except Exception as e:
        print(f"Error loading test data: {e}")
        sys.exit(1)
    
    # Make predictions
    try:
        y_pred = model.predict(X_test)
        print("Predictions generated successfully")
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Inference accuracy: {accuracy:.4f}")
        
        # Print detailed classification report
        print("\nInference Classification Report:")
        print(classification_report(y_test, y_pred))
        
        # Show some example predictions
        print("\nExample predictions (first 10 samples):")
        for i in range(min(10, len(y_test))):
            print(f"True: {y_test[i]}, Predicted: {y_pred[i]}")
            
    except Exception as e:
        print(f"Error during inference: {e}")
        sys.exit(1)
    
    print("Inference pipeline completed successfully!")


if __name__ == "__main__":
    main() 