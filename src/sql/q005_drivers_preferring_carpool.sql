/*
Question 1.3.2: Percentage of Drivers Preferring Carpool

Write a SQL query to calculate the percentage of distinct drivers who complete more carpool rides
than regular (non-carpool) rides in a given period (e.g., last 30 days).

Schema from setup_scripts/scenario_1_ridesharing_setup.sql:

fact_rides:
- ride_id (INTEGER PRIMARY KEY AUTOINCREMENT)
- driver_user_key (INTEGER, FK -> dim_users)
- ride_type_key (INTEGER, FK -> dim_ride_type)
- vehicle_key (INTEGER, FK -> dim_vehicle)
- start_location_key (INTEGER, FK -> dim_location)
- end_location_key (INTEGER, FK -> dim_location)
- start_timestamp (TEXT)
- end_timestamp (TEXT)
- total_fare (REAL)
- total_distance (REAL)
- total_duration (INTEGER)
- date_key (INTEGER, FK -> dim_date) -- Used for filtering by period
- time_key (INTEGER, FK -> dim_time)

dim_ride_type:
- ride_type_key (INTEGER PRIMARY KEY AUTOINCREMENT)
- ride_type_name (TEXT UNIQUE NOT NULL) -- e.g., 'Carpool', 'Regular', 'Premium'

dim_users:
- user_key (INTEGER PRIMARY KEY AUTOINCREMENT)
- user_id (VARCHAR(50) UNIQUE NOT NULL)
- user_name (TEXT)
- user_type (TEXT CHECK(user_type IN ('rider', 'driver')))

dim_date:
- date_key (INTEGER PRIMARY KEY) -- YYYYMMDD format
- full_date (DATE)
- ... (other date attributes)

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