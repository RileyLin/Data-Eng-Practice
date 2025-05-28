/*
Solution to Question 4.3.1: Top Collaborative Files

Write a SQL query to find the top 10 files with the most unique users 
who performed any action on them in the last 7 days.
*/

-- Assume a table `file_actions` with `file_id`, `user_id`, `action_timestamp`.

SELECT
    fa.file_id,
    COUNT(DISTINCT fa.user_id) AS unique_user_action_count
FROM
    file_actions fa
WHERE
    fa.action_timestamp >= CURRENT_DATE - INTERVAL '7 days' 
    AND fa.action_timestamp < CURRENT_DATE -- Actions in the last 7 full days (up to, but not including, current day)
GROUP BY
    fa.file_id
ORDER BY
    unique_user_action_count DESC,
    fa.file_id ASC -- Secondary sort for tie-breaking if counts are equal
LIMIT 10;

/*
Explanation:

1.  The query selects from a `file_actions` table (aliased as `fa`). This table is assumed to log every action a user performs on a file.
    Key columns expected: `file_id`, `user_id`, `action_timestamp`.

2.  `WHERE fa.action_timestamp >= CURRENT_DATE - INTERVAL '7 days' AND fa.action_timestamp < CURRENT_DATE`:
    *   Filters the actions to include only those that occurred within the last 7 full days. 
    *   `CURRENT_DATE - INTERVAL '7 days'` defines the start of the period (e.g., if today is 2023-03-20, this is 2023-03-13 00:00:00).
    *   `fa.action_timestamp < CURRENT_DATE` ensures we don't include partial data from the current day if the query runs mid-day. It includes all actions up to yesterday 23:59:59.999...  This correctly captures "the last 7 days" fully.

3.  `GROUP BY fa.file_id`:
    *   Groups the filtered actions by `file_id`, so aggregate functions operate on each file separately.

4.  `COUNT(DISTINCT fa.user_id) AS unique_user_action_count`:
    *   For each `file_id`, this counts the number of unique `user_id`s who performed any action on that file within the specified 7-day period. This directly measures the breadth of collaboration.

5.  `ORDER BY unique_user_action_count DESC, fa.file_id ASC`:
    *   Orders the results primarily by `unique_user_action_count` in descending order, so files with more unique collaborators appear first.
    *   `fa.file_id ASC` is a secondary sort criterion. This ensures that if multiple files have the same number of unique collaborators, they are listed in a consistent order (by file ID, ascending), making the output deterministic.

6.  `LIMIT 10`:
    *   Restricts the output to the top 10 files based on the ordering defined.

The query effectively identifies files that have been interacted with by the highest number of different users recently, which is a strong indicator of high collaborative activity.

Schema Assumptions:
file_actions:
- action_id (PK, optional, e.g., SERIAL)
- file_id (INTEGER, Identifier for the file)
- user_id (INTEGER, Identifier for the user performing the action)
- action_type (TEXT, e.g., 'view', 'edit', 'comment', 'share') - Not used in this query but often present
- action_timestamp (TIMESTAMP, Timestamp of the action)

(Optional: A `dim_files` table with `file_id` and `file_name` could be joined if file names are desired in the output, but the question only asks for `file_id`.)

Example DDL & DML for testing (PostgreSQL syntax):

DROP TABLE IF EXISTS file_actions;
CREATE TABLE file_actions (
    action_id SERIAL PRIMARY KEY,
    file_id INTEGER,
    user_id INTEGER,
    action_type TEXT,
    action_timestamp TIMESTAMP
);

-- Sample data for the last 7 days (assuming CURRENT_DATE is e.g., '2023-03-20' for this example)
INSERT INTO file_actions (file_id, user_id, action_type, action_timestamp) VALUES
-- File 101: 3 unique users in last 7 days
(101, 1, 'edit', CURRENT_DATE - INTERVAL '1 day'),
(101, 2, 'view', CURRENT_DATE - INTERVAL '1 day'),
(101, 1, 'comment', CURRENT_DATE - INTERVAL '2 days'), -- User 1 again, doesn't add to distinct count
(101, 3, 'edit', CURRENT_DATE - INTERVAL '2 days'),

-- File 102: 2 unique users in last 7 days
(102, 1, 'view', CURRENT_DATE - INTERVAL '3 days'),
(102, 4, 'edit', CURRENT_DATE - INTERVAL '3 days'),

-- File 103: 1 unique user in last 7 days
(103, 2, 'edit', CURRENT_DATE - INTERVAL '4 days'),

-- File 104: 2 unique users in last 7 days (actions spread out)
(104, 5, 'share', CURRENT_DATE - INTERVAL '1 day'),
(104, 6, 'view', CURRENT_DATE - INTERVAL '6 days'),

-- File 105: 1 unique user, but action is OUTSIDE last 7 days
(105, 1, 'edit', CURRENT_DATE - INTERVAL '8 days'), 

-- Adding more data to ensure we can test the LIMIT 10 functionality
(106, 1, 'edit', CURRENT_DATE - INTERVAL '1 day'), (106, 2, 'view', CURRENT_DATE - INTERVAL '1 day'), (106, 7, 'comment', CURRENT_DATE - INTERVAL '1 day'), -- File 106: 3 users
(107, 8, 'edit', CURRENT_DATE - INTERVAL '2 days'), (107, 9, 'edit', CURRENT_DATE - INTERVAL '2 days'), -- File 107: 2 users
(108, 1, 'view', CURRENT_DATE - INTERVAL '3 days'), -- File 108: 1 user
(109, 2, 'edit', CURRENT_DATE - INTERVAL '4 days'), (109, 3, 'view', CURRENT_DATE - INTERVAL '4 days'), (109, 4, 'comment', CURRENT_DATE - INTERVAL '4 days'), (109, 5, 'edit', CURRENT_DATE - INTERVAL '4 days'), -- File 109: 4 users
(110, 6, 'view', CURRENT_DATE - INTERVAL '5 days'), (110, 7, 'edit', CURRENT_DATE - INTERVAL '5 days'), -- File 110: 2 users
(111, 1, 'share', CURRENT_DATE - INTERVAL '1 day'), (111, 2, 'view', CURRENT_DATE - INTERVAL '2 days'), (111, 3, 'edit', CURRENT_DATE - INTERVAL '3 days'), (111, 4, 'comment', CURRENT_DATE - INTERVAL '4 days'), (111, 5, 'view', CURRENT_DATE - INTERVAL '5 days'), -- File 111: 5 users
(112, 10, 'edit', CURRENT_DATE - INTERVAL '1 day'); -- File 112: 1 user

-- Expected Output (Top 10, File 105 ignored as its action is outside 7 days):
-- file_id | unique_user_action_count
-- --------|--------------------------
-- 111     | 5
-- 109     | 4
-- 101     | 3
-- 106     | 3 
-- 102     | 2
-- 104     | 2
-- 107     | 2
-- 110     | 2
-- 103     | 1
-- 108     | 1
-- (Order among files with the same count is determined by file_id ASC due to the secondary sort condition.)
*/ 