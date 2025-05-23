/*
Solution to Question 1.3.2: Percentage of Drivers Preferring Carpool

Write a SQL query to calculate the percentage of distinct drivers who complete more carpool rides
than regular (non-carpool) rides in a given period (e.g., last 30 days).
*/

WITH DriverRideCounts AS (
    SELECT
        fr.driver_user_key,
        SUM(CASE WHEN drt.ride_type_name = 'Carpool' THEN 1 ELSE 0 END) AS carpool_rides_count,
        SUM(CASE WHEN drt.ride_type_name != 'Carpool' THEN 1 ELSE 0 END) AS regular_rides_count
    FROM
        fact_rides fr
    JOIN
        dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key
    WHERE
        fr.overall_trip_date_key >= (CURRENT_DATE - INTERVAL '30 days')
    GROUP BY
        fr.driver_user_key
),
TotalDistinctDrivers AS (
    SELECT COUNT(DISTINCT driver_user_key) as total_drivers
    FROM DriverRideCounts
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
    DriversPreferringCarpool dpc, TotalDistinctDrivers tdd;

/*
Explanation:

This query calculates the percentage of drivers who complete more carpool rides than regular rides in the last 30 days. 
Here's how it works:

1. DriverRideCounts CTE:
   - Groups by driver_user_key from fact_rides
   - Calculates two metrics for each driver:
     a) carpool_rides_count: Number of rides where ride_type_name = 'Carpool'
     b) regular_rides_count: Number of rides where ride_type_name ≠ 'Carpool'
   - Filters for rides within the last 30 days

2. TotalDistinctDrivers CTE:
   - Gets the total count of distinct drivers who had any rides in the period
   - This will be our denominator for the percentage calculation

3. DriversPreferringCarpool CTE:
   - Counts only drivers where carpool_rides_count > regular_rides_count
   - These are drivers who did more carpool rides than regular rides
   - This will be our numerator for the percentage calculation

4. Final Query:
   - Calculates (drivers_preferring_carpool_count / total_drivers) * 100
   - Uses a CASE statement to handle division by zero (if there are no drivers)

This metric is useful for:
- Measuring driver adoption of the carpool feature
- Identifying driver preferences
- Tracking the effectiveness of incentives for carpool rides
- Informing marketing and operational strategies

Alternative implementations:

1. Using a subquery approach (may be more readable for some):
   
   SELECT
       (COUNT(DISTINCT CASE WHEN carpool_rides_count > regular_rides_count THEN driver_user_key END) * 100.0) /
       NULLIF(COUNT(DISTINCT driver_user_key), 0) AS percentage_drivers_preferring_carpool
   FROM (
       SELECT
           fr.driver_user_key,
           SUM(CASE WHEN drt.ride_type_name = 'Carpool' THEN 1 ELSE 0 END) AS carpool_rides_count,
           SUM(CASE WHEN drt.ride_type_name != 'Carpool' THEN 1 ELSE 0 END) AS regular_rides_count
       FROM
           fact_rides fr
       JOIN
           dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key
       WHERE
           fr.overall_trip_date_key >= (CURRENT_DATE - INTERVAL '30 days')
       GROUP BY
           fr.driver_user_key
   ) driver_counts;

2. For databases without support for INTERVAL, using a date key comparison:
   
   WHERE fr.overall_trip_date_key >= 20230101  -- Assuming YYYYMMDD format for date_key
*/ 