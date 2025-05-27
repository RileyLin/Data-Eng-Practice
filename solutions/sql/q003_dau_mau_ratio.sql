/*
Solution to Question 5.3.1: DAU Over MAU Ratio Trend

Write a SQL query to calculate the DAU/MAU ratio (stickiness) for each of the last 30 days,
showing the trend over time.
*/

-- Generic SQL (PostgreSQL compatible for generate_series and interval syntax)
-- Adjust date functions and interval syntax for other SQL dialects if needed.

WITH date_series AS (
    -- Generate a series of dates for the last 30 days up to yesterday
    SELECT generate_series(
        (CURRENT_DATE - INTERVAL '30 days')::date,
        (CURRENT_DATE - INTERVAL '1 day')::date,
        INTERVAL '1 day'
    ) AS activity_date
),
DailyActiveUsers AS (
    SELECT
        DATE(ua.activity_timestamp) AS activity_date,
        COUNT(DISTINCT ua.user_id) AS dau
    FROM
        user_activity ua -- Generic user activity table
    WHERE
        ua.activity_timestamp >= (CURRENT_DATE - INTERVAL '30 days')
        AND ua.activity_timestamp < CURRENT_DATE
    GROUP BY
        DATE(ua.activity_timestamp)
),
RollingMonthlyActiveUsers AS (
    SELECT
        d.activity_date,
        COUNT(DISTINCT ua.user_id) AS mau
    FROM
        date_series d
    JOIN
        user_activity ua ON DATE(ua.activity_timestamp) <= d.activity_date
                       AND DATE(ua.activity_timestamp) > (d.activity_date - INTERVAL '30 days')
        -- User is active if they had any activity in the 30-day window ending on d.activity_date
    GROUP BY
        d.activity_date
)
SELECT
    ds.activity_date,
    COALESCE(dau.dau, 0) AS dau,
    COALESCE(mau.mau, 0) AS mau,
    CASE
        WHEN COALESCE(mau.mau, 0) = 0 THEN 0.0
        ELSE ROUND((COALESCE(dau.dau, 0) * 1.0 / mau.mau), 4) -- Multiply by 1.0 for float division
    END AS dau_mau_ratio
FROM
    date_series ds
LEFT JOIN
    DailyActiveUsers dau ON ds.activity_date = dau.activity_date
LEFT JOIN
    RollingMonthlyActiveUsers mau ON ds.activity_date = mau.activity_date
ORDER BY
    ds.activity_date ASC;

