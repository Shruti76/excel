# April Site Visit Calendar Analysis

## Overview

This script analyzes 5 types of Excel files and generates a comprehensive April site visit calendar report.

## Input File Types

### 1. Site Master File
**Example:** `Colo_Sonatel-APS.xlsx`
- Contains master site data
- Columns: Site ID, Site Name, Site Type, Project
- Used for: Site identification and consolidation

### 2. HTS Calendar File
**Example:** `HTS Site Visits Calendar March 26 R0.xlsx`
- Sheet: "Planning"
- Contains historical visit planning data
- Used for: Historical visit context

### 3. PM Assignments File
**Example:** `PM_ZONE1_2_MARS_2026.xlsx`
- Columns: YAS SID, HTS SID, Assigned to, Planning Date
- 823 preventive maintenance records
- Used for: PM workload distribution

### 4. Project Sites File
**Example:** `Project sites BNS plan for March 2026.xlsx`
- Sheet: "Mars sites"
- 64 project-based sites
- Used for: Project activity identification

### 5. Critical Sites File
**Example:** `RT High Risk List_of_sites_BE_failed 1.xlsx`
- Sheet: "Failed sites"
- 132 critical/high-risk sites
- Columns: Site ID, Site name, Priority (P0/P1/P2)
- Used for: Priority-based scheduling

## Output Report Format

**File Name:** `HT_Site_Visit_Calendar_April_2026.xlsx`

### Sheet 1: Summary
- Report date: April 2026
- Total sites scheduled: 1764
- Breakdown by visit type:
  - Critical sites
  - PM sites
  - Project sites
  - Routine sites
- High priority count
- Total PM hours

### Sheet 2: April Schedule
- Site ID
- Visit Type (CRITICAL, PM, PROJECT, ROUTINE)
- Priority (HIGH, MEDIUM, LOW)
- Scheduled Week (Week 1-4)
- Target Date
- Status
- Team (for assignment)
- Duration (hours)

### Sheet 3: High Priority Sites
- Top 50 priority sites requiring immediate attention
- From critical sites list (P0/P1 priority)
- 118 high priority sites identified

### Sheet 4: PM Workload
- Assignment distribution by PM zone
- Count of sites per assignee
- Percentage distribution
- 40 unique assignments

### Sheet 5: Analysis Log
- Complete execution log with timestamps
- All processing steps documented

## Usage

### Local Usage

```bash
python scripts/april_analysis.py \
  --site-master data/Colo_Sonatel-APS.xlsx \
  --hts-calendar data/HTS\ Site\ Visits\ Calendar\ March\ 26\ R0.xlsx \
  --pm-assignments data/PM_ZONE1_2_MARS_2026.xlsx \
  --project-sites data/Project\ sites\ BNS\ plan\ for\ March\ 2026.xlsx \
  --critical-sites data/RT\ High\ Risk\ List_of_sites_BE_failed\ 1.xlsx \
  --output output \
  --report-name HT_Site_Visit_Calendar_April_2026.xlsx
```

### GitHub Actions Workflow

1. Go to **Actions** tab in GitHub
2. Select **April Site Visit Calendar Generation**
3. Click **Run workflow**
4. Enter file names for each input (they should be in data folder)
5. Click **Run workflow**
6. Wait for completion
7. Download report from **Artifacts**

## Key Metrics Generated

| Metric | Value | Description |
|--------|-------|-------------|
| Total Sites | 1764 | All unique sites across 5 files |
| Critical Sites | TBD | From high-risk/failed sites list |
| PM Sites | TBD | Preventive maintenance assignments |
| Project Sites | 64 | Project-based site activities |
| High Priority | 118 | Sites marked P0/P1 |
| PM Hours | TBD | Total hours required |
| Assignments | 40 | Unique PM team members |

## Analysis Process

1. **Load Data**: Read all 5 Excel files
2. **Extract Site IDs**: Consolidate unique sites from all sources
3. **Visit Type Assignment**: Classify visits as CRITICAL/PM/PROJECT/ROUTINE
4. **Priority Assignment**: Mark based on critical site list
5. **Schedule Distribution**: Distribute across 4 weeks of April
6. **Workload Analysis**: Analyze PM assignments and distribution
7. **Report Generation**: Create multi-sheet Excel report

## Error Handling

If any file is missing or malformed:
- Remaining files are still processed
- Report includes data from available sources
- Error messages logged in Analysis Log sheet

## Sample Output Statistics

```
Starting April Site Visit Analysis...
✅ Loaded Site Master: 54 sites
✅ Loaded HTS Calendar: (55, 16233)
✅ Loaded PM Assignments: 823 records
✅ Loaded Project Sites: 64 sites
✅ Loaded Critical Sites: 132 sites
📊 Total unique sites identified: 1764
✅ April schedule generated: 1764 visits
✅ High priority sites identified: 118
✅ Summary statistics created
✅ PM workload analysis: 40 assignments
✅ Report saved: HT_Site_Visit_Calendar_April_2026.xlsx
```

## Technical Details

- **Language:** Python 3.11
- **Key Libraries:**
  - pandas: Data manipulation and Excel I/O
  - openpyxl: Excel file generation
  - numpy: Numerical operations
  - python-dateutil: Date handling

- **Report Format:** Excel (.xlsx) with multiple worksheets
- **Color Scheme:**
  - Headers: Blue (#1F4E78, #4472C4)
  - Subheaders: Light blue (#D9E1F2)

## Troubleshooting

### File Not Found
- Ensure all 5 files are in the `data/` folder
- Check file names match exactly (case-sensitive)

### Memory Issues (Large Files)
- HTS Calendar can have many columns (16,233 in sample)
- Script handles this automatically
- May take 1-2 minutes to process

### Empty Report
- Check that at least one input file contains data
- Review Analysis Log sheet for error messages

## Future Enhancements

- [ ] Add team assignment optimization
- [ ] Include resource availability constraints
- [ ] Add weather impact filtering
- [ ] Generate individual team schedules
- [ ] Add email notifications
- [ ] Support multiple months
- [ ] Add site visit history tracking
- [ ] Implement risk scoring

---

**Last Updated:** April 26, 2026
**Report Version:** 1.0
