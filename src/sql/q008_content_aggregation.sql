/*
Question 3.3.2: Content Aggregation

Given a watch_fact table (content_id, user_id, total_watch_time_seconds, date_key), 
write a query to get the distinct user count and sum of total watch time per content_id for a specific date.

Schema based on setup_scripts/scenario_3_streaming_platform_setup.sql (mapping watch_fact to fact_viewing_sessions_streaming):

fact_viewing_sessions_streaming:
- viewing_session_id (INTEGER PRIMARY KEY AUTOINCREMENT)
- user_key (INTEGER, FK to dim_users_streaming) -> maps to user_id in question
- content_key (INTEGER, FK to dim_content_streaming) -> maps to content_id in question
- device_key (INTEGER)
- session_start_timestamp (TEXT)
- session_end_timestamp (TEXT)
- view_duration_seconds (INTEGER) -> maps to total_watch_time_seconds in question
- date_key (INTEGER, FK to dim_date) -> maps to date_key in question
- ... (other fields)

dim_content_streaming:
- content_key (INTEGER PRIMARY KEY AUTOINCREMENT)
- content_id (VARCHAR(50) UNIQUE NOT NULL) -- Use this as the output `content_id`
- title (TEXT NOT NULL)
- ... (other fields)

dim_users_streaming:
- user_key (INTEGER PRIMARY KEY AUTOINCREMENT)
- user_id (VARCHAR(50) UNIQUE NOT NULL)
- ... (other fields)

Expected Output:
- content_id (from dim_content_streaming.content_id)
- distinct_user_count
- sum_total_watch_time_seconds
Ordered by content_id.
*/

-- Write your SQL query here:
SELECT
    dcs.content_id, -- Select the public facing content_id
    COUNT(DISTINCT fvs.user_key) AS distinct_user_count,
    SUM(fvs.view_duration_seconds) AS sum_total_watch_time_seconds
FROM
    fact_viewing_sessions_streaming fvs
JOIN
    dim_content_streaming dcs ON fvs.content_key = dcs.content_key
WHERE
    fvs.date_key = 20230110 -- Example: YYYYMMDD format for an integer date_key from scenario_3_streaming_platform_setup.sql
    -- If date_key in fact table was a DATE type, use: fvs.date_key = DATE '2023-01-10'
GROUP BY
    dcs.content_id
ORDER BY
    dcs.content_id; 