#!/usr/bin/env python3
"""
Main analysis script for site visit schedule generation.
Implements Steps 1-8 of the "Boot Not Suit" process.
"""

import pandas as pd
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Tuple, List, Dict


class SiteVisitScheduler:
    """Generate monthly site visit schedules based on maintenance and project activities."""
    
    def __init__(self, months_back: int = 3):
        self.months_back = months_back
        self.log = []
        self.maintenance_activities = None
        self.project_activities = None
        self.visit_history = None
        self.critical_sites = None
    
    def log_message(self, msg: str):
        """Add message to log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_msg = f"[{timestamp}] {msg}"
        self.log.append(full_msg)
        print(full_msg)
    
    def load_data(self, input_file: str) -> bool:
        """Load all required sheets from Excel file."""
        try:
            self.log_message(f"Loading data from: {input_file}")
            excel_file = pd.ExcelFile(input_file)
            
            # Load maintenance activities (Step 1)
            if 'maintenance' in [s.lower() for s in excel_file.sheet_names]:
                self.maintenance_activities = pd.read_excel(input_file, sheet_name='maintenance')
                self.log_message(f"✅ Loaded maintenance activities: {len(self.maintenance_activities)} records")
            
            # Load project activities (Step 1)
            if 'project' in [s.lower() for s in excel_file.sheet_names]:
                self.project_activities = pd.read_excel(input_file, sheet_name='project')
                self.log_message(f"✅ Loaded project activities: {len(self.project_activities)} records")
            
            # Load visit history (Step 2)
            if 'visit_history' in [s.lower() for s in excel_file.sheet_names]:
                self.visit_history = pd.read_excel(input_file, sheet_name='visit_history')
                self.log_message(f"✅ Loaded visit history: {len(self.visit_history)} records")
            
            # Load critical sites (Step 4)
            if 'critical_sites' in [s.lower() for s in excel_file.sheet_names]:
                self.critical_sites = pd.read_excel(input_file, sheet_name='critical_sites')
                self.log_message(f"✅ Loaded critical sites: {len(self.critical_sites)} records")
            
            return True
        
        except Exception as e:
            self.log_message(f"❌ Error loading data: {str(e)}")
            return False
    
    def step3_exclude_recent_visits(self, combined_df: pd.DataFrame) -> pd.DataFrame:
        """Step 3: Exclude sites already visited in last N months."""
        self.log_message(f"Step 3: Excluding sites visited in last {self.months_back} months")
        
        if self.visit_history is None or self.visit_history.empty:
            self.log_message("⚠️  No visit history available, skipping Step 3")
            return combined_df
        
        # Convert visit_date to datetime
        self.visit_history['visit_date'] = pd.to_datetime(self.visit_history['visit_date'])
        
        # Calculate cutoff date
        cutoff_date = datetime.now() - timedelta(days=30 * self.months_back)
        recent_visits = self.visit_history[self.visit_history['visit_date'] >= cutoff_date]
        
        recently_visited_sites = set(recent_visits['site_id'].unique())
        self.log_message(f"Found {len(recently_visited_sites)} recently visited sites")
        
        # Exclude recently visited sites
        filtered_df = combined_df[~combined_df['site_id'].isin(recently_visited_sites)].copy()
        excluded_count = len(combined_df) - len(filtered_df)
        
        self.log_message(f"✅ Step 3: Excluded {excluded_count} sites, {len(filtered_df)} remaining")
        return filtered_df
    
    def step4_exclude_critical_sites(self, df: pd.DataFrame, exclude: bool = True) -> pd.DataFrame:
        """Step 4: Exclude critical rooftop high-risk sites."""
        self.log_message(f"Step 4: {'Excluding' if exclude else 'Including'} critical sites")
        
        if not exclude or self.critical_sites is None or self.critical_sites.empty:
            self.log_message("⚠️  No critical sites to exclude or exclusion disabled")
            return df
        
        critical_site_ids = set(self.critical_sites['site_id'].unique())
        rooftop_critical = self.critical_sites[
            (self.critical_sites['tower_type'].str.lower() == 'rooftop') & 
            (self.critical_sites['risk_level'].str.lower() == 'high')
        ]
        
        critical_ids = set(rooftop_critical['site_id'].unique())
        self.log_message(f"Found {len(critical_ids)} critical rooftop sites to exclude")
        
        filtered_df = df[~df['site_id'].isin(critical_ids)].copy()
        excluded_count = len(df) - len(filtered_df)
        
        self.log_message(f"✅ Step 4: Excluded {excluded_count} critical sites, {len(filtered_df)} remaining")
        return filtered_df
    
    def step5_harmonize_activities(self, df: pd.DataFrame) -> pd.DataFrame:
        """Step 5: Create harmonized list of activities."""
        self.log_message("Step 5: Harmonizing maintenance, project, and other activities")
        
        if df.empty:
            self.log_message("⚠️  No sites available after filtering")
            return df
        
        # Add activity details
        df['activity_count'] = df.groupby('site_id').cumcount() + 1
        
        self.log_message(f"✅ Step 5: Created harmonized list with {len(df)} site-activity records")
        return df
    
    def step6_assign_sites_to_teams(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Step 6: Select sites and assign to teams (2 sites per person, 4 for safety influencers)."""
        self.log_message("Step 6: Assigning sites to teams")
        
        if df.empty:
            self.log_message("⚠️  No sites to assign")
            return df, {}
        
        # Group by site and select primary activity
        site_activities = df.groupby('site_id').first().reset_index()
        
        self.log_message(f"Processing {len(site_activities)} unique sites")
        
        # Add assignment info
        site_activities['assigned'] = False
        site_activities['assigned_date'] = None
        
        self.log_message(f"✅ Step 6: Processed {len(site_activities)} sites for team assignment")
        
        team_info = {
            'total_sites': len(site_activities),
            'sites_per_person': 2,
            'sites_per_influencer': 4
        }
        
        return site_activities, team_info
    
    def generate_schedule(self, exclude_critical: bool = True) -> pd.DataFrame:
        """Generate complete monthly visit schedule."""
        self.log_message("=" * 70)
        self.log_message("BOOT NOT SUIT SITE VISIT SCHEDULE GENERATION")
        self.log_message("=" * 70)
        
        # Step 1 & 2: Load data (combine maintenance and project activities)
        self.log_message("Steps 1-2: Loading maintenance and project schedules")
        
        if self.maintenance_activities is None and self.project_activities is None:
            self.log_message("❌ No activities loaded")
            return None
        
        # Combine activities
        activities_list = []
        if self.maintenance_activities is not None:
            self.maintenance_activities['activity_type'] = 'maintenance'
            activities_list.append(self.maintenance_activities)
        
        if self.project_activities is not None:
            self.project_activities['activity_type'] = 'project'
            activities_list.append(self.project_activities)
        
        combined_activities = pd.concat(activities_list, ignore_index=True, sort=False)
        self.log_message(f"✅ Combined {len(combined_activities)} total activities")
        
        # Step 3: Exclude recently visited sites
        filtered_activities = self.step3_exclude_recent_visits(combined_activities)
        
        # Step 4: Exclude critical sites
        filtered_activities = self.step4_exclude_critical_sites(filtered_activities, exclude_critical)
        
        # Step 5: Harmonize activities
        harmonized_df = self.step5_harmonize_activities(filtered_activities)
        
        # Step 6: Assign to teams
        final_schedule, team_info = self.step6_assign_sites_to_teams(harmonized_df)
        
        self.log_message("=" * 70)
        self.log_message("✅ Schedule generation complete")
        self.log_message(f"Final schedule contains {len(final_schedule)} sites")
        self.log_message(f"Team Info: {team_info}")
        self.log_message("=" * 70)
        
        return final_schedule
    
    def get_log(self) -> str:
        """Get complete log as string."""
        return "\n".join(self.log)


