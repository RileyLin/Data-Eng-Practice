/*
Solution to Question 2.3.2: Posts with Reactions but No Comments

Calculate the percentage of content items (e.g., posts, videos) created today 
that received at least one 'reaction' event but zero 'comment' events on the same day.
*/

-- Assuming 'today' means the current calendar date.
-- Table names: `posts` and `engagement_events`
-- `posts` has `post_id`, `creation_timestamp`
-- `engagement_events` has `post_id`, `event_type` ('reaction', 'comment'), `event_timestamp`

WITH PostsCreatedToday AS (
    SELECT
        p.post_id
    FROM
        posts p
    WHERE
        DATE(p.creation_timestamp) = CURRENT_DATE
),
ReactionsToday AS (
    SELECT DISTINCT
        ee.post_id
    FROM
        engagement_events ee
    JOIN
        PostsCreatedToday pct ON ee.post_id = pct.post_id
    WHERE
        ee.event_type = 'reaction'
        AND DATE(ee.event_timestamp) = CURRENT_DATE
),
CommentsToday AS (
    SELECT DISTINCT
        ee.post_id
    FROM
        engagement_events ee
    JOIN
        PostsCreatedToday pct ON ee.post_id = pct.post_id
    WHERE
        ee.event_type = 'comment'
        AND DATE(ee.event_timestamp) = CURRENT_DATE
),
EligiblePosts AS (
    -- Posts created today with at least one reaction today and no comments today
    SELECT
        rt.post_id
    FROM
        ReactionsToday rt
    LEFT JOIN
        CommentsToday ct ON rt.post_id = ct.post_id
    WHERE
        ct.post_id IS NULL
)
SELECT
    CASE
        WHEN (SELECT COUNT(*) FROM PostsCreatedToday) = 0 THEN 0.0
        ELSE (
            (SELECT COUNT(*) FROM EligiblePosts) * 100.0 / 
            (SELECT COUNT(*) FROM PostsCreatedToday)
        )
    END AS percentage_posts_reaction_no_comment;

/*
Explanation:

1.  `PostsCreatedToday` CTE:
    *   Selects `post_id` for all posts created on the `CURRENT_DATE`.

2.  `ReactionsToday` CTE:
    *   Finds distinct `post_id`s from `PostsCreatedToday` that received at least one 'reaction' event also on `CURRENT_DATE`.

3.  `CommentsToday` CTE:
    *   Finds distinct `post_id`s from `PostsCreatedToday` that received at least one 'comment' event also on `CURRENT_DATE`.

4.  `EligiblePosts` CTE:
    *   Selects `post_id`s from `ReactionsToday` (posts with reactions today).
    *   It then `LEFT JOIN`s with `CommentsToday`.
    *   The `WHERE ct.post_id IS NULL` condition ensures that only posts with reactions but no comments today are kept.

5.  Final `SELECT` Statement:
    *   Calculates the percentage: (`COUNT(EligiblePosts)` * 100.0) / `COUNT(PostsCreatedToday)`.
    *   A `CASE` statement handles the scenario where no posts were created today to prevent division by zero, returning 0.0 in such cases.

Schema Assumptions:
posts:
- post_id (PK)
- user_id (FK, creator)
- creation_timestamp

engagement_events:
- event_id (PK)
- post_id (FK -> posts)
- user_id (FK, user who engaged)
- event_type ('reaction', 'comment', 'like', etc.)
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

-- Assuming CURRENT_DATE is '2023-03-17' for this sample data
INSERT INTO posts (post_id, user_id, creation_timestamp) VALUES
(1, 101, '2023-03-17 08:00:00'), -- P1: Created today
(2, 102, '2023-03-17 09:00:00'), -- P2: Created today
(3, 103, '2023-03-17 10:00:00'), -- P3: Created today
(4, 104, '2023-03-17 11:00:00'), -- P4: Created today
(5, 105, '2023-03-16 12:00:00'); -- P5: Created yesterday

INSERT INTO engagement_events (post_id, user_id, event_type, event_timestamp) VALUES
-- P1: Reaction today, Comment today
(1, 201, 'reaction', '2023-03-17 10:00:00'),
(1, 202, 'comment', '2023-03-17 11:00:00'),
-- P2: Reaction today, No comment today
(2, 203, 'reaction', '2023-03-17 12:00:00'),
-- P3: No reaction today, Comment today
(3, 204, 'comment', '2023-03-17 13:00:00'),
-- P4: Reaction today, Comment on a different day (counts as no comment today)
(4, 205, 'reaction', '2023-03-17 14:00:00'),
(4, 206, 'comment', '2023-03-18 10:00:00'),
-- P5 (created yesterday): Reaction today (not relevant as post not created today)
(5, 207, 'reaction', '2023-03-17 15:00:00');

-- Analysis for CURRENT_DATE = '2023-03-17':
-- PostsCreatedToday: P1, P2, P3, P4 (Count = 4)
-- ReactionsToday for these posts: P1, P2, P4
-- CommentsToday for these posts: P1, P3

-- EligiblePosts (Reaction today AND NO Comment today):
-- P1: Reaction today, Comment today. -> No
-- P2: Reaction today, No Comment today. -> Yes (Eligible)
-- P3: No Reaction today. -> No (Not in ReactionsToday)
-- P4: Reaction today, No Comment today (comment is for tomorrow). -> Yes (Eligible)

-- Count(EligiblePosts) = 2 (P2, P4)
-- Count(PostsCreatedToday) = 4
-- Percentage = (2 / 4) * 100.0 = 50.0

-- Expected Output:
-- percentage_posts_reaction_no_comment
-- --------------------------------------
-- 50.0
*/ 