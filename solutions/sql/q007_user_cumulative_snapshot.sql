/*
Solution to Question 3.3.1: User Cumulative Snapshot Update

Describe the logic and write/outline SQL for a batch process to update a user_cumulative_snapshot table 
(with total view time) using data from the daily fact_viewing_sessions. 
Address how to avoid scanning the full fact table for the daily delta and optimize the update.
*/

/*
Logic Description:

Objective: Maintain a `user_cumulative_snapshot` table that stores the total view time for each user up to the latest processed date. 
This update should be efficient, using only the latest daily data from `fact_viewing_sessions` rather than re-scanning the entire history.

Tables Involved:
1.  `fact_viewing_sessions` (Source - daily delta):
    *   `user_id`
    *   `session_date` (or `date_key`)
    *   `view_duration_seconds` (for that session)
    *   Other relevant fields like `session_id`, `content_id`.
    *   Assumption: This table (or a view/staging table) contains only the sessions for the specific day being processed (e.g., yesterday's data).

2.  `user_cumulative_snapshot` (Target - to be updated):
    *   `user_id` (PK)
    *   `total_view_time_seconds` (cumulative sum)
    *   `last_updated_date` (the date up to which this snapshot is current)

Batch Process Steps (e.g., run daily for yesterday's data):

1.  **Identify Daily Delta:**
    *   Assume `fact_viewing_sessions` for the process date (e.g., `YESTERDAY_DATE`) contains only that day's session data. This is crucial for not scanning the full fact table.
    *   If `fact_viewing_sessions` is a large historical table, create a staging table or CTE that selects only the sessions for the specific `session_date` to be processed.
        Example: `SELECT user_id, SUM(view_duration_seconds) as daily_view_time FROM fact_viewing_sessions WHERE session_date = 'YESTERDAY_DATE' GROUP BY user_id;`

2.  **Aggregate Daily View Time per User:**
    *   From the daily delta (yesterday's sessions), calculate the total `view_duration_seconds` for each `user_id` for that specific day.
    *   Let's call this `daily_user_view_summary (user_id, daily_total_view_time)`.

3.  **Update Cumulative Snapshot:**
    *   Use a `MERGE` statement (if available in the SQL dialect, e.g., SQL Server, Oracle, PostgreSQL 15+) or an `INSERT ... ON CONFLICT DO UPDATE` (PostgreSQL) or separate `UPDATE` and `INSERT` logic.
    *   **For existing users in `user_cumulative_snapshot`:** Add their `daily_total_view_time` from `daily_user_view_summary` to their existing `total_view_time_seconds` in `user_cumulative_snapshot`. Update `last_updated_date` to `YESTERDAY_DATE`.
    *   **For new users (present in `daily_user_view_summary` but not in `user_cumulative_snapshot`):** Insert a new row into `user_cumulative_snapshot` with their `user_id`, `daily_total_view_time` as `total_view_time_seconds`, and `last_updated_date` as `YESTERDAY_DATE`.

Optimization & Considerations:
*   **Incremental Processing:** The core idea is that `fact_viewing_sessions` (or the derived daily delta) only contains new data for the processing day. This avoids full table scans of historical session data.
*   **Indexing:** 
    *   `fact_viewing_sessions` should be indexed on `session_date` (if it's a historical table) and `user_id`.
    *   `user_cumulative_snapshot` must have a primary key or unique index on `user_id` for efficient lookups during the MERGE/UPDATE.
*   **Staging Table for Daily Data:** If `fact_viewing_sessions` is very large and contains all history, it's best practice to first extract and aggregate the relevant day's data into a temporary or staging table. This staging table (`daily_user_view_summary`) would then be used to update the snapshot.
*   **Transaction Control:** The update process should be atomic (all or nothing) to ensure data consistency. Wrap the operations in a transaction.
*   **Idempotency:** Design the job to be idempotent. If it runs twice for the same day, it shouldn't double-count. This can be managed by:
    *   Ensuring the `daily_user_view_summary` strictly contains only that day's sum.
    *   The update logic itself: `total_view_time_seconds = user_cumulative_snapshot.total_view_time_seconds + daily_view_time`. If `daily_view_time` is consistently calculated for that specific day, re-running only adds that day's sum correctly if the snapshot wasn't updated, or if the snapshot has a `last_processed_session_date` and the update is conditional.
A common way is to update based on `last_updated_date` in snapshot vs. current processing date.
*   **Backfills/Reconciliation:** Have a strategy for backfills or recalculations if historical `fact_viewing_sessions` data is corrected or if the snapshot needs to be rebuilt from scratch for some reason (though this would be a full scan).
*/

-- SQL Outline (Conceptual - PostgreSQL syntax for MERGE or INSERT ON CONFLICT)

