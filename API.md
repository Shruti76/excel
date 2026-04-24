# API Documentation for Analysis Modules

## validate_input.py

Validates Excel input files for required columns and data format.

### Usage

```bash
python scripts/validate_input.py --file data/sample.xlsx --log data/output/validation.txt
```

### Parameters

- `--file` (required): Path to Excel file to validate
- `--log` (optional): Path to save validation report

### Output

Returns exit code:
- `0`: All validations passed
- `1`: Validation failed

### Validation Rules

#### Maintenance Sheet
Required columns:
- `site_id`: Unique identifier
- `site_name`: Site name
- `nearest_hi`: Numeric value
- `tower_type`: Tower classification
- `activity_type`: Should be "maintenance"

#### Project Sheet
Required columns:
- `site_id`: Unique identifier
- `site_name`: Site name
- `project_name`: Project name
- `department`: Department name

#### Visit History Sheet (Optional)
Required columns:
- `site_id`: Previously visited site
- `visit_date`: Date in YYYY-MM-DD format
- `team_member`: Person who visited

#### Critical Sites Sheet (Optional)
Required columns:
- `site_id`: Site identifier
- `site_name`: Site name
- `tower_type`: Tower type
- `risk_level`: high/medium/low
- `reason`: Reason for being critical

---

## main_analysis.py

Generates site visit schedules following the 8-step process.

### Usage

```bash
python scripts/main_analysis.py \
  --input data/sample.xlsx \
  --output data/output \
  --analysis-type full_schedule \
  --exclude-critical true \
  --months-back 3 \
  --log data/output/analysis.txt
```

### Parameters

- `--input` (required): Input Excel file path
- `--output` (required): Output directory for results
- `--analysis-type` (optional): Type of analysis
  - `full_schedule`: Complete 8-step process (default)
  - `validate_data`: Only data validation
  - `team_assignment`: Only team assignments
  - `site_exclusion`: Only filtering
- `--exclude-critical` (optional): Exclude critical sites (true/false, default: true)
- `--months-back` (optional): Months to look back (default: 3)
- `--log` (optional): Log file path

### Output Files

1. **sites_schedule.csv**: Filtered sites ready for assignment
2. **analysis_log.txt**: Detailed execution log

### Process Flow

```
Input Excel
    ↓
Load Data (Steps 1-2)
    ↓
Exclude Recent Visits (Step 3)
    ↓
Exclude Critical Sites (Step 4)
    ↓
Harmonize Activities (Step 5)
    ↓
Assign to Teams (Step 6)
    ↓
Output Schedule
```

### Class: SiteVisitScheduler

#### Methods

**`__init__(months_back: int = 3)`**
Initialize the scheduler with lookback period.

**`load_data(input_file: str) -> bool`**
Load all data from Excel file.

**`generate_schedule(exclude_critical: bool = True) -> pd.DataFrame`**
Generate complete schedule following 8 steps.

**`get_log() -> str`**
Get complete execution log.

---

## team_assignment.py

Assigns sites to teams and forms team pairs/trios.

### Usage

```bash
python scripts/team_assignment.py \
  --schedule data/output/sites_schedule.csv \
  --output data/output/team_assignments.csv \
  --log data/output/team_assignment.txt \
  --sites-per-person 2 \
  --sites-per-influencer 4
```

### Parameters

- `--schedule` (required): Sites schedule CSV file
- `--output` (required): Output CSV file for assignments
- `--log` (optional): Log file path
- `--sites-per-person` (optional): Sites per team member (default: 2)
- `--sites-per-influencer` (optional): Sites per influencer (default: 4)

### Output Files

1. **team_assignments.csv**: Site-to-team assignments
2. **team_assignments_summary.csv**: Team workload summary

### CSV Format

#### team_assignments.csv

```
site_id,site_name,team_id,technical_lead,non_technical_members,activity_type,time_limit,assigned_date
SDK0001,DK_ZONE_B,TEAM_001,Member_1,Member_2; Member_3,maintenance,09:00-17:00,2024-01-15
```

#### team_assignments_summary.csv

```
team_id,sites_assigned,technical_lead,non_technical_members,activity_type
TEAM_001,2,Member_1,Member_2; Member_3,maintenance; project
```

### Class: TeamAssigner

#### Methods

**`load_schedule(schedule_file: str) -> pd.DataFrame`**
Load sites from schedule CSV.

**`create_team_pairs(sites_df, team_members) -> List[Dict]`**
Form balanced teams with technical and non-technical staff.

