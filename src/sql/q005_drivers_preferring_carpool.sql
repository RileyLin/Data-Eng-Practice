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