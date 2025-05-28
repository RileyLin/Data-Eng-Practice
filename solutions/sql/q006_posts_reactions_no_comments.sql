/*
Solution to Question 2.3.2: Posts with Reactions but No Comments

Calculate the percentage of content items (e.g., posts, videos) created today 
that received at least one 'reaction' event but zero 'comment' events on the same day.
*/

-- Assuming 'today' means the current calendar date for the 'created_timestamp' and 'event_timestamp'.
-- Table names are based on scenario_2_short_video_setup.sql:
-- dim_posts_shortvideo (post_key, created_timestamp)
-- fact_engagement_events_shortvideo (post_key, engagement_type_key, event_timestamp)
-- dim_engagement_types_shortvideo (engagement_type_key, engagement_type_name)

WITH PostsCreatedToday AS (
    SELECT
        p.post_key,
        DATE(p.created_timestamp) AS creation_date -- Extract date part for comparison
    FROM
        dim_posts_shortvideo p
    WHERE
        DATE(p.created_timestamp) = DATE('now') -- Filter for posts created "today"
        -- For testing with fixed data, replace DATE('now') with a specific date string e.g., '2023-03-17'
),
ReactionsToday AS (
    SELECT DISTINCT -- A post only needs one reaction to count
        fee.post_key
    FROM
        fact_engagement_events_shortvideo fee
    JOIN
        PostsCreatedToday pct ON fee.post_key = pct.post_key -- Join with posts created today
    JOIN
        dim_engagement_types_shortvideo det ON fee.engagement_type_key = det.engagement_type_key
    WHERE
        det.engagement_type_name = 'reaction' -- Filter for 'reaction' type events
        AND DATE(fee.event_timestamp) = pct.creation_date -- Ensure reaction happened on the same day as creation
),
CommentsToday AS (
    SELECT DISTINCT -- A post only needs one comment to be excluded
        fee.post_key
    FROM
        fact_engagement_events_shortvideo fee
    JOIN
        PostsCreatedToday pct ON fee.post_key = pct.post_key -- Join with posts created today
    JOIN
        dim_engagement_types_shortvideo det ON fee.engagement_type_key = det.engagement_type_key
    WHERE
        det.engagement_type_name = 'comment' -- Filter for 'comment' type events
        AND DATE(fee.event_timestamp) = pct.creation_date -- Ensure comment happened on the same day as creation
),
EligiblePosts AS (
    -- Posts created today that have at least one reaction today AND no comments today
    SELECT
        rt.post_key
    FROM
        ReactionsToday rt
    LEFT JOIN
        CommentsToday ct ON rt.post_key = ct.post_key
    WHERE
        ct.post_key IS NULL -- This ensures no comments were found for the post that had a reaction
)
SELECT
    CASE
        WHEN (SELECT COUNT(*) FROM PostsCreatedToday) = 0 THEN 0.0 -- Avoid division by zero if no posts created today
        ELSE (
            (SELECT COUNT(*) FROM EligiblePosts) * 100.0 / 
            (SELECT COUNT(*) FROM PostsCreatedToday)
        )
    END AS percentage_posts_reaction_no_comment;

/*
Explanation:

1.  `PostsCreatedToday` CTE:
    *   Selects `post_key` for all posts created on the `CURRENT_DATE` (using `DATE('now')` for SQLite, adjust for other DBs).
    *   Also extracts `creation_date` for accurate same-day comparison with events.

2.  `ReactionsToday` CTE:
    *   Finds distinct `post_key`s from `PostsCreatedToday` that received at least one 'reaction' event (based on `dim_engagement_types_shortvideo.engagement_type_name`) on their `creation_date`.

3.  `CommentsToday` CTE:
    *   Finds distinct `post_key`s from `PostsCreatedToday` that received at least one 'comment' event on their `creation_date`.

4.  `EligiblePosts` CTE:
    *   Selects `post_key`s that are present in `ReactionsToday` (had a reaction on creation day).
    *   It then `LEFT JOIN`s with `CommentsToday`.
    *   The `WHERE ct.post_key IS NULL` condition filters to keep only those posts that had reactions but did NOT have comments on their creation day.

5.  Final `SELECT` Statement:
    *   Calculates the percentage: (`COUNT(EligiblePosts)` * 100.0) / `COUNT(PostsCreatedToday)`.
    *   A `CASE` statement handles the scenario where no posts were created today, returning 0.0 to prevent division by zero.

This query structure clearly separates the logic for identifying posts created today, posts with reactions, posts with comments, and then combines these to find the eligible posts for the percentage calculation.
*/ 