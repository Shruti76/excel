#!/usr/bin/env python3
"""
Generate final Excel report with all analysis results and visualizations.
"""

import pandas as pd
import sys
import argparse
from pathlib import Path
from datetime import datetime


class ReportGenerator:
    """Generate comprehensive Excel report from analysis results."""
    
    def __init__(self):
        self.log = []
    
    def log_message(self, msg: str):
        """Log message."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_msg = f"[{timestamp}] {msg}"
        self.log.append(full_msg)
        print(full_msg)
    
    def generate_report(self, input_dir: str, output_file: str) -> bool:
        """Generate comprehensive Excel report."""
        self.log_message("=" * 70)
        self.log_message("GENERATING FINAL REPORT")
        self.log_message("=" * 70)
        
        try:
            input_path = Path(input_dir)
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create Excel writer
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # Sheet 1: Summary
                summary_data = {
                    'Report Date': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                    'Report Type': ['Boot Not Suit Site Visit Schedule'],
                    'Status': ['Generated']
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                self.log_message("✅ Added Summary sheet")
                
                # Sheet 2: Sites Schedule
                schedule_file = input_path / 'sites_schedule.csv'
                if schedule_file.exists():
                    schedule_df = pd.read_csv(schedule_file)
                    schedule_df.to_excel(writer, sheet_name='Sites Schedule', index=False)
                    self.log_message(f"✅ Added Sites Schedule sheet ({len(schedule_df)} sites)")
                
                # Sheet 3: Team Assignments
                assignments_file = input_path / 'team_assignments.csv'
                if assignments_file.exists():
                    assignments_df = pd.read_csv(assignments_file)
                    assignments_df.to_excel(writer, sheet_name='Team Assignments', index=False)
                    self.log_message(f"✅ Added Team Assignments sheet ({len(assignments_df)} assignments)")
                    
                    # Sheet 4: Team Summary
                    summary_file = input_path / 'team_assignments_summary.csv'
                    if summary_file.exists():
                        team_summary_df = pd.read_csv(summary_file)
                        team_summary_df.to_excel(writer, sheet_name='Team Summary', index=False)
                        self.log_message(f"✅ Added Team Summary sheet")
                
                # Sheet 5: Analysis Logs
                analysis_log_file = input_path / 'analysis_log.txt'
                if analysis_log_file.exists():
                    with open(analysis_log_file, 'r') as f:
                        log_content = f.read().split('\n')
                    log_df = pd.DataFrame({'Log': log_content})
                    log_df.to_excel(writer, sheet_name='Analysis Log', index=False)
                    self.log_message("✅ Added Analysis Log sheet")
            
            self.log_message(f"✅ Report generated successfully: {output_file}")
            return True
        
        except Exception as e:
            self.log_message(f"❌ Error generating report: {str(e)}")
            return False
    
    def get_log(self) -> str:
        """Get complete log."""
        return "\n".join(self.log)


def main():
    parser = argparse.ArgumentParser(
        description='Generate final Excel report'
    )
    parser.add_argument('--input', required=True, help='Input directory with analysis results')
    parser.add_argument('--output', required=True, help='Output Excel file')
    parser.add_argument('--log', required=False, help='Log file path')
    
    args = parser.parse_args()
    
    generator = ReportGenerator()
    
    if generator.generate_report(args.input, args.output):
        exit_code = 0
    else:
        exit_code = 1
    
    # Save log
    if args.log:
        log_path = Path(args.log)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, 'w') as f:
            f.write(generator.get_log())
        print(f"\nLog saved to: {log_path}")
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
