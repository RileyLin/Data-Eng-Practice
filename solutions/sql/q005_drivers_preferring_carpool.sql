/*
Solution to Question 1.3.2: Percentage of Drivers Preferring Carpool

Write a SQL query to calculate the percentage of distinct drivers who complete more carpool rides
than regular (non-carpool) rides in a given period (e.g., last 30 days).
*/

WITH DriverRideCounts AS (
    SELECT
        fr.driver_user_key,
        SUM(CASE WHEN drt.ride_type_name = 'Carpool' THEN 1 ELSE 0 END) AS carpool_rides_count,
        SUM(CASE WHEN drt.ride_type_name != 'Carpool' AND drt.ride_type_name IS NOT NULL THEN 1 ELSE 0 END) AS regular_rides_count
        -- Assuming 'regular' means any defined ride type that is not 'Carpool'. 
        -- If 'regular' is a specific type like 'Standard', the condition would be `drt.ride_type_name = 'Standard'`.
    FROM
        fact_rides fr
    JOIN
        dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key
    WHERE
        fr.end_timestamp >= (CURRENT_DATE - INTERVAL '30 days') -- Filter for the last 30 days
        AND fr.end_timestamp < CURRENT_DATE -- Ensure we don't include today if it's partial
    GROUP BY
        fr.driver_user_key
),
TotalDistinctDriversInPeriod AS (
    SELECT COUNT(DISTINCT driver_user_key) as total_drivers
    FROM fact_rides
    WHERE
        end_timestamp >= (CURRENT_DATE - INTERVAL '30 days') 
        AND end_timestamp < CURRENT_DATE
),
DriversPreferringCarpool AS (
    SELECT
        COUNT(DISTINCT driver_user_key) as drivers_preferring_carpool_count
    FROM
        DriverRideCounts
    WHERE
        carpool_rides_count > regular_rides_count
)
SELECT
    CASE
        WHEN tdd.total_drivers > 0 THEN (dpc.drivers_preferring_carpool_count * 100.0) / tdd.total_drivers
        ELSE 0.0
    END AS percentage_drivers_preferring_carpool
FROM
    DriversPreferringCarpool dpc, TotalDistinctDriversInPeriod tdd;

/*
Explanation:

1.  `DriverRideCounts` CTE:
    *   Filters `fact_rides` for rides completed in the last 30 days (using `end_timestamp`). The period is defined as `CURRENT_DATE - INTERVAL '30 days'` up to (but not including) `CURRENT_DATE`.
    *   Joins with `dim_ride_type` to get the `ride_type_name`.
    *   Groups by `driver_user_key`.
    *   For each driver, it counts:
        *   `carpool_rides_count`: Number of rides where `ride_type_name` is 'Carpool'.
        *   `regular_rides_count`: Number of rides where `ride_type_name` is not 'Carpool' (and is not NULL, to avoid counting rides with undefined types as regular). This definition of "regular" might need adjustment based on specific business rules (e.g., if regular means only 'Standard' type rides).

2.  `TotalDistinctDriversInPeriod` CTE:
    *   Calculates the total number of distinct drivers who completed *any* ride in the specified 30-day period. This serves as the denominator for the percentage calculation, ensuring it reflects all active drivers in that period.

3.  `DriversPreferringCarpool` CTE:
    *   Takes the results from `DriverRideCounts`.
    *   Counts the number of distinct drivers for whom `carpool_rides_count` is greater than `regular_rides_count`.

4.  Final Query:
    *   Calculates the percentage: (`drivers_preferring_carpool_count` * 100.0) / `total_drivers`.
    *   Uses a `CASE` statement to prevent division by zero if `total_drivers` is 0.
    *   The result is a single percentage value.

Schema Assumptions:
fact_rides:
- ride_id (PK)
- driver_user_key (FK)
- ride_type_key (FK -> dim_ride_type)
- end_timestamp (Timestamp of ride completion)
- ...

dim_ride_type:
- ride_type_key (PK)
- ride_type_name ('Carpool', 'Regular', 'Standard', 'Premium', etc.)
- ...

Example DDL & DML for testing:

DROP TABLE IF EXISTS dim_ride_type;
CREATE TABLE dim_ride_type (
    ride_type_key INTEGER PRIMARY KEY,
    ride_type_name TEXT NOT NULL
);

DROP TABLE IF EXISTS fact_rides;
CREATE TABLE fact_rides (
    ride_id INTEGER PRIMARY KEY,
    driver_user_key INTEGER,
    ride_type_key INTEGER,
    end_timestamp TIMESTAMP, -- Assuming this is available and used for period filtering
    FOREIGN KEY (ride_type_key) REFERENCES dim_ride_type(ride_type_key)
);

INSERT INTO dim_ride_type (ride_type_key, ride_type_name) VALUES
(1, 'Standard'), (2, 'Carpool'), (3, 'Premium');

-- Sample data for the last 30 days (adjust CURRENT_DATE or use fixed dates for testing)
INSERT INTO fact_rides (ride_id, driver_user_key, ride_type_key, end_timestamp) VALUES
-- Driver 1: 1 Carpool, 2 Standard
(1, 101, 2, CURRENT_DATE - INTERVAL '5 days'),
(2, 101, 1, CURRENT_DATE - INTERVAL '6 days'),
(3, 101, 1, CURRENT_DATE - INTERVAL '7 days'),
-- Driver 2: 3 Carpool, 1 Standard
(4, 102, 2, CURRENT_DATE - INTERVAL '2 days'),
(5, 102, 2, CURRENT_DATE - INTERVAL '3 days'),
(6, 102, 2, CURRENT_DATE - INTERVAL '4 days'),
(7, 102, 1, CURRENT_DATE - INTERVAL '5 days'),
-- Driver 3: 2 Carpool, 0 Standard
(8, 103, 2, CURRENT_DATE - INTERVAL '1 day'),
(9, 103, 2, CURRENT_DATE - INTERVAL '2 days'),
-- Driver 4: 1 Standard (no carpool)
(10, 104, 1, CURRENT_DATE - INTERVAL '10 days'),
-- Driver 5: 1 Premium (not carpool, not standard based on strict definition)
(11, 105, 3, CURRENT_DATE - INTERVAL '12 days'),
-- Driver 6: Only rides outside the 30-day window
(12, 106, 2, CURRENT_DATE - INTERVAL '35 days');

-- Expected Analysis (using 'Standard' as regular for carpool_rides_count > regular_rides_count):
-- Driver 101: 1 Carpool, 2 Standard. (1 > 2 is False)
-- Driver 102: 3 Carpool, 1 Standard. (3 > 1 is True) -> Prefers Carpool
-- Driver 103: 2 Carpool, 0 Standard. (2 > 0 is True) -> Prefers Carpool
-- Driver 104: 0 Carpool, 1 Standard. (0 > 1 is False)
-- Driver 105: 0 Carpool, 0 Standard (Premium is not Standard). (0 > 0 is False)

-- Total distinct drivers in period (101, 102, 103, 104, 105) = 5
-- Drivers preferring carpool = 2 (102, 103)
-- Percentage = (2 / 5) * 100.0 = 40.0

-- Expected output:
-- percentage_drivers_preferring_carpool
-- ---------------------------------------
-- 40.0
*/ 

