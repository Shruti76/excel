#!/usr/bin/env python3
"""
Create a sample Excel template for testing the pipeline.
"""

import pandas as pd
from datetime import datetime, timedelta
import random

# Sample maintenance activities
maintenance_data = {
    'site_id': [f'SDK{i:04d}' for i in range(1, 21)],
    'site_name': [
        'DK_ZONE_B', 'DK_YOFF_OCEAN', 'DK_FASS_GRAND_MBAO', 'DK_DIAMALAYE_VDN',
        'DK_PKAGE_TOLL_DIAZ', 'DK_DALIFOR3', 'DK_CITE_FAYCAL', 'DK_SACRE_COEUR3_MONTAGNE',
        'DK_VDN_CPI', 'DK_ECHANGEUR_NORD_FOIRE', 'DK_MERMOZ_PYROTECH', 'DK_MALIKA_WAROUAYE',
        'DK_YOFF_TONGHOR', 'DL_TOUBA_MOSQUE', 'DK_PIKINE_OUEST3', 'DK_HANN_MARISTE',
        'DK_MERMOZ_SOTRAC', 'DK_SICAP_BAOBAB', 'TH_SALY_LAGON', 'DK_PIKINES'
    ],
    'nearest_hi': [56, 34, 8, 69, 98, 5, 12, 21, 30, 79, 82, 97, 70, 53, 74, 99, 118, 119, 140, 104],
    'tower_type': ['Rooftop'] * 15 + ['Greenfield'] * 5,
    'activity_type': ['maintenance'] * 20,
    'time_limit': ['09:00-17:00'] * 20
}

# Sample project activities
project_data = {
    'site_id': [f'PROJ{i:04d}' for i in range(1, 16)],
    'site_name': [
        'DK_PARCELLES_U6', 'DK_RUE_HOPITAL', 'DK_CITE_MAMELLES', 'DK_ILIM_GRAND_MEDINE',
        'DK_TERRAIN_KEUR_MB_FALL', 'DK_OUAKAM_MONUMENT', 'DK_REIF_SIPRES', 'DL_THIERNO_KANDJI2',
        'DL_TOUBA_MOSQ_OUEST', 'DK_GUEDIAWAYE2', 'DK_MBAO_SOMISCI', 'DK_SOTFEL',
        'DK_YOFF_LAYENNE', 'DK_PIKINE', 'DK_MAMELLES_AVIONS'
    ],
    'project_name': [
        'Network Expansion', 'Infrastructure Upgrade', 'Coverage Enhancement', 'Capacity Planning',
        'Site Optimization', 'Equipment Replacement', 'Maintenance Upgrade', 'Safety Improvement',
        'Performance Enhancement', 'Network Consolidation', 'Site Migration', 'Frequency Refarming',
        'Modernization', 'Site Upgrade', 'Network Integration'
    ],
    'department': ['Engineering'] * 15,
    'activity_type': ['project'] * 15,
    'time_limit': ['TBC'] * 15
}

# Sample visit history (sites visited in last 3 months)
visited_sites = [f'SDK{i:04d}' for i in range(1, 6)]
visit_dates = [
    datetime.now() - timedelta(days=15),
    datetime.now() - timedelta(days=25),
    datetime.now() - timedelta(days=35),
    datetime.now() - timedelta(days=45),
    datetime.now() - timedelta(days=60)
]

visit_history_data = {
    'site_id': visited_sites,
    'visit_date': visit_dates,
    'team_member': ['Team_Member_1', 'Team_Member_2', 'Team_Member_3', 'Team_Member_1', 'Team_Member_4']
}

# Sample critical sites
critical_sites_data = {
    'site_id': [f'SDK{i:04d}' for i in range(1, 6)],
    'site_name': ['DK_ZONE_B', 'DK_YOFF_OCEAN', 'DK_SACRE_COEUR3_MONTAGNE', 'DK_ECHANGEUR_NORD_FOIRE', 'DK_MALIKA_WAROUAYE'],
    'tower_type': ['Rooftop'] * 5,
    'risk_level': ['high', 'high', 'critical', 'high', 'medium'],
    'reason': [
        'Height hazard',
        'Ocean proximity',
        'Congested area',
        'High traffic',
        'Access difficulty'
    ]
}

# Create DataFrames
maintenance_df = pd.DataFrame(maintenance_data)
project_df = pd.DataFrame(project_data)
visit_history_df = pd.DataFrame(visit_history_data)
critical_sites_df = pd.DataFrame(critical_sites_data)

# Write to Excel
output_file = '/Users/shrutisohan/Desktop/excel/data/sample_schedule.xlsx'
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    maintenance_df.to_excel(writer, sheet_name='maintenance', index=False)
    project_df.to_excel(writer, sheet_name='project', index=False)
    visit_history_df.to_excel(writer, sheet_name='visit_history', index=False)
    critical_sites_df.to_excel(writer, sheet_name='critical_sites', index=False)

print(f"✅ Sample Excel template created: {output_file}")
print(f"   - Maintenance activities: {len(maintenance_df)} sites")
print(f"   - Project activities: {len(project_df)} projects")
print(f"   - Visit history: {len(visit_history_df)} records")
print(f"   - Critical sites: {len(critical_sites_df)} sites")
