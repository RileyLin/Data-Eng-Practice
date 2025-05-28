/*
Question 2.3.2: Posts with Reactions but No Comments

Calculate the percentage of content items (e.g., posts, videos) created today 
that received at least one 'reaction' event but zero 'comment' events on the same day.

Schema based on setup_scripts/scenario_2_short_video_setup.sql:

dim_posts_shortvideo:
- post_key (PK)
- post_id (VARCHAR(50))
- created_timestamp (TEXT, ISO 8601 format)
- ...

fact_engagement_events_shortvideo:
- event_id (PK)
- post_key (FK)
- engagement_type_key (FK)
- event_timestamp (TEXT, ISO 8601 format)
- ...

dim_engagement_types_shortvideo:
- engagement_type_key (PK)
- engagement_type_name (TEXT) -- e.g., 'view', 'like', 'comment', 'share', 'reaction'
- ...

Expected output:
A single percentage value.
*/

-- Write your SQL query here:
WITH PostsCreatedToday AS (
    SELECT
        p.post_key,
        DATE(p.created_timestamp) as creation_date
    FROM
        dim_posts_shortvideo p
    WHERE
        DATE(p.created_timestamp) = DATE('now') -- Or your specific date for "today"
),
ReactionsToday AS (
    SELECT DISTINCT
        fee.post_key
    FROM
        fact_engagement_events_shortvideo fee
    JOIN
        PostsCreatedToday pct ON fee.post_key = pct.post_key
    JOIN
        dim_engagement_types_shortvideo det ON fee.engagement_type_key = det.engagement_type_key
    WHERE
        det.engagement_type_name = 'reaction' -- Assuming 'reaction' is a defined type
        AND DATE(fee.event_timestamp) = pct.creation_date
),
CommentsToday AS (
    SELECT DISTINCT
        fee.post_key
    FROM
        fact_engagement_events_shortvideo fee
    JOIN
        PostsCreatedToday pct ON fee.post_key = pct.post_key
    JOIN
        dim_engagement_types_shortvideo det ON fee.engagement_type_key = det.engagement_type_key
    WHERE
        det.engagement_type_name = 'comment'
        AND DATE(fee.event_timestamp) = pct.creation_date
),
EligiblePosts AS (
    SELECT
        rt.post_key
    FROM
        ReactionsToday rt
    LEFT JOIN
        CommentsToday ct ON rt.post_key = ct.post_key
    WHERE
        ct.post_key IS NULL
)
SELECT
    CASE
        WHEN (SELECT COUNT(*) FROM PostsCreatedToday) = 0 THEN 0.0
        ELSE (
            (SELECT COUNT(*) FROM EligiblePosts) * 100.0 / 
            (SELECT COUNT(*) FROM PostsCreatedToday)
        )
    END AS percentage_posts_reaction_no_comment; 