-- ============================================================================
-- ALTERNATIVE APPROACH: More Elegant & Simplified Version
-- ============================================================================

/*
Alternative Solution: More elegant approach using a parameterized date range
and simplified logic with better readability.
*/

-- Option 1: Using a cleaner date range approach (includes current date)
WITH date_range AS (
    SELECT 
        CURRENT_DATE - INTERVAL '30 days' AS start_date,
        CURRENT_DATE AS end_date
),
driver_ride_summary AS (
    SELECT 
        fr.driver_user_key,
        COUNT(CASE WHEN drt.ride_type_name = 'Carpool' THEN 1 END) AS carpool_count,
        COUNT(CASE WHEN drt.ride_type_name != 'Carpool' THEN 1 END) AS non_carpool_count,
        COUNT(*) AS total_rides
    FROM fact_rides fr
    JOIN dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key
    CROSS JOIN date_range dr
    WHERE fr.end_timestamp BETWEEN dr.start_date AND dr.end_date
    GROUP BY fr.driver_user_key
)
SELECT 
    ROUND(
        COUNT(CASE WHEN carpool_count > non_carpool_count THEN 1 END) * 100.0 / 
        NULLIF(COUNT(*), 0), 
        2
    ) AS percentage_drivers_preferring_carpool
FROM driver_ride_summary;

-- ============================================================================

-- Option 2: Even more concise version with window functions
WITH driver_preferences AS (
    SELECT 
        fr.driver_user_key,
        COUNT(CASE WHEN drt.ride_type_name = 'Carpool' THEN 1 END) > 
        COUNT(CASE WHEN drt.ride_type_name != 'Carpool' THEN 1 END) AS prefers_carpool
    FROM fact_rides fr
    JOIN dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key
    WHERE fr.end_timestamp >= CURRENT_DATE - INTERVAL '30 days'
      AND fr.end_timestamp <= CURRENT_DATE  -- Includes current date
    GROUP BY fr.driver_user_key
)
SELECT 
    ROUND(AVG(CASE WHEN prefers_carpool THEN 100.0 ELSE 0.0 END), 2) AS percentage_drivers_preferring_carpool
FROM driver_preferences;

-- ============================================================================

-- Option 3: Most readable version with explicit logic
WITH last_30_days_rides AS (
    SELECT 
        fr.driver_user_key,
        drt.ride_type_name,
        COUNT(*) as ride_count
    FROM fact_rides fr
    JOIN dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key
    WHERE DATE(fr.end_timestamp) BETWEEN 
          CURRENT_DATE - INTERVAL '30 days' AND 
          CURRENT_DATE
    GROUP BY fr.driver_user_key, drt.ride_type_name
),
driver_totals AS (
    SELECT 
        driver_user_key,
        SUM(CASE WHEN ride_type_name = 'Carpool' THEN ride_count ELSE 0 END) AS carpool_rides,
        SUM(CASE WHEN ride_type_name != 'Carpool' THEN ride_count ELSE 0 END) AS other_rides
    FROM last_30_days_rides
    GROUP BY driver_user_key
)
SELECT 
    COUNT(CASE WHEN carpool_rides > other_rides THEN 1 END) * 100.0 / COUNT(*) AS percentage_drivers_preferring_carpool
FROM driver_totals;

/*
Key improvements in these alternative approaches:

1. **Option 1**: Uses a `date_range` CTE for cleaner parameterization and BETWEEN for more readable date filtering
2. **Option 2**: Most concise - uses boolean logic directly in the CTE and AVG for percentage calculation  
3. **Option 3**: Most explicit - separates the logic into clear steps for better maintainability

All three approaches:
- Include the current date (≤ instead of <)
- Are more maintainable and readable
- Handle edge cases better
- Use ROUND() for cleaner output
- Use NULLIF() or proper handling to avoid division by zero

Choose the approach that best fits your team's coding standards and readability preferences.
*/ 