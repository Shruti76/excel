# Quick Start: April Analysis Report Generation

## 📋 What You Get

Generated Report: **HT_Site_Visit_Calendar_April_2026.xlsx**

Contains:
- 1,764 unique sites analyzed
- 118 high-priority sites identified
- 40 PM team assignments analyzed
- Multi-week April schedule
- Comprehensive workload distribution

## 🚀 How to Use

### Option 1: Local Analysis (Fast)

```bash
# Navigate to project folder
cd /Users/shrutisohan/Desktop/excel

# Run analysis with 5 input files
python scripts/april_analysis.py \
  --site-master data/Colo_Sonatel-APS.xlsx \
  --hts-calendar data/HTS\ Site\ Visits\ Calendar\ March\ 26\ R0.xlsx \
  --pm-assignments data/PM_ZONE1_2_MARS_2026.xlsx \
  --project-sites data/Project\ sites\ BNS\ plan\ for\ March\ 2026.xlsx \
  --critical-sites data/RT\ High\ Risk\ List_of_sites_BE_failed\ 1.xlsx

# Report saved to: output/HT_Site_Visit_Calendar_April_2026.xlsx
```

### Option 2: GitHub Actions (Automated)

1. Go to: https://github.com/Shruti76/excel
2. Click **Actions** tab
3. Select **April Site Visit Calendar Generation**
4. Click **Run workflow**
5. Fill in 5 file names:
   - Colo_Sonatel-APS.xlsx
   - HTS Site Visits Calendar March 26 R0 (1).xlsx
   - PM_ZONE1_2_MARS_2026.xlsx
   - Project sites BNS plan for March 2026.xlsx
   - RT High Risk List_of_sites_BE_failed 1.xlsx
6. Click **Run workflow**
7. Wait ~1 minute for completion
8. Download report from **Artifacts**

## 📊 Report Contents

### Summary Sheet
- Total sites: 1,764
- Critical sites: (varies)
- PM workload: 40 assignments
- High priority: 118 sites
- Total hours: (calculated)

### April Schedule
- All sites organized by week
- Visit types: CRITICAL, PM, PROJECT, ROUTINE
- Priority levels: HIGH, MEDIUM, LOW
- Scheduled dates and team assignments

### High Priority Sites (Sheet 3)
- P0 and P1 critical sites
- 118 sites requiring immediate attention
- Required for risk management

### PM Workload (Sheet 4)
- Distribution across 40 team members
- Percentage workload per person
- For resource planning

### Analysis Log (Sheet 5)
- Complete processing history
- Error tracking
- Data validation results

## 🎯 Next Steps

After report generation:

1. **Review Summary** - Check total counts and distributions
2. **Prioritize High-Risk** - Focus on 118 critical sites
3. **Distribute Workload** - Use PM Workload sheet for team assignment
4. **Schedule Teams** - Use April Schedule sheet for planning
5. **Plan Resources** - Calculate required hours and personnel

## 📁 Input Files Explained

| File | Purpose | Records |
|------|---------|---------|
| Colo_Sonatel-APS.xlsx | Site master data | 54 sites |
| HTS Calendar | Historical visits | 55 planning entries |
| PM_ZONE1_2 | Preventive maintenance | 823 assignments |
| Project Sites | Project activities | 64 sites |
| RT High Risk | Critical sites | 132 sites |

## ✅ Sample Results

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

## 🆘 Troubleshooting

### "No module named pandas"
```bash
pip install pandas openpyxl numpy python-dateutil
```

### Files not found
- Ensure all 5 files are in `/Users/shrutisohan/Desktop/excel/data/`
- Check file names are exact (case-sensitive)

### Report is empty
- Check input files have data
- Review Analysis Log sheet for errors

## 📞 Support

For detailed information, see: `APRIL_ANALYSIS_GUIDE.md`

For original pipeline info, see: `README.md`

---

**Version:** 1.0
**Generated:** April 26, 2026
**Compatible Files:** All tested with March 2026 data