/*
Explanation:

1.  `date_series` CTE:
    *   Generates a continuous series of dates for the last 30 days, ending yesterday. This ensures that every day in the period has a row in the final output, even if there was no activity.
    *   Uses `generate_series` (PostgreSQL specific). For other SQL dialects, a calendar table or recursive CTE might be used.

2.  `DailyActiveUsers` (DAU) CTE:
    *   Calculates the number of distinct `user_id`s that had activity on each specific `activity_date` within the last 30 days.
    *   It groups by the date of activity.

3.  `RollingMonthlyActiveUsers` (MAU) CTE:
    *   For each `activity_date` in our `date_series`, this CTE calculates the number of distinct `user_id`s that were active at any point in the 30-day window *ending on that `activity_date`*.
    *   This is achieved by joining `date_series` with `user_activity` where the activity timestamp falls between `(d.activity_date - INTERVAL '30 days')` (exclusive of the start of this range boundary, meaning 29 days prior plus the current day) and `d.activity_date` (inclusive).

4.  Final `SELECT` Statement:
    *   Starts with the `date_series` to ensure all dates are present.
    *   `LEFT JOIN`s with `DailyActiveUsers` to get the DAU for each date. `COALESCE(dau.dau, 0)` handles days with no active users.
    *   `LEFT JOIN`s with `RollingMonthlyActiveUsers` to get the rolling MAU for each date. `COALESCE(mau.mau, 0)` handles cases where the MAU might be zero (e.g., at the very beginning of tracking if less than 30 days of data exist).
    *   Calculates `dau_mau_ratio`:
        *   `dau / mau`.
        *   `COALESCE(dau.dau, 0) * 1.0 / mau.mau`: Multiplying by `1.0` ensures floating-point division to get a decimal ratio.
        *   A `CASE` statement handles division by zero if MAU is 0, returning `0.0` in such instances.
        *   `ROUND(..., 4)` formats the ratio to 4 decimal places.
    *   Orders the results by `activity_date` to show the trend.

Schema Assumptions:
user_activity:
- user_id (Identifier for the user)
- activity_timestamp (Timestamp of user activity)
- ... (other activity-related fields)

Example DDL & DML for testing (Conceptual - requires date generation for full 30 days):

DROP TABLE IF EXISTS user_activity;
CREATE TABLE user_activity (
    user_id INTEGER,
    activity_timestamp TIMESTAMP
);

-- Insert sample data spanning several days for a few users
-- To test thoroughly, you'd need data for a 30-day period.
-- Example for a few days:
INSERT INTO user_activity (user_id, activity_timestamp) VALUES
(1, CURRENT_DATE - INTERVAL '1 day'), (2, CURRENT_DATE - INTERVAL '1 day'),
(1, CURRENT_DATE - INTERVAL '2 days'),
(3, CURRENT_DATE - INTERVAL '2 days'),
(1, CURRENT_DATE - INTERVAL '29 days'), (4, CURRENT_DATE - INTERVAL '29 days');

-- For CURRENT_DATE = '2023-10-30':
-- activity_date | dau | mau | dau_mau_ratio
-- --------------|-----|-----|---------------
-- ... (previous 28 days) ...
-- 2023-10-29    | 2   | 4   | 0.5000        (Users 1,2 active. MAU includes 1,2,3,4 from up to 29 days prior)
-- 2023-10-28    | 2   | 3   | 0.6667        (Users 1,3 active. MAU includes 1,3,4 from up to 29 days prior - user 2 not in this 30 day window if only active on 29th)
-- ...

-- To make this fully testable without complex date generation in DML:
-- One would typically populate user_activity for a full 30-day span for several users
-- and then run the query. The output would be a list of 30 dates with their DAU, MAU, and ratio.
*/

-- Calculate the DAU/MAU ratio for a specific month.

-- Assumptions (based on scenario_6_news_feed_setup.sql):
-- 1. `fact_feed_events_feed` logs user activity with `user_key` and `event_timestamp` (or `date_key`).
-- 2. `dim_date` table can be used to determine month and year from `date_key` or `event_timestamp`.
-- 3. An "active user" is any user with at least one event in `fact_feed_events_feed` on a given day (for DAU) or in a given month (for MAU).

-- Methodology:
-- 1. Specify the target month and year for the calculation.
-- 2. Calculate MAU: Count distinct users who had any activity in the target month.
-- 3. Calculate DAU for each day in the target month: Count distinct users active on that specific day.
-- 4. Calculate Average DAU: Average the daily DAU counts over the number of days in the target month.
-- 5. Calculate Ratio: Average DAU / MAU.

-- Let's use March 2023 as the target month, as per sample data in scenario_6_news_feed_setup.sql

WITH MonthlyActiveUsers AS (
    -- Calculate MAU for March 2023
    SELECT
        COUNT(DISTINCT ffe.user_key) AS mau
    FROM
        fact_feed_events_feed ffe
    JOIN
        dim_date dd ON ffe.date_key = dd.date_key
    WHERE
        dd.year = 2023 AND dd.month = 3
),
DailyActiveUsers AS (
    -- Calculate DAU for each day in March 2023
    SELECT
        ffe.date_key,
        COUNT(DISTINCT ffe.user_key) AS dau_count
    FROM
        fact_feed_events_feed ffe
    JOIN
        dim_date dd ON ffe.date_key = dd.date_key
    WHERE
        dd.year = 2023 AND dd.month = 3
    GROUP BY
        ffe.date_key
),
AverageDailyActiveUsers AS (
    -- Calculate the average DAU for March 2023
    -- Note: If there are days with no users, they won't appear in DailyActiveUsers.
    -- For a more robust average, one might want to average over the total number of days in the month.
    -- However, for simplicity here, we average the DAU counts we found.
    -- The sample data only has activity on 20230301 and 20230302.
    SELECT
        AVG(CAST(dau_count AS REAL)) AS average_dau,
        COUNT(date_key) AS active_days_in_month -- Number of days that had at least one active user
    FROM
        DailyActiveUsers
)
SELECT
    adau.average_dau,
    mau.mau,
    CASE
        WHEN mau.mau = 0 THEN 0 -- Avoid division by zero
        ELSE adau.average_dau / mau.mau
    END AS dau_mau_ratio,
    adau.active_days_in_month
