import pandas as pd

# Load cleaned, meerged data
df = pd.read_csv('/Users/ginomontero/Documents/mitochondria-project/data/processed/samples_clean.csv')

# Clean all column names for SQL (lowercase, underscores, no hyphens)
df.columns = (df.columns
              .str.strip()
              .str.lower()
              .str.replace(' ', '_')
              .str.replace('-', '_')
              .str.replace('(', '')
              .str.replace(')', ''))

# Identify which columns are deletions (numeric columns with underscores, like "983_13803")
metadata_cols = ['sample_id', 'diagnosis', 'sex', 'age', 'age_group', 'top30_cumulative_deletion_pct']
# Check for any GEO/dbGaP columns to be kept or dropped
other_cols = [c for c in df.columns if 'geo' in c.lower() or 'dbgap' in c.lower() or 'rna' in c.lower() or 'dna' in c.lower()]

deletion_cols = [c for c in df.columns if c not in metadata_cols + other_cols]

print(f"Found {len(deletion_cols)} deletion columns")
print(f"Metadata columns: {metadata_cols}")
print(f"First 5 deletion columns: {deletion_cols[:5]}")

# === TABLE 1: samples ===
samples = df[metadata_cols].copy()
samples.to_csv('/Users/ginomontero/Documents/mitochondria-project/data/sql_imports/samples.csv', index=False)
print(f"\nCreated samples table: {len(samples)} rows, {len(samples.columns)} columns")

# === TABLE 2: deletions (long format) ===
deletions_long = df[['sample_id'] + deletion_cols].melt(
    id_vars=['sample_id'],
    var_name='deletion_name',
    value_name='deletion_read_pct'
)

# Add auto-increment ID
deletions_long['deletion_id'] = range(1, len(deletions_long) + 1)
deletions_long = deletions_long[['deletion_id', 'sample_id', 'deletion_name', 'deletion_read_pct']]

deletions_long.to_csv('/Users/ginomontero/Documents/mitochondria-project/data/sql_imports/deletions.csv', index=False)
print(f"Created deletions table: {len(deletions_long)} rows (long format)")
print(f" → {len(deletion_cols)} deletions × {len(samples)} samples = {len(deletions_long)} rows")

print("\n✅ SQL import files ready in data/sql_imports/")

