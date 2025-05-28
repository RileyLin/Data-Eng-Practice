/*
Question 6.3.1: Valid Post Reads

Write a SQL query to count the number of valid post reads per user for the last 7 days. 
A valid read is defined as either:
1. The post was viewed for at least 5 seconds (view_time_ms >= 5000)
2. The post reached at least 80% visibility on screen (visibility_percent >= 80.0)

Schema (from scenario_6_news_feed_setup.sql):
fact_feed_events_feed:
- event_id (PK)
- user_key (FK)
- content_item_key (FK) -- Represents the post
- event_type_key (FK)
- event_timestamp (TIMESTAMP)
- view_time_ms (INTEGER) -- Milliseconds the content was viewed
- visibility_percent (DECIMAL) -- Max percentage of content visible
- ...

dim_event_types_feed:
- event_type_key (PK)
- event_name (TEXT) -- e.g., 'view_start', 'impression', 'view_complete'
- ...

Expected Output:
- user_key
- valid_read_count (count of distinct content_item_key validly read by the user)
Ordered by valid_read_count DESC, then user_key ASC.
*/

-- Write your SQL query here:
WITH RelevantFeedEvents AS (
    SELECT
        ffe.user_key,
        ffe.content_item_key,
        ffe.view_time_ms,
        ffe.visibility_percent
    FROM
        fact_feed_events_feed ffe
    JOIN
        dim_event_types_feed det ON ffe.event_type_key = det.event_type_key
    WHERE
        ffe.event_timestamp >= (CURRENT_DATE - INTERVAL '7 days')
        AND ffe.event_timestamp < CURRENT_DATE
        -- Consider events that typically carry visibility/duration metrics
        AND det.event_name IN ('view_start', 'view_complete', 'impression', 'scroll_view') 
),
ValidReadsPerPost AS (
    SELECT DISTINCT -- Ensures one valid read per user-post combination in the period
        rfe.user_key,
        rfe.content_item_key
    FROM
        RelevantFeedEvents rfe
    WHERE
        (rfe.view_time_ms >= 5000) OR (rfe.visibility_percent >= 80.0)
)
SELECT
    vr.user_key,
    COUNT(vr.content_item_key) AS valid_read_count
FROM
    ValidReadsPerPost vr
GROUP BY
    vr.user_key
ORDER BY
    valid_read_count DESC,
    vr.user_key ASC; 