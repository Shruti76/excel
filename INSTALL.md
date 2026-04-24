# Installation & Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Setup](#local-setup)
3. [GitHub Repository Setup](#github-repository-setup)
4. [Pipeline Deployment](#pipeline-deployment)
5. [First Run](#first-run)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required
- **Git**: [Download](https://git-scm.com/downloads)
- **GitHub Account**: [Create free account](https://github.com/join)
- **Python 3.11+**: [Download](https://www.python.org/downloads/)
- **Excel file** with your data

### Optional (for local testing)
- **VS Code**: [Download](https://code.visualstudio.com/)
- **GitHub Desktop**: [Download](https://desktop.github.com/)

### System Requirements
- **macOS/Linux/Windows** with Bash or Zsh shell
- **2GB+ RAM** for processing
- **500MB+ disk space** for dependencies

## Local Setup

### Step 1: Clone or Download Project

**Option A: Using Git (Recommended)**

```bash
# Clone the repository
git clone https://github.com/yourusername/boot-not-suit-analysis.git
cd boot-not-suit-analysis
```

**Option B: Manual Download**

1. Download as ZIP from GitHub
2. Extract to your desired location
3. Open terminal and navigate to folder

### Step 2: Verify Project Structure

```bash
# List project files
ls -la

# Should see:
# .github/workflows/excel-analysis.yml
# scripts/
# requirements.txt
# README.md
# etc.
```

### Step 3: Install Python Dependencies (Local Testing)

```bash
# Create virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import pandas; print(pandas.__version__)"
```

### Step 4: Test Scripts Locally (Optional)

```bash
# Create sample Excel file
python create_sample.py

# Validate the sample
python scripts/validate_input.py --file data/sample_schedule.xlsx

# Run analysis
python scripts/main_analysis.py \
  --input data/sample_schedule.xlsx \
  --output data/output \
  --log data/output/analysis.log

# Check results
ls -la data/output/
```

## GitHub Repository Setup

### Step 1: Create GitHub Repository

**Method 1: Via GitHub Web UI**

1. Go to [github.com/new](https://github.com/new)
2. Fill in details:
   - **Repository name**: `boot-not-suit-analysis`
   - **Description**: Site Visit Schedule Analysis Pipeline
   - **Visibility**: Private (recommended) or Public
   - **Initialize**: Leave unchecked
3. Click **Create repository**
4. Copy the repository URL (HTTPS or SSH)

**Method 2: Using GitHub CLI**

```bash
# Login to GitHub (first time only)
gh auth login

# Create repository
gh repo create boot-not-suit-analysis \
  --private \
  --source=. \
  --remote=origin \
  --push
```

### Step 2: Initialize Git Locally

```bash
# Navigate to project folder
cd /Users/shrutisohan/Desktop/excel

# Initialize if not already a git repo
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Boot Not Suit analysis pipeline"
```

### Step 3: Connect to Remote Repository

```bash
# Add remote (replace with your URL)
git remote add origin https://github.com/yourusername/boot-not-suit-analysis.git

# Verify remote
git remote -v
# Should show:
# origin  https://github.com/yourusername/boot-not-suit-analysis.git (fetch)
# origin  https://github.com/yourusername/boot-not-suit-analysis.git (push)
```

### Step 4: Push to GitHub

```bash
# Push code to GitHub
git branch -M main
git push -u origin main

# Verify on GitHub (should see all files)
# Open browser: https://github.com/yourusername/boot-not-suit-analysis
```

## Pipeline Deployment

### Step 1: Verify Workflow Installation

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Should see **Excel File Analysis Pipeline** in the list
4. Click it to view workflow details

If not visible:
- Wait 1 minute for GitHub to process
- Refresh the page
- Check that `.github/workflows/excel-analysis.yml` exists

### Step 2: Set Up Repository Secrets (Optional)

For Slack or email notifications:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add secrets as needed:
   - `SLACK_WEBHOOK`: Slack webhook URL
   - `NOTIFICATION_EMAIL`: Email for notifications

### Step 3: Enable Actions (if needed)

1. Go to **Settings** → **Actions**
2. Ensure **Actions** is enabled for this repository
3. Should see "Allow all actions and reusable workflows"

### Step 4: Configure Workflow Parameters (Optional)

Edit `.github/workflows/excel-analysis.yml` to change defaults:

```yaml
months_back:
  default: '3'  # Change this value
  
exclude_critical_sites:
  default: true  # Change this value
```

Then commit and push:

```bash
git add .github/workflows/excel-analysis.yml
git commit -m "Update workflow defaults"
git push
```

## First Run

### Option 1: Upload File via GitHub Web UI

1. Go to your repository
2. Click **Add file** → **Upload files**
3. Upload your Excel file (e.g., `Colo_Sonatel-APS.xlsx`)
4. Click **Commit changes**
5. Go to **Actions** tab

### Option 2: Run Workflow Directly

1. Go to **Actions** tab
2. Click **Excel File Analysis Pipeline**
3. Click **Run workflow** button
4. Fill in parameters:
   - **excel_file**: Name of your uploaded Excel file
   - **analysis_type**: `full_schedule`
   - **exclude_critical_sites**: `true`
   - **months_back**: `3`
5. Click **Run workflow**

### Option 3: Upload + Run via Commands

```bash
# Copy your Excel file to the project
cp /path/to/your/Colo_Sonatel-APS.xlsx .

# Commit and push
git add Colo_Sonatel-APS.xlsx
git commit -m "Add Colo Sonatel schedule data"
git push

# Run workflow via GitHub CLI
gh workflow run excel-analysis.yml \
  -f excel_file="Colo_Sonatel-APS.xlsx" \
  -f analysis_type="full_schedule" \
  -f exclude_critical_sites="true" \
  -f months_back="3"
```

### Monitor Execution

1. Go to **Actions** tab
2. Click the running workflow
3. Watch logs in real-time
4. Each job shows progress with ✅ or ❌

### Download Results

1. Workflow should complete in 2-5 minutes
2. Scroll to **Artifacts** section
3. Download `analysis-results` folder
4. Extract and review files:
   - `final_report.xlsx` - Main report
   - `team_assignments.csv` - Team assignments
   - `sites_schedule.csv` - Processed sites
   - `*_log.txt` - Execution logs

## Troubleshooting

### Workflow Not Running

**Problem**: Workflow doesn't appear in Actions tab

**Solutions**:
1. Wait 2-3 minutes after pushing
2. Refresh GitHub page
3. Check that `.github/workflows/excel-analysis.yml` exists
4. Verify workflow file has no syntax errors

```bash
# Test workflow syntax locally (if github-cli is installed)
gh workflow view excel-analysis.yml
```

### File Not Found Error

**Problem**: `Error: File 'myfile.xlsx' not found`

**Solutions**:
1. Verify exact filename spelling
2. Ensure file is uploaded or committed to repo
3. Use absolute path if needed
4. Check file isn't in subdirectory

```bash
# Check if file exists
git ls-files | grep xlsx

# Upload file
git add myfile.xlsx
git push
```

### Python Package Errors

**Problem**: `ModuleNotFoundError: No module named 'pandas'`

**Solutions**:
1. Check `requirements.txt` has dependencies
2. Verify workflow installs packages
3. Test locally:

```bash
# Create fresh environment
rm -rf venv/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Invalid Excel Format

**Problem**: `Error: Unable to read Excel file`

**Solutions**:
1. Ensure file is valid Excel format (.xlsx)
2. Check all required sheets exist
3. Verify sheet names match expected names
4. Test file locally:

```bash
python scripts/validate_input.py --file yourfile.xlsx
```

### Out of Memory

**Problem**: `MemoryError: Unable to allocate memory`

**Solutions**:
1. Use GitHub's larger runner (requires paid plan)
2. Split large files into smaller pieces
3. Process in batches using scripts

### Artifacts Not Generated

**Problem**: No output files in Artifacts section

**Solutions**:
1. Check if workflow completed successfully (look for ✅)
2. If failed, check error logs in workflow run
3. Review validation report for data issues
4. Check output directory permissions

```bash
# View workflow logs
gh run view <run-id> --log
```

### Authentication Issues

**Problem**: `fatal: Authentication failed`

**Solutions**:
1. Create personal access token:
   - Go to GitHub → Settings → Developer settings → Personal access tokens
   - Generate new token with `repo` scope
   - Copy token
2. Use token for git operations:

```bash
# macOS/Linux: Store credentials
git config --global credential.helper osxkeychain
# Then use token when prompted

# Or use token in URL
git remote set-url origin https://<token>@github.com/username/repo.git
```

### Workflow Timeout

**Problem**: Workflow runs too long and times out (max 6 hours)

**Solutions**:
1. Optimize code to run faster
2. Process files in parallel
3. Use GitHub's faster runner (requires payment)

## Next Steps After Installation

1. ✅ Run first workflow with sample data
2. ✅ Review output format and structure
3. ✅ Customize Python scripts if needed
4. ✅ Set up notifications (Slack, email)
5. ✅ Create scheduled runs (optional)
6. ✅ Document your specific requirements

## Maintenance

### Regular Updates

```bash
# Check for updates to dependencies
pip list --outdated

# Update requirements.txt
pip install --upgrade pip
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt

# Commit changes
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### Monitor Workflows

1. Go to **Insights** → **Workflows**
2. Check success rate and execution times
3. Review logs for patterns

### Backup Results

```bash
# Download all artifacts
gh run download <run-id> -D backup/

# Or download via GitHub UI and save locally
```

## Uninstallation

If you need to remove:

```bash
# Delete local repository
rm -rf /Users/shrutisohan/Desktop/excel

# Or delete GitHub repository:
# 1. Go to Settings → General → Danger Zone
# 2. Click "Delete this repository"
# 3. Confirm
```

## Support Resources

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Python Pandas Docs**: https://pandas.pydata.org/docs/
- **GitHub CLI Help**: `gh help`
- **Project README**: See README.md
- **API Documentation**: See API.md

---

**Congratulations!** Your pipeline is now deployed and ready to use! 🎉

**Questions?** Review SETUP.md for quick start or README.md for detailed documentation.
