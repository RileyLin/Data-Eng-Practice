/*
Question 1.3.1 (Carpool Segment Percentage):

Write a SQL query to calculate the percentage of ride segments that belong to a 'Carpool' ride type.
Assume fact_ride_segments links to fact_rides, and fact_rides links to dim_ride_type.

Schema from setup_scripts/scenario_1_ridesharing_setup.sql:

fact_ride_segments:
- ride_segment_id (INTEGER PRIMARY KEY AUTOINCREMENT)
- ride_id (INTEGER, FK -> fact_rides)
- rider_user_key (INTEGER, FK -> dim_users)
- segment_pickup_timestamp (TEXT)
- segment_dropoff_timestamp (TEXT)
- segment_pickup_location_key (INTEGER, FK -> dim_location)
- segment_dropoff_location_key (INTEGER, FK -> dim_location)
- segment_fare (REAL)
- segment_distance (REAL)
- pickup_sequence_in_ride (INTEGER)
- dropoff_sequence_in_ride (INTEGER)

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
- date_key (INTEGER, FK -> dim_date)
- time_key (INTEGER, FK -> dim_time)

dim_ride_type:
- ride_type_key (INTEGER PRIMARY KEY AUTOINCREMENT)
- ride_type_name (TEXT UNIQUE NOT NULL) -- e.g., 'Carpool', 'Regular', 'Premium'

dim_users:
- user_key (INTEGER PRIMARY KEY AUTOINCREMENT)
- user_id (VARCHAR(50) UNIQUE NOT NULL)
- user_name (TEXT)
- user_type (TEXT CHECK(user_type IN ('rider', 'driver')))

Expected Output:
The query should return a single row with a percentage value showing what proportion
of all ride segments (from fact_ride_segments) belong to 'Carpool' rides.
*/

-- Write your SQL query here:
SELECT
    (COUNT(CASE WHEN drt.ride_type_name = 'Carpool' THEN frs.ride_segment_id ELSE NULL END) * 100.0)
    / NULLIF(COUNT(frs.ride_segment_id), 0) AS carpool_segment_percentage
FROM
    fact_ride_segments frs
JOIN
    fact_rides fr ON frs.ride_id = fr.ride_id
JOIN
    dim_ride_type drt ON fr.ride_type_key = drt.ride_type_key;

/*
Query Variation: Find users who only use the app to go to airports

This query identifies riders who exclusively use the rideshare service for airport trips.
Assumes dim_location has location_name or location_type fields to identify airports.

Expected Output:
- user_id: The user identifier
- user_name: The user's name  
- total_airport_rides: Number of rides to airport
- total_rides: Total number of rides (should equal airport rides for these users)

Business Use Case:
- Identify airport-focused user segment for targeted marketing
- Understand travel patterns for airport shuttle services
- Optimize driver allocation for airport routes
*/

-- Query to find users who only take rides to airports
WITH user_ride_analysis AS (
    SELECT 
        u.user_id,
        u.user_name,
        COUNT(*) as total_rides,
        COUNT(CASE 
            WHEN dl_dropoff.location_name LIKE '%Airport%' 
                OR dl_dropoff.location_name LIKE '%airport%'
                OR dl_dropoff.location_type = 'Airport'
            THEN 1 
            ELSE NULL 
        END) as airport_rides
    FROM 
        dim_users u
    JOIN 
        fact_ride_segments frs ON u.user_key = frs.rider_user_key
    JOIN 
        dim_location dl_dropoff ON frs.segment_dropoff_location_key = dl_dropoff.location_key
    WHERE 
        u.user_type = 'rider'
    GROUP BY 
        u.user_key, u.user_id, u.user_name
)
SELECT 
    user_id,
    user_name,
    airport_rides as total_airport_rides,
    total_rides
FROM 
    user_ride_analysis
WHERE 
    airport_rides = total_rides  -- Only users where ALL rides go to airport
    AND total_rides > 0          -- Exclude users with no rides
ORDER BY 
    total_rides DESC;

