#!/bin/bash
# Quick Start Script for Boot Not Suit Analysis Pipeline
# This script helps set up the project for GitHub Actions

set -e

echo "================================"
echo "Boot Not Suit Pipeline Setup"
echo "================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Not in the project root directory."
    echo "Please navigate to the project folder and try again."
    exit 1
fi

echo "✅ Found project files"
echo ""

# Initialize git repository
if [ ! -d ".git" ]; then
    echo "🔧 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already initialized"
fi

# Add all files
echo "🔧 Adding files to git..."
git add .
echo "✅ Files added"
echo ""

# Get repository URL
echo "Enter your GitHub repository URL (e.g., https://github.com/username/repo.git):"
read REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ Repository URL cannot be empty"
    exit 1
fi

# Add remote
echo "🔧 Adding remote repository..."
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"
echo "✅ Remote added: $REPO_URL"
echo ""

# Create initial commit
echo "🔧 Creating initial commit..."
git branch -M main
git commit -m "Initial commit: Boot Not Suit analysis pipeline" || true
echo "✅ Commit created"
echo ""

# Push to GitHub
echo "🔧 Pushing to GitHub..."
echo "Note: You may be prompted for authentication"
git push -u origin main

echo ""
echo "================================"
echo "✅ Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Go to GitHub: $REPO_URL"
echo "2. Click 'Actions' tab"
echo "3. Select 'Excel File Analysis Pipeline'"
echo "4. Click 'Run workflow'"
echo "5. Upload your Excel file and configure parameters"
echo ""
echo "For more information, see SETUP.md"
