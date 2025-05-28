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

