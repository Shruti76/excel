# Visual Guide & Architecture

## 🎨 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GITHUB REPOSITORY                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              GitHub Actions Workflow                │   │
│  │         (Triggered via Actions Tab)                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ↓                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Job 1: SETUP                                        │   │
│  │  • Initialize directories                           │   │
│  │  • Set environment variables                        │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ↓                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Job 2: VALIDATE            Job 3: ANALYZE           │   │
│  │  • Check Excel format       • Load data (Step 1-2)  │   │
│  │  • Verify columns           • Filter recent (Step 3)│   │
│  │  • Check data types         • Filter critical (Step 4)│  │
│  └──────────────────────────────────────────────────────┘   │
│                          ↓                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Job 4: TEAM FORMATION                               │   │
│  │  • Harmonize activities (Step 5)                     │   │
│  │  • Form teams (Steps 6-7)                           │   │
│  │  • Set timelines (Step 8)                           │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ↓                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Job 5: UPLOAD & NOTIFY                              │   │
│  │  • Save artifacts (30-day retention)                │   │
│  │  • Generate summary report                          │   │
│  │  • Create GitHub release                            │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ↓                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  ARTIFACTS (Ready to Download)                       │   │
│  │  • final_report.xlsx                                │   │
│  │  • team_assignments.csv                             │   │
│  │  • sites_schedule.csv                               │   │
│  │  • *.log (execution logs)                           │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow Diagram

```
INPUT EXCEL FILE
├── Sheet: maintenance (500 rows)
│   └─ site_id, site_name, activity_type, ...
├── Sheet: project (300 rows)
│   └─ site_id, site_name, project_name, ...
├── Sheet: visit_history (150 rows)
│   └─ site_id, visit_date, team_member
└── Sheet: critical_sites (50 rows)
    └─ site_id, risk_level, reason

                    ↓ VALIDATION
        ✓ All sheets present?
        ✓ All columns exist?
        ✓ Data format valid?
        ✓ No null values?

                    ↓ LOADING (Step 1-2)
        → Load 500 maintenance sites
        → Load 300 project sites
        → Combine: 800 total activities

                    ↓ STEP 3: FILTER RECENT
        → Check visit_history
        → Remove 50 recently visited
        → Result: 750 sites available

                    ↓ STEP 4: FILTER CRITICAL
        → Check critical_sites list
        → Remove 30 high-risk rooftop
        → Result: 720 sites available

                    ↓ STEP 5: HARMONIZE
        → Combine maintenance & projects
        → Add metadata
        → Result: 720 harmonized activities

                    ↓ STEP 6: ASSIGN TEAMS
        → Group by team (20 teams × 2)
        → 2 sites per person
        → Result: 40 people, 720 sites

                    ↓ STEP 7: FORM TEAMS
        → Create 20 teams
        → Technical lead + non-technical
        → Rotate composition
        → Result: Balanced teams

                    ↓ STEP 8: SET TIMELINES
        → Maintenance: Use schedule
        → Projects: Mark TBC
        → Result: Time limits set

OUTPUT FILES
├── sites_schedule.csv (720 rows)
├── team_assignments.csv (720 rows)
├── team_assignments_summary.csv (20 rows)
├── final_report.xlsx (5 sheets)
└── *.log (3 files)
```

---

## 🔄 Processing Pipeline

