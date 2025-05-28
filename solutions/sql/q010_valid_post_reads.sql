/*
Solution to Question 6.3.1: Valid Post Reads

Write a SQL query to count the number of valid post reads per user for the last 7 days. 
A valid read is defined as either:
1. The post was viewed for at least 5 seconds (view_time_ms >= 5000)
2. The post reached at least 80% visibility on screen (visibility_percent >= 80.0)
*/

-- Schema (from scenario_6_news_feed_setup.sql):
-- fact_feed_events_feed (user_key, content_item_key, event_timestamp, view_time_ms, visibility_percent, event_type_key)
-- dim_event_types_feed (event_type_key, event_name)

WITH RelevantFeedEvents AS (
    SELECT
        ffe.user_key,
        ffe.content_item_key,
        MAX(ffe.view_time_ms) AS max_view_time_ms, -- Max view time for a user-post within the period
        MAX(ffe.visibility_percent) AS max_visibility_percent -- Max visibility for a user-post
    FROM
        fact_feed_events_feed ffe
    JOIN
        dim_event_types_feed det ON ffe.event_type_key = det.event_type_key
    WHERE
        ffe.event_timestamp >= (CURRENT_DATE - INTERVAL '7 days')
        AND ffe.event_timestamp < CURRENT_DATE
        -- It's important to select event types that actually record view_time_ms and visibility_percent.
        -- If a user has multiple events for the same post (e.g. impression then scroll), we want the max values.
        AND det.event_name IN ('view_start', 'view_complete', 'impression', 'scroll_view', 'content_view') -- Add other relevant event names
    GROUP BY
        ffe.user_key, ffe.content_item_key
),
ValidReadsPerPost AS (
    -- Determine if each user-post combination qualifies as a valid read based on aggregated metrics
    SELECT
        rfe.user_key,
        rfe.content_item_key
    FROM
        RelevantFeedEvents rfe
    WHERE
        (rfe.max_view_time_ms >= 5000) OR (rfe.max_visibility_percent >= 80.0)
)
SELECT
    vr.user_key,
    COUNT(vr.content_item_key) AS valid_read_count -- Count distinct posts that were validly read
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
    *   Filters `fact_feed_events_feed` for events within the last 7 days.
    *   Joins with `dim_event_types_feed` to filter by `event_name`. This is crucial because not all event types might populate `view_time_ms` or `visibility_percent`.
        We select events likely to have these metrics (e.g., 'impression', 'view_start', 'view_complete', 'scroll_view', 'content_view'). The exact names might vary based on the specific logging setup.
    *   Groups by `user_key` and `content_item_key` to aggregate metrics per user per post over the 7-day period.
    *   `MAX(ffe.view_time_ms)` and `MAX(ffe.visibility_percent)`: If a user interacts multiple times with the same post (e.g., multiple scroll events, or an impression followed by a longer view), we take the maximum recorded view time and visibility for that post by that user within the period to determine if any of those interactions met the criteria.

2.  `ValidReadsPerPost` CTE:
    *   Takes the output from `RelevantFeedEvents`.
    *   Applies the valid read criteria: `(rfe.max_view_time_ms >= 5000) OR (rfe.max_visibility_percent >= 80.0)`.
    *   This CTE will contain one row for each `user_key` and `content_item_key` that meets at least one of the valid read conditions. The `DISTINCT` keyword was used in the `src` file, but with the `GROUP BY` in `RelevantFeedEvents` and then selecting user_key, content_item_key here, it is implicitly distinct for user-post pairs.

3.  Final `SELECT` Statement:
    *   Selects `user_key` from `ValidReadsPerPost`.
    *   `COUNT(vr.content_item_key) AS valid_read_count`: Counts how many distinct `content_item_key` (posts) were validly read by each user.
    *   `GROUP BY vr.user_key`: Aggregates these counts per user.
    *   `ORDER BY valid_read_count DESC, vr.user_key ASC`: Orders the results as requested.

This approach ensures that each post is counted at most once per user as a "valid read" if any of their interactions with that post in the last 7 days met the criteria.
It also correctly handles multiple events for the same user-post by taking the maximum values for evaluation.
*/ 