FROM
    AverageDailyActiveUsers adau, MonthlyActiveUsers mau;

-- Explanation for scenario_6_news_feed_setup.sql sample data:
-- Target Month: March 2023

-- dim_users_feed:
-- User 1 (AliceFeedReader)
-- User 2 (BobScroller)

-- fact_feed_events_feed activity in March 2023:
-- Date 20230301 (Key): User 1 is active.
-- Date 20230302 (Key): User 2 is active.

-- MAU (March 2023):
-- Users active in March 2023 are User 1 and User 2. So, MAU = 2.

-- DAU:
-- For 2023-03-01: User 1 is active. DAU = 1.
-- For 2023-03-02: User 2 is active. DAU = 1.
-- Other days in March 2023 have 0 active users in the sample data.

-- Average DAU (based on days with activity):
-- The DailyActiveUsers CTE will have two rows: (20230301, 1) and (20230302, 1).
-- Average DAU = (1 + 1) / 2 = 1.0.
-- active_days_in_month = 2

-- DAU/MAU Ratio:
-- Ratio = Average DAU / MAU = 1.0 / 2 = 0.5.

-- Expected Output with sample data:
-- average_dau | mau | dau_mau_ratio | active_days_in_month
-- ------------|-----|---------------|----------------------
-- 1.0         | 2   | 0.5           | 2

-- Note: A more common way to calculate Average DAU for a month is to sum all daily DAUs
-- and divide by the total number of days in that specific month (e.g., 31 for March).
-- The query above averages DAU over days that *had activity*.
-- If we wanted to average over all days in March 2023 (31 days):
/*
WITH TargetMonthDays AS (
    SELECT COUNT(DISTINCT date_key) as num_days_in_month
    FROM dim_date
    WHERE year = 2023 AND month = 3
    -- This assumes dim_date is populated for all days of the month.
    -- For the sample data, dim_date only has 2 days, so this would be 2.
    -- If dim_date was complete for March, it would be 31.
),
MonthlyActiveUsers AS (
    SELECT COUNT(DISTINCT ffe.user_key) AS mau
    FROM fact_feed_events_feed ffe
    JOIN dim_date dd ON ffe.date_key = dd.date_key
    WHERE dd.year = 2023 AND dd.month = 3
),
SumOfDailyActiveUsers AS (
    SELECT SUM(dau_count) AS total_dau_for_month
    FROM (
        SELECT ffe.date_key, COUNT(DISTINCT ffe.user_key) AS dau_count
        FROM fact_feed_events_feed ffe
        JOIN dim_date dd ON ffe.date_key = dd.date_key
        WHERE dd.year = 2023 AND dd.month = 3
        GROUP BY ffe.date_key
    ) daily_counts
)
SELECT
    (SELECT total_dau_for_month FROM SumOfDailyActiveUsers) / CAST((SELECT num_days_in_month FROM TargetMonthDays) AS REAL) AS average_dau_strict,
    (SELECT mau FROM MonthlyActiveUsers) AS mau,
    ((SELECT total_dau_for_month FROM SumOfDailyActiveUsers) / CAST((SELECT num_days_in_month FROM TargetMonthDays) AS REAL)) / (SELECT mau FROM MonthlyActiveUsers) AS dau_mau_ratio_strict;

-- Using sample data, num_days_in_month from dim_date would be 2 (as only 2 days are in dim_date for March).
-- total_dau_for_month = 1 (for 20230301) + 1 (for 20230302) = 2.
-- average_dau_strict = 2 / 2.0 = 1.0
-- mau = 2
-- dau_mau_ratio_strict = 1.0 / 2 = 0.5
-- The result happens to be the same because dim_date in sample only covers active days.
-- If dim_date had all 31 days for March, average_dau_strict would be 2 / 31.0 = 0.0645...
*/ 