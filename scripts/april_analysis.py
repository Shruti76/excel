#!/usr/bin/env python3
"""
April Site Visit Calendar Analysis Script
Processes 5 types of input files and generates comprehensive April report

File Types:
1. Colo_Sonatel-APS.xlsx - Site master data (ID, name, type, project)
2. HTS Site Visits Calendar - Planning schedule with visit history
3. PM_ZONE1_2_MARS_2026.xlsx - Preventive maintenance assignments
4. Project sites BNS plan - Project-based site requirements
5. RT High Risk List - Critical/failed sites requiring priority visits
"""

import pandas as pd
import numpy as np
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows


class AprilReportGenerator:
    """Generate comprehensive April site visit schedule report from 5 file types."""
    
    def __init__(self, output_folder: str = "output"):
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)
        self.log = []
        self.report_date = datetime(2026, 4, 1)  # April 2026
        
        # Loaded data
        self.site_master = None
        self.hts_calendar = None
        self.pm_assignments = None
        self.project_sites = None
        self.critical_sites = None
        
        # Analysis results
        self.april_schedule = None
        self.team_assignments = None
        self.summary_stats = None
    
    def log_message(self, msg: str):
        """Log message with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_msg = f"[{timestamp}] {msg}"
        self.log.append(full_msg)
        print(full_msg)
    
    def load_files(self, file_dict: Dict[str, str]) -> bool:
        """
        Load all 5 file types.
        
        Args:
            file_dict: Dictionary with keys:
                - 'site_master': Colo_Sonatel-APS.xlsx
                - 'hts_calendar': HTS Site Visits Calendar
                - 'pm_assignments': PM_ZONE1_2_MARS_2026.xlsx
                - 'project_sites': Project sites BNS plan
                - 'critical_sites': RT High Risk List
        """
        try:
            # Load site master (File 1)
            if 'site_master' in file_dict:
                self.site_master = pd.read_excel(file_dict['site_master'], sheet_name=0)
                self.log_message(f"✅ Loaded Site Master: {len(self.site_master)} sites")
            
            # Load HTS Calendar (File 2)
            if 'hts_calendar' in file_dict:
                self.hts_calendar = pd.read_excel(file_dict['hts_calendar'], sheet_name='Planning')
                self.log_message(f"✅ Loaded HTS Calendar: {self.hts_calendar.shape}")
            
            # Load PM Assignments (File 3)
            if 'pm_assignments' in file_dict:
                self.pm_assignments = pd.read_excel(file_dict['pm_assignments'])
                self.log_message(f"✅ Loaded PM Assignments: {len(self.pm_assignments)} records")
            
            # Load Project Sites (File 4)
            if 'project_sites' in file_dict:
                df = pd.read_excel(file_dict['project_sites'])
                # Clean up the dataframe - remove empty rows/columns
                df = df.dropna(how='all').dropna(axis=1, how='all')
                self.project_sites = df
                self.log_message(f"✅ Loaded Project Sites: {len(self.project_sites)} sites")
            
            # Load Critical Sites (File 5)
            if 'critical_sites' in file_dict:
                self.critical_sites = pd.read_excel(file_dict['critical_sites'])
                self.log_message(f"✅ Loaded Critical Sites: {len(self.critical_sites)} sites")
            
            return True
        
        except Exception as e:
            self.log_message(f"❌ Error loading files: {str(e)}")
            return False
    
    def extract_site_ids(self) -> set:
        """Extract all unique site IDs from all sources."""
        site_ids = set()
        
        if self.site_master is not None:
            cols = [c for c in self.site_master.columns if 'id' in c.lower() or 'sid' in c.lower()]
            for col in cols:
                site_ids.update(self.site_master[col].dropna().unique())
        
        if self.pm_assignments is not None:
            cols = [c for c in self.pm_assignments.columns if 'id' in c.lower() or 'sid' in c.lower()]
            for col in cols:
                site_ids.update(self.pm_assignments[col].dropna().unique())
        
        if self.critical_sites is not None:
            cols = [c for c in self.critical_sites.columns if 'id' in c.lower() or 'sid' in c.lower()]
            for col in cols:
                site_ids.update(self.critical_sites[col].dropna().unique())
        
        self.log_message(f"📊 Total unique sites identified: {len(site_ids)}")
        return site_ids
    
    def generate_april_schedule(self) -> pd.DataFrame:
        """Generate April visit schedule combining all sources."""
        self.log_message("Generating April schedule...")
        
        site_ids = self.extract_site_ids()
        schedule_data = []
        
        # Group visits by week for distribution
        april_start = datetime(2026, 4, 1)
        weeks = {}
        
        for site_id in site_ids:
            # Determine visit type
            visit_types = []
            
            # Check if in critical sites
            if self.critical_sites is not None:
                id_cols = [c for c in self.critical_sites.columns if 'id' in c.lower()]
                if any(self.critical_sites[col].isin([site_id]).any() for col in id_cols):
                    visit_types.append('CRITICAL')
            
            # Check if in PM assignments
            if self.pm_assignments is not None:
                id_cols = [c for c in self.pm_assignments.columns if 'id' in c.lower()]
                if any(self.pm_assignments[col].isin([site_id]).any() for col in id_cols):
                    visit_types.append('PM')
            
            # Check if in project sites
            if self.project_sites is not None:
                id_cols = [c for c in self.project_sites.columns if 'id' in c.lower()]
                if any(self.project_sites[col].isin([site_id]).any() for col in id_cols):
                    visit_types.append('PROJECT')
            
            if not visit_types:
                visit_types.append('ROUTINE')
            
            # Distribute across April (8 weeks of April)
            week_num = len(schedule_data) % 4 + 1
            week_date = april_start + timedelta(days=(week_num - 1) * 7)
            
            schedule_data.append({
                'Site ID': site_id,
                'Visit Type': ', '.join(visit_types),
                'Priority': 'HIGH' if 'CRITICAL' in visit_types else ('MEDIUM' if 'PM' in visit_types else 'LOW'),
                'Scheduled Week': f"Week {week_num}",
                'Target Date': week_date,
                'Status': 'Scheduled',
                'Team': '',
                'Duration (hours)': 4 if 'CRITICAL' in visit_types else 2
            })
        
        self.april_schedule = pd.DataFrame(schedule_data)
        self.log_message(f"✅ April schedule generated: {len(self.april_schedule)} visits")
        return self.april_schedule
    
    def analyze_pm_workload(self) -> pd.DataFrame:
        """Analyze workload by PM zone/assignment."""
        if self.pm_assignments is None:
            return pd.DataFrame()
        
        self.log_message("Analyzing PM workload...")
        
        # Group by assignment column
        assigned_col = [c for c in self.pm_assignments.columns if 'assigned' in c.lower()]
        
        if assigned_col:
            workload = self.pm_assignments.groupby(assigned_col[0]).size().reset_index(name='Count')
            workload['Percentage'] = (workload['Count'] / workload['Count'].sum() * 100).round(2)
            self.log_message(f"✅ PM workload analysis: {len(workload)} assignments")
            return workload
        
        return pd.DataFrame()
    
    def identify_high_priority_sites(self) -> pd.DataFrame:
        """Identify high priority sites requiring immediate attention."""
        high_priority = []
        
        if self.critical_sites is not None:
            # Get sites marked as failed or P0/P1
            priority_col = [c for c in self.critical_sites.columns if 'priority' in c.lower()]
            
            if priority_col:
                critical_sites_list = self.critical_sites[
                    self.critical_sites[priority_col[0]].isin(['P0', 'P1'])
                ]
                high_priority.append(critical_sites_list)
        
        if high_priority:
            result = pd.concat(high_priority, ignore_index=True)
            self.log_message(f"✅ High priority sites identified: {len(result)}")
            return result
        
        return pd.DataFrame()
    
    def create_summary_statistics(self) -> Dict:
        """Create summary statistics for the report."""
        stats = {
            'Report Date': self.report_date.strftime("%B %Y"),
            'Total Sites Scheduled': len(self.april_schedule) if self.april_schedule is not None else 0,
            'Critical Sites': 0,
            'PM Sites': 0,
            'Project Sites': 0,
            'Routine Sites': 0,
            'Total PM Hours': 0,
            'High Priority Count': 0
        }
        
        if self.april_schedule is not None:
            stats['Critical Sites'] = (self.april_schedule['Visit Type'] == 'CRITICAL').sum()
            stats['PM Sites'] = self.april_schedule['Visit Type'].str.contains('PM', na=False).sum()
            stats['Project Sites'] = self.april_schedule['Visit Type'].str.contains('PROJECT', na=False).sum()
            stats['Routine Sites'] = (self.april_schedule['Visit Type'] == 'ROUTINE').sum()
            stats['Total PM Hours'] = self.april_schedule['Duration (hours)'].sum()
        
        high_priority = self.identify_high_priority_sites()
        stats['High Priority Count'] = len(high_priority)
        
        self.summary_stats = stats
        self.log_message(f"✅ Summary statistics created")
        return stats
    
    def create_excel_report(self, output_filename: str = "HT_Site_Visit_Calendar_April_2026.xlsx"):
        """Create comprehensive Excel report with multiple sheets."""
        self.log_message(f"Creating Excel report: {output_filename}")
        
        output_path = self.output_folder / output_filename
        
        # Create workbook
        wb = Workbook()
        wb.remove(wb.active)  # Remove default sheet
        
        # 1. Summary Sheet
        ws_summary = wb.create_sheet("Summary", 0)
        self._write_summary_sheet(ws_summary)
        
        # 2. April Schedule Sheet
        if self.april_schedule is not None:
            ws_schedule = wb.create_sheet("April Schedule", 1)
            self._write_dataframe_sheet(ws_schedule, self.april_schedule, "Site Visit Schedule")
        
        # 3. High Priority Sites
        high_priority = self.identify_high_priority_sites()
        if not high_priority.empty:
            ws_priority = wb.create_sheet("High Priority", 2)
            self._write_dataframe_sheet(ws_priority, high_priority.head(50), "High Priority Sites")
        
        # 4. PM Workload Analysis
        pm_workload = self.analyze_pm_workload()
        if not pm_workload.empty:
            ws_pm = wb.create_sheet("PM Workload", 3)
            self._write_dataframe_sheet(ws_pm, pm_workload, "PM Assignment Summary")
        
        # 5. Analysis Log
        ws_log = wb.create_sheet("Analysis Log", 4)
        self._write_log_sheet(ws_log)
        
        # Save
        wb.save(output_path)
        self.log_message(f"✅ Report saved: {output_path}")
        return output_path
    
    def _write_summary_sheet(self, ws):
        """Write summary statistics to sheet."""
        ws['A1'] = 'HTS SITE VISIT CALENDAR - APRIL 2026'
        ws['A1'].font = Font(size=14, bold=True, color="FFFFFF")
        ws['A1'].fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
        ws.merge_cells('A1:D1')
        
        row = 3
        ws[f'A{row}'] = 'Report Summary'
        ws[f'A{row}'].font = Font(size=12, bold=True)
        
        row += 2
        if self.summary_stats:
            for key, value in self.summary_stats.items():
                ws[f'A{row}'] = key
                ws[f'B{row}'] = value
                row += 1
        
        # Auto-fit columns
        ws.column_dimensions['A'].width = 30
        ws.column_dimensions['B'].width = 15
    
    def _write_dataframe_sheet(self, ws, df: pd.DataFrame, title: str):
        """Write dataframe to sheet with formatting."""
        # Add title
        ws['A1'] = title
        ws['A1'].font = Font(size=12, bold=True, color="FFFFFF")
        ws['A1'].fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        ws.merge_cells(f'A1:{chr(65 + len(df.columns) - 1)}1')
        
        # Write dataframe
        for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 2):
            for c_idx, value in enumerate(row, 1):
                cell = ws.cell(row=r_idx, column=c_idx, value=value)
                
                # Format header
                if r_idx == 2:
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
        
        # Auto-fit columns
        for col_idx, col in enumerate(df.columns, 1):
            try:
                col_values = df[col].fillna('').astype(str)
                max_len = max(col_values.map(len).max() if col_values.map(len).max() > 0 else 0, len(col))
            except:
                max_len = len(col)
            ws.column_dimensions[chr(64 + col_idx)].width = min(max_len + 2, 40)
    
    def _write_log_sheet(self, ws):
        """Write analysis log to sheet."""
        ws['A1'] = 'Analysis Log'
        ws['A1'].font = Font(size=12, bold=True)
        
        for idx, msg in enumerate(self.log, 2):
            ws[f'A{idx}'] = msg
        
        ws.column_dimensions['A'].width = 100
    
    def run_analysis(self, files: Dict[str, str]) -> bool:
        """Execute complete analysis pipeline."""
        self.log_message("Starting April Site Visit Analysis...")
        
        if not self.load_files(files):
            return False
        
        self.generate_april_schedule()
        self.create_summary_statistics()
        self.create_excel_report()
        
        self.log_message("✅ Analysis complete!")
        return True


def main():
    parser = argparse.ArgumentParser(
        description='Generate April Site Visit Calendar from 5 file types'
    )
    parser.add_argument('--site-master', type=str, help='Path to site master file')
    parser.add_argument('--hts-calendar', type=str, help='Path to HTS calendar file')
    parser.add_argument('--pm-assignments', type=str, help='Path to PM assignments file')
    parser.add_argument('--project-sites', type=str, help='Path to project sites file')
    parser.add_argument('--critical-sites', type=str, help='Path to critical sites file')
    parser.add_argument('--output', type=str, default='output', help='Output folder')
    parser.add_argument('--report-name', type=str, default='HT_Site_Visit_Calendar_April_2026.xlsx',
                       help='Output report filename')
    
    args = parser.parse_args()
    
    # Create file dictionary
    files = {}
    if args.site_master:
        files['site_master'] = args.site_master
    if args.hts_calendar:
        files['hts_calendar'] = args.hts_calendar
    if args.pm_assignments:
        files['pm_assignments'] = args.pm_assignments
    if args.project_sites:
        files['project_sites'] = args.project_sites
    if args.critical_sites:
        files['critical_sites'] = args.critical_sites
    
    # Run generator
    generator = AprilReportGenerator(output_folder=args.output)
    success = generator.run_analysis(files)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
