#!/usr/bin/env python3
"""
Validate Excel input files for site visit schedule analysis.
Checks for required columns and data format.
"""

import pandas as pd
import sys
import argparse
from pathlib import Path
from datetime import datetime


def validate_maintenance_schedule(df):
    """Validate maintenance activities schedule."""
    required_cols = ['site_id', 'site_name', 'nearest_hi', 'tower_type', 'activity_type']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        return False, f"Missing columns in maintenance sheet: {missing_cols}"
    
    if df.empty:
        return False, "Maintenance schedule is empty"
    
    return True, "Maintenance schedule validated"


def validate_project_schedule(df):
    """Validate project activities schedule."""
    required_cols = ['site_id', 'site_name', 'project_name', 'department']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        return False, f"Missing columns in project sheet: {missing_cols}"
    
    if df.empty:
        return False, "Project schedule is empty"
    
    return True, "Project schedule validated"


def validate_visit_history(df):
    """Validate visit history (sites already visited)."""
    required_cols = ['site_id', 'visit_date', 'team_member']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        return False, f"Missing columns in visit history: {missing_cols}"
    
    return True, "Visit history validated"


def validate_critical_sites(df):
    """Validate critical sites list."""
    required_cols = ['site_id', 'site_name', 'risk_level', 'reason']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        return False, f"Missing columns in critical sites: {missing_cols}"
    
    return True, "Critical sites list validated"


def main():
    parser = argparse.ArgumentParser(
        description='Validate Excel input files for analysis'
    )
    parser.add_argument('--file', required=True, help='Path to Excel file')
    parser.add_argument('--log', required=False, help='Log output file')
    
    args = parser.parse_args()
    
    log_output = []
    log_output.append(f"Validation Report - {datetime.now().isoformat()}")
    log_output.append("=" * 60)
    
    try:
        file_path = Path(args.file)
        if not file_path.exists():
            log_output.append(f"❌ File not found: {file_path}")
            sys.exit(1)
        
        log_output.append(f"📄 Validating file: {file_path.name}")
        log_output.append("")
        
        # Read all sheets
        excel_file = pd.ExcelFile(file_path)
        log_output.append(f"Found sheets: {excel_file.sheet_names}")
        log_output.append("")
        
        validation_results = {}
        
        # Validate each sheet based on naming convention
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            log_output.append(f"\nValidating sheet: '{sheet_name}'")
            log_output.append(f"Rows: {len(df)}, Columns: {len(df.columns)}")
            log_output.append(f"Columns: {list(df.columns)}")
            
            if 'maintenance' in sheet_name.lower():
                is_valid, msg = validate_maintenance_schedule(df)
                validation_results[sheet_name] = (is_valid, msg)
                log_output.append(f"{'✅' if is_valid else '❌'} {msg}")
            
            elif 'project' in sheet_name.lower():
                is_valid, msg = validate_project_schedule(df)
                validation_results[sheet_name] = (is_valid, msg)
                log_output.append(f"{'✅' if is_valid else '❌'} {msg}")
            
            elif 'visit' in sheet_name.lower() or 'history' in sheet_name.lower():
                is_valid, msg = validate_visit_history(df)
                validation_results[sheet_name] = (is_valid, msg)
                log_output.append(f"{'✅' if is_valid else '❌'} {msg}")
            
            elif 'critical' in sheet_name.lower() or 'risk' in sheet_name.lower():
                is_valid, msg = validate_critical_sites(df)
                validation_results[sheet_name] = (is_valid, msg)
                log_output.append(f"{'✅' if is_valid else '❌'} {msg}")
            
            else:
                log_output.append("⚠️  Sheet type not recognized")
        
        # Summary
        log_output.append("\n" + "=" * 60)
        all_valid = all(is_valid for is_valid, _ in validation_results.values())
        
        if all_valid:
            log_output.append("✅ All validations passed!")
            exit_code = 0
        else:
            log_output.append("❌ Some validations failed!")
            exit_code = 1
        
        # Write log
        log_text = "\n".join(log_output)
        print(log_text)
        
        if args.log:
            Path(args.log).parent.mkdir(parents=True, exist_ok=True)
            with open(args.log, 'w') as f:
                f.write(log_text)
            print(f"\n📝 Log saved to: {args.log}")
        
        sys.exit(exit_code)
    
    except Exception as e:
        log_output.append(f"❌ Error during validation: {str(e)}")
        log_text = "\n".join(log_output)
        print(log_text)
        
        if args.log:
            Path(args.log).parent.mkdir(parents=True, exist_ok=True)
            with open(args.log, 'w') as f:
                f.write(log_text)
        
        sys.exit(1)


if __name__ == '__main__':
    main()
