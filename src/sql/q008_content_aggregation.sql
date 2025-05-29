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
select dcs.content_id,
count(distinct fvs.user_key) as distinct_users,
sum(fvs.view_duration_seconds) as total_watch_time
 from 
fact_viewing_sessions_streaming fvs
left join dim_content_streaming dcs on dcs.content_key = fvs.content_key
group by dcs.content_id
