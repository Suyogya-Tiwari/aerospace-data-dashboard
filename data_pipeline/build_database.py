import pandas as pd
import sqlite3
import os

print("Downloading Global Space Launch Dataset...")
csv_url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-01-15/launches.csv"

df = pd.read_csv(csv_url)
print(f"Downloaded {len(df)} total global launches. Cleaning data...")

def assign_agency(row):
    agency_str = str(row.get('agency', ''))
    state_code = str(row.get('state_code', ''))
    
    if state_code == 'IN':
        return 'ISRO'
    elif 'SPX' in agency_str or 'SpaceX' in agency_str:
        return 'SpaceX'
    elif state_code == 'US':
        return 'NASA'
    return 'Other'

df['dashboard_agency'] = df.apply(assign_agency, axis=1)

final_df = df[['dashboard_agency', 'launch_year', 'type', 'category']].copy()
final_df.columns = ['agency', 'year', 'rocket_type', 'success_status']
final_df['is_success'] = final_df['success_status'] == 'O'

print("Saving cleaned data to SQLite database...")

db_dir = os.path.join("..", "backend")
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

db_path = os.path.join(db_dir, "space_data.db")
conn = sqlite3.connect(db_path)
final_df.to_sql("launches", conn, if_exists="replace", index=False)
conn.close()

print(f"Success! Processed {len(final_df)} global records.")