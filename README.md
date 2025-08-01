# MLOps Artifact Pipeline

This repository contains a complete MLOps pipeline for digit classification using Logistic Regression and GitHub Actions.

## Project Overview

- **Dataset**: sklearn.datasets.load_digits (built-in)
- **Task**: Multiclass classification (digits 0-9)
- **Features**: 64 grayscale pixel values (flattened 8x8 images)
- **Model**: LogisticRegression from sklearn.linear_model

## Project Structure

```
.
├── src/
│   ├── train.py
│   ├── inference.py
│   └── utils.py
├── config/
│   └── config.json
├── tests/
│   └── test_train.py
├── .github/
│   └── workflows/
│       ├── train.yml
│       ├── test.yml
│       └── inference.yml
├── requirements.txt
└── README.md
```

## Branches

- `main`: Initial repository with README
- `classification`: Training pipeline implementation
- `test`: Testing with pytest
- `inference`: Multi-job workflow with inference

## Setup Instructions

1. Clone the repository
2. Create conda environment: `conda create -n mlops python=3.8`
3. Activate environment: `conda activate mlops`
4. Install dependencies: `pip install -r requirements.txt`

## Usage

- Training: `python src/train.py`
- Testing: `pytest tests/`
- Inference: `python src/inference.py`

## GitHub Actions

The repository includes three workflows:
- `train.yml`: Training pipeline with artifact upload
- `test.yml`: Test execution
- `inference.yml`: Multi-job workflow (test → train → inference) 