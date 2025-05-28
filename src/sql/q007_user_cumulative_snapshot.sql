/*
Question 3.3.1: User Cumulative Snapshot Update

Describe the logic and write/outline SQL for a batch process to update a user_cumulative_snapshot table 
(with total view time) using data from the daily fact_viewing_sessions. 
Address how to avoid scanning the full fact table for the daily delta and optimize the update.

Schema:
fact_viewing_sessions:
- session_id (PK)
- user_id
- content_id
- session_date (DATE) -- Date of the viewing session
- view_duration_seconds (INTEGER) -- Duration of this specific session
- ...

user_cumulative_snapshot:
- user_id (PK)
- total_view_time_seconds (BIGINT)
- last_updated_date (DATE)
- ...

Expected output: The user_cumulative_snapshot table should be updated.
*/

-- Logic Description is in the solution file.
-- SQL Outline (PostgreSQL syntax for MERGE or INSERT ON CONFLICT):

-- 1. Define the processing date (e.g., yesterday)
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
-- 3. Use MERGE (PostgreSQL 15+) or INSERT ON CONFLICT

-- Using INSERT ... ON CONFLICT DO UPDATE (Common PostgreSQL approach)
INSERT INTO user_cumulative_snapshot (user_id, total_view_time_seconds, last_updated_date)
SELECT
    delta.user_id,
    delta.daily_total_view_time,
    (CURRENT_DATE - INTERVAL '1 day') AS processing_date -- This should be last_updated_date
FROM
    DailyUserViewSummary delta
ON CONFLICT (user_id) DO UPDATE SET
    total_view_time_seconds = user_cumulative_snapshot.total_view_time_seconds + EXCLUDED.total_view_time_seconds,
    last_updated_date = EXCLUDED.last_updated_date;

-- For other databases like SQL Server, a MERGE statement would be more direct:
/*
MERGE INTO user_cumulative_snapshot snap
USING (
    SELECT
        fvs.user_id,
        SUM(fvs.view_duration_seconds) AS daily_total_view_time
    FROM
        fact_viewing_sessions fvs
    WHERE
        fvs.session_date = (CURRENT_DATE - INTERVAL '1 day')
    GROUP BY
        fvs.user_id
) AS delta
ON snap.user_id = delta.user_id
WHEN MATCHED THEN
    UPDATE SET 
        total_view_time_seconds = snap.total_view_time_seconds + delta.daily_total_view_time,
        last_updated_date = (CURRENT_DATE - INTERVAL '1 day')
WHEN NOT MATCHED BY TARGET THEN
    INSERT (user_id, total_view_time_seconds, last_updated_date)
    VALUES (delta.user_id, delta.daily_total_view_time, (CURRENT_DATE - INTERVAL '1 day'));
*/ 