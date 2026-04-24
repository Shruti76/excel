# GitHub Actions Setup Guide

## Quick Start (5 minutes)

### Step 1: Create a GitHub Repository

1. Go to [github.com](https://github.com)
2. Click **"New"** button to create a new repository
3. Enter repository name: `boot-not-suit-analysis` (or your preferred name)
4. Choose **Public** or **Private** (depending on your needs)
5. Click **"Create repository"**

### Step 2: Initialize Git Locally

```bash
# Navigate to your excel folder
cd /Users/shrutisohan/Desktop/excel

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Boot Not Suit analysis pipeline"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/boot-not-suit-analysis.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Enable GitHub Actions

The workflow file is already in `.github/workflows/excel-analysis.yml`. Actions are enabled by default.

To verify:
1. Go to your repository on GitHub
2. Click **"Actions"** tab
3. You should see "Excel File Analysis Pipeline" listed

## Running the Pipeline

### Method 1: Via Web UI (Easiest)

1. Go to your repository → **Actions** tab
2. Click **"Excel File Analysis Pipeline"** on the left
3. Click **"Run workflow"** button
4. Fill in parameters:
   - **excel_file**: Your Excel filename (e.g., `Colo_Sonatel-APS.xlsx`)
   - **analysis_type**: `full_schedule`
   - **exclude_critical_sites**: `true`
   - **months_back**: `3`
5. Click **"Run workflow"**
6. Monitor the execution in real-time

### Method 2: Via GitHub CLI

```bash
# Install GitHub CLI if not already installed
brew install gh

# Authenticate with GitHub
gh auth login

# Run the workflow
gh workflow run excel-analysis.yml \
  -f excel_file="sample_schedule.xlsx" \
  -f analysis_type="full_schedule" \
  -f exclude_critical_sites="true" \
  -f months_back="3"
```

### Method 3: Upload Excel File via Web UI

1. Go to repository → **"Add file"** → **"Upload files"**
2. Upload your Excel file
3. Commit to main branch
4. Go to **Actions** → Run workflow with your filename

## Viewing Results

### During Execution
1. Click on the workflow run to see real-time logs
2. Each job shows:
   - ✅ Validation results
   - ✅ Analysis progress
   - ✅ Team assignments
   - ✅ Report generation

### After Completion
1. Scroll to **"Artifacts"** section
2. Download:
   - `analysis-results` (all output files)
   - Includes CSV files and Excel report

## File Structure on GitHub

```
boot-not-suit-analysis/
├── .github/
│   └── workflows/
│       └── excel-analysis.yml
├── scripts/
│   ├── validate_input.py
│   ├── main_analysis.py
│   ├── team_assignment.py
│   └── generate_report.py
├── data/
│   ├── sample_schedule.xlsx
│   └── uploads/          # For uploaded files
├── output/               # Generated results
├── requirements.txt
├── README.md
└── SETUP.md
```

## Troubleshooting

### 401 Unauthorized Error
- Run: `gh auth login`
- Select HTTPS
- Generate personal access token at github.com/settings/tokens

### Workflow Not Appearing
- Ensure `.github/workflows/excel-analysis.yml` exists
- Commit and push the file
- Wait 1 minute and refresh the Actions page

### Artifacts Not Showing
- Check if workflow completed (look for ✅ checkmark)
- If failed, click on the failed job to see error logs

### "No Excel file uploaded"
- Use exact filename in workflow input
- File should be in repository root or `data/uploads/` folder

## Local Testing (Optional)

### Test Validation Script

```bash
# Navigate to project
cd /Users/shrutisohan/Desktop/excel

# Install dependencies
pip install -r requirements.txt

# Run validation
python scripts/validate_input.py --file data/sample_schedule.xlsx

# View output
cat data/output/validation_report.txt
```

### Test Analysis Script

```bash
# Run main analysis
python scripts/main_analysis.py \
  --input data/sample_schedule.xlsx \
  --output data/output \
  --exclude-critical true \
  --months-back 3

# Check results
ls -la data/output/
```

## Customization

### Change Workflow Trigger

Edit `.github/workflows/excel-analysis.yml`:

```yaml
# To run on schedule (daily at 9 AM UTC)
on:
  schedule:
    - cron: '0 9 * * *'
  workflow_dispatch:  # Keep manual trigger too
```

### Add Slack Notifications

Add to workflow after `notify` job:

```yaml
- name: Notify Slack
  if: always()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
```

Then add secret in GitHub:
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Name: `SLACK_WEBHOOK`
4. Value: Your Slack webhook URL

### Email Notifications

GitHub automatically sends email when:
- Workflow fails
- You're watching the repository
- You're part of the organization

## Performance & Costs

### Free Tier Includes
- 2,000 minutes per month for workflow runs
- Unlimited storage for artifacts (30 day retention)
- Unlimited public repositories

### Estimated Usage Per Run
- **Validation**: 10-15 seconds
- **Analysis**: 30-90 seconds
- **Team Assignment**: 20-30 seconds
- **Report Generation**: 10-15 seconds
- **Total**: ~2-3 minutes per execution

## Advanced Configuration

### Increase Retention Period

Edit workflow to keep artifacts longer:

```yaml
- name: Upload analysis results
  uses: actions/upload-artifact@v3
  with:
    name: analysis-results
    path: data/output/
    retention-days: 90  # Change from 30
```

### Run on Specific Schedule

```yaml
on:
  schedule:
    - cron: '0 8 * * MON'  # Every Monday at 8 AM UTC
```

### Add Code Review Check

```yaml
- name: Validate outputs
  run: |
    if [ ! -f data/output/final_report.xlsx ]; then
      echo "❌ Report not generated"
      exit 1
    fi
```

## Next Steps

1. ✅ Push to GitHub
2. ✅ Run first workflow
3. ✅ Download results
4. ✅ Review output format
5. ✅ Customize as needed
6. ✅ Set up integrations (Slack, email, etc.)

## Support

For issues:
1. Check workflow logs in GitHub Actions
2. Review error messages in artifacts
3. Verify Excel file format
4. Check Python script logs

---

**Ready to get started?**
1. Push this code to GitHub
2. Go to Actions tab
3. Click "Run workflow"
4. Monitor execution
5. Download results!
