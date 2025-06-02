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

WITH drivers AS (
    SELECT 
        DISTINCT 
        du.user_name, 
        du.user_key,
        SUM(CASE WHEN drt.ride_type_name = 'Carpool' THEN 1 ELSE 0 END) AS carpool_num,
        SUM(CASE WHEN drt.ride_type_name = 'Regular' THEN 1 ELSE 0 END) AS regular_num
    FROM fact_rides fr 
    LEFT JOIN dim_users du ON du.user_key = fr.driver_user_key
    LEFT JOIN dim_ride_type drt ON drt.ride_type_key = fr.ride_type_key
    LEFT JOIN dim_date dd ON dd.date_key = fr.date_key
    WHERE dd.full_date >= CURRENT_DATE - INTERVAL '30' DAY  -- ANSI SQL: Last 30 days
      AND du.user_type = 'driver'                          -- Only drivers
    GROUP BY du.user_name, du.user_key
)

SELECT 
    SUM(CASE WHEN carpool_num > regular_num THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS percentage
FROM drivers