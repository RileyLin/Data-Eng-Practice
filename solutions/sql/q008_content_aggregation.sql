/*
Solution to Question 3.3.2: Content Aggregation

Given a watch_fact table (content_id, user_id, total_watch_time_seconds, date_key), 
write a query to get the distinct user count and sum of total watch time per content_id for a specific date.
*/

-- Assume `watch_fact` table exists with the specified columns.
-- Assume the specific date for querying is '2023-10-29'. This can be parameterized.

SELECT
    wf.content_id,
    COUNT(DISTINCT wf.user_id) AS distinct_user_count,
    SUM(wf.total_watch_time_seconds) AS sum_total_watch_time_seconds
FROM
    watch_fact wf
WHERE
    wf.date_key = '20231029' -- Assuming date_key is in YYYYMMDD integer format or a direct date match
    -- If date_key is a DATE type, use: wf.date_key = DATE '2023-10-29'
GROUP BY
    wf.content_id
ORDER BY
    wf.content_id;

/*
Explanation:

1.  The query selects from the `watch_fact` table (aliased as `wf`).

2.  `WHERE wf.date_key = '20231029'`:
    *   Filters the records to include only those for the specific date of interest. 
    *   The format of the date literal ('20231029') should match the data type and format of the `date_key` column.
    *   If `date_key` is of DATE type, the condition would be `wf.date_key = DATE '2023-10-29'` or similar depending on the SQL dialect.

3.  `GROUP BY wf.content_id`:
    *   Groups the filtered rows by `content_id`, so that aggregate functions operate on each group of content separately.

4.  Aggregate Functions in the `SELECT` clause:
    *   `COUNT(DISTINCT wf.user_id) AS distinct_user_count`:
        *   For each `content_id`, this counts the number of unique `user_id`s who watched that content on the specified date.
    *   `SUM(wf.total_watch_time_seconds) AS sum_total_watch_time_seconds`:
        *   For each `content_id`, this calculates the sum of all `total_watch_time_seconds` from all user sessions for that content on the specified date.

5.  `ORDER BY wf.content_id`:
    *   Orders the results by `content_id` for consistent and readable output.

The query will return one row for each `content_id` that had viewing activity on the specified `date_key`, along with the distinct count of users who watched it and the total watch time for it on that day.

Schema Assumptions:
watch_fact:
- content_id (Identifier for the content)
- user_id (Identifier for the user)
- total_watch_time_seconds (Watch time for this user-content-date record)
- date_key (Date of activity, e.g., YYYYMMDD integer or DATE type)

Example DDL & DML for testing:

DROP TABLE IF EXISTS watch_fact;
CREATE TABLE watch_fact (
    record_id SERIAL PRIMARY KEY, -- Added for uniqueness of rows if needed
    content_id INTEGER,
    user_id INTEGER,
    total_watch_time_seconds INTEGER,
    date_key INTEGER -- Assuming YYYYMMDD format
);

INSERT INTO watch_fact (content_id, user_id, total_watch_time_seconds, date_key) VALUES
-- Date: 20231029
(101, 1, 1200, 20231029),
(101, 2, 1800, 20231029), -- Content 101 watched by 2 users
(102, 1, 3000, 20231029), -- Content 102 watched by 1 user
(101, 1, 600, 20231029),  -- User 1 watched Content 101 again (or continued)

-- Date: 20231028 (different date, should be filtered out)
(101, 1, 500, 20231028),
(103, 3, 2400, 20231028);

-- Expected Output for date_key = 20231029:
-- content_id | distinct_user_count | sum_total_watch_time_seconds
-- -----------|---------------------|-------------------------------
-- 101        | 2                   | 3600 (1200 + 1800 + 600)
-- 102        | 1                   | 3000
*/ 