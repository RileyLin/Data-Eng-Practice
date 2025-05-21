/*
Question 5.3.1: DAU Over MAU Ratio

Write a SQL query to calculate the DAU/MAU ratio (stickiness) for each of the last 30 days, 
showing the trend over time.

Schema:
user_activity:
- activity_id (PK)
- user_id
- activity_type
- activity_timestamp
- device_type
- os_version
- ...

Expected Output:
A result set with columns:
- activity_date: The calendar date
- dau: Count of distinct users active on that date
- mau: Count of distinct users active in the 30-day window ending on that date
- stickiness_ratio: DAU/MAU ratio as a decimal between 0 and 1
Ordered by date from oldest to newest
*/

-- Write your SQL query here:
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

1. First, we create a CTE called date_range to generate a series of the last 30 days
   (This implementation uses PostgreSQL's generate_series function, but could be adapted for other databases)

2. We create a CTE called daily_active to count distinct users per day (DAU)

3. We create a CTE called monthly_active to calculate the rolling 30-day MAU for each day
   in our date range. For each day, we count distinct users active in the 30-day window ending on that day.

4. Finally, we join these CTEs together to:
   - Include all dates in our range (even those with no activity)
   - Calculate the stickiness ratio as DAU/MAU for each day
   - Handle edge cases like zero MAU to avoid division by zero
   - Order the results by date

Alternative approach for databases without generate_series:
You could create a date dimension table or use a recursive CTE to generate the date range.

For example, in SQL Server:
WITH date_range AS (
    SELECT DATEADD(day, -30, CAST(GETDATE() AS date)) AS activity_date
    UNION ALL
    SELECT DATEADD(day, 1, activity_date)
    FROM date_range
    WHERE activity_date < DATEADD(day, -1, CAST(GETDATE() AS date))
)
SELECT * FROM date_range
OPTION (MAXRECURSION 100);
*/ 