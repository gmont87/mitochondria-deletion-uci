import sqlite3
import pandas as pd
import os

# STEP 1: Create DATABASE FILE
# SQLite stores everything in one file (.db)
os.makedirs('../data', exist_ok=True)
conn = sqlite3.connect('/Users/ginomontero/Documents/mitochondria-project/data/mitochondria_deletions.db')
print("📁 Database file: /Users/ginomontero/Documents/mitochondria-project/data/mitochondria_deletions.db\n")

# STEP 2: CREATE TABLES (RUN SQL SCHEMA)

with open('/Users/ginomontero/Documents/mitochondria-project/sql/01_create_schema.sql', 'r') as f:
    schema_sql = f.read()
    conn.executescript(schema_sql)
    print("✅ Created tables: samples, deletions")
    print("✅ Created 5 indexes for fast queries\n")

# Step 3: IMPORT CSV DATA INTO TABLES

tables = ['samples', 'deletions']

for table in tables:
    # Read CSV
    file_path = f'/Users/ginomontero/Documents/mitochondria-project/data/sql_imports/{table}.csv'
    df = pd.read_csv(file_path)

    # Write to SQL (replace if table exists)
    df.to_sql(table, conn, if_exists='replace', index=False)

    # Verify it worked
    result = pd.read_sql(f"SELECT COUNT(*) as count FROM {table}", conn)
    count = result['count'][0]
    print(f"✅ Loaded {table}: {count:,} rows")

# Step 4: VERYIFY DATA INTEGRITY
print("\n🔍 Running integrity checks...")

# Check 1: Do all deletions reference valid sample?
orphans = pd.read_sql("""
    SELECT COUNT(*) as orphan_count
    FROM deletions d
    LEFT JOIN samples s ON d.sample_id = s.sample_id
    WHERE s.sample_id IS NULL
""", conn)
    
if orphans['orphan_count'][0] == 0:
    print("✅ All deletion records link to valid samples (no orphans)")
else:
    print(f"⚠️ Warning: {orphans['orphan_count'][0]} orphaned deletion records")

# Check 2: Sample counts match
samples_count = pd.read_sql("SELECT COUNT(DISTINCT sample_id) FROM samples", conn)['COUNT(DISTINCT sample_id)'][0]
deletions_samples = pd.read_sql("SELECT COUNT(DISTINCT sample_id) FROM deletions", conn)['COUNT(DISTINCT sample_id)'][0]

if samples_count == deletions_samples:
    print(f"✅ Sample counts match: {samples_count} samples in both tables")
else:
    print(f"⚠️ Mismatch: {samples_count} samples vs {deletions_samples} in deletions")

conn.close()
print("\n🎉 Database ready! You can now run SQL queries.\n")


