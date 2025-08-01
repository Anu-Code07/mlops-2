#!/bin/bash

# MLOps Assignment 2 - Repository Setup Script
# This script helps set up the Git repository with the required branching structure

echo "🚀 Setting up MLOps Assignment 2 Repository"
echo "=========================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Initialize git repository (if not already initialized)
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
else
    echo "✅ Git repository already initialized"
fi

# Add all files to git
echo "📝 Adding files to Git..."
git add .

# Make initial commit
echo "💾 Making initial commit..."
git commit -m "Initial commit: MLOps Assignment 2 setup"

# Create the required branches as per assignment guidelines
echo "🌿 Creating branches following assignment guidelines..."

# Create classification branch from main
echo "Creating classification branch..."
git checkout -b classification
git push -u origin classification

# Create test branch from classification
echo "Creating test branch from classification..."
git checkout -b test
git push -u origin test

# Create inference branch from test
echo "Creating inference branch from test..."
git checkout -b inference
git push -u origin inference

# Go back to main branch
git checkout main

echo ""
echo "✅ Repository setup completed!"
echo ""
echo "📋 Branch Structure Created:"
echo "   main → classification → test → inference"
echo ""
echo "🔗 Next Steps:"
echo "   1. Push to your GitHub repository:"
echo "      git remote add origin https://github.com/Anu-Code07/mlops-2.git"
echo "      git push -u origin main"
echo ""
echo "   2. Work on each phase in the correct branch:"
echo "      - Phase 1 (Training): classification branch"
echo "      - Phase 2 (Testing): test branch"
echo "      - Phase 3 (Inference): inference branch"
echo ""
echo "   3. Each branch builds upon the previous one without merging back to main"
echo ""
echo "🎯 Remember: Don't merge branches back to main as per assignment requirements!" 