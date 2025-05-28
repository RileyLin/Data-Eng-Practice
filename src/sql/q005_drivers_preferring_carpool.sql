/*
Question 1.3.2: Percentage of Drivers Preferring Carpool

Write a SQL query to calculate the percentage of distinct drivers who complete more carpool rides
than regular (non-carpool) rides in a given period (e.g., last 30 days).

Schema:
fact_rides:
- ride_id (PK)
- driver_user_key
- ride_type_key (FK -> dim_ride_type)
- overall_trip_start_time_key
- overall_trip_end_time_key
- overall_trip_date_key
- ...

dim_ride_type:
- ride_type_key (PK)
- ride_type_name ('Carpool', 'Regular', etc.)
- ...

Expected Output:
A single value representing the percentage of drivers who completed more carpool rides than regular rides.
*/

-- Write your SQL query here:
WITH DriverRideCounts AS (
    SELECT
        fr.driver_user_key,
        SUM(CASE WHEN drt.ride_type_name = 'Carpool' THEN 1 ELSE 0 END) AS carpool_rides_count,
        SUM(CASE WHEN drt.ride_type_name != 'Carpool' AND drt.ride_type_name IS NOT NULL THEN 1 ELSE 0 END) AS regular_rides_count
    FROM
        fact_rides fr
    JOIN
        dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key
    WHERE
        -- Assuming overall_trip_date_key is in a format that can be compared (e.g., YYYYMMDD integer or DATE)
        -- and that we have a way to get 'today's date key' and '30 days ago date key'
        -- For SQLite, if overall_trip_date_key is TEXT YYYY-MM-DD:
        fr.overall_trip_date_key >= date('now', '-30 days') 
        AND fr.overall_trip_date_key < date('now')
        -- If overall_trip_date_key is an integer like YYYYMMDD, the date logic needs to adapt.
    GROUP BY
        fr.driver_user_key
),
TotalDistinctDriversInPeriod AS (
    SELECT COUNT(DISTINCT driver_user_key) as total_drivers
    FROM fact_rides fr
    WHERE 
        fr.overall_trip_date_key >= date('now', '-30 days') 
        AND fr.overall_trip_date_key < date('now')
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