# Quick Reference Guide

## 🚀 Get Started in 60 Seconds

### Step 1: Copy Project (10 seconds)
```bash
cd /Users/shrutisohan/Desktop/excel
```

### Step 2: Initialize Git (20 seconds)
```bash
git init
git add .
git commit -m "Initial commit"
```

### Step 3: Push to GitHub (20 seconds)
```bash
git remote add origin https://github.com/yourusername/boot-not-suit-analysis.git
git push -u origin main
```

### Step 4: Run Workflow (10 seconds)
1. Go to GitHub → Actions tab
2. Click "Excel File Analysis Pipeline"
3. Click "Run workflow"
4. Fill in your Excel filename
5. Click "Run workflow"

---

## 📋 Commands Reference

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Create sample Excel
python create_sample.py

# Validate Excel
python scripts/validate_input.py --file data/sample_schedule.xlsx

# Run analysis
python scripts/main_analysis.py \
  --input data/sample_schedule.xlsx \
  --output data/output

# Generate report
python scripts/generate_report.py \
  --input data/output \
  --output data/output/final_report.xlsx
```

### GitHub Operations

```bash
# Check workflow status
gh workflow list

# Run workflow
gh workflow run excel-analysis.yml \
  -f excel_file="your-file.xlsx" \
  -f analysis_type="full_schedule"

# View runs
gh run list

# Download results
gh run download <run-id> -D results/

# View logs
gh run view <run-id> --log
```

### Git Operations

```bash
# Check status
git status

# Add files
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main

# View commit history
git log --oneline
```

---

## 📁 File Structure Quick Map

```
📦 Project Root
├── 🔧 Setup Files
│   ├── requirements.txt (dependencies)
│   ├── .gitignore (git exclusions)
│   ├── config.properties (settings)
│   └── setup.sh (auto-setup script)
│
├── 📄 Documentation (READ THESE)
│   ├── README.md (Main guide - START HERE)
│   ├── SETUP.md (GitHub setup - 5 min read)
│   ├── INSTALL.md (Full installation - 15 min read)
│   ├── API.md (Technical reference - For developers)
│   └── PROJECT_OVERVIEW.md (Complete overview)
│
├── 🤖 Automation
│   ├── .github/workflows/excel-analysis.yml (GitHub Actions)
│   │   ├── validate (Check Excel)
│   │   ├── analyze (Process data)
│   │   ├── upload (Save results)
│   │   └── notify (Send summary)
│
├── 🐍 Python Scripts
│   ├── scripts/validate_input.py (Validate Excel)
│   ├── scripts/main_analysis.py (8-step analysis)
│   ├── scripts/team_assignment.py (Team formation)
│   ├── scripts/generate_report.py (Excel report)
│   └── create_sample.py (Sample data)
│
├── 📊 Data Directories
│   ├── data/ (Input files)
│   │   └── uploads/ (User uploads)
│   └── output/ (Results)
│
└── ℹ️ This file
    └── QUICK_REFERENCE.md