```
START HERE
    ↓
[RECEIVE USER INPUT]
    ├─ Excel filename
    ├─ Analysis type
    ├─ Exclude critical sites? (Yes/No)
    └─ Months to look back (0-12)
    ↓
[GITHUB ACTIONS TRIGGERED]
    ↓
┌─────────────────────────────────────────┐
│ PARALLEL PROCESSING                     │
├─────────────────────────────────────────┤
│                                         │
│  Path A: VALIDATION         Path B: ANALYSIS
│  ┌──────────────────────┐  ┌──────────────────────┐
│  │ validate_input.py    │  │ main_analysis.py     │
│  │                      │  │                      │
│  │ Check Excel format   │  │ Load data            │
│  │ Verify columns       │  │ Filter recent        │
│  │ Check data types     │  │ Filter critical      │
│  │ Generate report      │  │ Harmonize            │
│  │                      │  │ Assign teams         │
│  │ Output:              │  │ Output:              │
│  │ validation_report    │  │ sites_schedule.csv   │
│  │ ✅ or ❌             │  │ analysis_log.txt     │
│  └──────────────────────┘  └──────────────────────┘
│        ↓                           ↓
└─────────────────────────────────────────┘
    ↓
    [BOTH COMPLETE? → Continue]
    ↓
[TEAM ASSIGNMENT]
├─ team_assignment.py
├─ Form balanced teams
├─ Assign sites to teams
├─ Calculate team workload
└─ Output:
   ├─ team_assignments.csv
   ├─ team_assignments_summary.csv
   └─ team_assignment_log.txt
    ↓
[REPORT GENERATION]
├─ generate_report.py
├─ Compile all results
├─ Create Excel workbook
├─ Add multiple sheets
└─ Output:
   └─ final_report.xlsx
    ↓
[UPLOAD & STORE]
├─ Compress results
├─ Upload to artifacts
├─ Set 30-day retention
└─ Create GitHub release
    ↓
[NOTIFY]
├─ Generate summary
├─ Add to job summary
├─ (Optional: Slack/Email)
└─ Mark as complete ✅
    ↓
[USER DOWNLOADS RESULTS]
    ↓
[DONE! 🎉]
```

---

## 📈 File Size Estimates

```
INPUT
├── Small file (100 sites)
│   └─ 50 KB Excel
├── Medium file (1000 sites)
│   └─ 200 KB Excel
└── Large file (10000 sites)
    └─ 2 MB Excel

PROCESSING TIME
├── Small: < 1 minute
├── Medium: 1-3 minutes
└── Large: 3-10 minutes

OUTPUT
├── sites_schedule.csv: 50-500 KB
├── team_assignments.csv: 50-500 KB
├── team_assignments_summary.csv: 10 KB
├── final_report.xlsx: 100-1000 KB
└── Logs: 20-100 KB

TOTAL ARTIFACTS
├── Small: ~200 KB
├── Medium: ~1 MB
└── Large: ~3 MB
```

---

## 🔄 Team Formation Logic

```
INPUT SITES: 100 sites
TEAM MEMBERS: 10 people

┌─────────────────────────────────────────┐
│ TEAM FORMATION ALGORITHM                │
├─────────────────────────────────────────┤
│                                         │
│ 1. Split team members in half:          │
│    ├─ 5 technical leads                │
│    └─ 5 non-technical resources        │
│                                         │
│ 2. Create team pairs:                   │
│    ├─ Team 1: Lead + 2 non-tech        │
│    ├─ Team 2: Lead + 2 non-tech        │
│    ├─ Team 3: Lead + 2 non-tech        │
│    ├─ Team 4: Lead + 2 non-tech        │
│    └─ Team 5: Lead + 1 non-tech        │
│                                         │
│ 3. Assign sites:                        │
│    ├─ Team 1: 20 sites ✅              │
│    ├─ Team 2: 20 sites ✅              │
│    ├─ Team 3: 20 sites ✅              │
│    ├─ Team 4: 20 sites ✅              │
│    └─ Team 5: 20 sites ✅              │
│                                         │
│ Total assigned: 100 sites              │
│ Result: Balanced workload ✅           │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🎯 Filtering Pipeline

```
START: 1000 SITES
    ↓
┌─ STEP 3: FILTER RECENT VISITS ─┐
│ Check visit_history             │
│ Look back: 3 months             │
│ Found: 150 recent visits        │
│ Remove: 150 sites               │
│ Remaining: 850 sites            │
└─────────────────────────────────┘
    ↓
┌─ STEP 4: FILTER CRITICAL ──────┐
│ Check critical_sites list       │
│ Risk level: HIGH                │
│ Tower type: ROOFTOP             │
│ Found: 50 critical sites        │
│ Remove: 50 sites                │
│ Remaining: 800 sites            │
└─────────────────────────────────┘
    ↓
