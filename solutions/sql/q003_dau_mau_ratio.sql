/*
Solution to Question 5.3.1: DAU Over MAU Ratio

Write a SQL query to calculate the DAU/MAU ratio (stickiness) for each of the last 30 days,
showing the trend over time.
*/

-- PostgreSQL solution using generate_series
WITH date_range AS (
    SELECT 
        date::date AS activity_date
    FROM 
        generate_series(
            current_date - interval '30 days', 
            current_date - interval '1 day', 
            interval '1 day'
        ) date
),
daily_active AS (
    SELECT 
        date(activity_timestamp) AS activity_date,
        count(DISTINCT user_id) AS dau
    FROM 
        user_activity
    WHERE 
        activity_timestamp >= current_date - interval '30 days'
        AND activity_timestamp < current_date
    GROUP BY 
        date(activity_timestamp)
),
monthly_active AS (
    SELECT 
        date(a.activity_date) AS activity_date,
        count(DISTINCT ua.user_id) AS mau
    FROM 
        date_range a
    CROSS JOIN LATERAL (
        SELECT 
            user_id
        FROM 
            user_activity
        WHERE 
            activity_timestamp >= a.activity_date - interval '29 days'
            AND activity_timestamp <= a.activity_date
    ) ua
    GROUP BY 
        a.activity_date
)
SELECT 
    dr.activity_date,
    COALESCE(da.dau, 0) AS dau,
    COALESCE(ma.mau, 0) AS mau,
    CASE 
        WHEN COALESCE(ma.mau, 0) = 0 THEN 0
        ELSE COALESCE(da.dau, 0)::decimal / COALESCE(ma.mau, 1)
    END AS stickiness_ratio
FROM 
    date_range dr
LEFT JOIN 
    daily_active da ON dr.activity_date = da.activity_date
LEFT JOIN 
    monthly_active ma ON dr.activity_date = ma.activity_date
ORDER BY 
    dr.activity_date;

/*
Explanation:

This query calculates the Daily Active Users (DAU) over Monthly Active Users (MAU) ratio, 
often called "stickiness," for each day in a 30-day period. Here's how it works:

1. date_range CTE: 
   - Creates a continuous sequence of dates for the past 30 days
   - Ensures we have a row for every day, even if there was no activity

2. daily_active CTE:
   - Calculates the count of distinct users active on each day (DAU)
   - Groups by date to get one row per day with the count

3. monthly_active CTE:
   - For each day in date_range, counts distinct users active in the 30-day window ending on that day
   - Uses CROSS JOIN LATERAL to run a subquery for each day (similar to a correlated subquery)
   - This gives us a rolling 30-day MAU for each date

4. Final query:
   - Joins the three CTEs to get one row per day with its DAU and MAU
   - Uses COALESCE to replace NULL values with 0
   - Calculates stickiness_ratio = DAU/MAU, handling edge cases to avoid division by zero
   - Orders by date to show the trend over time

Key technical concepts demonstrated:
1. Window functions and datetime manipulation
2. LATERAL joins for correlated subqueries
3. Handling NULL values and division by zero
4. Data type conversion (using ::decimal)

This approach supports DAU/MAU analysis which is critical for measuring user engagement 
and retention - important metrics for product and business analysis.

Alternative for SQL Server or other databases without generate_series:

WITH date_range AS (
    SELECT DATEADD(day, -30, CAST(GETDATE() AS date)) AS activity_date
    UNION ALL
    SELECT DATEADD(day, 1, activity_date)
    FROM date_range
    WHERE activity_date < DATEADD(day, -1, CAST(GETDATE() AS date))
)
-- Then continue with the rest of the query
*/ 