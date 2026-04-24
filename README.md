# Boot Not Suit - Site Visit Schedule Pipeline

Automated pipeline for generating monthly site visit schedules using GitHub Actions and Python analysis.

## Overview

This pipeline implements the "Boot Not Suit" site visit program workflow with 8 key steps:

1. **Receipt of schedules** - Maintenance and project activities
2. **Receipt of exceptions** - Non-maintenance activities and department requests
3. **Exclude recent visits** - Remove sites visited in last N months
4. **Exclude critical sites** - Remove high-risk rooftop sites
5. **Harmonize activities** - Create unified list of all activities
6. **Assign to teams** - Select sites and assign to team members (2 per person, 4 per influencer)
7. **Form teams** - Create pairs/trios with technical and non-technical staff
8. **Set time limits** - Define visit timelines based on activity type

## Project Structure

```
excel/
├── .github/
│   └── workflows/
│       └── excel-analysis.yml          # GitHub Actions workflow
├── scripts/
│   ├── validate_input.py               # Input validation
│   ├── main_analysis.py                # Core schedule generation (Steps 1-6)
│   ├── team_assignment.py              # Team formation (Steps 7-8)
│   └── generate_report.py              # Final report generation
├── data/
│   └── uploads/                        # Input Excel files (populated by workflow)
├── output/                             # Generated reports and CSVs
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## Required Excel File Format

Your input Excel file should contain the following sheets:

### Sheet 1: maintenance
Required columns:
- `site_id` - Unique site identifier
- `site_name` - Site name
- `nearest_hi` - Nearest Hi (numeric)
- `tower_type` - Type of tower (e.g., 'Rooftop', 'Greenfield')
- `activity_type` - Type of activity (should be 'maintenance')
- Additional columns as per your data

### Sheet 2: project
Required columns:
- `site_id` - Unique site identifier
- `site_name` - Site name
- `project_name` - Name of project
- `department` - Department name
- Additional columns as per your data

### Sheet 3: visit_history (Optional)
Required columns:
- `site_id` - Site that was visited
- `visit_date` - Date of visit (YYYY-MM-DD format)
- `team_member` - Team member who visited

### Sheet 4: critical_sites (Optional)
Required columns:
- `site_id` - Site identifier
- `site_name` - Site name
- `tower_type` - Type of tower
- `risk_level` - Risk level (e.g., 'high', 'medium', 'low')
- `reason` - Reason for being critical

## Installation

### Prerequisites
- Git repository on GitHub
- Python 3.11+
- GitHub Actions enabled on your repository

### Setup Steps

1. **Clone your repository locally** (or create a new one):
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Copy project files**:
   ```bash
   # Copy all files from this project to your repo
   cp -r .github/ scripts/ data/ requirements.txt README.md .
   ```

3. **Commit and push to GitHub**:
   ```bash
   git add .
   git commit -m "Add Boot Not Suit analysis pipeline"
   git push origin main
   ```

## Usage

### Via GitHub Actions UI

1. **Go to your repository on GitHub**
2. **Click "Actions" tab**
3. **Select "Excel File Analysis Pipeline" workflow**
4. **Click "Run workflow" button**
5. **Fill in the parameters**:
   - **excel_file**: Name of your Excel file (e.g., `Colo_Sonatel-APS.xlsx`)
   - **analysis_type**: Choose one:
     - `full_schedule` - Complete analysis with all 8 steps
     - `validate_data` - Only validate input data
     - `team_assignment` - Only generate team assignments
     - `site_exclusion` - Only perform site filtering
   - **exclude_critical_sites**: Toggle to exclude high-risk rooftop sites
   - **months_back**: Number of months to look back for recent visits (default: 3)
6. **Click "Run workflow"**

### Via GitHub CLI

```bash
# List workflows
gh workflow list

# Run workflow with parameters
gh workflow run excel-analysis.yml \
  -f excel_file="Colo_Sonatel-APS.xlsx" \
  -f analysis_type="full_schedule" \
  -f exclude_critical_sites="true" \
  -f months_back="3"