-- 0. Assume these tables exist:
/*
CREATE TABLE fact_viewing_sessions (
    session_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    content_id INTEGER,
    session_date DATE NOT NULL, -- Date of the viewing session
    view_duration_seconds INTEGER NOT NULL, -- Duration of this specific session
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_cumulative_snapshot (
    user_id INTEGER PRIMARY KEY,
    total_view_time_seconds BIGINT DEFAULT 0 NOT NULL,
    last_updated_date DATE NOT NULL
);

-- Index for snapshot table
CREATE UNIQUE INDEX IF NOT EXISTS idx_user_cumulative_snapshot_user_id ON user_cumulative_snapshot(user_id);
-- Index for fact table (if it's historical and large)
CREATE INDEX IF NOT EXISTS idx_fact_viewing_sessions_session_date ON fact_viewing_sessions(session_date);
CREATE INDEX IF NOT EXISTS idx_fact_viewing_sessions_user_id ON fact_viewing_sessions(user_id);
*/

-- 1. Define the processing date (e.g., yesterday)
-- In a real script, this would be a parameter or derived.
-- For this example, let's assume it's '2023-10-29'.
-- DEFINE processing_date DATE = CURRENT_DATE - INTERVAL '1 day';

-- 2. Create a CTE or Staging Table for the daily aggregated view time
WITH DailyUserViewSummary AS (
    SELECT
        fvs.user_id,
        SUM(fvs.view_duration_seconds) AS daily_total_view_time
    FROM
        fact_viewing_sessions fvs
    WHERE
        fvs.session_date = (CURRENT_DATE - INTERVAL '1 day') -- Process for yesterday's data
    GROUP BY
        fvs.user_id
)
-- 3. Use MERGE (PostgreSQL 15+) or INSERT ON CONFLICT for atomicity

-- Using MERGE (PostgreSQL 15+ example)
/*
MERGE INTO user_cumulative_snapshot snap
USING DailyUserViewSummary delta
ON snap.user_id = delta.user_id
WHEN MATCHED THEN
    UPDATE SET 
        total_view_time_seconds = snap.total_view_time_seconds + delta.daily_total_view_time,
        last_updated_date = (CURRENT_DATE - INTERVAL '1 day')
WHEN NOT MATCHED THEN
    INSERT (user_id, total_view_time_seconds, last_updated_date)
    VALUES (delta.user_id, delta.daily_total_view_time, (CURRENT_DATE - INTERVAL '1 day'));
*/

-- Using INSERT ... ON CONFLICT DO UPDATE (Common PostgreSQL approach prior to MERGE)
INSERT INTO user_cumulative_snapshot (user_id, total_view_time_seconds, last_updated_date)
SELECT
    delta.user_id,
    delta.daily_total_view_time,
    (CURRENT_DATE - INTERVAL '1 day') AS last_updated_date -- Corrected alias to match column name
FROM
    DailyUserViewSummary delta
ON CONFLICT (user_id) DO UPDATE SET
    total_view_time_seconds = user_cumulative_snapshot.total_view_time_seconds + EXCLUDED.total_view_time_seconds,
    last_updated_date = EXCLUDED.last_updated_date;

/*
Example DML for testing (assuming CURRENT_DATE is '2023-10-30'):
So, (CURRENT_DATE - INTERVAL '1 day') is '2023-10-29'.

-- Initial state of snapshot (optional, could be empty)
INSERT INTO user_cumulative_snapshot (user_id, total_view_time_seconds, last_updated_date) VALUES
(101, 1200, '2023-10-28'), -- User 101 already exists
(102, 300, '2023-10-28');  -- User 102 already exists

-- Yesterday's viewing sessions (for 2023-10-29)
INSERT INTO fact_viewing_sessions (user_id, session_date, view_duration_seconds) VALUES
(101, '2023-10-29', 300), -- User 101 watched more
(101, '2023-10-29', 150),
(103, '2023-10-29', 600), -- User 103 is a new user for the snapshot
(102, '2023-10-29', 50);  -- User 102 watched a bit more

-- After running the INSERT ON CONFLICT statement:
-- DailyUserViewSummary for '2023-10-29':
-- user_id | daily_total_view_time
-- --------|----------------------
-- 101     | 450
-- 102     | 50
-- 103     | 600

-- Expected state of user_cumulative_snapshot:
-- user_id | total_view_time_seconds | last_updated_date
-- --------|-------------------------|-------------------
-- 101     | 1650 (1200 + 450)       | 2023-10-29
-- 102     | 350  (300 + 50)         | 2023-10-29
-- 103     | 600                     | 2023-10-29
*/

-- To verify:
-- SELECT * FROM user_cumulative_snapshot ORDER BY user_id; 