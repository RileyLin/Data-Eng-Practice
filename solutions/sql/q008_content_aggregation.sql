/*
Solution to Question 3.3.2: Content Aggregation

Given a watch_fact table (content_id, user_id, total_watch_time_seconds, date_key), 
write a query to get the distinct user count and sum of total watch time per content_id for a specific date.
*/

-- Assume `watch_fact` table exists with the specified columns.
-- Assume the specific date for querying is '20231029' (integer YYYYMMDD) or DATE '2023-10-29'. This can be parameterized.

SELECT
    wf.content_id,
    COUNT(DISTINCT wf.user_id) AS distinct_user_count,
    SUM(wf.total_watch_time_seconds) AS sum_total_watch_time_seconds
FROM
    watch_fact wf
WHERE
    wf.date_key = 20231029 -- Replace with your specific date value or parameter
    -- If date_key is of DATE type, use: wf.date_key = DATE '2023-10-29'
    -- Or if date_key is TEXT 'YYYY-MM-DD', use: wf.date_key = '2023-10-29'
GROUP BY
    wf.content_id
ORDER BY
    wf.content_id ASC; -- Explicitly ASC for clarity, though often default

/*
Explanation:

1.  The query selects from the `watch_fact` table (aliased as `wf`).

2.  `WHERE wf.date_key = 20231029`:
    *   Filters the records to include only those for the specific date of interest.
    *   The format of the date literal (`20231029`) must match the data type and format of the `date_key` column in your `watch_fact` table.
        *   If `date_key` is an `INTEGER` representing `YYYYMMDD`, then `20231029` is correct.
        *   If `date_key` is a `DATE` type, the condition should be `wf.date_key = DATE '2023-10-29'` (or equivalent syntax for your SQL dialect, e.g., `CAST('2023-10-29' AS DATE)`).
        *   If `date_key` is a `TEXT` field in `'YYYY-MM-DD'` format, use `wf.date_key = '2023-10-29'`.

3.  `GROUP BY wf.content_id`:
    *   Groups the filtered rows by `content_id`. This means all aggregate functions (`COUNT(DISTINCT ...)`, `SUM(...)`) will operate independently for each unique `content_id`.

4.  Aggregate Functions in the `SELECT` clause:
    *   `COUNT(DISTINCT wf.user_id) AS distinct_user_count`:
        *   For each `content_id` group, this counts the number of unique `user_id`s. This gives the number of distinct users who watched that specific content on the given date.
    *   `SUM(wf.total_watch_time_seconds) AS sum_total_watch_time_seconds`:
        *   For each `content_id` group, this calculates the sum of `total_watch_time_seconds`. This gives the total combined watch duration for that specific content from all users on the given date.

5.  `ORDER BY wf.content_id ASC`:
    *   Orders the final result set by `content_id` in ascending order. This makes the output predictable and easier to read.

The query will return one row for each `content_id` that had any viewing activity on the specified `date_key`, showing the count of unique viewers and their total combined watch time for that content on that day.

Schema Assumptions:
watch_fact:
- content_id (Identifier for the content, e.g., INTEGER)
- user_id (Identifier for the user, e.g., INTEGER)
- total_watch_time_seconds (Watch time for this user-content-date record, e.g., INTEGER)
- date_key (Date of activity, e.g., INTEGER as YYYYMMDD, or DATE type, or TEXT as YYYY-MM-DD)

Example DDL & DML for testing (using INTEGER date_key as YYYYMMDD):

DROP TABLE IF EXISTS watch_fact;
CREATE TABLE watch_fact (
    record_id SERIAL PRIMARY KEY, 
    content_id INTEGER,
    user_id INTEGER,
    total_watch_time_seconds INTEGER,
    date_key INTEGER -- Assuming YYYYMMDD format
);

INSERT INTO watch_fact (content_id, user_id, total_watch_time_seconds, date_key) VALUES
-- Date: 20231029
(101, 1, 1200, 20231029),
(101, 2, 1800, 20231029), -- Content 101 watched by 2 unique users on this date
(102, 1, 3000, 20231029), -- Content 102 watched by 1 unique user on this date
(101, 1, 600, 20231029),  -- User 1 watched Content 101 again (or continued watching), contributes to sum but not distinct count for this user
(103, 3, 500, 20231029),  -- Content 103 by user 3

-- Date: 20231028 (different date, should be filtered out by WHERE clause)
(101, 1, 500, 20231028),
(103, 3, 2400, 20231028);

-- Expected Output for date_key = 20231029:
-- content_id | distinct_user_count | sum_total_watch_time_seconds
-- -----------|---------------------|-------------------------------
-- 101        | 2                   | 3600  (1200 + 1800 + 600)
-- 102        | 1                   | 3000
-- 103        | 1                   | 500
*/ 