```

## Pipeline Steps Explained

### Step 1-2: Data Loading
Loads maintenance and project activities from Excel file.

### Step 3: Exclude Recent Visits
Filters out sites that have been visited within the specified number of months (default: 3 months).

### Step 4: Exclude Critical Sites
Removes high-risk rooftop sites from the critical sites list to ensure team safety.

### Step 5: Harmonize Activities
Creates a unified list combining maintenance, project, and other department activities.

### Step 6: Assign Sites to Teams
- Selects sites based on available activities
- Assigns 2 sites per team member
- Assigns 4 sites per safety influencer

### Step 7: Form Teams
- Creates pairs or trios
- Pairs technical leads with non-technical resources
- Rotates team composition monthly for variety

### Step 8: Set Time Limits
- Maintenance activities: Use original schedule time limits
- Project activities: Mark as "TBC" (To Be Confirmed) for team coordination

## Output Files

After successful pipeline execution, the following files are generated:

### 1. **sites_schedule.csv**
Contains the filtered and processed list of sites ready for team assignment.

**Columns**:
- site_id
- site_name
- activity_type
- assigned
- assigned_date

### 2. **team_assignments.csv**
Contains complete team assignments with site details.

**Columns**:
- site_id
- site_name
- team_id
- technical_lead
- non_technical_members
- activity_type
- time_limit
- assigned_date

### 3. **team_assignments_summary.csv**
Summary of teams and their workload.

**Columns**:
- team_id
- sites_assigned
- technical_lead
- non_technical_members
- activity_type

### 4. **final_report.xlsx**
Comprehensive Excel report with multiple sheets:
- **Summary**: Report metadata
- **Sites Schedule**: Processed sites list
- **Team Assignments**: Detailed assignments
- **Team Summary**: Team workload overview
- **Analysis Log**: Complete execution log

### 5. **validation_report.txt**
Input validation results and data quality checks.

### 6. **analysis_log.txt**
Detailed execution log of all analysis steps.

## Accessing Results

### During Workflow Execution
1. Go to Actions → Workflow Run
2. Scroll to "Artifacts" section
3. Download desired files

### After Workflow Completion
Files are automatically retained for 30 days in GitHub Actions artifacts.

## Customization

### Modify Analysis Parameters

Edit `.github/workflows/excel-analysis.yml` to change defaults:

```yaml
months_back:
  description: 'Exclude sites visited in last N months'
  required: false
  type: string
  default: '3'  # Change this value
```

### Add Additional Validation Rules

Edit `scripts/validate_input.py` to add custom validation logic:

```python
def validate_custom_rules(df):
    # Add your validation logic here
    pass
```

### Extend Analysis Logic

Edit `scripts/main_analysis.py` to add new steps or modify existing ones.

### Change Team Formation Rules

Edit `scripts/team_assignment.py` to modify:
- Sites per person (default: 2)
- Sites per influencer (default: 4)
- Team composition logic

## Troubleshooting

### Workflow Fails with "File not found"
**Solution**: Ensure the Excel filename in the workflow input matches exactly with your file, including extension.

### "Missing columns" Validation Error
**Solution**: Check that your Excel sheets have the required column names (case-sensitive).

### No output files generated
**Solution**: 
1. Check validation report for data quality issues
2. Ensure input Excel file has data in all required sheets
3. Review analysis log for specific errors

### Memory issues with large files
**Solution**: Split large Excel files into multiple runs or increase GitHub Actions runner memory (requires larger runner).

## Dependencies

- **pandas**: Data manipulation and analysis
- **openpyxl**: Excel file writing
- **numpy**: Numerical operations
- **python-dateutil**: Date parsing and manipulation

All dependencies are automatically installed by the workflow.

## Performance

- **Small files** (< 10,000 sites): < 1 minute
- **Medium files** (10,000 - 50,000 sites): 1-5 minutes
- **Large files** (> 50,000 sites): 5-15 minutes

## Cost

GitHub Actions provides:
- **Free tier**: 2,000 workflow run minutes per month for public repos
- **Paid tier**: Additional minutes available

This pipeline uses approximately 2-5 minutes per execution on standard runners.

## Best Practices

1. **Data Quality**: Ensure input Excel files are clean and complete
2. **Date Format**: Use YYYY-MM-DD format for all date fields
3. **Site IDs**: Keep site IDs unique and consistent
4. **Version Control**: Commit input Excel files to track changes
5. **Backup**: Keep copies of output reports for compliance

## Example Workflow

```
1. Prepare Excel file with maintenance and project schedules
2. Push to GitHub repository or upload via Actions UI
3. Run workflow with desired parameters
4. Download generated reports
5. Review team assignments and validate against constraints
6. Export final schedule to deployment system
```

## Support & Maintenance

### Updating Python Packages
Update `requirements.txt` with newer versions:
```bash
pip install --upgrade pandas openpyxl numpy
pip freeze > requirements.txt
```

### Monitoring Workflow Health
- Check GitHub Actions logs for each run
- Review workflow statistics in "Insights" → "Workflows"

## License

This project is provided as-is for internal use.

## Contact & Questions

For issues or improvements, contact the development team or create a GitHub issue in your repository.

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Production Ready
