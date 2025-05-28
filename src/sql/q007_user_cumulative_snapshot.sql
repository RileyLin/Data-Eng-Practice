/*
Question 3.3.1: User Cumulative Snapshot Update

Describe the logic and write/outline SQL for a batch process to update a user_cumulative_snapshot table 
(with total view time) using data from the daily fact_viewing_sessions. 
Address how to avoid scanning the full fact table for the daily delta and optimize the update.

Schema based on setup_scripts/scenario_3_streaming_platform_setup.sql:

fact_viewing_sessions_streaming:
- viewing_session_id (INTEGER PRIMARY KEY AUTOINCREMENT)
- user_key (INTEGER, FK to dim_users_streaming)
- content_key (INTEGER, FK to dim_content_streaming)
- device_key (INTEGER, FK to dim_devices_streaming)
- session_start_timestamp (TEXT NOT NULL, ISO 8601 format)
- session_end_timestamp (TEXT, ISO 8601 format)
- view_duration_seconds (INTEGER) -- Duration of this specific session
- content_duration_seconds (INTEGER)
- completion_percentage (REAL)
- pause_count (INTEGER DEFAULT 0)
- seek_count (INTEGER DEFAULT 0)
- last_pause_timestamp (TEXT)
- watch_progress_seconds (INTEGER)
- is_completed (BOOLEAN DEFAULT FALSE)
- date_key (INTEGER, FK to dim_date) -- Date of session_start_timestamp, use this for daily delta
- time_key (INTEGER, FK to dim_time)
- session_guid (TEXT UNIQUE)
- client_version (TEXT)
- FOREIGN KEY (user_key) REFERENCES dim_users_streaming(user_key)
- FOREIGN KEY (content_key) REFERENCES dim_content_streaming(content_key)
- FOREIGN KEY (device_key) REFERENCES dim_devices_streaming(device_key)
- FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
- FOREIGN KEY (time_key) REFERENCES dim_time(time_key)

user_cumulative_snapshot: (Assumed structure, as it's the target table to be updated)
- user_key (PK, FK to dim_users_streaming.user_key)
- total_view_time_seconds (BIGINT)
- last_updated_date (DATE) -- Represents the date of the last processed batch from fact_viewing_sessions_streaming
- first_active_date (DATE)
- last_active_date (DATE)
- total_sessions_count (INTEGER)

dim_users_streaming:
- user_key (INTEGER PRIMARY KEY AUTOINCREMENT)
- user_id (VARCHAR(50) UNIQUE NOT NULL)
- ... (other attributes)

dim_date:
- date_key (INTEGER PRIMARY KEY)
- calendar_date (DATE UNIQUE)
- ... (other attributes)

Expected output: The user_cumulative_snapshot table should be updated.
*/

-- Logic Description is in the solution file.
-- SQL Outline (PostgreSQL syntax for MERGE or INSERT ON CONFLICT):

-- 1. Define the processing date (e.g., yesterday's date_key or calendar_date)
-- For this example, let's assume we use calendar_date from dim_date for `processing_date`
-- And that fact_viewing_sessions_streaming.date_key corresponds to dim_date.date_key

-- 2. Create a CTE or Staging Table for the daily aggregated view time
WITH DailyUserViewSummary AS (
    SELECT
        fvs.user_key,
        SUM(fvs.view_duration_seconds) AS daily_total_view_time,
        COUNT(DISTINCT fvs.session_guid) AS daily_sessions_count,
        d.calendar_date AS processing_calendar_date -- Get the actual date for updates
    FROM
        fact_viewing_sessions_streaming fvs
    JOIN
        dim_date d ON fvs.date_key = d.date_key
    WHERE
        d.calendar_date = (CURRENT_DATE - INTERVAL '1 day') -- Process for yesterday's data
    GROUP BY
        fvs.user_key, d.calendar_date
)
-- 3. Use MERGE (PostgreSQL 15+) or INSERT ON CONFLICT

-- Using INSERT ... ON CONFLICT DO UPDATE (Common PostgreSQL approach)
INSERT INTO user_cumulative_snapshot (user_key, total_view_time_seconds, last_updated_date, first_active_date, last_active_date, total_sessions_count)
SELECT
    delta.user_key,
    delta.daily_total_view_time,
    delta.processing_calendar_date, -- last_updated_date is the date of this batch
    delta.processing_calendar_date, -- first_active_date for new users
    delta.processing_calendar_date, -- last_active_date is updated to this batch date
    delta.daily_sessions_count
FROM
    DailyUserViewSummary delta
ON CONFLICT (user_key) DO UPDATE SET
    total_view_time_seconds = user_cumulative_snapshot.total_view_time_seconds + EXCLUDED.total_view_time_seconds,
    last_updated_date = EXCLUDED.last_updated_date, -- This is the processing_calendar_date from delta
    last_active_date = EXCLUDED.last_active_date,   -- This is also the processing_calendar_date from delta
    total_sessions_count = user_cumulative_snapshot.total_sessions_count + EXCLUDED.total_sessions_count
    -- first_active_date remains unchanged for existing users
;

-- For other databases like SQL Server, a MERGE statement would be more direct:
/*
MERGE INTO user_cumulative_snapshot snap
USING (
    SELECT
        fvs.user_key,
        SUM(fvs.view_duration_seconds) AS daily_total_view_time,
        COUNT(DISTINCT fvs.session_guid) AS daily_sessions_count,
        d.calendar_date AS processing_calendar_date
    FROM
        fact_viewing_sessions_streaming fvs
    JOIN
        dim_date d ON fvs.date_key = d.date_key
    WHERE
        d.calendar_date = (CURRENT_DATE - INTERVAL '1 day')
    GROUP BY
        fvs.user_key, d.calendar_date
) AS delta
ON snap.user_key = delta.user_key
WHEN MATCHED THEN
    UPDATE SET 
        total_view_time_seconds = snap.total_view_time_seconds + delta.daily_total_view_time,
        last_updated_date = delta.processing_calendar_date,
        last_active_date = delta.processing_calendar_date,
        total_sessions_count = snap.total_sessions_count + delta.daily_sessions_count
WHEN NOT MATCHED BY TARGET THEN
    INSERT (user_key, total_view_time_seconds, last_updated_date, first_active_date, last_active_date, total_sessions_count)
    VALUES (delta.user_key, delta.daily_total_view_time, delta.processing_calendar_date, delta.processing_calendar_date, delta.processing_calendar_date, delta.daily_sessions_count);
*/ 