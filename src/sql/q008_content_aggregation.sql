/*
Question 3.3.2: Content Aggregation

Given a watch_fact table (content_id, user_id, total_watch_time_seconds, date_key), 
write a query to get the distinct user count and sum of total watch time per content_id for a specific date.

Schema:
watch_fact:
- record_id (PK, optional)
- content_id (INTEGER)
- user_id (INTEGER)
- total_watch_time_seconds (INTEGER)
- date_key (INTEGER or DATE) -- e.g., YYYYMMDD format or actual DATE type

Expected Output:
- content_id
- distinct_user_count
- sum_total_watch_time_seconds
Ordered by content_id.
*/

-- Write your SQL query here:
SELECT
    wf.content_id,
    COUNT(DISTINCT wf.user_id) AS distinct_user_count,
    SUM(wf.total_watch_time_seconds) AS sum_total_watch_time_seconds
FROM
    watch_fact wf
WHERE
    wf.date_key = 20231029 -- Example: YYYYMMDD format for an integer date_key
    -- If date_key is a DATE type, use: wf.date_key = DATE '2023-10-29'
GROUP BY
    wf.content_id
ORDER BY
    wf.content_id; 