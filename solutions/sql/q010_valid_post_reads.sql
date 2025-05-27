/*
Solution to Question 6.3.1: Valid Post Reads

Write a SQL query to count the number of valid post reads per user for the last 7 days. 
A valid read is defined as either:
1. The post was viewed for at least 5 seconds (view_time_ms >= 5000)
2. The post reached at least 80% visibility on screen (visibility_percent >= 80.0)
*/

-- Using schema from scenario_6_news_feed_setup.sql

WITH RelevantFeedEvents AS (
    -- Filter events for the last 7 days and identify potential read events
    -- Assuming 'view_start' or a generic 'view' event type captures these metrics.
    -- If impressions also have these metrics, they could be included or handled separately.
    SELECT
        ffe.user_key,
        ffe.content_item_key,
        ffe.event_timestamp,
        ffe.view_time_ms,
        ffe.visibility_percent,
        det.event_name
    FROM
        fact_feed_events_feed ffe
    JOIN
        dim_event_types_feed det ON ffe.event_type_key = det.event_type_key
    WHERE
        ffe.event_timestamp >= (CURRENT_DATE - INTERVAL '7 days')
        AND ffe.event_timestamp < CURRENT_DATE
        AND det.event_name IN ('view_start', 'view', 'impression') -- Adjust if only specific event types carry these metrics
        -- We are interested in any event that records view_time_ms or visibility_percent for a content item by a user.
),
ValidReadsPerPost AS (
    -- Determine if each interaction with a post by a user counts as a valid read
    -- This CTE helps to ensure that a single post is counted only once per user even if multiple events qualify it.
    SELECT DISTINCT
        rfe.user_key,
        rfe.content_item_key
    FROM
        RelevantFeedEvents rfe
    WHERE
        (rfe.view_time_ms >= 5000) OR (rfe.visibility_percent >= 80.0)
)
SELECT
    vr.user_key,
    COUNT(vr.content_item_key) AS valid_read_count -- Counts distinct posts validly read by the user
FROM
    ValidReadsPerPost vr
GROUP BY
    vr.user_key
ORDER BY
    valid_read_count DESC,
    vr.user_key ASC;

/*
Explanation:

1.  `RelevantFeedEvents` CTE:
    *   Selects feed events from `fact_feed_events_feed` that occurred in the last 7 full days.
    *   Joins with `dim_event_types_feed` to filter for event types that are likely to carry `view_time_ms` and `visibility_percent` metrics. This might include events like 'view_start', a generic 'view', or even 'impression' if those impressions are instrumented with visibility data.
The choice of `event_name IN ('view_start', 'view', 'impression')` should be confirmed based on actual event instrumentation.
    *   Pulls `user_key`, `content_item_key`, `event_timestamp`, `view_time_ms`, and `visibility_percent`.

2.  `ValidReadsPerPost` CTE:
    *   Takes events from `RelevantFeedEvents`.
    *   Applies the conditions for a valid read: `(rfe.view_time_ms >= 5000)` OR `(rfe.visibility_percent >= 80.0)`.
    *   Uses `SELECT DISTINCT user_key, content_item_key` to ensure that if a user interacts with the same post multiple times within the 7-day window and several of those interactions qualify as a valid read (e.g., one event has long view time, another has high visibility), that post is still counted only once as a valid read for that user.

3.  Final `SELECT` Statement:
    *   Selects from `ValidReadsPerPost`.
    *   Groups by `user_key`.
    *   `COUNT(vr.content_item_key)` then counts the number of distinct posts that were validly read by each user.
    *   Results are ordered by the count of valid reads in descending order, and then by `user_key` for tie-breaking.

Schema from `scenario_6_news_feed_setup.sql` used:
-   `fact_feed_events_feed (user_key, content_item_key, event_type_key, event_timestamp, view_time_ms, visibility_percent)`
-   `dim_event_types_feed (event_type_key, event_name)`
-   `dim_users_feed (user_key, username)` (implicitly, for `user_key`)

Example (Conceptual - using data from `scenario_6_news_feed_setup.sql` if timestamps were recent):
Assume CURRENT_DATE is '2023-03-08'. Last 7 days means from '2023-03-01' to '2023-03-07'.

Sample data from `fact_feed_events_feed` for User 1 (user_key=1):
- Event for C001 (content_item_key=1) on '2023-03-01 11:00:00' (event_type 'impression', visibility_percent=100.0) -> Qualifies (visibility >= 80)
- Event for C002 (content_item_key=2) on '2023-03-01 11:00:05' (event_type 'impression', visibility_percent=80.0) -> Qualifies (visibility >= 80)
- Event for C001 (content_item_key=1) on '2023-03-01 11:00:10' (event_type 'view_start', visibility_percent=100.0) -> Qualifies (already counted C001 for user 1)
- Event for C001 (content_item_key=1) on '2023-03-01 11:05:00' (event_type 'view_complete', view_time_ms implied to be 5min*60*1000 = 300000ms) -> Qualifies (view_time >= 5000, C001 already counted for user 1)
- Event for C002 (content_item_key=2) on '2023-03-01 11:05:05' (event_type 'view_start', visibility_percent=90.0) -> Qualifies (already counted C002 for user 1)

So, for User 1, valid reads are for C001 and C002. Count = 2.

Sample data for User 2 (user_key=2):
- Event for C003 (content_item_key=3) on '2023-03-02 11:10:00' (event_type 'impression', visibility_percent=100.0) -> Qualifies.
- Event for C001 (content_item_key=1) on '2023-03-02 11:10:05' (event_type 'impression', visibility_percent=70.0, view_time_ms=NULL or <5000) -> Does NOT qualify.
- Event for C003 (content_item_key=3) on '2023-03-02 11:10:10' (event_type 'view_start', visibility_percent=100.0) -> Qualifies (C003 already counted for user 2).

So, for User 2, valid read is for C003. Count = 1.

Expected Output (Conceptual):
-- user_key | valid_read_count
-- ---------|-----------------
-- 1         | 2
-- 2         | 1
*/ 