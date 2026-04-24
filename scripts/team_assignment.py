#!/usr/bin/env python3
"""
Team assignment and formation module.
Implements Steps 6-7: Team formation with technical and non-technical resources.
"""

import pandas as pd
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
import random


class TeamAssigner:
    """Assign sites to teams with balanced composition."""
    
    def __init__(self, sites_per_person: int = 2, sites_per_influencer: int = 4):
        self.sites_per_person = sites_per_person
        self.sites_per_influencer = sites_per_influencer
        self.log = []
        self.team_assignments = []
    
    def log_message(self, msg: str):
        """Log message with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_msg = f"[{timestamp}] {msg}"
        self.log.append(full_msg)
        print(full_msg)
    
    def load_schedule(self, schedule_file: str) -> pd.DataFrame:
        """Load sites schedule."""
        try:
            df = pd.read_csv(schedule_file)
            self.log_message(f"✅ Loaded {len(df)} sites from schedule")
            return df
        except Exception as e:
            self.log_message(f"❌ Error loading schedule: {str(e)}")
            return None
    
    def create_team_pairs(self, sites_df: pd.DataFrame, team_members: List[str]) -> List[Dict]:
        """
        Step 7: Form teams as pairs/trios with technical and non-technical resources.
        Rotate team composition monthly for variety.
        """
        self.log_message("Step 7: Forming teams with balanced composition")
        
        if not team_members or len(team_members) == 0:
            self.log_message("⚠️  No team members provided, generating default team")
            # Create default teams from site IDs
            team_members = [f"Team_Member_{i}" for i in range(1, 11)]
        
        teams = []
        
        # Separate technical and non-technical resources
        technical_resources = team_members[:len(team_members)//2]
        non_technical_resources = team_members[len(team_members)//2:]
        
        self.log_message(f"Technical resources: {len(technical_resources)}")
        self.log_message(f"Non-technical resources: {len(non_technical_resources)}")
        
        # Shuffle to create rotating combinations
        random.shuffle(technical_resources)
        random.shuffle(non_technical_resources)
        
        # Form pairs/trios
        pair_id = 1
        for i, technical in enumerate(technical_resources):
            non_tech_indices = [j % len(non_technical_resources) for j in range(i, i + 2)]
            non_tech_members = [non_technical_resources[j] for j in non_tech_indices]
            
            team = {
                'team_id': f'TEAM_{pair_id:03d}',
                'technical_lead': technical,
                'non_technical_members': ', '.join(non_tech_members),
                'team_size': 1 + len(non_tech_members),
                'sites_assigned': 0
            }
            teams.append(team)
            pair_id += 1
        
        self.log_message(f"✅ Created {len(teams)} team pairs/trios")
        return teams
    
    def assign_sites_to_teams(self, sites_df: pd.DataFrame, teams: List[Dict]) -> pd.DataFrame:
        """Assign each site to a team with time allocation."""
        self.log_message("Assigning sites to teams")
        
        assignments = []
        site_index = 0
        
        for site_idx, site in sites_df.iterrows():
            team_idx = site_index % len(teams)
            team = teams[team_idx]
            
            # Determine time limit based on activity type
            if 'activity_type' in site.index and site['activity_type'] == 'maintenance':
                time_limit = site.get('time_limit', 'As per schedule')
            else:
                time_limit = 'TBC'  # To Be Confirmed for projects
            
            assignment = {
                'site_id': site.get('site_id', f'SITE_{site_idx}'),
                'site_name': site.get('site_name', 'Unknown'),
                'team_id': team['team_id'],
                'technical_lead': team['technical_lead'],
                'non_technical_members': team['non_technical_members'],
                'activity_type': site.get('activity_type', 'other'),
                'time_limit': time_limit,
                'assigned_date': datetime.now().strftime('%Y-%m-%d')
            }
            assignments.append(assignment)
            site_index += 1
        
        assignment_df = pd.DataFrame(assignments)
        self.log_message(f"✅ Assigned {len(assignment_df)} sites to teams")
        
        return assignment_df
    
    def generate_team_summary(self, assignments_df: pd.DataFrame) -> pd.DataFrame:
        """Generate summary of teams and their assignments."""
        self.log_message("Generating team summary")
        
        team_summary = assignments_df.groupby('team_id').agg({
            'site_id': 'count',
            'technical_lead': 'first',
            'non_technical_members': 'first',
            'activity_type': lambda x: ', '.join(x.unique())
        }).rename(columns={'site_id': 'sites_assigned'}).reset_index()
        
        self.log_message(f"✅ Team summary created for {len(team_summary)} teams")
        
        return team_summary
    
    def get_log(self) -> str:
        """Get complete log."""
        return "\n".join(self.log)


def main():
    parser = argparse.ArgumentParser(
        description='Assign sites to teams'
    )
    parser.add_argument('--schedule', required=True, help='Sites schedule CSV file')
    parser.add_argument('--output', required=True, help='Output CSV file for assignments')
    parser.add_argument('--log', required=False, help='Log file path')
    parser.add_argument('--sites-per-person', type=int, default=2,
                       help='Number of sites per team member')
    parser.add_argument('--sites-per-influencer', type=int, default=4,
                       help='Number of sites per safety influencer')
    
    args = parser.parse_args()
    
    # Create output directory
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Run team assignment
    assigner = TeamAssigner(
        sites_per_person=args.sites_per_person,
        sites_per_influencer=args.sites_per_influencer
    )
    
    assigner.log_message("=" * 70)
    assigner.log_message("TEAM ASSIGNMENT PROCESS")
    assigner.log_message("=" * 70)
    
    # Load schedule
    sites_df = assigner.load_schedule(args.schedule)
    
    if sites_df is not None and not sites_df.empty:
        # Create teams
        default_team_members = [
            f"Member_{i}" for i in range(1, 11)
        ]
        teams = assigner.create_team_pairs(sites_df, default_team_members)
        
        # Assign sites
        assignments = assigner.assign_sites_to_teams(sites_df, teams)
        
        # Generate summary
        team_summary = assigner.generate_team_summary(assignments)
        
        # Save assignments
        assignments.to_csv(args.output, index=False)
        assigner.log_message(f"✅ Assignments saved to: {args.output}")
        
        # Save summary
        summary_path = output_path.parent / (output_path.stem + '_summary.csv')
        team_summary.to_csv(summary_path, index=False)
        assigner.log_message(f"✅ Team summary saved to: {summary_path}")
    
    # Save log
    if args.log:
        log_path = Path(args.log)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, 'w') as f:
            f.write(assigner.get_log())
        print(f"\nLog saved to: {log_path}")


if __name__ == '__main__':
    main()