**`assign_sites_to_teams(sites_df, teams) -> pd.DataFrame`**
Assign each site to a team.

---

## generate_report.py

Creates final Excel report from analysis results.

### Usage

```bash
python scripts/generate_report.py \
  --input data/output \
  --output data/output/final_report.xlsx \
  --log data/output/report.txt
```

### Parameters

- `--input` (required): Input directory with analysis results
- `--output` (required): Output Excel file path
- `--log` (optional): Log file path

### Output Format

Excel file with sheets:

1. **Summary**
   - Report metadata
   - Generation date
   - Report type

2. **Sites Schedule**
   - All processed sites
   - Activity types
   - Assignment status

3. **Team Assignments**
   - Site-to-team mappings
   - Team composition
   - Time allocations

4. **Team Summary**
   - Team workload overview
   - Members per team
   - Activity distribution

5. **Analysis Log**
   - Complete execution log
   - All processing steps

---

## Data Structures

### Site Record

```python
{
    'site_id': 'SDK0001',
    'site_name': 'DK_ZONE_B',
    'nearest_hi': 56,
    'tower_type': 'Rooftop',
    'activity_type': 'maintenance',
    'time_limit': '09:00-17:00',
    'assigned': False,
    'assigned_date': None
}
```

### Team Record

```python
{
    'team_id': 'TEAM_001',
    'technical_lead': 'Member_1',
    'non_technical_members': ['Member_2', 'Member_3'],
    'team_size': 3,
    'sites_assigned': 0
}
```

### Assignment Record

```python
{
    'site_id': 'SDK0001',
    'site_name': 'DK_ZONE_B',
    'team_id': 'TEAM_001',
    'technical_lead': 'Member_1',
    'non_technical_members': 'Member_2; Member_3',
    'activity_type': 'maintenance',
    'time_limit': '09:00-17:00',
    'assigned_date': '2024-01-15'
}
```

---

## Error Handling

### Common Errors

#### FileNotFoundError
```
Error: [Errno 2] No such file or directory
Solution: Verify file path exists and is correct
```

#### KeyError (Missing Column)
```
Error: 'site_id' not found in columns
Solution: Ensure Excel sheet has all required columns
```

#### ValueError (Date Parsing)
```
Error: time data does not match format
Solution: Use YYYY-MM-DD format for all dates
```

#### MemoryError
```
Error: Unable to allocate memory
Solution: Process smaller files or use GitHub's larger runner
```

---

## Performance Optimization

### Batch Processing

For large files, process in batches:

```python
chunk_size = 1000
for i in range(0, len(df), chunk_size):
    chunk = df[i:i+chunk_size]
    # Process chunk
```

### Parallel Processing

Enable parallel execution:

```bash
# Process multiple files in parallel
python scripts/main_analysis.py --parallel-workers 4
```

### Memory Optimization

Use data type optimization:

```python
df['site_id'] = df['site_id'].astype('category')
```

---

## Logging

### Log Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General processing information (default)
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages indicating failures

### Log Format

```
[2024-01-15 10:30:45] ✅ Loaded maintenance activities: 50 records
[2024-01-15 10:30:46] Step 3: Excluding sites visited in last 3 months
[2024-01-15 10:30:47] ❌ Error: File not found
```

---

## Examples

### Example 1: Full Analysis

```bash
python scripts/validate_input.py --file data/input.xlsx
python scripts/main_analysis.py --input data/input.xlsx --output data/output
python scripts/team_assignment.py --schedule data/output/sites_schedule.csv --output data/output/team_assignments.csv
python scripts/generate_report.py --input data/output --output data/output/final_report.xlsx
```

### Example 2: Data Validation Only

```bash
python scripts/validate_input.py --file data/input.xlsx --log data/validation.txt
```

### Example 3: Custom Configuration

```bash
python scripts/main_analysis.py \
  --input data/input.xlsx \
  --output data/output \
  --exclude-critical false \
  --months-back 6
```

---

## Testing

### Unit Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_analysis.py

# Run with coverage
python -m pytest --cov=scripts tests/
```

### Integration Tests

```bash
# Test full pipeline
bash tests/integration_test.sh
```

---

## Contributing

To extend or modify:

1. Follow PEP 8 style guidelines
2. Add docstrings to all functions
3. Include error handling
4. Update API documentation
5. Add unit tests

---

**Version**: 1.0.0  
**Last Updated**: 2024-01-15  
**Maintainer**: Development Team
