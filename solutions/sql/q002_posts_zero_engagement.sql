/*
Solution to Question 2.3.1: Posts with Zero Engagement on Creation Day

Write a SQL query to find post_ids for posts that received zero 'like' or 'react' events 
on the same calendar day they were created.
*/

-- Using NOT EXISTS approach
SELECT p.post_id
FROM posts p
WHERE NOT EXISTS (
    SELECT 1
    FROM engagement_events e
    WHERE e.post_id = p.post_id
    AND e.event_type IN ('like', 'react') -- Assuming 'react' covers various reactions
    AND DATE(e.event_timestamp) = DATE(p.creation_timestamp)
)
ORDER BY p.post_id;

/*
Explanation:

1.  The query aims to find `post_id`s from a `posts` table that have no corresponding 'like' or 'react' events in an `engagement_events` table on the day the post was created.

2.  `posts` table (aliased as `p`):
    *   Assumed to have `post_id` (PK) and `creation_timestamp` (when the post was made).

3.  `engagement_events` table (aliased as `e`):
    *   Assumed to have `event_id` (PK), `post_id` (FK to `posts`), `event_type` (e.g., 'like', 'react', 'comment', 'share', 'view'), and `event_timestamp`.

4.  `NOT EXISTS` Subquery:
    *   This is an efficient way to find posts that do not have any matching engagement events satisfying the specified criteria.
    *   The subquery `SELECT 1 FROM engagement_events e WHERE ...` attempts to find at least one engagement event for the current post `p` from the outer query that meets the conditions.
    *   If the subquery finds no such rows (i.e., no 'like' or 'react' on the creation day), `NOT EXISTS` evaluates to true, and the `post_id` from the outer query is included in the result.

5.  Conditions within the Subquery:
    *   `e.post_id = p.post_id`: Links the engagement event to the post from the outer query.
    *   `e.event_type IN ('like', 'react')`: Filters for only 'like' or 'react' types of engagement. The term 'react' could encompass various reactions (e.g., love, haha, wow) if the platform supports them beyond simple likes.
    *   `DATE(e.event_timestamp) = DATE(p.creation_timestamp)`: This is the crucial condition. It ensures that the engagement event occurred on the exact same calendar day as the post's creation. The `DATE()` function extracts the date part from a timestamp, ignoring the time.

6.  `ORDER BY p.post_id`: The results are ordered by `post_id` for consistent output.

Alternative using LEFT JOIN:

SELECT p.post_id
FROM posts p
LEFT JOIN engagement_events e ON p.post_id = e.post_id
    AND e.event_type IN ('like', 'react')
    AND DATE(e.event_timestamp) = DATE(p.creation_timestamp)
WHERE e.event_id IS NULL -- No matching engagement event found
ORDER BY p.post_id;

This alternative joins `posts` with `engagement_events` based on the criteria. If a post has no matching engagement events, the columns from `engagement_events` (like `e.event_id`) will be `NULL`. The `WHERE e.event_id IS NULL` clause then filters to keep only those posts.
Both approaches are valid, with `NOT EXISTS` often being more performant on large datasets for this type of check.

Schema Assumptions:
posts:
- post_id (PK)
- user_id (FK, creator)
- creation_timestamp
- content_text / content_url

engagement_events:
- event_id (PK)
- post_id (FK -> posts)
- user_id (FK, user who engaged)
- event_type ('like', 'react', 'comment', 'share', 'view')
- event_timestamp

Example DDL & DML for testing:

DROP TABLE IF EXISTS engagement_events;
DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    post_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    creation_timestamp TIMESTAMP
);

CREATE TABLE engagement_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER,
    user_id INTEGER,
    event_type TEXT,
    event_timestamp TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);

INSERT INTO posts (post_id, user_id, creation_timestamp) VALUES
(1, 101, '2023-03-15 10:00:00'), -- Post 1, created Mar 15
(2, 102, '2023-03-15 12:00:00'), -- Post 2, created Mar 15
(3, 101, '2023-03-16 09:00:00'), -- Post 3, created Mar 16
(4, 103, '2023-03-16 14:00:00'); -- Post 4, created Mar 16

INSERT INTO engagement_events (post_id, user_id, event_type, event_timestamp) VALUES
-- Post 1: gets a like on creation day
(1, 102, 'like', '2023-03-15 11:00:00'),
-- Post 1: gets a comment on a different day (not relevant for this query)
(1, 103, 'comment', '2023-03-16 10:00:00'),
-- Post 2: gets a view on creation day (not a like/react)
(2, 101, 'view', '2023-03-15 13:00:00'),
-- Post 2: gets a like on the next day (not creation day)
(2, 103, 'like', '2023-03-16 14:00:00'),
-- Post 3: gets a react on creation day
(3, 102, 'react', '2023-03-16 09:30:00'),
-- Post 4: no likes/reacts on creation day (or any day in this sample)
(4, 101, 'view', '2023-03-16 15:00:00');

-- Expected output:
-- Post 1: Has a 'like' on creation day. Not included.
-- Post 2: No 'like' or 'react' on creation day (view doesn't count, like is on next day). Included.
-- Post 3: Has a 'react' on creation day. Not included.
-- Post 4: No 'like' or 'react' on creation day (view doesn't count). Included.

-- post_id
-- -------
-- 2
-- 4
*/