┌─ STEP 5: HARMONIZE ────────────┐
│ Combine maintenance & projects  │
│ Add metadata                    │
│ Final count: 800 sites          │
│ Status: Ready for assignment    │
└─────────────────────────────────┘
    ↓
OUTPUT: 800 READY-TO-ASSIGN SITES
```

---

## 📋 Excel Sheet Structure

```
SHEET 1: maintenance
┌─────────────────────────────────────────────────────┐
│ site_id │ site_name │ tower_type │ activity_type   │
├─────────────────────────────────────────────────────┤
│ SDK0001 │ DK_ZONE_B │ Rooftop    │ maintenance     │
│ SDK0002 │ DK_YOFF   │ Greenfield │ maintenance     │
│ ...     │ ...       │ ...        │ ...             │
├─────────────────────────────────────────────────────┤
│ Total Rows: 500                                     │
└─────────────────────────────────────────────────────┘

SHEET 2: project
┌─────────────────────────────────────────────────────┐
│ site_id │ site_name │ project_name │ department     │
├─────────────────────────────────────────────────────┤
│ PROJ001 │ DK_PARC   │ Network Exp  │ Engineering    │
│ PROJ002 │ DK_CITE   │ Upgrade      │ Engineering    │
│ ...     │ ...       │ ...          │ ...            │
├─────────────────────────────────────────────────────┤
│ Total Rows: 300                                     │
└─────────────────────────────────────────────────────┘

SHEET 3: visit_history
┌─────────────────────────────────────────────────────┐
│ site_id │ visit_date │ team_member                  │
├─────────────────────────────────────────────────────┤
│ SDK0001 │ 2024-01-15 │ Team_Member_1               │
│ SDK0002 │ 2024-01-16 │ Team_Member_2               │
│ ...     │ ...        │ ...                         │
├─────────────────────────────────────────────────────┤
│ Total Rows: 150                                     │
└─────────────────────────────────────────────────────┘

SHEET 4: critical_sites
┌─────────────────────────────────────────────────────┐
│ site_id │ site_name │ tower_type │ risk_level      │
├─────────────────────────────────────────────────────┤
│ SDK0001 │ DK_ZONE_B │ Rooftop    │ high            │
│ SDK0003 │ DK_CITE   │ Rooftop    │ critical        │
│ ...     │ ...       │ ...        │ ...             │
├─────────────────────────────────────────────────────┤
│ Total Rows: 50                                      │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Workflow Trigger Points

```
┌─────────────────────────────────────────┐
│    HOW TO START THE WORKFLOW            │
└─────────────────────────────────────────┘

Option 1: GitHub Web UI (Most Common)
┌─────────────────────────────────────────┐
│ 1. Go to: GitHub → Your Repo            │
│ 2. Click: Actions tab                   │
│ 3. Select: Excel File Analysis Pipeline │
│ 4. Click: Run workflow                  │
│ 5. Fill: Parameters                     │
│ 6. Click: Run workflow                  │
│                                         │
│ Time: ~30 seconds                       │
└─────────────────────────────────────────┘

Option 2: GitHub CLI
┌─────────────────────────────────────────┐
│ gh workflow run excel-analysis.yml \   │
│   -f excel_file="file.xlsx" \          │
│   -f analysis_type="full_schedule"     │
│                                         │
│ Time: ~10 seconds                       │
└─────────────────────────────────────────┘

Option 3: Git Push (Automated)
┌─────────────────────────────────────────┐
│ git add your-file.xlsx                 │
│ git commit -m "Add data"                │
│ git push origin main                    │
│                                         │
│ Workflow: Triggered automatically       │
│ (if configured with push trigger)       │
│                                         │
│ Time: ~5 seconds                        │
└─────────────────────────────────────────┘
```

---

## 📊 Performance Metrics

