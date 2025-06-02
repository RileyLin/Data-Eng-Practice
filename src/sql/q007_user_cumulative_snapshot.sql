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

-- SQL Solution using SELECT syntax with FULL OUTER JOIN and COALESCE
-- This approach simulates the update of the user_cumulative_snapshot table for a given processing date.
-- It avoids scanning the full fact_viewing_sessions_streaming table by processing only a daily delta.

-- 1. Define the processing date dynamically (e.g., yesterday's date).
--    The DailyUserViewSummary CTE will filter fact_viewing_sessions_streaming for this date.

WITH DailyUserViewSummary AS (
    -- Calculates daily aggregates for users from fact_viewing_sessions_streaming
    -- for a specific processing date (e.g., yesterday).
    SELECT
        fvs.user_key,
        SUM(fvs.view_duration_seconds) AS daily_total_view_time,
        COUNT(DISTINCT fvs.session_guid) AS daily_sessions_count,
        d.calendar_date AS processing_calendar_date -- The actual date of the data being processed
    FROM
        fact_viewing_sessions_streaming fvs
    JOIN
        dim_date d ON fvs.date_key = d.date_key
    WHERE
        -- This condition ensures only the delta for the specified date is processed.
        -- Replace with a specific date string like '''YYYY-MM-DD''' for fixed date processing if needed.
        d.calendar_date = (CURRENT_DATE - INTERVAL '''1 day''')
    GROUP BY
        fvs.user_key, d.calendar_date
),
CurrentSnapshot AS (
    -- Represents the current state of the user_cumulative_snapshot table.
    -- This CTE is used to clearly separate the existing snapshot data.
    SELECT
        user_key,
        total_view_time_seconds,
        last_updated_date,
        first_active_date,
        last_active_date,
        total_sessions_count
    FROM
        user_cumulative_snapshot -- This is the table we are conceptually updating
)
-- 2. Merge daily summary with current snapshot using FULL OUTER JOIN and COALESCE.
-- The SELECT statement below constructs the "new" state of the user_cumulative_snapshot.
-- In a batch update process, you might use this SELECT to repopulate the table
-- or use similar logic in an INSERT/UPDATE statement if the RDBMS doesn'''t support MERGE
-- or if a MERGE is not desired.
SELECT
    -- User Key: from snapshot or delta if new
    COALESCE(cs.user_key, dus.user_key) AS user_key,

    -- Total View Time: sum of existing (or 0 if new) and new daily view time (or 0 if no new activity)
    COALESCE(cs.total_view_time_seconds, 0) + COALESCE(dus.daily_total_view_time, 0) AS total_view_time_seconds,

    -- Last Updated Date:
    -- If user has new activity (in dus), it'''s the processing_calendar_date.
    -- Else (user only in cs, no new activity), it'''s their existing last_updated_date.
    COALESCE(dus.processing_calendar_date, cs.last_updated_date) AS last_updated_date,

    -- First Active Date:
    -- If user existed (in cs), keep their original first_active_date.
    -- Else (new user, only in dus), it'''s the processing_calendar_date.
    COALESCE(cs.first_active_date, dus.processing_calendar_date) AS first_active_date,

    -- Last Active Date:
    -- If user has new activity (in dus), it'''s the processing_calendar_date.
    -- Else (user only in cs, no new activity), it'''s their existing last_active_date.
    COALESCE(dus.processing_calendar_date, cs.last_active_date) AS last_active_date,

    -- Total Sessions Count: sum of existing (or 0 if new) and new daily sessions (or 0 if no new activity)
    COALESCE(cs.total_sessions_count, 0) + COALESCE(dus.daily_sessions_count, 0) AS total_sessions_count
FROM
    CurrentSnapshot cs
FULL OUTER JOIN
    DailyUserViewSummary dus ON cs.user_key = dus.user_key
;