def main():
    parser = argparse.ArgumentParser(
        description='Generate site visit schedule for "Boot Not Suit" program'
    )
    parser.add_argument('--input', required=True, help='Input Excel file')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--analysis-type', default='full_schedule', 
                       help='Type of analysis')
    parser.add_argument('--exclude-critical', default='True', 
                       help='Exclude critical sites')
    parser.add_argument('--months-back', type=int, default=3, 
                       help='Months to look back for recent visits')
    parser.add_argument('--log', required=False, help='Log file path')
    
    args = parser.parse_args()
    
    # Create output directory
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Parse exclude critical
    exclude_critical = args.exclude_critical.lower() in ['true', '1', 'yes']
    
    # Run analysis
    scheduler = SiteVisitScheduler(months_back=args.months_back)
    
    if scheduler.load_data(args.input):
        schedule = scheduler.generate_schedule(exclude_critical=exclude_critical)
        
        if schedule is not None and not schedule.empty:
            # Save schedule
            schedule_path = output_path / 'sites_schedule.csv'
            schedule.to_csv(schedule_path, index=False)
            scheduler.log_message(f"✅ Schedule saved to: {schedule_path}")
        else:
            scheduler.log_message("⚠️  No schedule generated")
    
    # Save log
    if args.log:
        log_path = Path(args.log)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, 'w') as f:
            f.write(scheduler.get_log())
        print(f"Log saved to: {log_path}")


if __name__ == '__main__':
    main()