```
EXECUTION TIME BREAKDOWN
┌──────────────────────────────┬───────────┐
│ Component                    │ Time (ms) │
├──────────────────────────────┼───────────┤
│ Setup job                    │ 5-10 sec  │
│ Validation job               │ 10-20 sec │
│ Analysis job                 │ 30-120 sec│
│ Team formation job           │ 10-30 sec │
│ Report generation job        │ 5-15 sec  │
│ Upload & notify              │ 5-10 sec  │
├──────────────────────────────┼───────────┤
│ TOTAL                        │ 60-240 sec│
└──────────────────────────────┴───────────┘

                    ↓

Total: 1-4 MINUTES FOR COMPLETE ANALYSIS
```

---

## 🔐 Data Security & Retention

```
GITHUB ARTIFACTS STORAGE
┌─────────────────────────────────┐
│ Default Retention: 30 days      │
│ Max Size: 5 GB per artifact     │
│ Access: Private to repo members │
│ Download: Available in UI       │
└─────────────────────────────────┘

DATA LOCATIONS
├─ Input: GitHub repo (committed)
├─ Processing: GitHub Actions runner (temp)
├─ Output: Artifacts (encrypted)
└─ Download: Your local computer

PRIVACY & COMPLIANCE
✅ Data encrypted in transit (HTTPS)
✅ No data stored permanently on GitHub
✅ Auto-cleanup after retention period
✅ Private repo: Only authorized access
✅ Audit logs available in GitHub
```

---

## 🎯 Decision Tree

```
START: Do you want to run the analysis?
  │
  ├─YES → Do you have a GitHub account?
  │         │
  │         ├─YES → Have you pushed code to GitHub?
  │         │         │
  │         │         ├─YES → Go to Actions tab → Run workflow ✅
  │         │         └─NO → Run setup.sh or push manually → Then run
  │         │
  │         └─NO → Create account at github.com → Then follow above
  │
  └─NO → Why not? (See README.md for details)
```

---

## 💾 File Organization Guide

```
YOUR COMPUTER
└── /Users/shrutisohan/Desktop/excel/
    ├── 📂 .github/ ............................ GitHub config
    ├── 📂 scripts/ ........................... Python code
    ├── 📂 data/ .............................. Input/output
    ├── 📄 README.md .......................... Start reading
    ├── 📄 SETUP.md ........................... Setup guide
    ├── 📄 requirements.txt ................... Dependencies
    └── 📄 *.py .............................. Sample scripts

GITHUB REPOSITORY (cloud.github.com)
└── boot-not-suit-analysis/
    ├── All files above ...................... Same structure
    ├── Actions tab .......................... Run workflows
    └── Artifacts ............................ Download results

LOCAL OUTPUT (After first run)
└── /Users/shrutisohan/Desktop/excel/data/output/
    ├── sites_schedule.csv ................... Processed sites
    ├── team_assignments.csv ................. Assignments
    ├── final_report.xlsx .................... Main report
    └── *.log ............................... Execution logs
```

---

## 📞 Support Decision Tree

```
Something went wrong? Follow this:

Error in workflow? 
  └─ Check GitHub Actions log
     └─ Look for red ❌ marker
        └─ Read error message
           └─ See INSTALL.md → Troubleshooting

"File not found"?
  └─ Use exact filename with extension
     └─ Example: Colo_Sonatel-APS.xlsx (not .xls)

"Column not found"?
  └─ Check Excel sheet has required columns
     └─ See README.md → Required Format

No output files?
  └─ Check validation_report.txt
     └─ Ensure Excel data is complete

Still stuck?
  └─ Read one of:
     ├─ README.md
     ├─ INSTALL.md
     └─ API.md
```

---

## ✨ Success Indicators

```
✅ WORKFLOW SUCCEEDED
├─ All jobs show green checkmarks
├─ Artifacts available to download
├─ 2-5 minutes execution time
└─ Output files present

✅ OUTPUT IS CORRECT
├─ sites_schedule.csv has data
├─ team_assignments.csv has assignments
├─ final_report.xlsx opens properly
└─ All logs show completion

✅ DATA LOOKS GOOD
├─ Team assignments total = input sites
├─ No duplicate assignments
├─ All team members have work
└─ Timelines are set correctly
```

---

**This visual guide helps you understand the complete flow and architecture. For step-by-step instructions, see the text documentation files.**

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Ready to Deploy ✅