-- q002_posts_zero_engagement.sql
-- Identify posts that have received zero engagement (likes, comments, shares).

-- Assumptions (based on scenario_6_news_feed_setup.sql):
-- 1. `dim_content_items_feed` contains all posts with `content_item_key` and `title`.
-- 2. `fact_feed_events_feed` logs all interactions with `content_item_key` and `event_type_key`.
-- 3. `dim_event_types_feed` maps `event_type_key` to `event_name`. 
--    Engagement events are identified by names like 'like', 'comment', 'share_intent', 'click'.
--    (Note: 'view_start', 'view_complete', 'impression' are considered views/impressions, not direct engagement for this query).

-- Methodology:
-- 1. Create a CTE `EngagementEventTypes` to list the `event_type_key`s that represent engagement.
-- 2. Create a CTE `PostsWithEngagement` to find all `content_item_key`s that have at least one 
--    engagement event recorded in `fact_feed_events_feed`.
-- 3. Select all posts from `dim_content_items_feed` that are NOT IN `PostsWithEngagement`.

WITH EngagementEventTypes AS (
    SELECT event_type_key
    FROM dim_event_types_feed
    WHERE event_name IN ('like', 'comment', 'share_intent', 'click') -- Define what constitutes engagement
),
PostsWithEngagement AS (
    SELECT DISTINCT fef.content_item_key
    FROM fact_feed_events_feed fef
    JOIN EngagementEventTypes eet ON fef.event_type_key = eet.event_type_key
)
SELECT
    dci.content_item_key,
    dci.title,
    dci.content_type,
    dci.created_timestamp
FROM
    dim_content_items_feed dci
LEFT JOIN
    PostsWithEngagement pwe ON dci.content_item_key = pwe.content_item_key
WHERE
    pwe.content_item_key IS NULL
ORDER BY
    dci.created_timestamp DESC;

-- To test with scenario_6_news_feed_setup.sql data:
-- The provided sample data has engagement for C001 (click, like via user A and B indirectly) and C003 (like via user B).
-- C002 (Global Summit Highlights) has an impression and view_start, but no direct likes, comments, shares, or clicks in the sample.
-- So, C002 should be the one listed as having zero engagement based on the chosen engagement types.

-- If we run the setup script and then this query:
-- dim_event_types_feed:
-- (1, 'impression', 'Exposure')
-- (2, 'click', 'Engagement')
-- (3, 'view_start', 'View')
-- (4, 'view_complete', 'View')
-- (5, 'like', 'Engagement')
-- (6, 'share_intent', 'Engagement')

-- fact_feed_events_feed for C001:
-- (1, 1, 1, 1, ...) -- impression
-- (1, 1, 3, 3, ...) -- view_start
-- (1, 1, 2, 4, ...) -- click
-- (1, 1, 4, 5, ...) -- view_complete
-- (2, 1, 1, 8, ...) -- impression by user B

-- fact_feed_events_feed for C002:
-- (1, 2, 1, 2, ...) -- impression
-- (1, 2, 3, 6, ...) -- view_start

-- fact_feed_events_feed for C003:
-- (2, 3, 1, 7, ...) -- impression
-- (2, 3, 3, 9, ...) -- view_start
-- (2, 3, 5, 10, ...) -- like

-- Expected Output (using the definition of engagement as like, comment, share_intent, click):
-- content_item_key | title                   | content_type | created_timestamp
-- ------------------|-------------------------|--------------|---------------------
-- 2                | Global Summit Highlights| article      | 2023-03-01 10:00:00 