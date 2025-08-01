# MLOps Assignment 2 - Complete Implementation Guide

## Overview

This repository contains a complete implementation of the MLOps Assignment 2, which builds a digit classification pipeline using Logistic Regression and GitHub Actions for CI/CD.

## Project Structure

```
mlops-assigment/
├── src/
│   ├── train.py          # Training script
│   ├── inference.py      # Inference script
│   └── utils.py          # Utility functions
├── config/
│   └── config.json       # Model hyperparameters
├── tests/
│   └── test_train.py     # Unit tests
├── .github/
│   └── workflows/
│       ├── train.yml     # Training workflow
│       ├── test.yml      # Testing workflow
│       └── inference.yml # Multi-job inference workflow
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── setup_repository.sh  # Repository setup script
└── ASSIGNMENT_GUIDE.md  # This file
```

## Implementation Details

### Phase 1: Training Pipeline (classification branch)

**Files Implemented:**
- `src/train.py`: Main training script
- `src/utils.py`: Utility functions for data loading and model persistence
- `config/config.json`: Configuration file with hyperparameters
- `.github/workflows/train.yml`: GitHub Actions workflow for training

**Key Features:**
- Loads digits dataset from sklearn
- Reads hyperparameters from JSON config file
- Trains LogisticRegression model with configurable parameters
- Saves model as `model_train.pkl` using joblib
- Uploads model as GitHub artifact
- Comprehensive error handling and logging

**Configuration Parameters:**
```json
{
    "C": 1.0,                    // Inverse regularization strength
    "solver": "lbfgs",           // Optimization algorithm
    "max_iter": 1000,            // Maximum iterations
    "random_state": 42,          // Random seed for reproducibility
    "test_size": 0.2,            // Test set proportion
    "accuracy_threshold": 0.9    // Minimum accuracy threshold
}
```

### Phase 2: Testing Pipeline (test branch)

**Files Implemented:**
- `tests/test_train.py`: Comprehensive unit tests
- `.github/workflows/test.yml`: GitHub Actions workflow for testing

**Test Coverage:**
1. **Configuration Tests:**
   - Config file loading and validation
   - Required hyperparameter existence
   - Data type validation
   - Value range validation

2. **Data Loading Tests:**
   - Digits dataset loading
   - Data split consistency
   - Feature and label validation

3. **Model Creation Tests:**
   - Model object type validation
   - Hyperparameter application
   - Model fitting verification

4. **Model Performance Tests:**
   - Accuracy threshold validation
   - Reasonable performance checks

5. **Model Persistence Tests:**
   - Save/load functionality
   - Prediction consistency

### Phase 3: Inference Pipeline (inference branch)

**Files Implemented:**
- `src/inference.py`: Inference script
- `.github/workflows/inference.yml`: Multi-job workflow

**Multi-Job Workflow Structure:**
1. **Test Cases Job:** Runs all unit tests
2. **Train Job:** Trains model and uploads artifact (depends on test-cases)
3. **Inference Job:** Downloads model and runs inference (depends on train)

**Job Dependencies:**
- Uses `needs` parameter for proper job chaining
- Artifacts passed between jobs using `actions/upload-artifact` and `actions/download-artifact`

## Setup Instructions

### 1. Local Development Setup

```bash
# Create conda environment
conda create -n mlops python=3.8
conda activate mlops

# Install dependencies
pip install -r requirements.txt
```

### 2. Repository Setup

```bash
# Run the setup script
./setup_repository.sh

# Or manually set up Git repository
git init
git add .
git commit -m "Initial commit: MLOps Assignment 2 setup"

# Add remote repository
git remote add origin https://github.com/Anu-Code07/mlops-2.git

# Create branches as per assignment
git checkout -b classification
git checkout -b test
git checkout -b inference
```

### 3. Branching Strategy

**Important:** Follow the linear branching approach as specified in the assignment:

```
main → classification → test → inference
```

- **DO NOT** merge branches back to main
- Each branch builds upon the previous one
- Work on each phase in the correct branch

## Testing Locally

### Run Training
```bash
python src/train.py
```

### Run Tests
```bash
pytest tests/ -v
```

### Run Inference
```bash
python src/inference.py
```

## GitHub Actions Workflows

### 1. Training Workflow (`train.yml`)
- **Trigger:** Push/PR to `classification` branch
- **Actions:**
  - Setup Python 3.8
  - Install dependencies
  - Run training script
  - Upload model as artifact

### 2. Testing Workflow (`test.yml`)
- **Trigger:** Push/PR to `test` branch
- **Actions:**
  - Setup Python 3.8
  - Install dependencies
  - Run pytest with verbose output

### 3. Inference Workflow (`inference.yml`)
- **Trigger:** Push/PR to `inference` branch
- **Jobs:**
  - `test-cases`: Run unit tests
  - `train`: Train model (depends on test-cases)
  - `inference`: Run inference (depends on train)

## Performance Metrics

The implementation includes comprehensive performance tracking:

- **Accuracy Score:** Primary metric for model evaluation
- **Classification Report:** Detailed per-class performance
- **Accuracy Threshold:** Configurable minimum performance requirement
- **Loss Tracking:** Training progress monitoring

## Key Features

### 1. Modularity
- Separate modules for training, inference, and utilities
- Clean separation of concerns
- Reusable components

### 2. Configuration Management
- JSON-based configuration
- No hardcoded values
- Easy parameter tuning

### 3. Error Handling
- Comprehensive exception handling
- Meaningful error messages
- Graceful failure handling

### 4. Reproducibility
- Fixed random seeds
- Versioned dependencies
- Consistent data splits

### 5. CI/CD Integration
- Automated testing
- Model artifact management
- Multi-job workflows

## Assignment Requirements Checklist

- ✅ **Repository Setup:** Public GitHub repository with proper structure
- ✅ **Training Pipeline:** Complete implementation with config file
- ✅ **Testing:** Comprehensive unit tests with pytest
- ✅ **GitHub Actions:** All three workflows implemented
- ✅ **Artifact Management:** Model upload/download between jobs
- ✅ **Job Dependencies:** Proper use of `needs` parameter
- ✅ **Branching Strategy:** Linear approach without merging to main
- ✅ **Documentation:** Comprehensive README and guides

## Performance Analysis

The Logistic Regression model typically achieves:
- **Accuracy:** 95-98% on the digits dataset
- **Training Time:** < 30 seconds
- **Memory Usage:** < 100MB
- **Model Size:** < 1MB

## Troubleshooting

### Common Issues:

1. **Import Errors:** Ensure you're in the correct directory and Python path is set
2. **Config File Not Found:** Check that `config/config.json` exists
3. **Model File Not Found:** Ensure training has been run first
4. **GitHub Actions Failures:** Check workflow syntax and dependencies

### Debug Commands:

```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Verify config file
python -c "from src.utils import load_config; print(load_config())"

# Test data loading
python -c "from src.utils import load_digits_data; print(load_digits_data()[0].shape)"
```

## Submission Notes

1. **Repository Visibility:** Make public after deadline
2. **Branch Preservation:** Don't delete any branches
3. **Documentation:** Include comprehensive analysis in report
4. **Screenshots:** Capture command-line interactions and GitHub workflows
5. **Performance Comparison:** Include accuracy/F1-score analysis

This implementation provides a complete, production-ready MLOps pipeline that demonstrates best practices in machine learning operations, continuous integration, and deployment automation. 