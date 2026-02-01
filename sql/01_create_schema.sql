-- ============================================
-- MITOCHONDRIAL DELETIONS DATABASE SCHEMA
-- ============================================

-- Table 1: SAMPLES
-- Stores one row per person with their metadata
CREATE TABLE IF NOT EXISTS samples (
    sample_id VARCHAR(100) PRIMARY KEY,  -- Unique identifier (UCI_10, UCI_11, etc.)
    diagnosis VARCHAR(50),                -- CTRL, SCZ, PD, AD, etc.
    sex VARCHAR(10),                      -- M or F
    age INTEGER,                          -- Age in years
    age_group VARCHAR(10),                -- Age bin: <30, 30-50, 50-70, 70+
    top30_cumulative_deletion_pct REAL    -- Sum of all 30 deletion percentages
);

-- Table 2: DELETIONS
-- Stores one row per sample-deletion combination (long format)
CREATE TABLE IF NOT EXISTS deletions (
    deletion_id INTEGER PRIMARY KEY,      -- Auto-increment unique ID
    sample_id VARCHAR(100),               -- Links to samples table
    deletion_name VARCHAR(50),            -- e.g., "6335_13999" (mtDNA positions)
    deletion_read_pct REAL,               -- Percentage of reads spanning this deletion
    FOREIGN KEY (sample_id) REFERENCES samples(sample_id)
);

-- ============================================
-- INDEXES FOR FASTER QUERIES
-- ============================================
-- These make lookups much faster (like a book index)

CREATE INDEX IF NOT EXISTS idx_samples_diagnosis ON samples(diagnosis);
CREATE INDEX IF NOT EXISTS idx_samples_age ON samples(age);
CREATE INDEX IF NOT EXISTS idx_samples_age_group ON samples(age_group);
CREATE INDEX IF NOT EXISTS idx_deletions_name ON deletions(deletion_name);
CREATE INDEX IF NOT EXISTS idx_deletions_sample ON deletions(sample_id);
