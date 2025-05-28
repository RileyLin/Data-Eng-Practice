/*
Question 2.3.2: Posts with Reactions but No Comments

Calculate the percentage of content items (e.g., posts, videos) created today 
that received at least one 'reaction' event but zero 'comment' events on the same day.

Schema based on setup_scripts/scenario_2_short_video_setup.sql:

dim_posts_shortvideo:
- post_key (INTEGER PRIMARY KEY AUTOINCREMENT)
- post_id (VARCHAR(50) UNIQUE NOT NULL)
- created_timestamp (TEXT, ISO 8601 format)
- creator_user_key (INTEGER, FK to dim_users_shortvideo)
- original_post_key (INTEGER, FK to dim_posts_shortvideo)
- parent_post_key (INTEGER, FK to dim_posts_shortvideo)
- share_depth_level (INTEGER DEFAULT 0)
- is_original (BOOLEAN DEFAULT TRUE)
- content_text (TEXT)
- video_url (TEXT)

fact_engagement_events_shortvideo:
- event_id (INTEGER PRIMARY KEY AUTOINCREMENT)
- user_key (INTEGER, FK to dim_users_shortvideo)
- post_key (INTEGER, FK to dim_posts_shortvideo)
- engagement_type_key (INTEGER, FK to dim_engagement_types_shortvideo)
- event_timestamp (TEXT, ISO 8601 format)
- event_date_key (INTEGER, FK to dim_date)
- event_time_key (INTEGER, FK to dim_time)
- event_metadata (TEXT, JSON stored as TEXT)

dim_engagement_types_shortvideo:
- engagement_type_key (INTEGER PRIMARY KEY AUTOINCREMENT)
- engagement_type_name (TEXT UNIQUE NOT NULL) -- e.g., 'view', 'like', 'comment', 'share', 'reaction', 'follow'
- description (TEXT)
- is_active (BOOLEAN DEFAULT TRUE)

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