```

---

## 🎯 Workflow Parameters Explained

| Parameter | Example | What it does |
|-----------|---------|-------------|
| **excel_file** | `Colo_Sonatel-APS.xlsx` | Which Excel file to analyze |
| **analysis_type** | `full_schedule` | Run all 8 steps (or specific steps) |
| **exclude_critical_sites** | `true` | Skip high-risk rooftop sites |
| **months_back** | `3` | Exclude sites visited in last 3 months |

---

## 📊 Input Excel Sheets

### Must Have
- **maintenance**: Maintenance activities
- **project**: Project activities

### Optional
- **visit_history**: Sites already visited
- **critical_sites**: High-risk sites to exclude

---

## 📤 Output Files

| File | Size | What's inside |
|------|------|---------------|
| **sites_schedule.csv** | ~50KB | Filtered sites ready for teams |
| **team_assignments.csv** | ~50KB | Which team visits which site |
| **team_assignments_summary.csv** | ~10KB | Team workload summary |
| **final_report.xlsx** | ~200KB | Excel report with all data |
| **validation_report.txt** | ~5KB | Data quality check |
| **analysis_log.txt** | ~20KB | What the pipeline did |

---

## 🔴 If Something Goes Wrong

### "Workflow not found"
→ Wait 1 minute and refresh GitHub page

### "File not found"
→ Use exact filename: `Colo_Sonatel-APS.xlsx` (with extension!)

### "Missing columns"
→ Check your Excel sheet has all required columns

### "No output files"
→ Look at validation_report.txt in artifacts

### "Package not found"
→ Workflow will auto-install from requirements.txt

---

## 💡 Pro Tips

✅ Test with sample_schedule.xlsx first
✅ Check analysis_log.txt if anything seems wrong
✅ Keep backup copies of output reports
✅ Use Ctrl+Click to download all files at once
✅ Review team assignments before using in production

---

## 📞 Quick Help

### Issue: Workflow runs but generates no results
**Check**: 
1. Are there error messages in the workflow log?
2. Is validation_report.txt showing errors?
3. Does your Excel file have data in all required sheets?

### Issue: Team assignments don't look right
**Check**:
1. Review team_assignments_summary.csv
2. Check sites_schedule.csv for filtering issues
3. Look at analysis_log.txt for step-by-step details

### Issue: Takes too long
**Solution**: 
- Split large files into smaller pieces
- Or just wait (large files are normal)

---

## 🔗 Important Links

- **Repository**: https://github.com/yourusername/boot-not-suit-analysis
- **GitHub Actions**: https://docs.github.com/en/actions
- **Python Pandas**: https://pandas.pydata.org/docs
- **This Project on GitHub**: Your repo URL

---

## 📋 Checklist for First Run

- [ ] Project downloaded/cloned
- [ ] Git initialized
- [ ] Code pushed to GitHub
- [ ] Can see "Excel File Analysis Pipeline" in Actions
- [ ] Have an Excel file ready to test
- [ ] Parameters filled in correctly
- [ ] Workflow executed
- [ ] Results downloaded
- [ ] Output files reviewed

---

## 🎓 Key Concepts

**8-Step Process**:
1. ✅ Load maintenance + project schedules
2. ✅ Get exception requests
3. ✅ Remove recently visited sites
4. ✅ Remove dangerous sites
5. ✅ Combine all activities
6. ✅ Assign sites to teams
7. ✅ Form team pairs/trios
8. ✅ Set time limits

**Output**: Team schedule with assignments → Sites → Timelines

---

## 🚀 What Happens When You Run the Workflow

```
You click "Run workflow"
         ↓
GitHub spins up Ubuntu server
         ↓
Python gets installed
         ↓
Dependencies get installed
         ↓
Excel file gets validated
         ↓
Analysis runs (8 steps)
         ↓
Teams get formed
         ↓
Report gets generated
         ↓
Results saved to Artifacts
         ↓
You download results
         ↓
All done in 2-5 minutes! ✅
```

---

## 💾 Saving Your Results

### Via GitHub UI
1. Go to Actions → Your workflow run
2. Scroll to Artifacts
3. Click "analysis-results"
4. Files download as ZIP

### Via GitHub CLI
```bash
gh run download <run-id> -D my-results/
```

### Via Git
```bash
git pull origin main  # Gets latest
```

---

## 📈 Success Metrics

✅ Validation report shows no errors
✅ Analysis completes in 2-5 minutes
✅ Output files are generated
✅ Team assignments total = input sites
✅ All team members have assignments
✅ No sites assigned twice

---

## 🎯 Next Actions

**Immediate** (Next 5 minutes):
- Push code to GitHub
- Run first workflow with sample data
- Download and review results

**Short-term** (This week):
- Test with your actual data
- Customize parameters
- Review output format

**Medium-term** (This month):
- Set up regular runs
- Integrate with other systems
- Train team on process

**Long-term** (Ongoing):
- Monitor workflow performance
- Update dependencies
- Optimize for your data

---

## 🆘 Where to Find Help

| Question | Look Here |
|----------|-----------|
| How do I get started? | README.md |
| How do I set up GitHub? | SETUP.md |
| How do I install locally? | INSTALL.md |
| What's in each file? | PROJECT_OVERVIEW.md |
| Technical details? | API.md |
| Something broke! | INSTALL.md → Troubleshooting |

---

## ⚡ Quick Commands

```bash
# Everything in one shot (for GitHub)
git init && git add . && git commit -m "Initial commit" && git remote add origin [URL] && git push -u origin main

# Local test (Python)
python scripts/validate_input.py --file data/sample_schedule.xlsx && python scripts/main_analysis.py --input data/sample_schedule.xlsx --output data/output

# Check workflow (CLI)
gh run list && gh run view [run-id] --log
```

---

## 🎉 You're All Set!

Everything is ready to go. Choose your next action:

1. **New to GitHub?** → Read SETUP.md
2. **Need step-by-step?** → Read INSTALL.md
3. **Ready to deploy?** → Push to GitHub and run!
4. **Technical questions?** → Check API.md

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Ready to Use ✅

Happy scheduling! 🚀
